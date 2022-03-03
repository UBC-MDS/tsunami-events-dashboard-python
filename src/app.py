from tkinter import font
import dash
from dash import Dash, html, dcc, State, Input, Output
# from .. import world_map_plot as wmp
# from .. import line_plot as lp
# from .. import dropdown_plot as dp
# import json

# from dash import Dash, dcc, html, Input, Output
# import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd

# Read in data
tsunami_df = pd.read_csv('data/processed/tsunami-events.csv')

years = tsunami_df['year'].dropna().unique() # need to add start and end year

countries = tsunami_df['country'].dropna().unique()
country_list = sorted(list(countries)) # countries are listed alphabetically

# Setup app and layout/frontend
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up theme of dashboard
colour = {
    'background': '#000000',
    'border' : '#58c3c0',
    'text': '#FFFBF1'
}

app.layout = dbc.Container([
    # Title of dashboard (if there is time, we can add 'Fade'/'Collapse' as a description of how to use our dashboard)
    html.H1(['Tsunami History Dashboard',
        dbc.Button(
            'More',
            id = 'collapse-button',
            n_clicks=0,
            size = 'sm',
            color = 'secondary',
            className="d-grid gap-2 d-md-flex justify-content-md-end",
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody('Info about our app'),
            style = {
                'color': colour['text'],
                'backgroundColor': '#6d6d6d',
                'font-size': '14px',
                'text-align': 'left'
            }),
            id = 'collapse',
            is_open = False,
        ),
    ], 
        style = {
            'backgroundColor': colour['border'],
            'padding': 10,
            'color': colour['text'],
            'margin-top': 20,
            'margin-bottom': 30,
            'text-align': 'center',
            'font-size': '48px',
            'border-radius': 3,
            'font-family': 'Georgia, serif'}),

    # The first column - the search criteria
    dbc.Row([
        # First column: Navigation
        dbc.Col([
            # html.Iframe(
            #             id = 'scatter4',
            #             style={'border-width': '0', 'width': '100%', 'height': '50px'}),
            html.H5('Years of Interest (1800 - 2022)',
                    style = {
                        'color': colour['text'],
                        'margin-top': 20,
                        'margin-bottom': 30,
                        'text-align': 'center',
                        'font-size': '15px',
                        'border-radius': 3,
                        'font-family': 'Georgia, serif',
                        'font-weight': 'bold'}),
            html.Br(),
            dcc.RangeSlider(
                min = 1800, 
                max = 2022,
                value = [tsunami_df['year'].min(), tsunami_df['year'].max()],
                marks = None, 
                # marks = {1800: '1800', 1850:'1850', 1900: '1900', 1950: '1950', 2000: '2000', 2022: '2022'},
                id = 'year-slider',
                allowCross = False, # Prevent handles from crossing each other
                tooltip = {'placement': 'bottom',
                            'always_visible': True}),
            html.Br(),
            html.Br(),
            html.Br(),
            # html.Iframe(
            #             id = 'scatter5',
            #             style={'border-width': '0', 'width': '100%', 'height': '100px'}),
            html.H5('Countries of Interest',
                     style = {
                        'color': colour['text'],
                        'margin-top': 20,
                        'margin-bottom': 30,
                        'text-align': 'center',
                        'font-size': '15px',
                        'border-radius': 3,
                        'font-family': 'Georgia, serif',
                        'font-weight': 'bold'}),
            html.Br(),
            dcc.Dropdown(
                id = 'country_select',
                multi = True,
                value = ['INDONESIA','JAPAN'],
                options = [{'label': country, 'value': country} for country in country_list])
            # NEED A SELECT ALL OPTION
            # dcc.Checklist(
            #     id = 'select-all',
            #     options = [{'label': 'Select All', 'value': country_list}],
            #     values = [])
        ],
        width = 3,
        style = {
            'border': '5px solid',
            'backgroundColor': colour['border'],
            'padding': 10,
            'margin-top': 20,
            'margin-bottom': 30,
            'border-radius': 4,
            'font-family': 'Georgia, serif'}
        ),
        # Second Column: Plots
        dbc.Col([
            dbc.Row([
                html.H2('World Map',
                        style = {
                            'backgroundColor': colour['border'],
                            'padding': 10,
                            'color': colour['text'],
                            'margin-top': 20,
                            'margin-bottom': 30,
                            'text-align': 'center',
                            'font-size': '30px',
                            'border-radius': 1,
                            'font-family': 'Georgia, serif'}),
                html.Iframe(
                        id = 'scatter',
                        style={'border-width': '0', 'width': '100%', 'height': '400px'})
            ]),
            dbc.Row([
                dbc.Col([
                    html.H2('Line Plot',
                            style = {
                                    'backgroundColor': colour['border'],
                                        'padding': 10,
                                        'color': colour['text'],
                                        'margin-top': 20,
                                        'margin-bottom': 30,
                                        'text-align': 'center',
                                        'font-size': '30px',
                                        'border-radius': 1,
                                        'font-family': 'Georgia, serif'}),
                    html.Iframe(
                        id = 'scatter2',
                        style={'border-width': '0', 'width': '100%', 'height': '200px'}),
                ]),
                dbc.Col([
                    html.H2('Dropdown Plot',
                            style = {
                            'backgroundColor': colour['border'],
                                'padding': 10,
                                'color': colour['text'],
                                'margin-top': 20,
                                'margin-bottom': 30,
                                'text-align': 'center',
                                'font-size': '30px',
                                'border-radius': 1,
                                'font-family': 'Georgia, serif'}),
                    html.Iframe(
                        id = 'scatter3',
                        style={'border-width': '0', 'width': '100%', 'height': '200px'})
                ])
            ])
        ])
    ])
    ], style = {
        'backgroundColor': colour['background']
    }
    )

@app.callback(
    Output('collapse', 'is_open'),
    [Input('collapse-button', 'n_clicks')],
    [State('collapse', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__': 
    app.run_server(debug=True)

# @app.callback(
#     Output('', ''),
#     Input('year-slider', 'start-year'),
#     Input('year-slider', 'end-year')
# )

# # Output for year-slider
# def update_output(start-year, end-year):
#     return 'You have selected {start-year} and {end-year}'