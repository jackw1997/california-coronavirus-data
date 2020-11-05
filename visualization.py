
# import data for visualization 
import pandas as pd
import re
from datetime import datetime as dt

# total dataset
ds = pd.read_csv('latimes-state-totals.csv')
confirm = ds[['date', 'new_confirmed_cases', 'confirmed_cases', 'deaths']]
for i in range(len(confirm)):
    date_split = confirm.iloc[i, 0].split('-')
    confirm.iloc[i, 0] = dt(int(date_split[0]), int(date_split[1]), int(date_split[2]))


# race dataset
race_ds = pd.read_csv('cdph-race-ethnicity.csv')
# reduce the dataset size to only data needed in visualization
race_ds = race_ds.loc[race_ds['age'] == 'all']
races = list(race_ds['race'].unique())


#bokeh
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import CustomJS, DatePicker, ColumnDataSource, LabelSet, ranges, Label, Div
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap

x = confirm['date'].to_list()
origin_date = ds['date'].to_list()
y = confirm['new_confirmed_cases'].to_list()
confirmed_cases=confirm['confirmed_cases'].to_list()
total_deaths=confirm['deaths'].to_list()

x.reverse()
y.reverse()
origin_date.reverse()
confirmed_cases.reverse()
total_deaths.reverse()

all_races = race_ds['race'].to_list()
dates = race_ds['date'].to_list()
cases = race_ds['confirmed_cases_percent'].to_list()
num_cases = race_ds['confirmed_cases_total'].to_list()
deaths = race_ds['deaths_percent'].to_list()
num_deaths = race_ds['deaths_total'].to_list()

s1 = ColumnDataSource(data=dict(x=x, y=y, z=origin_date, p=confirmed_cases, q=total_deaths))
s2 = ColumnDataSource(data=dict(x=[], y=[], names=[], confirmed_cases=[], deaths=[]))
s3 = ColumnDataSource(data=dict(x=races, cases=[0 for i in range(len(races))], \
    deaths=[0 for i in range(len(races))], positionx=[1,2,3,4,5,6], positiony1=[0.5 for i in range(len(races))], \
    num_cases = [0 for i in range(len(races))], num_deaths = [0 for i in range(len(races))], \
    label1=[0 for i in range(len(races))], cases_text = ['0%' for i in range(len(races))], deaths_text = ['0%' for i in range(len(races))]))
s4 = ColumnDataSource(data=dict(x=all_races, date=dates, cases=cases, deaths=deaths,\
    num_cases=num_cases, num_deaths=num_deaths))

plot = figure(plot_height=600, plot_width=1200, x_axis_type="datetime", tools="", toolbar_location=None, title="Covid-19 August Newly Confirmed Cases")
plot.line(x, y)
date = dt(2020, 8, 1)

date_picker = DatePicker(title='Select date', value="2020-08-01", min_date="2020-08-01", max_date="2020-08-31")
date_picker.js_on_change('value', CustomJS(args=dict(s1=s1, s2=s2, s3=s3, s4=s4), code="""
    var d1 = s1.data;
    var d2 = s2.data;
    var f = cb_obj.value;
    d2['x'] = [];
    d2['y'] = [];
    d2['names'] = [];
    d2['confirmed_cases'] = [];
    d2['deaths'] = [];
    for (var i = 0; i < d1['x'].length; i ++){
        if (d1['z'][i] == f){
            d2['x'].push(d1['x'][i]);
            d2['y'].push(d1['y'][i]);
            d2['names'].push(d1['y'][i] + ' new cases on ' + f);
            d2['confirmed_cases'].push(d1['p'][i] + ' confirmed cases');
            d2['deaths'].push(d1['q'][i] + ' deaths');
            break;
        }
    }
    s2.change.emit()

    var d3 = s3.data;
    var d4 = s4.data;
    d3['cases'] = Array(d3['x'].length).fill(0);
    d3['deaths'] = Array(d3['x'].length).fill(0);
    d3['cases_text'] = Array(d3['x'].length).fill('0%');
    d3['deaths_text'] = Array(d3['x'].length).fill('0%');
    d3['num_cases'] = Array(d3['x'].length).fill(0);
    d3['num_deaths'] = Array(d3['x'].length).fill(0);
    for (var i = 0; i < d4['x'].length; i ++){
        if (d4['date'][i] == f){
            for (var j = 0; j < d3['x'].length; j ++){
                if (d4['x'][i] == d3['x'][j]){
                    d3['cases'][j] = Number((d4['cases'][i]).toFixed(4));
                    d3['deaths'][j] = Number((d4['deaths'][i]).toFixed(4));
                    d3['cases_text'][j] = Number((d4['cases'][i]*100).toFixed(4)) + '%';
                    d3['deaths_text'][j] = Number((d4['deaths'][i]*100).toFixed(4)) + '%';
                    d3['num_cases'][j] = d4['num_cases'][i];
                    d3['num_deaths'][j] = d4['num_deaths'][i];
                }
            }
            
        }
    }
    s3.change.emit()
"""
))

