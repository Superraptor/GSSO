"""
Mapper module: transforms lgbtDB Wikibase entities into GSSO 3.0.0 class models
and maintains an exact QID <-> GSSO ID mapping table.
"""

import os
import csv
import re
from dataclasses import dataclass, field
from typing import Dict, List, Set, Any, Optional

from .config import (
    DEFAULT_GSSO_PREFIX,
    START_NEW_GSSO_ID,
    MAPPING_FILE,
    OUTPUT_DIR,
    PROP_SUBCLASS_OF,
    PROP_GSSO_V2_ID,
    PROP_GSSO_V1_ID,
    PROP_WIKIDATA_ID,
    PROP_HOMOSAURUS_V3,
    PROP_HOMOSAURUS_V2,
    PROP_HOMOSAURUS_V1,
    PROP_MESH_SUBJECT,
    PROP_FMA_ID,
    PROP_HPO_ID
)


@dataclass
class GSSOClassModel:
    qid: str
    gsso_id: str             # e.g. "GSSO_000135"
    gsso_iri: str            # e.g. "http://purl.obolibrary.org/obo/GSSO_000135"
    label_en: str
    labels: Dict[str, str] = field(default_factory=dict)         # lang -> label
    definition_en: Optional[str] = None                          # IAO:0000115
    synonyms_en: List[str] = field(default_factory=list)         # hasExactSynonym
    multilingual_synonyms: Dict[str, List[str]] = field(default_factory=dict)
    parent_qids: List[str] = field(default_factory=list)         # subClassOf (QIDs)
    parent_gsso_ids: List[str] = field(default_factory=list)     # subClassOf (GSSO IDs)
    xrefs: List[str] = field(default_factory=list)               # hasDbXref
    is_v2_term: bool = False
    v2_id: Optional[str] = None


def normalize_language_tag(lang: str) -> Optional[str]:
    """Corrects known non-standard language tags to BCP 47."""
    lang = lang.lower().strip()
    mapping = {
        "jp": "ja",
        "eb": "en",
        "e": "en",
        "pt-br": "pt-BR",
        "zh-cn": "zh-CN",
        "zh-tw": "zh-TW",
    }
    if lang in mapping:
        return mapping[lang]
    # Discard single-letter invalid codes
    if len(lang) == 1:
        return None
    return lang


