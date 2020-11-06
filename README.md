# Data

The README of the data is available on https://github.com/datadesk/california-coronavirus-data

# Bokeh Visualization

### Activate Conda

Start an vitural environment using

`python3 -m venv dsci560h5`

Activate the vitural environment:

`source dsci560h5/bin/activate`

Install the dependencies:

`pip3 install -r requirements.txt`

### Run Bokeh

Run the following code to start the bokeh serve

`bokeh serve --show visualization.py`

The visualization should run automatically, otherwise try the following url: 

http://localhost:5006/visualization

### Visualization

Select the date you would like to view on the top of the page. It has been limited to August as the homework requires.

The first graph shows all the new cases trend, with a red circle indicating the new cases on the specific day you've chosen. The words beside it shows the number of new cases, confirmed cases and deaths. The second graph shows the percentage of cases respect to races. The number on the top of each bar representing the percentage and number. The second graph shows the percentage of deaths respect to races. The number on the top of each bar representing the percentage and number. You can find the source and url at the bottom of each graph.

Since there are some missing data, some of the cases by races and deaths by races will show all 0% if the data of that day is missing.

### Docker

Build the docker using:

`docker build --tag dsci560h5 .`

Run the image using:

`docker run -p 5006:5006 -it dsci560h5`

And get the result:

`http://localhost:5006/visualization`


