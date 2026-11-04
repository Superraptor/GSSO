"""
Command-line interface for the lgbtDB -> GSSO 3.0.0 converter backbone.
"""

import argparse
import sys
from typing import Optional

from .fetcher import LGBTDBFetcher
from .mapper import LGBTDBMapper
from .generator import GSSO3SlimGenerator
from .validator import LGBTDBConstraintValidator
from .config import (
    SLIM_OWL_FILE,
    MAPPING_FILE,
    REPORT_FILE
)


def cmd_fetch(args: argparse.Namespace):
    fetcher = LGBTDBFetcher()
    entities = fetcher.get_class_candidate_entities(
        max_classes=args.limit,
        use_cache=not args.no_cache
    )
    print(f"\n[Done] Fetched {len(entities)} entities into cache.")


def cmd_convert(args: argparse.Namespace):
    fetcher = LGBTDBFetcher()
    entities = fetcher.get_class_candidate_entities(
        max_classes=args.limit,
        use_cache=not args.no_cache
    )

    mapper = LGBTDBMapper()
    classes = mapper.map_entities(entities)
    mapper.export_mapping_tsv(MAPPING_FILE)

    generator = GSSO3SlimGenerator()
    owl_file = generator.generate_owl(classes, SLIM_OWL_FILE)

    if not args.skip_dist:
        generator.convert_distributions(owl_file)

    print(f"\n[Done] Converted {len(classes)} classes into GSSO 3.0.0 slim release.")


def cmd_validate(args: argparse.Namespace):
    fetcher = LGBTDBFetcher()
    entities = fetcher.get_class_candidate_entities(
        max_classes=args.limit,
        use_cache=not args.no_cache
    )

    mapper = LGBTDBMapper()
    classes = mapper.map_entities(entities)

    validator = LGBTDBConstraintValidator(classes)
    report_file = validator.generate_report(REPORT_FILE, SLIM_OWL_FILE)
    print(f"\n[Done] Validation complete. Review report at: {report_file}")


def cmd_all(args: argparse.Namespace):
    print("=== Step 1: Fetching Entities from lgbtDB ===")
    fetcher = LGBTDBFetcher()
    entities = fetcher.get_class_candidate_entities(
        max_classes=args.limit,
        use_cache=not args.no_cache
    )

    print("\n=== Step 2: Mapping to GSSO 3.0.0 Class Models ===")
    mapper = LGBTDBMapper()
    classes = mapper.map_entities(entities)
    mapper.export_mapping_tsv(MAPPING_FILE)

    print("\n=== Step 3: Generating Slim Release Artifacts ===")
    generator = GSSO3SlimGenerator()
    owl_file = generator.generate_owl(classes, SLIM_OWL_FILE)
    if not args.skip_dist:
        generator.convert_distributions(owl_file)

    print("\n=== Step 4: Running Constraint & Reasoner Validation ===")
    validator = LGBTDBConstraintValidator(classes)
    report_file = validator.generate_report(REPORT_FILE, owl_file)

    print(f"\n=======================================================")
    print(f"GSSO 3.0.0 Slim Backbone Pipeline Execution Complete!")
    print(f"OWL File:       {SLIM_OWL_FILE}")
    print(f"Mapping TSV:    {MAPPING_FILE}")
    print(f"Report:         {report_file}")
    print(f"=======================================================")


def main():
    parser = argparse.ArgumentParser(
        description="lgbtDB to GSSO 3.0.0 Slim Converter Backbone"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Common options
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--limit", type=int, default=None, help="Limit number of classes to process (default: all)")
    common.add_argument("--no-cache", action="store_true", help="Bypass local cache and query lgbtDB directly")
    common.add_argument("--skip-dist", action="store_true", help="Skip OBO/JSON conversion via ROBOT")

    # Subcommands
    subparsers.add_parser("fetch", parents=[common], help="Fetch class candidate entities from lgbtDB into cache")
    subparsers.add_parser("convert", parents=[common], help="Convert cached entities to GSSO 3.0.0 slim OWL ontology")
    subparsers.add_parser("validate", parents=[common], help="Run constraint checking and reasoner validation")
    subparsers.add_parser("all", parents=[common], help="Run full pipeline: fetch, convert, and validate")

    args = parser.parse_args()

    if args.command == "fetch":
        cmd_fetch(args)
    elif args.command == "convert":
        cmd_convert(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "all" or args.command is None:
        cmd_all(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