cr = plot.circle('x', 'y', source=s2, color='red')
labelx = LabelSet(x='x', y='y', text='names', source=s2, \
    render_mode='canvas', x_offset=15, y_offset=-10, level='glyph', \
    text_font_size='18px')
labely = LabelSet(x='x', y='y', text='confirmed_cases', source=s2, \
    render_mode='canvas', x_offset=15, y_offset=-30, level='glyph', \
    text_font_size='18px')
labelz = LabelSet(x='x', y='y', text='deaths', source=s2, \
    render_mode='canvas', x_offset=15, y_offset=-50, level='glyph', \
    text_font_size='18px')
plot.add_layout(labelx)
plot.add_layout(labely)
plot.add_layout(labelz)

div11 = Div(text="""
    Source of data: <a href="https://github.com/datadesk/california-coronavirus-data/blob/master/latimes-state-totals.csvv">latimes-state-totals.csv</a>, 
    from <a href="https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/">Los Angeles Times</a>
""")
div12 = Div(text="""
    Last update: {}
""".format(confirm['date'].max()))

plot2 = figure(plot_height=600, plot_width=1200, x_range=races, \
    tools="", toolbar_location=None, title="Covid-19 Cases by Races", \
    x_axis_label="Races", y_axis_label="Percentage", y_range=ranges.Range1d(start=0, end=1))
plot2.vbar(x='x', top='cases', width=0.8, source=s3, legend_field='x',\
    fill_color=factor_cmap('x', palette=Spectral6, factors=races))

plot2.text(x='x', y='cases', text='num_cases', source=s3, x_offset=-15)
plot2.text(x='x', y='cases', text='cases_text', source=s3, x_offset=-15, y_offset=-15)

div21 = Div(text="""
    Source of data: <a href="https://github.com/datadesk/california-coronavirus-data/blob/master/cdph-race-ethnicity.csv">cdph-race-ethnicity.csv</a>, 
    from <a href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx">California Department of Public Health</a>
""")
div22 = Div(text="""
    Last update: {}
""".format(race_ds['date'].max()))

plot3 = figure(plot_height=600, plot_width=1200, x_range=races, \
    tools="", toolbar_location=None, title="Covid-19 Deaths by Races", \
    x_axis_label="Races", y_axis_label="Percentage", y_range=ranges.Range1d(start=0, end=1))
plot3.vbar(x='x', top='deaths', width=0.8, source=s3, legend_field='x',\
    fill_color=factor_cmap('x', palette=Spectral6, factors=races))

plot3.text(x='x', y='deaths', text='num_deaths', source=s3, x_offset=-15)
plot3.text(x='x', y='deaths', text='deaths_text', source=s3, x_offset=-15, y_offset=-15)

div31 = Div(text="""
    Source of data: <a href="https://github.com/datadesk/california-coronavirus-data/blob/master/cdph-race-ethnicity.csv">cdph-race-ethnicity.csv</a>, 
    from <a href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx">California Department of Public Health</a>
""")
div32 = Div(text="""
    Last update: {}
""".format(race_ds['date'].max()))


curdoc().add_root(column(date_picker, plot, div11, div12, plot2, div21, div22, plot3, div31, div32))




