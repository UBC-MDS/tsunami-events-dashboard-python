from dash import Dash, html
# from .. import world_map_plot as wmp
# from .. import line_plot as lp
# from .. import dropdown_plot as dp
import json

from dash import Dash, dcc, html, Input, Output
import altair as alt
import dash_bootstrap_components as dbc

# Read in data
tsunami_df = pd.read_csv('data/processed/tsunami.csv')

years = tsunami_df['year'].dropna().unique() # need to add start and end year

countries = tsunami_df['country'].dropna().unique()
country_list = list(countries)

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    # Title of dashboard (if there is time, we can add 'Fade'/'Collapse' as a description of how to use our dashboard)
    html.H1('Tsunami History Dashboard',
                style = {
                    'backgroundColor': '#c50017',
                        'padding': 10,
                        'color': 'white',
                        'margin-top': 20,
                        'margin-bottom': 30,
                        'text-align': 'center',
                        'font-size': '48px',
                        'border-radius': 3,
                        'font-family': 'cursive'}),
    

    # The first column - the search criteria
    dbc.Col([
        dbc.Row([
            html.Div('Years of Interest (1800 - 2022'),
            html.Br(),
            dcc.RangeSlider(
                min = 1800, 
                max = 2022,
                value = [tsunami_df['year'].min(), tsunami_df['year'].max()],
                marks = {1800: '1800', 1850:'1850', 1900: '1900', 1950: '1950', 2000: '2000', 2022: '2022'}
                id = 'year-slider',
                allowCross = False, # Prevent handles from crossing each other
                tooltip = {'placement': 'bottom',
                            'always_visible': True}),
            html.Br(),
            html.Br(),
            html.Br(),
            # List of countries (how to set an option for all countries)
            html.Div('Countries of Interest'),
            dccDropdown(
                id = 'country_select',
                multi = TRUE,
                value = country_list
                options = [{'label': country, 'value': country} for country in country_list],
                #style = {'border': ...}
            ),
        ])
    ]),

    # The Second Column - all the plots
    dbc.Col([
        dbc.Row([
            html.Div('World Map')
        ]),
        dbc.Row([
            dbc.Col([
                html.Div('Line Plot')
            ]),
            dbc.Col([
                html.Div('Dropdown Plot')
            ])
        ])
    ]),
    html.Hr(),
    html.P([f'''
        This dashbaord was made by Gautham, Jacqueline, Rowan and Vadim])'''])
    

@app.callback(
    Output('', ''),
    Input('year-slider', 'start-year'),
    Input('year-slider', 'end-year')
)

# Output for year-slider
def update_output(start-year, end-year):
    return 'You have selected {start-year} and {end-year}'