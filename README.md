# Data

The README of the data is available on https://github.com/datadesk/california-coronavirus-data

# Bokeh Visualization

### Activate Conda

Start an anaconda environment using

`conda create -name <env> --file requirements.txt`

Activate the conda env:

`conda activate <env>`

### Run Bokeh

Run the following code to start the bokeh serve

`bokeh serve --show visualization.py`

The visualization will automatically start, if not try the following url: 

http://localhost:5006/visualization

### Visualization

Select the date you would like to view on the top of the page. It has been limited to August as the homework requires.

The first graph shows all the new cases trend, with a red circle indicating the new cases on the specific day you've chosen. The words beside it shows the number of new cases, confirmed cases and deaths.

The second graph shows the percentage of cases respect to races. The number on the top of each bar representing the percentage and number.

The second graph shows the percentage of deaths respect to races. The number on the top of each bar representing the percentage and number.

You can find the source and url at the bottom of each graph.