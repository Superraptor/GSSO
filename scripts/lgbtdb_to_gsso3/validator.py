"""
Constraint and reasoner validator for lgbtDB -> GSSO 3.0.0.
Performs graph cycle detection, checks for duplicate labels/definitions,
dangling references, and validates logical consistency with ROBOT reasoners.
Outputs an actionable Markdown report for lgbtDB maintainers.
"""

import os
import subprocess
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional

from .config import (
    REPORT_FILE,
    SLIM_OWL_FILE,
    ITEM_URL_TEMPLATE
)
from .mapper import GSSOClassModel


class LGBTDBConstraintValidator:
    def __init__(self, classes: Dict[str, GSSOClassModel]):
        self.classes = classes
        self.qid_to_label = {qid: m.label_en for qid, m in classes.items()}

    def find_cycles(self) -> List[List[str]]:
        """
        Detects cycles in the subclass hierarchy using Tarjan's strongly connected components algorithm.
        Returns a list of cycles (each cycle is a list of QIDs).
        """
        graph: Dict[str, List[str]] = defaultdict(list)
        for qid, model in self.classes.items():
            for pqid in model.parent_qids:
                if pqid in self.classes:
                    graph[qid].append(pqid)

        index = 0
        indices: Dict[str, int] = {}
        lowlinks: Dict[str, int] = {}
        on_stack: Set[str] = set()
        stack: List[str] = []
        cycles: List[List[str]] = []

        def strongconnect(node: str):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in indices:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif neighbor in on_stack:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])

            # If node is a root of an SCC
            if lowlinks[node] == indices[node]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    scc.append(w)
                    if w == node:
                        break
                # Only components with >1 node (or self-loops) are cycles
                if len(scc) > 1 or (node in graph.get(node, [])):
                    cycles.append(scc)

        for qid in self.classes:
            if qid not in indices:
                strongconnect(qid)

        return cycles

    def find_dangling_parents(self) -> Dict[str, List[str]]:
        """Finds parent QIDs referenced in P2 that are not defined in the class set."""
        dangling: Dict[str, List[str]] = defaultdict(list)
        for qid, model in self.classes.items():
            for pqid in model.parent_qids:
                if pqid not in self.classes:
                    dangling[pqid].append(qid)
        return dangling

    def find_duplicate_labels(self) -> Dict[str, List[str]]:
        """Finds English labels shared by more than one class."""
        label_map: Dict[str, List[str]] = defaultdict(list)
        for qid, model in self.classes.items():
            if model.label_en:
                norm_lbl = model.label_en.strip().lower()
                label_map[norm_lbl].append(qid)
        return {lbl: qids for lbl, qids in label_map.items() if len(qids) > 1}

    def find_missing_metadata(self) -> Tuple[List[str], List[str]]:
        """Identifies classes missing an English label or missing a definition."""
        missing_labels: List[str] = []
        missing_definitions: List[str] = []

        for qid, model in self.classes.items():
            if not model.label_en or model.label_en == qid:
                missing_labels.append(qid)
            if not model.definition_en:
                missing_definitions.append(qid)

        return missing_labels, missing_definitions

    def run_robot_reasoner_check(self, owl_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        Runs ROBOT ELK reasoner on the generated slim OWL ontology to verify logical consistency.
        """
        source_owl = owl_path or SLIM_OWL_FILE
        if not os.path.exists(source_owl):
            return False, f"Ontology file not found: {source_owl}"

        try:
            cmd = ["robot", "reason", "-i", source_owl, "--reasoner", "ELK"]
            res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            output = (res.stderr or "") + "\n" + (res.stdout or "")
            cleaned = "\n".join(l for l in output.splitlines() if not l.startswith("WARNING: sun.misc.Unsafe") and not l.startswith("WARNING: A terminally deprecated") and not l.startswith("WARNING: Please consider")).strip()
            if res.returncode == 0:
                return True, "Consistent: ELK reasoner completed successfully with 0 unsatisfiable classes."
            else:
                return False, f"Inconsistent or Reasoner Error:\n{cleaned}"
        except Exception as e:
            return False, f"Could not run ROBOT reasoner check: {e}"

    def run_robot_profile_check(self, owl_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        Runs ROBOT validate-profile on DL to check for OWL 2 DL compliance.
        """
        source_owl = owl_path or SLIM_OWL_FILE
        if not os.path.exists(source_owl):
            return False, f"Ontology file not found: {source_owl}"

        try:
            cmd = ["robot", "validate-profile", "--profile", "DL", "-i", source_owl]
            res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            output = (res.stderr or "") + "\n" + (res.stdout or "")
            cleaned = "\n".join(l for l in output.splitlines() if not l.startswith("WARNING: sun.misc.Unsafe") and not l.startswith("WARNING: A terminally deprecated") and not l.startswith("WARNING: Please consider")).strip()
            if res.returncode == 0 or "Ontology and imports closure in profile" in output:
                return True, "OWL 2 DL Compliant: [Ontology and imports closure in profile]"
            else:
                return False, f"Violations:\n{cleaned}"
        except Exception as e:
            return False, f"Could not run ROBOT profile check: {e}"

    def generate_report(self, output_path: Optional[str] = None, owl_path: Optional[str] = None) -> str:
        """
        Executes all checks and generates an actionable Markdown constraint report.
        """
        out_file = output_path or REPORT_FILE
        os.makedirs(os.path.dirname(out_file), exist_ok=True)

        print("Executing constraint checks and reasoner validation...")

        cycles = self.find_cycles()
        dangling = self.find_dangling_parents()
        duplicate_labels = self.find_duplicate_labels()
        missing_labels, missing_definitions = self.find_missing_metadata()

        reasoner_ok, reasoner_msg = self.run_robot_reasoner_check(owl_path)
        profile_ok, profile_msg = self.run_robot_profile_check(owl_path)

        total_classes = len(self.classes)
        v2_count = sum(1 for m in self.classes.values() if m.is_v2_term)
        new_count = total_classes - v2_count

        lines = [
            "# lgbtDB to GSSO 3.0.0 Slim: Constraint & Reasoner Report",
            "",
            "> **Purpose**: This report details constraint checks and reasoner validations for the GSSO 3.0.0 slim release generated from lgbtDB.",
            "> Maintainers can review the actionable issue lists below to make necessary changes directly on [lgbtDB](https://lgbtdb.wikibase.cloud/) prior to committing the full version to the repository.",
            "",
            "## Executive Summary",
            "",
            "| Metric | Count / Status | Notes |",
            "| :--- | :--- | :--- |",
            f"| **Total Classes Evaluated** | `{total_classes}` | Classes extracted from lgbtDB |",
            f"| **Retained GSSO V2 Terms** | `{v2_count}` | Mapped via `P25` or `P1376` |",
            f"| **New GSSO 3.0.0 Terms** | `{new_count}` | Minted starting at `GSSO_012936` |",
            f"| **Subclass Cycles** | `{'0 (PASS)' if not cycles else f'{len(cycles)} (ACTION REQUIRED)'}` | Must be resolved on lgbtDB |",
            f"| **Dangling Parents** | `{'0 (PASS)' if not dangling else f'{len(dangling)} parents referenced'}` | Referenced in `P2` but unextracted |",
            f"| **Duplicate English Labels** | `{len(duplicate_labels)}` | Classes sharing identical names |",
            f"| **Missing English Labels** | `{len(missing_labels)}` | Classes with no English label |",
            f"| **Missing Definitions** | `{len(missing_definitions)}` | Classes with no English description |",
            f"| **Logical Consistency (ELK)** | `{'PASS' if reasoner_ok else 'FAIL'}` | {reasoner_msg.splitlines()[0]} |",
            f"| **OWL 2 DL Profile** | `{'PASS' if profile_ok else 'FAIL'}` | {profile_msg.splitlines()[0]} |",
            "",
            "---",
            "",
            "## 1. Subclass Cycle Detection (P2)",
            ""
        ]

        if not cycles:
            lines.append("No subclass cycles found. The hierarchy is a strict Directed Acyclic Graph (DAG).")
        else:
            lines.append(f"> [!WARNING]\n> Found **{len(cycles)}** cycle(s) in the subclass hierarchy! Each cycle causes circular reasoning and collapses classes to equivalents. Please edit these items on lgbtDB:")
            for idx, cycle in enumerate(cycles, 1):
                lines.append(f"### Cycle #{idx} ({len(cycle)} classes)")
                for qid in cycle:
                    lbl = self.qid_to_label.get(qid, "No label")
                    url = ITEM_URL_TEMPLATE.format(qid=qid)
                    lines.append(f"- [{qid} ({lbl})]({url})")
                lines.append("")

        lines.extend([
            "---",
            "",
            "## 2. Duplicate English Labels",
            ""
        ])

        if not duplicate_labels:
            lines.append("No duplicate English labels detected across classes.")
        else:
            lines.append(f"> [!NOTE]\n> Found **{len(duplicate_labels)}** duplicate label(s) where multiple distinct items share the same English name. Consider disambiguating labels or consolidating duplicate entities on lgbtDB:")
            for lbl, qids in sorted(duplicate_labels.items()):
                lines.append(f"### Label: *\"{lbl}\"* ({len(qids)} items)")
                for qid in qids:
                    url = ITEM_URL_TEMPLATE.format(qid=qid)
                    desc = self.classes[qid].definition_en or "No description"
                    lines.append(f"- [{qid}]({url}): {desc}")
                lines.append("")

        lines.extend([
            "---",
            "",
            "## 3. Dangling Superclass References",
            ""
        ])

        if not dangling:
            lines.append("All parent entities referenced in `P2` are present in the class collection.")
        else:
            lines.append(f"> [!NOTE]\n> The following **{len(dangling)}** parent entities are referenced in `P2` but were not extracted as part of the initial class scope:")
            for pqid, child_qids in sorted(dangling.items(), key=lambda x: len(x[1]), reverse=True)[:30]:
                p_url = ITEM_URL_TEMPLATE.format(qid=pqid)
                lines.append(f"- [{pqid}]({p_url}) (referenced as parent by {len(child_qids)} child classes: {', '.join(child_qids[:5])})")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 4. Missing Definitions (Descriptions)",
            ""
        ])

        if not missing_definitions:
            lines.append("All classes have English definitions (`obo:IAO_0000115`).")
        else:
            lines.append(f"A total of **{len(missing_definitions)}** classes currently lack an English description on lgbtDB.")
            lines.append("Sample items needing definitions:")
            for qid in missing_definitions[:20]:
                lbl = self.qid_to_label.get(qid, "No label")
                url = ITEM_URL_TEMPLATE.format(qid=qid)
                lines.append(f"- [{qid} ({lbl})]({url})")
            if len(missing_definitions) > 20:
                lines.append(f"- *...and {len(missing_definitions) - 20} more.*")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 5. Reasoner & Profile Validation Details",
            "",
            "### ELK Reasoner Output",
            "```text",
            reasoner_msg,
            "```",
            "",
            "### OWL 2 DL Profile Output",
            "```text",
            profile_msg,
            "```",
            ""
        ])

        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Generated constraint and reasoner report at: {out_file}")
        return out_file
