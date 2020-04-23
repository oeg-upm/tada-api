[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3764197.svg)](https://doi.org/10.5281/zenodo.3764197)

# tada-web
This is a web API project (with Swagger) using `tada-hdt-entity` and the `pytada-hdt-entity` libraries


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


