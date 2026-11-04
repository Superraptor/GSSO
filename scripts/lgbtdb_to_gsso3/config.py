"""
Configuration and constants for lgbtDB -> GSSO 3.0.0 converter backbone.
"""

import os

# lgbtDB Endpoints
BASE_URL = "https://lgbtdb.wikibase.cloud"
API_URL = f"{BASE_URL}/w/api.php"
SPARQL_URL = f"{BASE_URL}/query/sparql"
ITEM_URL_TEMPLATE = f"{BASE_URL}/wiki/Item:{{qid}}"

# User-Agent header for API queries
USER_AGENT = "GSSO-Converter/3.0.0 (https://github.com/Superraptor/GSSO; pair-programming maintainer)"

# Key Wikibase Properties on lgbtDB
PROP_SUBCLASS_OF = "P2"
PROP_INSTANCE_OF = "P1"
PROP_GSSO_V2_ID = "P25"
PROP_GSSO_V1_ID = "P1376"
PROP_WIKIDATA_ID = "P3"
PROP_HOMOSAURUS_V3 = "P26"
PROP_HOMOSAURUS_V2 = "P27"
PROP_HOMOSAURUS_V1 = "P28"
PROP_HOMOSAURUS_V0 = "P29"
PROP_BROADER = "P104"
PROP_NARROWER = "P105"
PROP_RELATED = "P106"
PROP_SYNONYM = "P114"
PROP_MESH_SUBJECT = "P206"
PROP_FMA_ID = "P172"
PROP_HPO_ID = "P196"

# GSSO 3.0.0 Ontology Metadata
ONTOLOGY_IRI = "http://purl.obolibrary.org/obo/gsso.owl"
VERSION_IRI = "http://purl.obolibrary.org/obo/gsso/releases/3.0.0/gsso.owl"
VERSION_INFO = "3.0.0-alpha-slim"
DEFAULT_GSSO_PREFIX = "http://purl.obolibrary.org/obo/GSSO_"
OBO_BASE_IRI = "http://purl.obolibrary.org/obo/"

# New GSSO IDs start above the highest V2 ID (12935)
START_NEW_GSSO_ID = 12936

# Working and Output Directories (configured to stay within workspace and in build/ to avoid premature commit)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")
CACHE_DIR = os.path.join(BUILD_DIR, "cache_lgbtdb")
OUTPUT_DIR = os.path.join(BUILD_DIR, "gsso_3.0.0_slim")

MAPPING_FILE = os.path.join(OUTPUT_DIR, "lgbtdb_to_gsso3_mapping.tsv")
REPORT_FILE = os.path.join(OUTPUT_DIR, "constraint_report.md")
SLIM_OWL_FILE = os.path.join(OUTPUT_DIR, "gsso_3.0.0_slim.owl")
SLIM_OBO_FILE = os.path.join(OUTPUT_DIR, "gsso_3.0.0_slim.obo")
SLIM_JSON_FILE = os.path.join(OUTPUT_DIR, "gsso_3.0.0_slim.json")
