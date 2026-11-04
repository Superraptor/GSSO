"""
Ontology generator: builds the GSSO 3.0.0 slim OWL/RDF XML release file,
as well as OBO and JSON distributions.
"""

import os
import subprocess
import xml.sax.saxutils as saxutils
from typing import Dict, Optional

from .config import (
    ONTOLOGY_IRI,
    VERSION_IRI,
    VERSION_INFO,
    SLIM_OWL_FILE,
    SLIM_OBO_FILE,
    SLIM_JSON_FILE,
    OUTPUT_DIR
)
from .mapper import GSSOClassModel


def xml_escape(text: str) -> str:
    """Escapes string for safe XML text and attribute output."""
    if not text:
        return ""
    return saxutils.escape(text, {'"': "&quot;", "'": "&apos;"})


class GSSO3SlimGenerator:
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_owl(self, classes: Dict[str, GSSOClassModel], output_path: Optional[str] = None) -> str:
        """
        Generates an OWL 2 DL compliant RDF/XML ontology file for GSSO 3.0.0 Slim.
        """
        out_file = output_path or SLIM_OWL_FILE
        os.makedirs(os.path.dirname(out_file), exist_ok=True)

        print(f"Generating GSSO 3.0.0 Slim OWL ontology at: {out_file}...")

        lines = [
            '<?xml version="1.0"?>',
            '<rdf:RDF xmlns="http://purl.obolibrary.org/obo/gsso.owl#"',
            '     xml:base="http://purl.obolibrary.org/obo/gsso.owl"',
            '     xmlns:obo="http://purl.obolibrary.org/obo/"',
            '     xmlns:owl="http://www.w3.org/2002/07/owl#"',
            '     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
            '     xmlns:xml="http://www.w3.org/XML/1998/namespace"',
            '     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"',
            '     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"',
            '     xmlns:terms="http://purl.org/dc/terms/"',
            '     xmlns:oboInOwl="http://www.geneontology.org/formats/oboInOwl#">',
            '',
            f'    <owl:Ontology rdf:about="{ONTOLOGY_IRI}">',
            f'        <owl:versionIRI rdf:resource="{VERSION_IRI}"/>',
            f'        <owl:versionInfo>{VERSION_INFO}</owl:versionInfo>',
            '        <rdfs:label xml:lang="en">Gender, Sex, and Sexual Orientation Ontology</rdfs:label>',
            '        <rdfs:comment xml:lang="en">GSSO Version 3.0.0 Slim Alpha release generated from lgbtDB (https://lgbtdb.wikibase.cloud/). Contains only core classes, subclass hierarchies, labels, definitions, synonyms, and external cross-references.</rdfs:comment>',
            '        <terms:license rdf:resource="http://www.apache.org/licenses/LICENSE-2.0"/>',
            '        <terms:license rdf:resource="https://creativecommons.org/licenses/by/4.0/"/>',
            '    </owl:Ontology>',
            '',
            '    <!-- Annotation Properties -->',
            '    <owl:AnnotationProperty rdf:about="http://purl.org/dc/terms/license">',
            '        <rdfs:label xml:lang="en">license</rdfs:label>',
            '    </owl:AnnotationProperty>',
            '    <owl:AnnotationProperty rdf:about="http://purl.obolibrary.org/obo/IAO_0000115">',
            '        <rdfs:label xml:lang="en">definition</rdfs:label>',
            '    </owl:AnnotationProperty>',
            '    <owl:AnnotationProperty rdf:about="http://www.geneontology.org/formats/oboInOwl#hasExactSynonym">',
            '        <rdfs:label xml:lang="en">has exact synonym</rdfs:label>',
            '    </owl:AnnotationProperty>',
            '    <owl:AnnotationProperty rdf:about="http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym">',
            '        <rdfs:label xml:lang="en">has related synonym</rdfs:label>',
            '    </owl:AnnotationProperty>',
            '    <owl:AnnotationProperty rdf:about="http://www.geneontology.org/formats/oboInOwl#hasDbXref">',
            '        <rdfs:label xml:lang="en">database cross reference</rdfs:label>',
            '    </owl:AnnotationProperty>',
            '',
            '    <!-- Classes -->'
        ]

        # Sort classes by GSSO ID
        sorted_classes = sorted(classes.values(), key=lambda c: c.gsso_id)

        for model in sorted_classes:
            lines.append(f'    <!-- {model.gsso_iri} -->')
            lines.append(f'    <owl:Class rdf:about="{model.gsso_iri}">')

            # Primary English label
            lines.append(f'        <rdfs:label xml:lang="en">{xml_escape(model.label_en)}</rdfs:label>')

            # Multilingual labels (excluding duplicate English)
            for lang, lbl in sorted(model.labels.items()):
                if lang != "en" and lbl:
                    lines.append(f'        <rdfs:label xml:lang="{xml_escape(lang)}">{xml_escape(lbl)}</rdfs:label>')

            # Definition (IAO_0000115)
            if model.definition_en:
                lines.append(f'        <obo:IAO_0000115 xml:lang="en">{xml_escape(model.definition_en)}</obo:IAO_0000115>')

            # English Synonyms
            for syn in sorted(set(model.synonyms_en)):
                if syn and syn.lower() != model.label_en.lower():
                    lines.append(f'        <oboInOwl:hasExactSynonym xml:lang="en">{xml_escape(syn)}</oboInOwl:hasExactSynonym>')

            # Multilingual Synonyms
            for lang, syns in sorted(model.multilingual_synonyms.items()):
                for syn in sorted(set(syns)):
                    if syn:
                        lines.append(f'        <oboInOwl:hasExactSynonym xml:lang="{xml_escape(lang)}">{xml_escape(syn)}</oboInOwl:hasExactSynonym>')

            # Cross-references (hasDbXref)
            for xref in sorted(set(model.xrefs)):
                if xref:
                    lines.append(f'        <oboInOwl:hasDbXref>{xml_escape(xref)}</oboInOwl:hasDbXref>')

            # Subclass Of
            for parent_iri in sorted(set(model.parent_gsso_ids)):
                full_parent_iri = f"http://purl.obolibrary.org/obo/{parent_iri}"
                lines.append(f'        <rdfs:subClassOf rdf:resource="{full_parent_iri}"/>')

            lines.append('    </owl:Class>')
            lines.append('')

        lines.append('</rdf:RDF>')

        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Successfully wrote {len(sorted_classes)} classes to {out_file}.")
        return out_file

    def convert_distributions(self, owl_path: Optional[str] = None):
        """
        Uses ROBOT to convert the slim OWL file into OBO and OBO Graph JSON formats.
        """
        source_owl = owl_path or SLIM_OWL_FILE
        if not os.path.exists(source_owl):
            print(f"[Warning] Source OWL file does not exist: {source_owl}")
            return

        # Check if robot is available
        try:
            # 1. Convert to OBO
            print(f"Converting slim release to OBO: {SLIM_OBO_FILE}...")
            subprocess.run(
                ["robot", "convert", "-i", source_owl, "--check", "false", "--format", "obo", "-o", SLIM_OBO_FILE],
                check=True,
                capture_output=True,
                shell=True
            )
            print("Successfully generated slim OBO distribution.")

            # 2. Convert to JSON
            print(f"Converting slim release to JSON: {SLIM_JSON_FILE}...")
            subprocess.run(
                ["robot", "convert", "-i", source_owl, "--format", "json", "-o", SLIM_JSON_FILE],
                check=True,
                capture_output=True,
                shell=True
            )
            print("Successfully generated slim JSON distribution.")
        except Exception as e:
            print(f"[Notice] Distribution conversion via ROBOT had notice: {e}")
