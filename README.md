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
To see the list of APIs`http://127.0.0.1:5000/apidocs/`

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
```
python -m unittest discover -s tests
```