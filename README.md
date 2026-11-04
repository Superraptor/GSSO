Update, 4 November 2026:
* **Ontology Development Kit (ODK) Compliance**: This repository has been updated to follow the standard [Ontology Development Kit](https://github.com/INCATools/ontology-development-kit) layout (`src/ontology/`, `src/sparql/`, `.github/workflows/qc.yml`) while retaining full Git history, all canonical release paths, and backwards compatibility.
* **Version 2.0.11 Release**: Resolves GitHub [Issue #12](https://github.com/Superraptor/GSSO/issues/12) (invalid language tags), achieves 100% OWL 2 DL profile compliance (resolving checks on [SchemaScope](https://www.schemascope.org/o/gsso/) and the OBO Dashboard), fixes PURL release redirection in OBO metadata (`metadata/gsso.yml`), and regenerates fully validated OBO (`gsso.obo`), OBO-JSON (`gsso.json`), and Manchester (`gsso_manchester.owl`) distribution files.
* **Upcoming GSSO Version 3.0.0 & lgbtDB Integration**: We have established an initial automated conversion and validation backbone (`scripts/lgbtdb_to_gsso3/`) to transition [lgbtDB](https://lgbtdb.wikibase.cloud/) into GSSO version 3.0.0. Version 3.0.0 will initially be released as a class-only slim release. The new pipeline automatically maps existing GSSO terms, mints new identifiers, detects subclass hierarchy cycles, flags duplicate labels or missing definitions, and verifies logical consistency using the ELK reasoner so that constraint and reasoner adjustments can be made directly on lgbtDB before committing the full release to the repository. However, some more adjustments will be necessary before this version can be released, and it is recommended to use lgbtDB itself until then.

Update, 24 October 2023: I have been engaging in efforts to expand the GSSO in a format more easily accessible to those without significant programming, database, or ontology experience. I have settled on using a Wikibase setup to attain these goals. So far I have been prototyping this structure [here](https://lgbtdb.wikibase.cloud/). I am still seeking a source of funding in order to work on the database and vocabulary full-time; please feel free to reach out to me if there are any suggestions you may have regarding full-time funding or positions in which I could continue this work full-time. This new work will include a complete mapping to all versions of the GSSO, meaning all usage of the current GSSO elements will remain intact. Please do not hesitate to reach out if you have any comments, questions, or concerns.


# Gender, Sex, and Sexual Orientation

The Gender, Sex, and Sexual Orientation (GSSO) ontology is an ontology which includes a vast amount of information related to gender identity, gender expression, romantic identity, sexual identity, sexual orientation, sexual behavior, sexual abuse, and various related topics. Its emphasis is on a multidisciplinary and intersectional approach to these topics.

## Usage

If you would like to use the raw OWL files here, it is recommended that you download the Protégé program [here](https://protege.stanford.edu/) and open it in that program. Alternatively you can access the system via the NCBO BioPortal API (explained below) or via our website: https://gsso.research.cchmc.org/. It is recommended to use the OWL format (which is RDF/XML from 2.0.5 onward).

If you use the GSSO in your projects, we would really appreciate the citation! Please use the most recent publication under "Publications - GSSO Publications".

### As An Educational Tool

The GSSO's stand-alone website at CCHMC (https://gsso.research.cchmc.org/) is meant as the most accessible site for referencing individual terms for educational purposes. We are always accepting suggestions on how this interface can be improved, or collaborations we can contribute to!

### As Subject Headings

The GSSO has entered a pilot phase for usage at subject headings with the GLBT Museum & Archives. If you are interested in similar usage, please contact the author(s) at the email below!

Generally, we recommend using the label or alternate name attributes, we the IRI in parenthetical afterward. This makes it easier to see during web scraping (if a centralized database is theoretically created) regardless of system used when entering subject heading guides.

### As A Natural Language Processing (NLP) Instrument

If you are planning on using the GSSO for NLP, please contact the authors! While the scripts are currently not available on the GitHub, we can share some of our scripts (written in Python3) via email if you would like!

We recommend downplaying related synonyms and short names, for instance, as these are often ambiguous in nature.

### Translating the GSSO

If you are interested in translating the GSSO, please let us know! Contact the author(s) below if you are engaging in translation.

### Website

The GSSO is separately available at Ontobee [here](http://www.ontobee.org/ontology/GSSO), at the NCBO BioPortal [here](https://bioportal.bioontology.org/ontologies/GSSO), EMBL-EBI OLS [here](https://www.ebi.ac.uk/ols/ontologies/gsso). However, there is also a stand-alone website hosted at Cincinnati Children's Hospital and Medical Center (CCHMC), [here](https://gsso.research.cchmc.org/).

These sites update periodically based on this GitHub repository. This means that the GitHub is the only resource that is guaranteed to be up-to-date.

At the stand-alone site, there is a [text annotation feature](https://gsso.research.cchmc.org/#!/detector). Other similar annotation features are available at the NCBO BioPortal and Ontobee.

### API Access

The API for the GSSO can be accessed as part of the NCBO BioPortal's API. For more information, consult the NCBO BioPortal API documentation [here](http://data.bioontology.org/documentation). Note that first you must create an NCBO BioPortal account and obtain an API key, in order for most of these calls to work.

The GSSO can also be accessed using Ontobee's SPARQL query interface [here](http://www.ontobee.org/sparql).

#### Getting Instances for a Class

In order to get instances for a given class, the BioPortal concept ID should be created from the class ID. After 2.0.4, URIs were changed to be OBO Foundry compliant. All IDs all the same, but the rest of the URI has changed, i.e.:

```
http://purl.bioontology.org/ontology/GSSO/000047
```

And 

```
http://purl.bioontology.org/ontology/GSSO/GSSO_000047
```

Are now rendered as:

```
http://purl.obolibrary.org/obo/GSSO_000047
```

Because the BioPortal system requires encoded URLs, we will shift this into:

```
http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FGSSO_000047
```

This can also be accomplished using any URL encoder, such as: https://www.urlencoder.org/.

This is why the normal NCBO BioPortal link is rendered as:

```
https://bioportal.bioontology.org/ontologies/GSSO/?p=classes&conceptid=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FGSSO_000047
```

(however, note that `https://bioportal.bioontology.org/ontologies/GSSO/?p=classes&conceptid=http://purl.obolibrary.org/obo/GSSO_000047` will also work.)

The full URL for access to the class is thus:

```
http://data.bioontology.org/ontologies/GSSO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FGSSO_000047/
```

Note that this method will only grab instances from the current class, not from subclasses; i.e. the following:

```
http://data.bioontology.org/ontologies/GSSO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FGSSO_000140/instances
```

Will pull LGBTQ slang, but not transgender slang.

Note that if any of the following queries do not function, reattempt with just the identifier and note the full URL. Alternatively use the URL as a search term via the GSSO website itself if problems persist.

For instance, the Homosaurus link mapping can be obtained using:

```
https://gsso.research.cchmc.org/#!/entry?iri=http://homosaurus.org/v2/LGBTQPeople
```

on the website.

#### Getting GSSO from Homosaurus

Simply use the Homosaurus URI in the `q` parameter, for instance with `http://homosaurus.org/v2/LGBTQPeople`:

```
http://data.bioontology.org/search?q=http://homosaurus.org/v2/LGBTQPeople&ontologies=GSSO&also_search_properties=true
```

#### Getting GSSO from LCSH

Obtain an LCSH URI, such as `http://id.loc.gov/authorities/subjects/sh2007003708` and add it as follows:

```
http://data.bioontology.org/search?q=http://id.loc.gov/authorities/subjects/sh2007003708&ontologies=GSSO&also_search_properties=true
```

#### Getting GSSO from LCC

Getting the entry for "RC571" is implemented as follows:

```
http://data.bioontology.org/search?q=RC571&ontologies=GSSO&also_search_properties=true
```

#### Getting GSSO from MeSH

MeSH such as `http://purl.bioontology.org/ontology/MESH/D063106` can be obtained with: 

```
http://data.bioontology.org/search?q=http://purl.bioontology.org/ontology/MESH/D063106&ontologies=GSSO&also_search_properties=true
```

#### Getting GSSO from Wikipedia

If you have a Wikipedia page URL or a Wikidata URL, you can attempt to add it as follows:

```
http://data.bioontology.org/search?q=https://en.wikipedia.org/wiki/Document&ontologies=GSSO&also_search_properties=true
```

#### Getting GSSO from NCI Thesaurus

If you have an identifier such as C19498, simply append it to `http://purl.obolibrary.org/obo/NCIT_`, then form the query as follows:

```
http://data.bioontology.org/search?q=http://purl.obolibrary.org/obo/NCIT_C19498&ontologies=GSSO&also_search_properties=true
```

#### Getting GSSO from SNOMED-CT

If you have a SNOMED-CT identifier, such as `302960008`, append it to `http://purl.bioontology.org/ontology/SNOMEDCT/` and run the following:

```
http://data.bioontology.org/search?q=http://purl.bioontology.org/ontology/SNOMEDCT/302960008&ontologies=GSSO&also_search_properties=true
```

## Development & Pipeline Workflows

### Ontology Development Kit (ODK) Setup

GSSO now follows standard [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit) conventions:
* **`src/ontology/`**: Contains ontology source files, catalogs, and build scripts.
  * `gsso-edit.owl`: The primary edit file for ontology maintainers when making changes directly via Protégé.
  * `gsso-odk.yaml`: ODK configuration file specifying repository metadata, build targets, and QC rules.
  * `catalog-v001.xml`: XML catalog file mapping URIs to local imports for offline editing.
  * `run.sh` / `run.bat`: Shell wrappers to execute ROBOT and ODK commands.
* **`src/sparql/`**: SPARQL quality-control queries that automatically check for invalid cross-references, missing definitions, misused obsolete labels, and structural constraints.
* **`.github/workflows/qc.yml`**: GitHub Actions continuous integration workflow that automatically executes ROBOT quality control checks, reasoner validation, and OWL 2 DL profile tests on pull requests.

### lgbtDB to GSSO 3.0.0 Conversion Backbone

As part of the evolution toward GSSO 3.0.0, community curation is hosted at [lgbtDB](https://lgbtdb.wikibase.cloud/). We have implemented an automated conversion pipeline in `scripts/lgbtdb_to_gsso3/` (`scripts/convert_lgbtdb_to_gsso3.py`) to extract terms from lgbtDB and compile them into GSSO 3.0.0 releases.

#### Pipeline Features:
1. **Automated Extraction (`fetcher.py`)**: Connects to the lgbtDB MediaWiki Action API with batch querying, rate-limiting, and recursive ancestor retrieval to ensure complete subclass closures.
2. **Deterministic ID Mapping (`mapper.py`)**:
   * Maps existing terms containing property `P25` ("GSSO ID") directly back to their canonical GSSO V2 identifiers (e.g., `GSSO:000130`), ensuring complete backwards compatibility.
   * Mints sequential, collision-free new identifiers starting at `GSSO:0012936` for new concepts introduced in lgbtDB.
   * Extracts labels, definitions, aliases/synonyms, external database cross-references (`hasDbXref`), and subclass relationships (`wdt:P3` / `wdt:P2`).
3. **Hierarchy & Cycle Validation (`validator.py`)**:
   * Detects and flags any circular subclass dependencies using Tarjan's strongly connected components algorithm.
   * Flags duplicate labels and missing textual definitions.
   * Automatically runs the ROBOT ELK reasoner (`robot reason --reasoner ELK`) and OWL 2 DL profile validation to confirm that the generated ontology is logically consistent and satisfiable.
4. **Multi-format Generation (`generator.py`)**:
   * Emits valid, compliant OWL 2 DL RDF/XML (`gsso_3.0.0_slim.owl`), OBO format (`gsso_3.0.0_slim.obo`), and OBO-JSON (`gsso_3.0.0_slim.json`).
   * Produces an automated Markdown constraint and audit report (`constraint_report.md`).

#### Usage:
To run a test conversion on a subset of entities:
```bash
python scripts/convert_lgbtdb_to_gsso3.py all --limit 150
```

To run a full conversion and validation build:
```bash
python scripts/convert_lgbtdb_to_gsso3.py all
```

Output files are generated in `build/gsso_3.0.0_slim/` (which is excluded from Git tracking via `.gitignore`). This allows maintainers and curators to inspect constraint reports and perform reasoner checks directly on lgbtDB before committing official 3.0.0 release artifacts to the repository.

## Versioning

Note that versions with "rdf_xml" in the title are in RDF/XML format, while those without utilize Manchester OWL syntax.

Further, note that PURLs utilize the "1.0.1" syntax as to be backwards compatible with any of the 1.0.1 releases. The 1.0.0 release is not forward or backward compatible at the present time. It is recommended that users utilize 2.0.0. 

Version 2.0.1 was created in an attempt to fix PURLs within the NCBO BioPortal version of GSSO so as to be more accessible, but it did not load as expected. We are in contact with the NCBO BioPortal team to attempt to fix this. Version 2.0.2 was another failed attempt, and does not function correctly (and therefore has not been updated).

Version 2.0.3 returns to the 2.0.0 PURLs and includes additional new Homosaurus mappings, mappings from the Leather Archives and Museum (LA&M), and mappings from the GLBT Historical Society's Archives.

Versions 2.0.4 and onward switch to OBO Foundry compliant PURLs, which will be maintained for all future versions.

Version 2.0.6 is an intermediate version, adding a number of terms from the backlog of needed additions, as well as touching up a number of existing entries. It is still a work-in-progress and do not yet contain full mappings to versions 1 and 3 of the Homosaurus.

Version 2.0.7 is an alpha version, as the conversion to OBO format is not currently working. Please be patient as we attempt to fix the issue.

Version 2.0.8 is also in alpha, with only a couple small changes based on reported issues. Conversion to JSON and OBO formats has not been possible, so those files are still version 2.0.7 as of 8 July 2022.

Version 2.0.11 fixes Issue #12 (invalid `xml:lang="e"` tag in CHEBI_50112 annotation replaced with `xsd:integer`), corrects invalid language tags (`xml:lang="e"`/`"eb"` to `"en"`, `"jp"` to `"ja"`), achieves 100% OWL 2 DL profile compliance (resolving SchemaScope and OBO Dashboard issues), corrects PURL redirection for releases in OBO metadata, and restores fully regenerated, valid OBO (`gsso.obo`), OBO-JSON (`gsso.json`), and Manchester (`gsso_manchester.owl`) artifacts alongside RDF/XML (`gsso.owl`). Repository layout is now compliant with the Ontology Development Kit (ODK).

Version 3.0.0 (upcoming) will transition GSSO to a continuous-integration pipeline pulling directly from [lgbtDB](https://lgbtdb.wikibase.cloud/). The first iteration of 3.0.0 will be released as a class-only slim release. An automated extraction, ID mapping, cycle-detection, and ELK reasoning validation framework has been created under `scripts/lgbtdb_to_gsso3/`. To ensure that any ontology constraints or reasoner-related considerations are thoroughly addressed and reviewed on lgbtDB first, the 3.0.0 artifacts remain in development and are not yet committed directly to the repository main branch.

* 1.0.0 (24 June 2019)
* 1.0.1a (11 September 2019)
* 1.0.1b (12 September 2019)
* 1.0.1c (13 September 2019)
* 1.0.1d (13 September 2019)
* 1.0.1e (13 September 2019)
* 2.0.0 (18 June 2020)
* 2.0.1 (22 July 2020)
* 2.0.2 (N/A)
* 2.0.3 (N/A)
* 2.0.4 (N/A)
* 2.0.5 (N/A)
* 2.0.6 (15 October 2021)
* 2.0.7 (22 December 2021)
* 2.0.8 (8 July 2022)
* 2.0.9 (6 September 2022)
* 2.0.10 (8 September 2022)
* 2.0.11 (4 November 2026)
* 3.0.0 (Upcoming - Slim release in development)

## Contributing

Please feel free to contribute! If there is a term or terms that include unsatisfactory information, broken links, derogatory terminology that is not appropriately marked, please contact us! Additionally, we are attempting to include as much information from disparate archives as possible. If you or someone you know runs an LGBTQIA+ and/or sex archive with a controlled terminology, let us know!

A very basic search/browse interface of version 1.0.0 was located [here](http://homepages.uc.edu/~kronkcj/gsso/). This site has been deprecated as of 2020. A new demo site is available [here](https://gsso.research.cchmc.org/).

An alpha version of 2.0.4 is also available on the NCBO BioPortal [here](http://bioportal.bioontology.org/ontologies/GSSO).

There is also a survey going over various features of the GSSO [here](https://gsso.research.cchmc.org/#!/survey) if you have time to rate the GSSO!

## Authors

* Clair Kronk (clair.kronk@gmail.com)

## License

This project and any associated software created as part of the GSSO system are currently bound by the Apache 2.0 License. The GSSO ontology itself is bound by the [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) license. All mapped ontologies within GSSO are within Creative Commons, but may require separate requirements. Please check with their respective creators before utilizing.

## Publications

### GSSO Publications

* Kronk C. ''Gender, Sex and Sexual Orientation in Medicine: A Linguistic Analysis'' (2021). University of Cincinnati School of Medicine. Ph.D. Thesis. Permalink: [ucin1617107411106107](http://rave.ohiolink.edu/etdc/view?acc_num=ucin1617107411106107).

* Kronk C, Dexheimer J. "Development of the Gender, Sex, and Sexual Orientation Ontology: Evaluation and Workflow." _Journal of the American Medical Informatics Association_. 2020. DOI: [10.1093/jamia/ocaa061](https://doi.org/10.1093/jamia/ocaa061). PMID: [32548638](https://pubmed.ncbi.nlm.nih.gov/32548638/).

* Kronk C, Tran G, Wu D. "Creating a Queer Ontology: Introduction of the Gender, Sex, and Sexual Orientation (GSSO) Ontology." _MEDINFO 2019: Health and Wellbeing e-Networks for All_. 2019:264. DOI: [10.3233/SHTI190213](https://doi.org/10.3233/SHTI190213). PMID: [31437915](https://www.ncbi.nlm.nih.gov/pubmed/31437915).

### Publications Which Utilize/Cite the GSSO

If you've published something that uses the GSSO, please contact us! We'd love to add your work here!

* Lynch, K, Alba P, Patterson O, Viernes B, Coronado G, DuVall S. "The Utility of Clinical Notes for Sexual Minority Health Research." _American Journal of Preventive Medicine_. 2020. DOI: [10.1016/j.amepre.2020.05.026](https://doi.org/10.1016/j.amepre.2020.05.026). PMID: [33011005](https://pubmed.ncbi.nlm.nih.gov/33011005/)

* Tai, J. "Cultural Humility as a Framework for Anti-Oppressive Archival Description." _Journal of Critical Library and Information Studies_. 2020. 

## Projects

### Projects Which Utilize/Cite the GSSO

* [EMERSE (Electronic Medical Record Search Engine) Synonyms](https://project-emerse.org/synonyms.html)
* [GLBT Historical Society, Online Archive of California](https://oac.cdlib.org/institutions/GLBT+Historical+Society)

## Resources

### Resources Which Link to the GSSO

* [Dictionaries, Glossaries, Ontologies, and Guides at New York University (NYU) Libraries Gender and Sexuality Studies Research Guide](https://guides.nyu.edu/genderandsex/terminology)

## Acknowledgments

* Judith W. Dexheimer
* Mark H. Eckman
* Giao Q. Tran
* Danny T. Y. Wu
