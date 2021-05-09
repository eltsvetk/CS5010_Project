#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
## Uncomment this section to run the code locally, in Spyder ##
## Review Renders at:  https://plotly.com/python/renderers/
##
import plotly.io as pio
pio.renderers
pio.renderers.default="browser" ## launch the browser by default on fig.show()
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np

## Read our data set from github
df = pd.read_csv("https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/merged.csv",dtype={"Unnamed: 0": str})
df.rename(columns = {"Unnamed: 0": "fips"}, inplace=True)

## Set up a dataframe with column descriptions
## This is used to display subtitles on the map
subtitles = pd.read_csv("https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/YCOM_2020_Metadata.csv", index_col=0)

## Add Population Density Description to the original metadata
## This was added to the Yale Data.
subtitles.loc['ScaledPopDensity'] = ["Number of people per square mile"]
subtitles.loc['Political_Affiliation'] = ["Mostly likely to lean toward Political Party"]

## Import the GeoJson counties file which forms the boundaries
## for counties in the US
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

## When this list is shorter our map renders faster
options_list = ['happening','worried','priority','Political_Affiliation','ScaledPopDensity']  ## We can have about 6 for 1 minute load time

## These are data column names we are displaying in the map
## as a drop down.
# options_list = ['happening','reducetax','CO2limits','localofficials','governor', 
#                 'congress','president','corporations','citizens','regulate',
#                 'supportRPS','drilloffshore','drillANWR','fundrenewables',
#                 'rebates','mediaweekly','gwvoteimp','teachGW','priority',
#                 'discuss','human','consensus','worried','personal','harmUS',
#                 'devharm','futuregen','harmplants','timing', 'affectweather',
#                 'PopDensity']

## Clean up the label names for the drop down
list_labels = {}
for k in options_list:
    
    if k == 'Political_Affiliation': 
        list_labels['Political_Affiliation'] = 'Political Affiliation'
        
    elif k == 'priority': 
        list_labels['priority'] = 'Voting Priority'
        
    elif k == 'ScaledPopDensity':
        list_labels['ScaledPopDensity'] = 'Population Density'
 
    elif k == 'worried': 
        list_labels['worried'] = 'People are Worried'

    elif k == 'happening': 
        list_labels['happening'] = 'This is Happening'
        
    else:
        list_labels[k] = k

## Make Political Affiliation a numeric scale for the color map
if 'Political_Affiliation' in options_list:
    party = {'Repub': 10, 'Demo': 0, 'Swing': 5}
    df['Political_Affiliation'].replace(party, inplace=True)

## We need zero instead of NaN for vote values
df['republican_votes'] = df['republican_votes'].fillna(0)
df['democrat_votes'] = df['democrat_votes'].fillna(0)

## Save some memory by eliminating what we don't need
dropme = []
for bigdrop in df.columns:  
    if bigdrop not in options_list and bigdrop not in ['fips', 'GeoName','PopDensity (pop/sq mi)','democrat_votes','republican_votes']: dropme.append(bigdrop)

df.drop(dropme, axis=1, inplace=True)

## to track the visibility of the chosen list option
visible = np.array(options_list)

# Use "traces" to create a map for each column item in the options_list
# Use "buttons" to handle the action for each list item
traces = []
buttons = []

# Use "varchoice" to store the chosen list item name
for varchoice in options_list:
    
    if varchoice == 'Political_Affiliation':      
        colorscale = "bluered"
        scalemin = 0
        scalemax = 10
    else:
        colorscale = "viridis"
        scalemin = 40
        scalemax = 80
    
    ## Add a new trace for each item in the options list
    traces.append(go.Choroplethmapbox(
        geojson=counties, 
        locations=df.fips, # Spatial coordinates
        z=df[varchoice],   # Data to be color-coded
        colorscale=colorscale, zmin=scalemin, zmax=scalemax,
        marker_opacity=0.5, marker_line_width=0, 
        colorbar_title=varchoice.title(),
        name=varchoice.title(), ## Hover Title
        customdata = df[['GeoName','PopDensity (pop/sq mi)','democrat_votes','republican_votes']],
        hovertemplate='%{customdata[0]}<br><br>' +
        'Population Density: %{customdata[1]:,.2f} /sq. mile<br>' +
        '2016 Democrat Votes: %{customdata[2]:,}<br>' +
        '2016 Republican Votes: %{customdata[3]:,}<br>' +                                    
        '<extra>%{fullData.name}: %{z:.1f}%</extra>',        
        visible = True if varchoice==options_list[0] else False))

    ## Add a button for each trace
    buttons.append(dict(label  = list_labels[varchoice], ## List Item Title
                        method = "update",
                        args   =[ { "visible" : list(visible == varchoice)},
                                  { "title"   : f"<b>{varchoice.title()}</b><br><sub>{subtitles.loc[varchoice][0]}</sub>"     } ]))
## Track which list item is active
## And the action to take (buttons) when active
updatemenus = [ { "active" : 0, "buttons" : buttons, } ]

## The Figure Object brings together the "data" in the form of maps
## And the list items, in the form of buttons, which are stored in updatemenus
fig = go.Figure(data   = traces,
                layout = dict(updatemenus = updatemenus))

## Finish defining the mapbox layout wiht mapbox attributes
fig.update_layout(mapbox_style = "carto-positron",
                  mapbox_zoom = 3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})

# Set need an initial value for title and subtitle
first_title = options_list[0]
fig.update_layout(title = f"<b>{first_title.title()}</b><br><sub>{subtitles.loc[first_title][0]}</sub>", title_x = 0.5)

fig.update_layout(autosize=False,width=1400,height=700,margin=dict(l=50,r=50,b=100,t=100,pad=4), paper_bgcolor="Linen",)
## Show our map!
## fig.show() ## use dash to render instead of show

## Now, introduce dash
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Climate Change Attitudes with Population Density'),

    html.Div(children='''
        Group 4: Elena, Jonathan, & Anita.
    '''),

    dcc.Graph(
        id='mapbox-usa-counties',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

