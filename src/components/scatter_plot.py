import altair as alt
from dash import Dash, dcc, html, Input, Output
import pandas as pd

PROCESSED_DATA_PATH = "data/processed/tsunami-events.csv"


def get_data(ymin=1500, ymax=2020, value_ctry=None):
    input = PROCESSED_DATA_PATH
    df = pd.read_csv(input,
                     parse_dates=True)[["year", "country", "total_deaths", "earthquake_magnitude"]]
    df = df[df['total_deaths'].notna()]
    df['mercalli_intensity'] = pd.cut(df['earthquake_magnitude'],
                                      bins=[1, 2, 4, 5, 6, 7, 10],
                                      labels=["I", "II-III", "IV–V", "VI–VII", "VII–IX", "VIII or higher"]).astype(str)
    if value_ctry == None:
        return df.loc[(df['year'] > ymin) & (df['year'] < ymax)]
    else:
        return df.loc[(df['year'] > ymin) &
                      (df['year'] < ymax) &
                      (df['country'].isin(value_ctry))
                      ]


def create_scatter_plot(ymin, ymax, value_ctry):
    chart = alt.Chart(get_data(ymin, ymax, value_ctry)).mark_point(opacity=0.5).encode(
        x=alt.X('earthquake_magnitude',
                title='Earthquake Magnitude (Richter Scale)',
                scale=alt.Scale(domain=(5.5, 10))),
        y=alt.Y('total_deaths',
                title='Total Deaths (log-transformed), per Event',
                scale=alt.Scale(type='log', base=10)),
        color='country',
        tooltip=['year', 'mercalli_intensity', 'country', 'total_deaths']
    ).interactive(
    ).properties(
        title='Scatter Plot of Earthquake Magnitude vs Total Deaths, per Deadly Tsunami Event, by Country'
    ).configure_title(
        fontSize=10,
        font='Courier',
        anchor='start',
        color='black'
    )
    return chart.to_html()
