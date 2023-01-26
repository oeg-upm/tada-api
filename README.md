# tada-web

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3764197.svg)](https://doi.org/10.5281/zenodo.3764197)
[![Python 3.6](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

This is a web API project (with Swagger) using `tada-hdt-entity` and the `pytada-hdt-entity` libraries

# Example with curl
```
curl --location --request POST 'https://api.tada.linkeddata.es/subject' \
--form 'col_id="1"' \
--form 'alpha="0.47"' \
--form 'dbpedia_only="true"' \
--form 'k="1"' \
--form 'source=@"t2dv2/5873256_0_7795190905731964989.csv"'
```

# Install
1. `sudo sh setup.sh`
2. `pip install git+https://github.com/oeg-upm/pytada-hdt-entity.git`
3. `pip install -r requirements.txt` 


# Run
`python app.py`
you can also specify the host IP and the port e.g., `python app.py 0.0.0.0 5001`
To see the list of APIs`http://127.0.0.1:5001/apidocs/`

# Parameters and Setup
* `sources.csv`. This file is expected to have the following headers: `id,name,type,source`. The `id` is the one that should be unique, but it won't be visible to the users. The `name` is the name of the source that would be shown to the users. The `type` can be an `HDT` or `SPARQL`. Finally, the `source` is the path (in the case of HDT) or the url (in the case of SPARQL). *Note that only HDT sources are supported at the moment.* 



# To cite
```
@software{alobaid_ahmad_2020_3764197,
  author       = {Alobaid, Ahmad and
                  Corcho, Oscar},
  title        = {tada-web},
  month        = apr,
  year         = 2020,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.3764197},
  url          = {https://doi.org/10.5281/zenodo.3764197}
}
```



# To run tests
1. Download the test.hdt
2. Set up environment variable `test_hdt_dir` to refer to the location of test.hdt.
3. Run tests `sh run_tests.sh`


## Tests cases
Test cases and files are taken from [tada-hdt-entity](https://github.com/oeg-upm/tada-hdt-entity)

