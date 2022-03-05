import dash
from dash import Dash, html, dcc, State, Input, Output
from components.map_plot import create_map_plot
from components.scatter_plot import create_scatter_plot
# from .. import line_plot as lp
# from .. import dropdown_plot as dp
# import json

import dash_bootstrap_components as dbc
import pandas as pd

# Read in data
tsunami_df = pd.read_csv('data/processed/tsunami-events.csv')

years = tsunami_df['year'].dropna().unique() # need to add start and end year
countries = tsunami_df['country'].dropna().unique()
country_list = ['All'] + sorted(list(countries)) # countries are listed alphabetically

app = dash.Dash(
    __name__, title = "Tsunami History", external_stylesheets=[dbc.themes.QUARTZ]
)
server = app.server

# Creating style for both sidebar and plots
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": '10rem',
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "z-index": 4000000,
}

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "z-index": -1,
}
# Structure of app, including selection criteria components
app.layout = dbc.Container([
    html.H1('Tsunami History Dashboard', 
        style = {
            'padding': 10,
            'margin-top': 20,
            'margin-bottom': 30,
            'text-align': 'center',
            'font-size': '48px'
        }),
    dbc.Row([
        dbc.Col([
            html.H3('Years and Countries Selection', className = 'text-dark'),
            html.Hr(),
            html.H5('Years of Interest (1800 - 2022)', className = 'text-dark'),
            dcc.RangeSlider(
                min = 1800, 
                max = 2022,
                value = [tsunami_df['year'].min(), tsunami_df['year'].max()],
                marks = None, 
                id='year_slider',
                allowCross = False, # Prevent handles from crossing each other
                tooltip = {'placement': 'bottom',
                            'always_visible': True}),
            html.Br(),
            html.Br(),
            html.H5('Countries of Interest', className = 'text-dark'),
            dcc.Dropdown(
                id='country_select',
                multi = True,
                value = [],
                options = [{'label': country, 'value': country} for country in country_list],
                className = 'text-dark'),
            html.Hr(),
            html.P(
                "A data visualisation app that allows viewers to observe the number and intensity of tsunamis based on years and countries",
                className = 'form-label'
            )
        ],
        style = SIDEBAR_STYLE,
        className = 'btn btn-light'),
        dbc.Col([
            dbc.Row([
                html.H2('World Map', className = 'btn btn-warning btn-lg'),
                html.Iframe(
                        id='map_plot',
                        style={'border-width': '0', 'width': '100%', 'height': '400px'},
                        srcDoc=create_map_plot(year_start=1800, year_end=2022, countries=[]))
            ]),
            dbc.Row([
                dbc.Col([
                    html.H2('Line Plot', className = 'btn btn-warning btn-lg'),
                    html.Iframe(
                        id = 'line_plot',
                        style={'border-width': '0', 'width': '100%', 'height': '400px'},
                        srcDoc = create_scatter_plot(ymin=1800, ymax=2022, value_ctry=[]))
                ]),
                dbc.Col([
                    html.H2('DropDown Plot', className = 'btn btn-warning btn-lg'),
                    html.Iframe(
                        id = 'drop_down_plot',
                        style={'border-width': '0', 'width': '100%', 'height': '400px'})
                ])
            ])
        ],
        style = CONTENT_STYLE)
    ])
], fluid = True,
    style = {
        'backgroundColor': 'black',
})

# App callback for map_plot
@app.callback(
    Output('map_plot', 'srcDoc'),
    Input('year_slider', 'value'),
    Input('country_select', 'value')
)
def update_map_plot(value, value_country):
    return create_map_plot(value[0], value[1], value_country)

# App callback for scatter_plot
@app.callback(
    Output('scatter_plot', 'srcDoc'),
    Input('year_slider', 'value'),
    Input('country_select', 'value')
)
def update_scatter_plot(value, value_country):
    return create_scatter_plot(value[0], value[1], value_country)

# # App callback for bar_plot
# @app.callback(
#     Output('bar_plot', 'srcDoc'),
#     Input('year_slider', 'value')
# )
# def update_bar_plot(value, value_country):
#     return create_bar_plot(value)


if __name__ == '__main__': 
    app.run_server(debug=True)