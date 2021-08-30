# Interactive molecular data explorer and online survey application
[![DOI](https://zenodo.org/badge/258546525.svg)](https://zenodo.org/badge/latestdoi/258546525)

This repository is the source of the [web application](https://www.molecular-photocatalysts-library.app) 
in our [published paper](https://doi.org/10.1039/D1SC02150H).

The online challenge link will guide users to one of our Google sheets and contributing 
the competition of prediction of hydrogen evolution rate between machine learning model and human.

It uses Dash to achieve interactive HTML functions and Plotly to build scatter figures.
The web app is deployed to Heroku server.


## Authors
Yu Che, Hao Pin, Linjiang Chen

### Related publication:
* Li, X., Maffettone, P. M., Che, Y., Liu, T., Chen, L., & Cooper, A. (2021). 
  Combining machine learning and high-throughput experimentation to discover 
  photocatalytically active organic molecules. Chemical Science.
* DOI: https://doi.org/10.1039/D1SC02150H

## Run application locally
Create a new virtual environment by ```conda```:

```
conda create -n dash_app python=3.7
conda activate dash_app
```

Install dependence packages:

```pip install -r requirements.txt```

After installation, you can run the web application through terminal:

```python app.py```

The default local web page is http://127.0.0.1:8050/

## More information
Tutorial for Dash:
https://dash.plotly.com/

Tutorial for plotly:
https://plotly.com/python/