import dash
from dash import Dash, html, dcc, State, Input, Output
from components.map_plot import create_map_plot
from components.scatter_plot import create_scatter_plot
from components.dropdown import create_bar_plot

import dash_bootstrap_components as dbc
import pandas as pd

# Read in data
tsunami_df = pd.read_csv('data/processed/tsunami-events.csv')

years = tsunami_df['year'].dropna().unique() # need to add start and end year
countries = tsunami_df['country'].dropna().unique()
country_list = sorted(list(countries)) # countries are listed alphabetically

app = dash.Dash(
    __name__, title = "Tsunami History", external_stylesheets=[dbc.themes.QUARTZ]
)

server = app.server

# Creating style for both sidebar and plots
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": '62px',
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "z-index": 4000000,
    'background-color': 'rgba(255,255,255,.25)'

}

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "z-index": -1,
}
# Structure of app, including selection criteria components

# Formatting NavBar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Tsunami Events Dashboard", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                # href="https://plotly.com",
                # style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                # search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        style = {
        'margin-left': '15px',
        'font-weight': "600"}
    ),
    color="dark",
    dark=True,
)

world_plot_card = dbc.Card(
    dbc.CardBody(
        [html.H6('Total Tsunami Hits by Country with Origin Points', className = 'card-title',
        style = {'margin-bottom': '0px'}),
        html.Iframe(
            id='map_plot',
            style={'border-width': '0', 'height': '380px', 'width': '100%'},
            srcDoc=create_map_plot(year_start=1800, year_end=2022, countries=[]))
        ], style = {'padding': '15px', 'padding-bottom': '0px'}
    ),
    style = {'padding': 0}
)

scatter_plot_card = dbc.Card(
    dbc.CardBody(
        [html.H6('Total Deaths by Earthquake Magnitude', className = 'card-title',
        style = {'margin-bottom': '0px'}),
        html.Iframe(
            id = 'scatter_plot',
            style={'border-width': '0', 'height': '220px','width': '100%'},
            srcDoc=create_scatter_plot(year_start=1800, year_end=2022, countries=[]) 
        )], style = {'padding': '15px', 'padding-bottom': '0px'}
    ),
    style = {'padding':0}
)

bar_chart_card = dbc.Card(
    dbc.CardBody(
        [html.H6('Top 10 most intense tsunami in given years', className = 'card-title',
        style = {'margin-bottom': '0px'}),
        html.Iframe(
            id = 'bar_plot',
            style={'border-width': '0', 'height': '220px','width': '100%'},
            srcDoc=create_bar_plot(year_start=1800, year_end=2022)
        )], style = {'padding': '15px', 'padding-bottom': '0px'}
    ),
    style = {'padding':0}
)

app.layout = dbc.Container([
    navbar,
    dbc.Row([
        dbc.Col([
            html.H5('Years and Countries Selection', className = 'form-label'),
            html.Hr(),
            html.H6('Years of Interest (1800 - 2022)', className = 'form-label'),
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
            html.H6('Countries of Interest', className = 'form-label'),
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
        className = "btn btn-secondary"
        ),
        dbc.Col([
            dbc.Row([
                world_plot_card
            ], style = {'margin': 'auto', 'width': '800px', 'padding':'0px'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    scatter_plot_card
                ], style = {'margin': 'auto', 'width': '400px'}),
                dbc.Col([
                    bar_chart_card
                ], style = {'margin': 'auto', 'width': '400px'})
            ],style = {'margin': 'auto', 'width': '1020px'})
        ],
        style = CONTENT_STYLE)
    ])
], fluid = True,
    style = {
        'backgroundColor': 'black',
        'padding': '0px',
        'height': '100vh'
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

# App callback for bar_plot
@app.callback(
    Output('bar_plot', 'srcDoc'),
    Input('year_slider', 'value')
)
def update_bar_plot(value):
    return create_bar_plot(value[0], value[1])

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__': 
    app.run_server()
