#!/usr/bin/env python

#
#	Clair Kronk
#	11 September 2020
#	convert_to_obo.py
#

# Note: It is not recommended to use the OBO version of the GSSO,
# as it only uses the first label, the first definition, and cuts
# out all instances/individuals (and all of their associated
# annotations and subannotations).
#
# In order to do this, you must modify a few of the files in the
# pronto package to avoid errors that will pop up because there
# are instances/individuals in the GSSO.
#
# Comment out line 235 `raise KeyError(id)` in ontology.py.
#
# Add an `except AttributeError: pass` after line 738 in 
# parsers/rdfxml.py. Also add a try/except around the block
# directly following, also ending with an `except AttributeError: pass`.
#
# Finally, add a try/except `ValueError: pass` around line 117 in 
# serializers/_fastobo.py.

# https://pypi.org/project/pronto/
# Version 2.2.3 used for conversions.
from pronto import Ontology

import os.path

gsso_owl_file = "../gsso.owl"

def main():
    if does_file_exist(gsso_owl_file):
        gsso_loaded = load_ontology(gsso_owl_file)
        convert_file(onto=gsso_loaded)
    else:
        print("File %s does not exist." % gsso_owl_file)

def load_ontology(ontology_uri=gsso_owl_file):
    return Ontology(ontology_uri)

def convert_file(onto, obo_file_name="../gsso.obo"):
    with open(obo_file_name, 'wb') as f:
        onto.dump(f, format='obo')
        
def does_file_exist(file_path):
    return os.path.isfile(file_path)
        
if __name__ == '__main__':
    main()