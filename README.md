[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kristianfoerster/DWA-a102/HEAD)

# DWA-a102
In the present work, a hydrological model based on regression equations proposed by the German techinical guideline DWA-A102 is implemented. It is a simple model and requires a limited amount of input data. The programm provides climatic data of reference (P, ETP) for 58 cities of Germany. That data can be used as input, in case that the user does not have a more recent/accurate data.

Important!!!

All the relevant methods to apply the water balance can be found in the file `dwa_a102.py`
The additional python files contain functions that are required by `dwa_a102.py`.

This work has been developed by students in different teaching contexts and it is designed for teaching purposes (with no warranty).

Files:
* `dwa_a102.py` is the library with all computations
* `dwa_a102.html` is an auto-generated help file for the library
* `Presentation_Examples.ipynb` is a jupyter notebook with examples
* `Beispiel.ipynb` is another jupyter notebook with examples (in German)
* `waterbalance_app.py` is a streamlit app, vailable at [https://wasserbilanz.streamlit.app/](https://wasserbilanz.streamlit.app/) (at present, in German only)

