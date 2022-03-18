import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, State, Input, Output
from .components.map_plot import create_map_plot
from .components.scatter_plot import create_scatter_plot
from .components.bar_plot import create_bar_plot

tsunami_events = pd.read_csv('data/processed/tsunami-events.csv')

countries = tsunami_events['country'].dropna().unique()
country_list = sorted(list(countries))
year_min = tsunami_events['year'].min()
year_max = tsunami_events['year'].max()
magnitude_min = tsunami_events['earthquake_magnitude'].min()
magnitude_max = tsunami_events['earthquake_magnitude'].max()

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.QUARTZ]
)
app.title = 'Tsunami Events'
server=app.server

SIDEBAR_STYLE={
    "position": "fixed",
    "top": '62px',
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "z-index": 4000000,
    'background-color': 'rgba(255,255,255,.25)'

}

CONTENT_STYLE={
    "margin-left": "20rem",
    "z-index": -1,
}

navbar=dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Tsunami Events Dashboard")),
                    ],
                    align="center",
                    className="g-0",
                ),
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        style={
            'margin-left': '1.2rem',
            'font-weight': "600"
        }
    ),
    color="dark",
    dark=True,
)

world_plot_card=dbc.Card(
    dbc.CardBody(
        [html.H6('Total Tsunami Hits by Country with Origin Points', className='card-title',
        style={'margin-bottom': '0px'}),
        html.Iframe(
            id='map_plot',
            style={'border-width': '0', 'height': '100%', 'width': '100%','padding-right': '0'},
            srcDoc=create_map_plot(year_start=year_min,
                                   year_end=year_max,
                                   countries=[],
                                   magnitude_start=magnitude_min,
                                   magnitude_end=magnitude_max))
        ], style={'padding': '15px', 'padding-bottom': '0px'}
    ),
    style={'padding': 0}
)

scatter_plot_card=dbc.Card(
    dbc.CardBody(
        [html.H6('Total Deaths and Earthquake Magnitude per Event', className='card-title',
        style={'margin-bottom': '0px'}),
        html.Iframe(
            id='scatter_plot',
            style={'border-width': '0', 'height': '360px','width': '100%'},
            srcDoc=create_scatter_plot(year_start=year_min,
                                       year_end=year_max,
                                       countries=[],
                                       magnitude_start=magnitude_min,
                                       magnitude_end=magnitude_max) 
        )], style={'padding': '15px', 'padding-bottom': '0px'}
    ),
    style={'padding': 0}
)

bar_chart_card=dbc.Card(
    dbc.CardBody(
        [html.H6('Top 10 Most Intense Tsunamis', className='card-title',
        style={'margin-bottom': '0px'}),
        html.Iframe(
            id='bar_plot',
            style={'border-width': '0', 'height': '360px','width': '100%'},
            srcDoc=create_bar_plot(year_start=year_min,
                                   year_end=year_max,
                                   magnitude_start=magnitude_min,
                                   magnitude_end=magnitude_max)
        )], style={'padding': '15px', 'padding-bottom': '0px'}
    ),
    style={'padding': 0}
)

app.layout=dbc.Container([
    navbar,
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H5('Years and Countries Selection', className='form-label'),
            html.Hr(),
            html.H6(f'Years of Interest ({year_min} - {year_max})', className='form-label'),
            dcc.RangeSlider(
                min=year_min, 
                max=year_max,
                value=[year_min, year_max],
                marks=None, 
                id='year_slider',
                allowCross=False, 
                tooltip={'placement': 'bottom',
                            'always_visible': True}),
            html.Br(),
            html.Br(),
            html.H6('Earthquake Magnitude of Interest', className='form-label'),
            dcc.RangeSlider(
                min=magnitude_min,
                max=magnitude_max,
                value=[magnitude_min, magnitude_max],
                marks=None,
                id='magnitude_slider',
                allowCross=False, 
                tooltip={'placement': 'bottom',
                            'always_visible': True}),
            html.Br(),
            html.Br(),
            html.H6('Countries of Interest', className='form-label'),
            dcc.Dropdown(
                id='country_select',
                multi=True,
                value=[],
                options=[{'label': country, 'value': country} for country in country_list],
                className='text-dark'),
            html.Hr(),
            html.P(
                "A data visualisation app that allows viewers to observe the number "
                "and intensity of tsunamis based on years and countries",
                className='form-label'
            )
        ],
        style=SIDEBAR_STYLE,
        className="btn btn-secondary"
        ),
        dbc.Col([
            dbc.Row([
                world_plot_card
            ], style={'margin': 'auto', 'width': '75vw', 'height': '600px', 'padding':'20px',
            'padding-bottom' : '10px'}),
            dbc.Row([
                dbc.Col([
                    scatter_plot_card
                ], style={'height': '600px'}),
                dbc.Col([
                    bar_chart_card
                ], style={'height': '600px'})
            ],style={'margin': 'auto', 'width': '75vw', 'height': '600px', 'padding':'10px'})
        ],
        style=CONTENT_STYLE)
    ])
], fluid=True,
    style={
        'backgroundColor': 'black',
        'padding': '0px',
        'height': '150vh'
})

# App callback for map_plot
@app.callback(
    Output('map_plot', 'srcDoc'),
    Input('year_slider', 'value'),
    Input('magnitude_slider', 'value'),
    Input('country_select', 'value'),
)
def update_map_plot(years, magnitudes, countries):
    return create_map_plot(year_start=years[0],
                           year_end=years[1],
                           magnitude_start=magnitudes[0],
                           magnitude_end=magnitudes[1],
                           countries=countries)

# App callback for scatter_plot
@app.callback(
    Output('scatter_plot', 'srcDoc'),
    Input('year_slider', 'va4lue'),
    Input('magnitude_slider', 'value'),
    Input('country_select', 'value')
)
def update_scatter_plot(value, value_magnitude, value_country):
    return create_scatter_plot(value[0], value[1], value_magnitude[0], value_magnitude[1], value_country)

# App callback for bar_plot
@app.callback(
    Output('bar_plot', 'srcDoc'),
    Input('year_slider', 'value'),
    Input('magnitude_slider', 'value')
)
def update_bar_plot(value, earthquake):
    return create_bar_plot(value[0], value[1], earthquake[0], earthquake[1])

# App callback for navbar
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
    app.run_server(debug=True)
