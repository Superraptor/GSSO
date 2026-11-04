#!/usr/bin/env python3
"""
Compiles GSSO JSON ontology into optimized static datasets for the GitHub Pages web application.
Generates:
  - www/data/gsso_terms.json: Master indexed term dictionary with labels, definitions, synonyms, comments, parents, children, and xrefs.
  - www/data/meta.json: Ontology metadata, release statistics, and top curated category entrypoints.
"""

import json
import os
import sys

def build_web_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "gsso.json")
    out_dir = os.path.join(base_dir, "www", "data")
    os.makedirs(out_dir, exist_ok=True)

    print(f"Loading {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = data["graphs"][0]
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    print(f"Loaded {len(nodes)} nodes and {len(edges)} edges.")

    # 1. Map parents and children relationships
    parents_map = {}
    children_map = {}
    for edge in edges:
        if edge.get("pred") == "is_a":
            sub = edge.get("sub", "").split("/")[-1]
            obj = edge.get("obj", "").split("/")[-1]
            if sub and obj:
                parents_map.setdefault(sub, []).append(obj)
                children_map.setdefault(obj, []).append(sub)

    # 2. Extract term metadata
    terms = {}
    label_map = {}

    for node in nodes:
        node_id = node.get("id", "")
        short_id = node_id.split("/")[-1]
        lbl = node.get("lbl", "")
        if short_id:
            label_map[short_id] = lbl

    for node in nodes:
        node_id = node.get("id", "")
        short_id = node_id.split("/")[-1]

        # Focus on GSSO terms
        if not short_id.startswith("GSSO_"):
            continue

        lbl = node.get("lbl", "") or short_id
        meta = node.get("meta", {})
        definition = meta.get("definition", {}).get("val", "")
        comments = meta.get("comments", [])
        
        # Collect synonyms categorized
        exact_synonyms = []
        related_synonyms = []
        narrow_synonyms = []
        broad_synonyms = []
        all_synonyms = []

        for s in meta.get("synonyms", []):
            val = s.get("val", "").strip()
            pred = s.get("pred", "")
            if not val or val in all_synonyms:
                continue
            all_synonyms.append(val)
            if "Exact" in pred:
                exact_synonyms.append(val)
            elif "Narrow" in pred:
                narrow_synonyms.append(val)
            elif "Broad" in pred:
                broad_synonyms.append(val)
            else:
                related_synonyms.append(val)

        # Basic properties (alternateName, replaces, external mappings)
        xrefs = []
        mappings = {}
        for bp in meta.get("basicPropertyValues", []):
            pred = bp.get("pred", "")
            val = bp.get("val", "").strip()
            if not val:
                continue
            if "alternateName" in pred or "hasSynonym" in pred:
                if val not in all_synonyms:
                    all_synonyms.append(val)
                    exact_synonyms.append(val)
            elif "replaces" in pred:
                if not val.startswith("http"):
                    if val not in all_synonyms:
                        all_synonyms.append(val)
                        related_synonyms.append(val)
            
            # Categorize external mappings
            if "homosaurus.org" in val:
                mappings.setdefault("Homosaurus", []).append(val)
            elif "wikidata.org" in val or "wiki/Q" in val:
                mappings.setdefault("Wikidata", []).append(val)
            elif "MESH" in val or "mesh" in val or "Property:P486" in pred:
                mappings.setdefault("MeSH", []).append(val)
            elif "loc.gov" in val or "sh20" in val:
                mappings.setdefault("LCSH", []).append(val)
            elif "snomed" in val.lower():
                mappings.setdefault("SNOMED-CT", []).append(val)
            elif "NCIT" in val or "ncit" in val:
                mappings.setdefault("NCIt", []).append(val)
            elif any(domain in val for domain in ["doi.org", "worldcat.org", "wikipedia.org"]):
                xrefs.append(val)

        for x in meta.get("xrefs", []):
            xval = x.get("val", "").strip()
            if xval and xval not in xrefs:
                xrefs.append(xval)

        # Parent and child terms with labels
        pars = []
        for pid in parents_map.get(short_id, []):
            pars.append({"id": pid, "lbl": label_map.get(pid, pid)})

        children = []
        for cid in children_map.get(short_id, []):
            if cid.startswith("GSSO_"):
                children.append({"id": cid, "lbl": label_map.get(cid, cid)})

        # Clean duplicates
        children = sorted(children, key=lambda x: x["lbl"].lower())
        pars = sorted(pars, key=lambda x: x["lbl"].lower())

        terms[short_id] = {
            "id": short_id,
            "iri": node_id,
            "lbl": lbl,
            "def": definition,
            "comm": comments,
            "syn": {
                "exact": exact_synonyms,
                "related": related_synonyms,
                "narrow": narrow_synonyms,
                "broad": broad_synonyms,
                "all": all_synonyms
            },
            "par": pars,
            "ch": children,
            "maps": mappings,
            "xref": xrefs
        }

    # 3. Create featured thematic branches for browse explorer
    featured_categories = [
        {
            "id": "GSSO_005835",
            "name": "LGBTQ+ Persons & Communities",
            "description": "Concepts, terms, and groups representing lesbian, gay, bisexual, transgender, queer, and allied communities.",
            "icon": "users"
        },
        {
            "id": "GSSO_011889",
            "name": "Gender Identities & Presentation",
            "description": "Terms describing personal gender identity, expressions, presentation, pronouns, and gender diversity.",
            "icon": "sparkles"
        },
        {
            "id": "GSSO_000484",
            "name": "Health & Affirming Care",
            "description": "Health conditions, gender-affirming treatments, surgical procedures, and medical terminology.",
            "icon": "heart-pulse"
        },
        {
            "id": "GSSO_000029",
            "name": "Social & Cultural Concepts",
            "description": "Sociological processes, historical movements, community spaces, slang, and cultural terminology.",
            "icon": "landmark"
        },
        {
            "id": "GSSO_000492",
            "name": "Knowledge & Educational Entities",
            "description": "Academic disciplines, literature, media, subject headings, and reference frameworks.",
            "icon": "book-open"
        },
        {
            "id": "GSSO_000721",
            "name": "Biological Interactions & Anatomy",
            "description": "Biological sex characteristics, genetics, endocrine systems, and physiological concepts.",
            "icon": "dna"
        }
    ]

    # Verify category labels from terms
    for cat in featured_categories:
        if cat["id"] in terms:
            cat["term_label"] = terms[cat["id"]]["lbl"]
            cat["subclass_count"] = len(terms[cat["id"]]["ch"])

    meta_info = {
        "title": "Gender, Sex, and Sexual Orientation (GSSO) Ontology",
        "version": "2.0.11",
        "date": "4 November 2026",
        "total_terms": len(terms),
        "total_edges": len(edges),
        "featured_categories": featured_categories,
        "purl_base": "http://purl.obolibrary.org/obo/GSSO_",
        "github_url": "https://github.com/Superraptor/GSSO",
        "lgbtdb_url": "https://lgbtdb.wikibase.cloud/"
    }

    terms_out = os.path.join(out_dir, "gsso_terms.json")
    search_out = os.path.join(out_dir, "search_index.json")
    meta_out = os.path.join(out_dir, "meta.json")

    # Generate lightweight instant search index
    search_index = []
    for tid, t in terms.items():
        search_index.append({
            "id": tid,
            "l": t["lbl"],
            "s": t["syn"]["all"][:8]
        })

    print(f"Writing {len(terms)} terms to {terms_out}...")
    with open(terms_out, "w", encoding="utf-8") as f:
        json.dump(terms, f, separators=(",", ":"))

    print(f"Writing search index to {search_out}...")
    with open(search_out, "w", encoding="utf-8") as f:
        json.dump(search_index, f, separators=(",", ":"))

    print(f"Writing metadata to {meta_out}...")
    with open(meta_out, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, indent=2)

    terms_size = os.path.getsize(terms_out) / (1024 * 1024)
    search_size = os.path.getsize(search_out) / (1024 * 1024)
    print(f"Done! gsso_terms.json: {terms_size:.2f} MB, search_index.json: {search_size:.2f} MB")

if __name__ == "__main__":
    build_web_data()
