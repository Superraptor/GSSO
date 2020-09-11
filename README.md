# Gender, Sex, and Sexual Orientation

The Gender, Sex, and Sexual Orientation (GSSO) ontology is an ontology which includes a vast amount of information related to gender identity, gender expression, romantic identity, sexual identity, sexual orientation, sexual behavior, sexual abuse, and various related topics. Its emphasis is on a multidisciplinary and intersectional approach to these topics.

## Usage

If you would like to use the raw OWL files here, it is recommended that you download the Protégé program [here](https://protege.stanford.edu/) and open it in that program. Alternatively you can access the system via the NCBO BioPortal API (explained below) or via our website: https://gsso.research.cchmc.org/.

### API Access

The API for the GSSO can be accessed as part of the NCBO BioPortal's API. For more information, consult the NCBO BioPortal API documentation [here](http://data.bioontology.org/documentation). Note that first you must create an NCBO BioPortal account and obtain an API key, in order for most of these calls to work.

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

## Versioning

Note that versions with "rdf_xml" in the title are in RDF/XML format, while those without utilize Manchester OWL syntax.

Further, note that PURLs utilize the "1.0.1" syntax as to be backwards compatible with any of the 1.0.1 releases. The 1.0.0 release is not forward or backward compatible at the present time. It is recommended that users utilize 2.0.0. 

Version 2.0.1 was created in an attempt to fix PURLs within the NCBO BioPortal version of GSSO so as to be more accessible, but it did not load as expected. We are in contact with the NCBO BioPortal team to attempt to fix this. Version 2.0.2 was another failed attempt, and does not function correctly (and therefore has not been updated).

Version 2.0.3 returns to the 2.0.0 PURLs and includes additional new Homosaurus mappings, mappings from the Leather Archives and Museum (LA&M), and mappings from the GLBT Historical Society's Archives.

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
* 2.0.4 (TBA)

## Contributing

Please feel free to contribute! If there is a term or terms that include unsatisfactory information, broken links, derogatory terminology that is not appropriately marked, please contact us! Additionally, we are attempting to include as much information from disparate archives as possible. If you or someone you know runs an LGBTQIA+ and/or sex archive with a controlled terminology, let us know!

A very basic search/browse interface of version 1.0.0 is located [here](http://homepages.uc.edu/~kronkcj/gsso/) for the time being. This site has been deprecated as of 2020. A new demo site is available [here](https://gsso.research.cchmc.org/).

An alpha version of 2.0.4 is also available on the NCBO BioPortal [here](http://bioportal.bioontology.org/ontologies/GSSO).

## Authors

* Clair Kronk (clair.kronk@gmail.com)

## License

This project is currently bound by the Apache 2.0 License. All mapped ontologies within GSSO are within Creative Commons, but may require separate requirements. Please check with their respective creators before utilizing.

## Publications

* Kronk C, Dexheimer J. "Development of the Gender, Sex, and Sexual Orientation Ontology: Evaluation and Workflow." _Journal of the American Medical Informatics Association_. 2020. DOI: [10.1093/jamia/ocaa061](https://doi.org/10.1093/jamia/ocaa061). PMID: [32548638](https://pubmed.ncbi.nlm.nih.gov/32548638/).
* Kronk C, Tran G, Wu D. "Creating a Queer Ontology: Introduction of the Gender, Sex, and Sexual Orientation (GSSO) Ontology." _MEDINFO 2019: Health and Wellbeing e-Networks for All_. 2019:264. DOI: [10.3233/SHTI190213](https://doi.org/10.3233/SHTI190213). PMID: [31437915](https://www.ncbi.nlm.nih.gov/pubmed/31437915).

## Acknowledgments

* Judith W. Dexheimer
* Giao Q. Tran
* Danny T. Y. Wu