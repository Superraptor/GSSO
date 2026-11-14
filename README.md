Update, 4 November 2026:
* **New GitHub Pages Web Portal**: To provide a permanent, reliable, and open replacement for the former CCHMC stand-alone site, we have launched an interactive web portal hosted directly from this repository at **[https://superraptor.github.io/GSSO/](https://superraptor.github.io/GSSO/)**. Located in the `www/` directory (fully isolated from ODK workflows), the portal provides instant client-side term search, the text annotation detector (`#!/detector`), an interactive hierarchy tree (`#!/tree`), cross-walk lookups (`#!/mappings`), and complete backward compatibility with PURL redirects and entry links (`#!/entry?iri=...`).
* **Ontology Development Kit (ODK) Compliance**: This repository has been updated to follow the standard [Ontology Development Kit](https://github.com/INCATools/ontology-development-kit) layout (`src/ontology/`, `src/sparql/`, `.github/workflows/qc.yml`) while retaining full Git history, all canonical release paths, and backwards compatibility.
* **Version 2.0.11 Release**: Resolves GitHub [Issue #12](https://github.com/Superraptor/GSSO/issues/12) (invalid language tags), achieves 100% OWL 2 DL profile compliance (resolving checks on [SchemaScope](https://www.schemascope.org/o/gsso/) and the OBO Dashboard), fixes PURL release redirection in OBO metadata (`metadata/gsso.yml`), and regenerates fully validated OBO (`gsso.obo`), OBO-JSON (`gsso.json`), and Manchester (`gsso_manchester.owl`) distribution files.
* **Upcoming GSSO Version 3.0.0 & lgbtDB Integration**: We have established an initial automated conversion and validation backbone (`scripts/lgbtdb_to_gsso3/`) to transition [lgbtDB](https://lgbtdb.wikibase.cloud/) into GSSO version 3.0.0. Version 3.0.0 will initially be released as a class-only slim release. The new pipeline automatically maps existing GSSO terms, mints new identifiers, detects subclass hierarchy cycles, flags duplicate labels or missing definitions, and verifies logical consistency using the ELK reasoner so that constraint and reasoner adjustments can be made directly on lgbtDB before committing the full release to the repository. However, some more adjustments will be necessary before this version can be released, and it is recommended to use lgbtDB itself until then.

Update, 24 October 2023: I have been engaging in efforts to expand the GSSO in a format more easily accessible to those without significant programming, database, or ontology experience. I have settled on using a Wikibase setup to attain these goals. So far I have been prototyping this structure [here](https://lgbtdb.wikibase.cloud/). I am still seeking a source of funding in order to work on the database and vocabulary full-time; please feel free to reach out to me if there are any suggestions you may have regarding full-time funding or positions in which I could continue this work full-time. This new work will include a complete mapping to all versions of the GSSO, meaning all usage of the current GSSO elements will remain intact. Please do not hesitate to reach out if you have any comments, questions, or concerns.


# Gender, Sex, and Sexual Orientation

The Gender, Sex, and Sexual Orientation (GSSO) ontology is an ontology which includes a vast amount of information related to gender identity, gender expression, romantic identity, sexual identity, sexual orientation, sexual behavior, sexual abuse, and various related topics. Its emphasis is on a multidisciplinary and intersectional approach to these topics.

## Usage

If you would like to use the raw OWL files here, it is recommended that you download the Protégé program [here](https://protege.stanford.edu/) and open it in that program. Alternatively you can access the system via the NCBO BioPortal API (explained below) or via our new website: **[https://superraptor.github.io/GSSO/](https://superraptor.github.io/GSSO/)** (note, the previous host at `https://gsso.research.cchmc.org/` is no longer available and has been replaced by GitHub Pages). It is recommended to use the OWL format (which is RDF/XML from 2.0.5 onward).

If you use the GSSO in your projects, we would really appreciate the citation! Please use the most recent publication under "Publications - GSSO Publications".

### As An Educational Tool

The GSSO's official web portal is available at **[https://superraptor.github.io/GSSO/](https://superraptor.github.io/GSSO/)** (which replaces the previous stand-alone site at CCHMC). It is meant as the most accessible site for referencing individual terms for educational purposes. We are always accepting suggestions on how this interface can be improved, or collaborations we can contribute to!

### As Subject Headings

The GSSO has entered a pilot phase for usage at subject headings with the GLBT Museum & Archives. If you are interested in similar usage, please contact the author(s) at the email below!

Generally, we recommend using the label or alternate name attributes, we the IRI in parenthetical afterward. This makes it easier to see during web scraping (if a centralized database is theoretically created) regardless of system used when entering subject heading guides.

### As A Natural Language Processing (NLP) Instrument

If you are planning on using the GSSO for NLP, please contact the authors! While the scripts are currently not available on the GitHub, we can share some of our scripts (written in Python3) via email if you would like! You can also use our interactive online **[Text Annotation & Concept Detector](https://superraptor.github.io/GSSO/#!/detector)**.

We recommend downplaying related synonyms and short names, for instance, as these are often ambiguous in nature.

### Translating the GSSO

If you are interested in translating the GSSO, please let us know! Contact the author(s) below if you are engaging in translation.

### Website

The GSSO is separately available at Ontobee [here](http://www.ontobee.org/ontology/GSSO), at the NCBO BioPortal [here](https://bioportal.bioontology.org/ontologies/GSSO), and EMBL-EBI OLS [here](https://www.ebi.ac.uk/ols/ontologies/gsso).

**Official Web Portal (GitHub Pages):**
Our new official web portal is live at **[https://superraptor.github.io/GSSO/](https://superraptor.github.io/GSSO/)**. Hosted directly from the `www/` directory without affecting ODK workflows, it provides:
* **Interactive Term Explorer**: Browse all 12,700+ terms, definitions, comments, synonyms, and mappings. Supports canonical PURL hash routing (e.g. `https://superraptor.github.io/GSSO/#!/entry?iri=http://purl.obolibrary.org/obo/GSSO_000130`).
* **Text Annotation Feature (`#!/detector`)**: Automatically identify, highlight, and annotate GSSO concepts in clinical notes, abstracts, and raw text.
* **Hierarchy Tree (`#!/tree`)**: Expandable ontology tree browser for navigating classes and subclasses.
* **Vocabulary Crosswalks (`#!/mappings`)**: Search across mappings to Homosaurus, Wikidata, MeSH, LCSH, NCIt, and SNOMED-CT.
* **Downloads Hub (`#!/downloads`)**: Quick downloads for OWL, OBO, JSON, and Manchester distributions.

*Historical Note:* A stand-alone website was previously hosted at Cincinnati Children's Hospital and Medical Center (CCHMC) at `https://gsso.research.cchmc.org/`. That server is no longer active, and all features (including the text detector and term browsing) have been migrated to the new GitHub Pages portal.

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
https://superraptor.github.io/GSSO/#!/entry?iri=http://homosaurus.org/v2/LGBTQPeople
```

on the website (formerly `https://gsso.research.cchmc.org/#!/entry?iri=...`).

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

A very basic search/browse interface of version 1.0.0 was located [here](http://homepages.uc.edu/~kronkcj/gsso/). This site has been deprecated as of 2020. A new demo site was available [here](https://gsso.research.cchmc.org/), but is no longer available.

An alpha version of 2.0.4 is also available on the NCBO BioPortal [here](http://bioportal.bioontology.org/ontologies/GSSO).

There was also a survey going over various features of the GSSO [here](https://gsso.research.cchmc.org/#!/survey), although it is now closed.

## Authors

* [Clair Kronk](https://orcid.org/0000-0001-8397-8810) (clair.kronk@gmail.com)

## License

This project and any associated software created as part of the GSSO system are currently bound by the Apache 2.0 License. The GSSO ontology itself is bound by the [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) license. All mapped ontologies within GSSO are within Creative Commons, but may require separate requirements. Please check with their respective creators before utilizing.

## Publications

### GSSO Publications

* Kronk C. ''Gender, Sex and Sexual Orientation in Medicine: A Linguistic Analysis'' (2021). University of Cincinnati School of Medicine. Ph.D. Thesis. Permalink: [ucin1617107411106107](http://rave.ohiolink.edu/etdc/view?acc_num=ucin1617107411106107).

* Kronk C, Dexheimer J. "Development of the Gender, Sex, and Sexual Orientation Ontology: Evaluation and Workflow." _Journal of the American Medical Informatics Association_. 2020. DOI: [10.1093/jamia/ocaa061](https://doi.org/10.1093/jamia/ocaa061). PMID: [32548638](https://pubmed.ncbi.nlm.nih.gov/32548638/).

* Kronk C, Tran G, Wu D. "Creating a Queer Ontology: Introduction of the Gender, Sex, and Sexual Orientation (GSSO) Ontology." _MEDINFO 2019: Health and Wellbeing e-Networks for All_. 2019:264. DOI: [10.3233/SHTI190213](https://doi.org/10.3233/SHTI190213). PMID: [31437915](https://www.ncbi.nlm.nih.gov/pubmed/31437915).

### Publications Which Utilize/Cite the GSSO (or lgbtDB)

If you've published something that uses the GSSO or lgbtDB, please contact us! We'd love to add your work here!

* Hogenboom J, Gouthamchand V, Cairns C, Janssen SHM, Way KM, Dekker AL, et al. "Knowledge Representation of a Multicenter Adolescent and Young Adult Cancer Infrastructure: Development of the STRONG AYA Knowledge Graph." _JCO Clinical Cancer Informatics_. 2026. DOI: [10.1200/cci-25-00177](https://doi.org/10.1200/cci-25-00177). PMID: [41534005](https://pubmed.ncbi.nlm.nih.gov/41534005/).

* Lv F, Qian Q, Fan Z, Zhan Y, Zeng J, Xiao J. "PWAS Atlas: a comprehensive knowledgebase of proteome-wide association studies." _Nucleic Acids Research_. 2026. DOI: [10.1093/nar/gkag967](https://doi.org/10.1093/nar/gkag967). PMID: [42865327](https://pubmed.ncbi.nlm.nih.gov/42865327/).

* Diksha, Sharma A, Dhar M. "Toward Inclusive Metadata: A Multilingual Framework for Representing Queer Identities in Indian Digital Repositories." _Cataloging & Classification Quarterly_. 2026. DOI: [10.1080/01639374.2026.2664520](https://doi.org/10.1080/01639374.2026.2664520).

* Perchyk T, Hunt IDV, Nicholson BD, Mounce LTA, Sykes K, Lyratzopoulos G, et al. "How well are marginalised groups represented in electronic records? A codelist development project and cross-sectional analysis of UK electronic health records." _BMJ Open_. 2025. DOI: [10.1136/bmjopen-2024-098305](https://doi.org/10.1136/bmjopen-2024-098305). PMID: [40789724](https://pubmed.ncbi.nlm.nih.gov/40789724/).

* Hochheiser H, Visweswaran S. "In defense of empathic informatics." _Journal of the American Medical Informatics Association_. 2025. DOI: [10.1093/jamia/ocaf107](https://doi.org/10.1093/jamia/ocaf107). PMID: [40644430](https://pubmed.ncbi.nlm.nih.gov/40644430/).

* Zhang X, Lai H, Meng Q, Bos J. "OntoURL: A Benchmark for Evaluating Large Language Models on Symbolic Ontological Understanding, Reasoning and Learning." _arXiv preprint arXiv:2505.11031_. 2025. DOI: [10.48550/arxiv.2505.11031](https://doi.org/10.48550/arxiv.2505.11031).

* Paletta P, Mosconi P, Bergamaschi R, Santucci C, Lepore V, Tavazzi E. "Sex and Gender Transition of People With Multiple Sclerosis: A Real‐World Perspective." _European Journal of Neurology_. 2025. DOI: [10.1111/ene.70409](https://doi.org/10.1111/ene.70409). PMID: [41288286](https://pubmed.ncbi.nlm.nih.gov/41288286/).

* Veloso L, Hirlimann L, Zidar LM, Wicke P, Hofmann V, Schütze H. "SLAyiNG: A Diverse and Community-validated Dataset of Queer Slang." _arXiv preprint arXiv:2509.17449_. 2025. DOI: [10.48550/arxiv.2509.17449](https://doi.org/10.48550/arxiv.2509.17449).

* Adamidou M, Wang S. "Towards Semi-automatic Construction of Multilingual LGBTQ+ Conceptual Models." _MDTT_. 2025. URL: [https://www.semanticscholar.org/paper/877f0156215fedf879647328631cb5db176f872b](https://www.semanticscholar.org/paper/877f0156215fedf879647328631cb5db176f872b).

* Ruiz‐Serra V, Buslón N, Philippe O, Saby D, Morales MP, Pontes CFT, et al. "Analyzing sex imbalance in EGA and dbGaP biological databases: Recommendations for better practices." _iScience_. 2024. DOI: [10.1016/j.isci.2024.110831](https://doi.org/10.1016/j.isci.2024.110831). PMID: [39474070](https://pubmed.ncbi.nlm.nih.gov/39474070/).

* Lobo P, Daga E, Alani H, Fernández M. "Enhancing Hate Speech Annotations with Background Semantics." _European Conference on Artificial Intelligence_. 2024. DOI: [10.3233/faia240957](https://doi.org/10.3233/faia240957).

* Wang S, Adamidou M. "Examining LGBTQ+-Related Concepts in the Semantic Web: Link Discovery, Concept Drift, Ambiguity, and Multilingual Information Reuse." _Lecture Notes in Computer Science_. 2024. DOI: [10.1007/978-3-031-77792-9_1](https://doi.org/10.1007/978-3-031-77792-9_1).

* Malatesta G, Marzoli D, Lucafò C, D’Anselmo A, Azzilonna T, Prete G, Tommasi L. "Functional lateralization in social-emotional processing: The influence of sexual orientation and gender identity on cradling preferences." _Early Human Development_. 2024. DOI: [10.1016/j.earlhumdev.2024.106049](https://doi.org/10.1016/j.earlhumdev.2024.106049). PMID: [38781713](https://pubmed.ncbi.nlm.nih.gov/38781713/).

* Kim W, Donise KR, Brown KA, Cancilliere MK, Chen ES. "Identifying and Characterizing the Transgender and Nonbinary Population Presenting to Pediatric Psychiatry Emergency Services." _PubMed Central_. 2024. PMID: [38827092](https://pubmed.ncbi.nlm.nih.gov/38827092/).

* Ho N, Williams A, Sun Z. "Improving radiology information systems for inclusivity of transgender and gender‐diverse patients: what are the problems and what are the solutions? A systematic review." _Journal of Medical Radiation Sciences_. 2024. DOI: [10.1002/jmrs.808](https://doi.org/10.1002/jmrs.808). PMID: [39030738](https://pubmed.ncbi.nlm.nih.gov/39030738/).

* Becker RA, Walsh CG. "Prospective Validation of a Suicide Event Risk Model in Transgender Patients." _AMIA Annual Symposium Proceedings_. 2024. PMID: [41726488](https://pubmed.ncbi.nlm.nih.gov/41726488/).

* Slater LT, Schofield PN, Wright J, Clift P, Irani A, Bradlow WM, Aziz F, Gkoutos GV. "Talking about diseases; developing a model of patient and public-prioritised disease phenotypes." _npj Digital Medicine_. 2024. DOI: [10.1038/s41746-024-01257-8](https://doi.org/10.1038/s41746-024-01257-8). PMID: [39349692](https://pubmed.ncbi.nlm.nih.gov/39349692/).

* Ruggieri S, Álvarez JM, Pugnana A, State L, Turini F. "Can We Trust Fair-AI?." _Proceedings of the AAAI Conference on Artificial Intelligence_. 2023. DOI: [10.1609/aaai.v37i13.26798](https://doi.org/10.1609/aaai.v37i13.26798).

* Lobo PR, Daga E, Alani H, Fernández M. "Knowledge-Grounded Target Group Language Recognition in Hate Speech." _Studies on the Semantic Web_. 2023. DOI: [10.3233/ssw230002](https://doi.org/10.3233/ssw230002).

* Dhrangadhariya A, Müller H. "Not so weak PICO: leveraging weak supervision for participants, interventions, and outcomes recognition for systematic review automation." _JAMIA Open_. 2023. DOI: [10.1093/jamiaopen/ooac107](https://doi.org/10.1093/jamiaopen/ooac107). PMID: [36632329](https://pubmed.ncbi.nlm.nih.gov/36632329/).

* Weathington K, Brubaker JR. "Queer Identities, Normative Databases: Challenges to Capturing Queerness On Wikidata." _Proc. ACM Hum. Comput. Interact_. 2023. DOI: [10.1145/3579517](https://doi.org/10.1145/3579517).

* Buslón N, Cortés À, Catuara‐Solarz S, Cirillo D, Rementeria MJ. "Raising awareness of sex and gender bias in artificial intelligence and health." _Frontiers in Global Women's Health_. 2023. DOI: [10.3389/fgwh.2023.970312](https://doi.org/10.3389/fgwh.2023.970312). PMID: [37746321](https://pubmed.ncbi.nlm.nih.gov/37746321/).

* Diller MA, Yin P, Brochhausen M, Bian J, Hu HZ, Hogan WR. "Representation of the External Exposome in Ontologies: A Scoping Review (Preprint)." 2023. DOI: [10.2196/preprints.49568](https://doi.org/10.2196/preprints.49568).

* Waltemath D, Beelich H, Töpfer P, Bergelt C, Flöel A, Katsari E, et al. "Representing Sex and Gender Information in Biomedical Research." _Studies in Health Technology and Informatics_. 2023. DOI: [10.3233/shti230259](https://doi.org/10.3233/shti230259). PMID: [37203489](https://pubmed.ncbi.nlm.nih.gov/37203489/).

* Slater KT, Schofield PN, Wright J, Clift P, Irani A, Bradlow W, Aziz F, Gkoutos GV. "Talking about diseases; developing a patient and public-centered phenotype model from social media data." _medRxiv_. 2023. DOI: [10.1101/2023.12.19.23300163](https://doi.org/10.1101/2023.12.19.23300163).

* Hastings J. "Achieving Inclusivity by Design: Social and Contextual Information in Medical Knowledge." _Yearbook of Medical Informatics_. 2022. DOI: [10.1055/s-0042-1742509](https://doi.org/10.1055/s-0042-1742509). PMID: [35654426](https://pubmed.ncbi.nlm.nih.gov/35654426/).

* Anderson EL, Eleazer JR, Kristensen Z, Amand CMS, Baker AM, Correro AN, et al. "Affirmative neuropsychological practice with transgender and gender diverse individuals and communities." _The Clinical Neuropsychologist_. 2022. DOI: [10.1080/13854046.2022.2073915](https://doi.org/10.1080/13854046.2022.2073915). PMID: [35642438](https://pubmed.ncbi.nlm.nih.gov/35642438/).

* Diller M, Hogan W. "An Ontological Representation of Money with a View Toward Economic Determinants of Health." _International Conference on Biomedical Ontology_. 2022. URL: [https://www.semanticscholar.org/paper/6802f20c31cda53e017dcdfc49035d2f3accb533](https://www.semanticscholar.org/paper/6802f20c31cda53e017dcdfc49035d2f3accb533).

* Goyer F, Fabry P, Barton A, Éthier J. "An Ontology for Healthcare Systems." _International Conference on Biomedical Ontology_. 2022. URL: [https://www.semanticscholar.org/paper/50b4c2ffbdb45388035cb01ab0823153a6c87ef9](https://www.semanticscholar.org/paper/50b4c2ffbdb45388035cb01ab0823153a6c87ef9).

* Nabergoj Makovec U, Goetzinger C, Ribaut J, Barnestein-Fonseca P, Haupenthal F, Herdeiro MT, et al. "Developing a medication adherence technologies repository: proposed structure and protocol for an online real-time Delphi study." _BMJ Open_. 2022. DOI: [10.1136/bmjopen-2021-059674](https://doi.org/10.1136/bmjopen-2021-059674). PMID: [35459677](https://pubmed.ncbi.nlm.nih.gov/35459677/).

* Tasker K, Taketa R, Macquarie C, Deardorff A. "Digital Archives and Data Science: Building Programs and Partnerships for Health Sciences Research." _Advances in Library and Information Science_. 2022. DOI: [10.4018/978-1-7998-9702-6.ch007](https://doi.org/10.4018/978-1-7998-9702-6.ch007).

* Koehle H, Kronk CA, Lee YJ. "Digital Health Equity: Addressing Power, Usability, and Trust to Strengthen Health Systems." _Yearbook of Medical Informatics_. 2022. DOI: [10.1055/s-0042-1742512](https://doi.org/10.1055/s-0042-1742512). PMID: [36463865](https://pubmed.ncbi.nlm.nih.gov/36463865/).

* Ladewig MS, Jacobsen JO, Wagner AH, Daniš D, Kassaby BE, Gargano MA, et al. "GA4GH Phenopackets: A Practical Introduction." _Advanced Genetics_. 2022. DOI: [10.1002/ggn2.202200016](https://doi.org/10.1002/ggn2.202200016). PMID: [36910590](https://pubmed.ncbi.nlm.nih.gov/36910590/).

* Hong Y, Zeng M. "International Classification of Diseases (ICD)." _Knowledge Organization_. 2022. DOI: [10.5771/0943-7444-2022-7-496](https://doi.org/10.5771/0943-7444-2022-7-496).

* Correro AN, Hinrichs KLM, Krishnan M, Cottingham ME, Trittschuh EH, Parmenter BA, Kang J, Stelmokas J. "Neuropsychological assessment with lesbian, gay, bisexual, transgender, and queer/questioning (LGBTQ+) individuals: Practice, education, and training survey." _The Clinical Neuropsychologist_. 2022. DOI: [10.1080/13854046.2022.2148379](https://doi.org/10.1080/13854046.2022.2148379). PMID: [36458596](https://pubmed.ncbi.nlm.nih.gov/36458596/).

* Morska N. "Ontology of human rights in today's globalized world: the philosophical dimension." _Revista Amazonia Investiga_. 2022. DOI: [10.34069/ai/2022.60.12.27](https://doi.org/10.34069/ai/2022.60.12.27).

* Crompton C. "SémantiQueer: Making Linked Data Work for Public History." _Springer_. 2022. DOI: [10.1007/978-3-031-11886-9_6](https://doi.org/10.1007/978-3-031-11886-9_6).

* Reavis KM, Bisgaard N, Canlon B, Dubno JR, Frisina RD, Hertzano RP, et al. "Sex-Linked Biology and Gender-Related Research Is Essential to Advancing Hearing Health." _Ear and Hearing_. 2022. DOI: [10.1097/aud.0000000000001291](https://doi.org/10.1097/aud.0000000000001291). PMID: [36384870](https://pubmed.ncbi.nlm.nih.gov/36384870/).

* Davison KS. "Standards Developments for Improving Care for Transgender People." _IntechOpen_. 2022. DOI: [10.5772/intechopen.101907](https://doi.org/10.5772/intechopen.101907).

* Lobo PR, Daga E, Alani H. "Supporting Online Toxicity Detection with Knowledge Graphs." _Proceedings of the International AAAI Conference on Web and Social Media_. 2022. DOI: [10.1609/icwsm.v16i1.19398](https://doi.org/10.1609/icwsm.v16i1.19398).

* Sineath RC, Blasdel G, Dy GW. "Addressing Urologic Health Disparities in Sexual and Gender Minority Communities Through Patient-Centered Outcomes Research." _Urology_. 2021. DOI: [10.1016/j.urology.2021.08.065](https://doi.org/10.1016/j.urology.2021.08.065). PMID: [34774931](https://pubmed.ncbi.nlm.nih.gov/34774931/).

* Kronk CA, Dexheimer JW. "An ontology-based review of transgender literature: Revealing a history of medicalization and pathologization." _International Journal of Medical Informatics_. 2021. DOI: [10.1016/j.ijmedinf.2021.104601](https://doi.org/10.1016/j.ijmedinf.2021.104601). PMID: [34649111](https://pubmed.ncbi.nlm.nih.gov/34649111/).

* Thompson HM, Kronk CA, Feasley K, Pachwicewicz P, Karnik NS. "Implementation of Gender Identity and Assigned Sex at Birth Data Collection in Electronic Health Records: Where Are We Now?." _International Journal of Environmental Research and Public Health_. 2021. DOI: [10.3390/ijerph18126599](https://doi.org/10.3390/ijerph18126599). PMID: [34205275](https://pubmed.ncbi.nlm.nih.gov/34205275/).

* Coladangelo LP. "Organizing Controversy: Toward Cultural Hospitality in Controlled Vocabularies Through Semantic Annotation." _Knowledge Organization_. 2021. DOI: [10.5771/0943-7444-2021-3-195](https://doi.org/10.5771/0943-7444-2021-3-195).

* Kloer C, Blasdel G, Morris MX, Zhao LC, Bluebond‐Langner R. "Overview of Gender Affirming Surgery for the Gynecologic Surgeon." _Journal of Gynecologic Surgery_. 2021. DOI: [10.1089/gyn.2021.0042](https://doi.org/10.1089/gyn.2021.0042).

* Antonio MG, Lau F, Davison KS, Devor A, Queen R, Courtney KL. "Toward an inclusive digital health system for sexual and gender minorities in Canada." _Journal of the American Medical Informatics Association_. 2021. DOI: [10.1093/jamia/ocab183](https://doi.org/10.1093/jamia/ocab183). PMID: [34605910](https://pubmed.ncbi.nlm.nih.gov/34605910/).

* Kronk CA, Everhart AR, Ashley F, Thompson HM, Schall TE, Goetz TG, et al. "Transgender data collection in the electronic health record: Current concepts and issues." _Journal of the American Medical Informatics Association_. 2021. DOI: [10.1093/jamia/ocab136](https://doi.org/10.1093/jamia/ocab136). PMID: [34486655](https://pubmed.ncbi.nlm.nih.gov/34486655/).

* Ram A, Kronk CA, Eleazer JR, Goulet JL, Brandt C, Wang K. "Transphobia, encoded: an examination of trans-specific terminology in SNOMED CT and ICD-10-CM." _Journal of the American Medical Informatics Association_. 2021. DOI: [10.1093/jamia/ocab200](https://doi.org/10.1093/jamia/ocab200). PMID: [34569604](https://pubmed.ncbi.nlm.nih.gov/34569604/).

* Lau F, Antonio MG, Davison KS, Queen R, Bryski K. "An Environmental Scan of Sex and Gender in Electronic Health Records: Analysis of Public Information Sources." _Journal of Medical Internet Research_. 2020. DOI: [10.2196/20050](https://doi.org/10.2196/20050). PMID: [33174858](https://pubmed.ncbi.nlm.nih.gov/33174858/).

* Lynch KE, Alba PR, Patterson OV, Viernes B, Coronado G, DuVall SL. "The Utility of Clinical Notes for Sexual Minority Health Research." _American Journal of Preventive Medicine_. 2020. DOI: [10.1016/j.amepre.2020.05.026](https://doi.org/10.1016/j.amepre.2020.05.026). PMID: [33011005](https://pubmed.ncbi.nlm.nih.gov/33011005/).

* Tai, J. "Cultural Humility as a Framework for Anti-Oppressive Archival Description." _Journal of Critical Library and Information Studies_. 2020.

## Projects

### Projects Which Utilize/Cite the GSSO (or lgbtDB)

* [EMERSE (Electronic Medical Record Search Engine) Synonyms](https://project-emerse.org/synonyms.html) - Clinical text search engine utilizing GSSO terminology for sexual and gender minority synonym expansion.
* [GLBT Historical Society, Online Archive of California](https://oac.cdlib.org/institutions/GLBT+Historical+Society) - Subject headings pilot integrating GSSO concepts into archival collection guides.
* [Obsessive Compulsive Disorder Ontology (OCDO)](https://github.com/Aliaia/ocd-ontology) - Biomedical domain ontology that integrates and imports GSSO for equivalence linking and demographic representation.
* [Sickle Cell Disease Ontology (SCDO)](https://github.com/scdodev/scdo-ontology) - Standardized sickle cell disease ontology utilizing GSSO cross-references in its official SSSOM mapping tables.
* [SLAyiNG (Queer Slang Dataset)](https://github.com/leonorv/slaying-dataset) - Open-source NLP benchmark dataset (LMU Munich / MCML) utilizing lgbtDB (`lgbtdb.wikibase.cloud`) and GSSO for community-validated terminology and slang.
* [Wikidata Property P9827 (GSSO ID)](https://www.wikidata.org/wiki/Property:P9827) - Dedicated Wikidata property with over 1,220 entities mapped to canonical GSSO identifiers, with claims utilizing GSSO as an authoritative reference source.

## Resources

### Resources Which Link to the GSSO

* [BARTOC: Basel Register of Thesauri, Ontologies & Classifications](https://bartoc.org/en/node/20833) - University of Basel European registry entry for the Gender, Sex, and Sexual Orientation Ontology.
* [Bioregistry (gsso)](https://bioregistry.io/registry/gsso) - Academic registry entry of biological prefixes, namespace schemas, and metadata for `gsso`.
* [Dictionaries, Glossaries, Ontologies, and Guides at New York University (NYU) Libraries Gender and Sexuality Studies Research Guide](https://guides.nyu.edu/genderandsex/terminology) - NYU Libraries resource guide for gender and sexuality terminology.
* [EMBL-EBI Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols4/ontologies/gsso) - European Bioinformatics Institute ontology browser and term hierarchy viewer.
* [NCBO BioPortal](https://bioportal.bioontology.org/ontologies/GSSO) - National Center for Biomedical Ontology repository, visualization, and REST API access.
* [OBO Foundry](https://obofoundry.org/ontology/gsso.html) - Official repository page and persistent URL resolver under the Open Biological and Biomedical Ontologies Foundry.
* [Ontobee](https://ontobee.org/ontology/GSSO) - Linked open data server and SPARQL query endpoint for GSSO.
* [SchemaScope](https://www.schemascope.org/o/gsso/) - Semantic web quality dashboard evaluating OWL 2 DL compliance, documentation, and structural metrics.

## Acknowledgments

* Judith W. Dexheimer
* Mark H. Eckman
* Giao Q. Tran
* Danny T. Y. Wu