class LGBTDBMapper:
    def __init__(self, start_id: int = START_NEW_GSSO_ID):
        self.next_new_id = start_id
        self.qid_to_gsso: Dict[str, str] = {}
        self.classes: Dict[str, GSSOClassModel] = {}

    def _extract_claim_values(self, claims: Dict[str, Any], prop_id: str) -> List[Any]:
        results = []
        for snak in claims.get(prop_id, []):
            mainsnak = snak.get("mainsnak", {})
            datavalue = mainsnak.get("datavalue", {})
            val = datavalue.get("value")
            if val is not None:
                results.append(val)
        return results

    def _extract_item_ids(self, claims: Dict[str, Any], prop_id: str) -> List[str]:
        items = []
        for snak in claims.get(prop_id, []):
            val = snak.get("mainsnak", {}).get("datavalue", {}).get("value", {})
            if isinstance(val, dict) and val.get("id"):
                items.append(val["id"])
        return items

    def _format_gsso_id(self, numeric_or_str: Any) -> str:
        s = str(numeric_or_str).strip().replace("GSSO_", "").replace("GSSO:", "")
        # Pad to 6 digits if numeric
        if s.isdigit():
            return f"GSSO_{int(s):06d}"
        return f"GSSO_{s}"

    def map_entities(self, raw_entities: Dict[str, Any]) -> Dict[str, GSSOClassModel]:
        """
        Maps raw Wikibase entities to GSSOClassModel objects.
        Assigns GSSO IDs: existing V2 IDs for mapped terms, or sequential IDs for new concepts.
        """
        print(f"Mapping {len(raw_entities)} lgbtDB entities to GSSO 3.0.0 class models...")

        # Pass 1: Assign IDs and basic metadata
        for qid, ent in raw_entities.items():
            claims = ent.get("claims", {})

            # 1. Check for GSSO V2 ID
            v2_vals = self._extract_claim_values(claims, PROP_GSSO_V2_ID)
            v1_vals = self._extract_claim_values(claims, PROP_GSSO_V1_ID)

            if v2_vals:
                v2_id = str(v2_vals[0]).strip()
                gsso_id = self._format_gsso_id(v2_id)
                is_v2 = True
            elif v1_vals:
                v1_id = str(v1_vals[0]).strip()
                gsso_id = self._format_gsso_id(v1_id)
                is_v2 = True
                v2_id = v1_id
            else:
                # Mint new GSSO ID
                gsso_id = f"GSSO_{self.next_new_id:06d}"
                self.next_new_id += 1
                is_v2 = False
                v2_id = None

            self.qid_to_gsso[qid] = gsso_id
            gsso_iri = f"{DEFAULT_GSSO_PREFIX}{gsso_id.replace('GSSO_', '')}"

            # 2. Extract Labels
            raw_labels = ent.get("labels", {})
            labels_dict: Dict[str, str] = {}
            for l_lang, l_data in raw_labels.items():
                norm_lang = normalize_language_tag(l_lang)
                if norm_lang and l_data.get("value"):
                    labels_dict[norm_lang] = l_data["value"].strip()

            label_en = labels_dict.get("en", ent.get("id", qid))

            # 3. Extract Definition (Description)
            raw_descriptions = ent.get("descriptions", {})
            desc_en = raw_descriptions.get("en", {}).get("value")
            if desc_en:
                desc_en = desc_en.strip()

            # 4. Extract Synonyms (Aliases)
            synonyms_en: List[str] = []
            multilingual_synonyms: Dict[str, List[str]] = {}
            raw_aliases = ent.get("aliases", {})
            for a_lang, a_list in raw_aliases.items():
                norm_lang = normalize_language_tag(a_lang)
                if norm_lang:
                    syns = [item.get("value", "").strip() for item in a_list if item.get("value")]
                    if syns:
                        if norm_lang == "en":
                            synonyms_en.extend(syns)
                        else:
                            multilingual_synonyms[norm_lang] = syns

            # 5. Extract Parent QIDs (subclass of P2)
            parent_qids = self._extract_item_ids(claims, PROP_SUBCLASS_OF)

            # 6. Extract Cross-references
            xrefs: List[str] = []
            for wkid in self._extract_claim_values(claims, PROP_WIKIDATA_ID):
                xrefs.append(f"wikidata:{wkid}")
            for homoid in self._extract_claim_values(claims, PROP_HOMOSAURUS_V3):
                xrefs.append(f"homosaurus:{homoid}")
            for homoid in self._extract_claim_values(claims, PROP_HOMOSAURUS_V2):
                xrefs.append(f"homosaurus_v2:{homoid}")
            for meshid in self._extract_claim_values(claims, PROP_MESH_SUBJECT):
                xrefs.append(f"mesh:{meshid}")
            for fmaid in self._extract_claim_values(claims, PROP_FMA_ID):
                xrefs.append(f"fma:{fmaid}")
            for hpoid in self._extract_claim_values(claims, PROP_HPO_ID):
                xrefs.append(f"hp:{hpoid}")
            # Add lgbtDB QID xref
            xrefs.append(f"lgbtdb:{qid}")

            self.classes[qid] = GSSOClassModel(
                qid=qid,
                gsso_id=gsso_id,
                gsso_iri=gsso_iri,
                label_en=label_en,
                labels=labels_dict,
                definition_en=desc_en,
                synonyms_en=synonyms_en,
                multilingual_synonyms=multilingual_synonyms,
                parent_qids=parent_qids,
                parent_gsso_ids=[],
                xrefs=xrefs,
                is_v2_term=is_v2,
                v2_id=v2_id
            )

        # Pass 2: Map parent QIDs to GSSO IDs
        for qid, model in self.classes.items():
            for pqid in model.parent_qids:
                if pqid in self.qid_to_gsso:
                    model.parent_gsso_ids.append(self.qid_to_gsso[pqid])

        print(f"Successfully mapped {len(self.classes)} classes. Next available new GSSO ID: GSSO_{self.next_new_id:06d}")
        return self.classes

    def export_mapping_tsv(self, output_path: Optional[str] = None) -> str:
        """Exports a TSV file documenting the lgbtDB QID to GSSO 3.0.0 mapping."""
        out_file = output_path or MAPPING_FILE
        os.makedirs(os.path.dirname(out_file), exist_ok=True)

        with open(out_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow([
                "lgbtdb_qid",
                "gsso_id",
                "gsso_iri",
                "label_en",
                "is_v2_term",
                "gsso_v2_id",
                "parent_qids",
                "parent_gsso_ids"
            ])
            for qid, m in sorted(self.classes.items(), key=lambda x: int(x[0][1:]) if x[0][1:].isdigit() else 0):
                writer.writerow([
                    m.qid,
                    m.gsso_id,
                    m.gsso_iri,
                    m.label_en,
                    str(m.is_v2_term),
                    m.v2_id or "",
                    ",".join(m.parent_qids),
                    ",".join(m.parent_gsso_ids)
                ])

        print(f"Exported mapping table to: {out_file}")
        return out_file
