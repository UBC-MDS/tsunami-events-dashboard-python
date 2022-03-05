import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd

PROCESSED_DATA_PATH = "data/processed/tsunami-events.csv"

def preprocess(year_start, year_end):
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['tsunami_instance'] = range(1, len(df) + 1)
    df['tsunami_instance'] = df.index
    df['combine'] = df['country'].astype(str) + ', ' + df['year'].astype(str)
    df = df.query('tsunami_intensity > 0')
    df = df.query(f"{year_start} <= year <= {year_end}")
    df = df.sort_values(by=['tsunami_intensity'], ascending = False)
    df = df[0:10]
    return df

def create_bar_plot(year_start, year_end):
    df = preprocess(year_start, year_end)
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('tsunami_intensity:Q', title = 'Tsunami Intensity', scale=alt.Scale(domain=(0, 12))),
        y=alt.Y('tsunami_instance:N', sort = '-x', title = 'Country', axis = alt.Axis(labelExpr="datum.country")),
        color=alt.Color('country:O'),
        tooltip=("country:O", "location_name:O", "tsunami_intensity:Q", "earthquake_magnitude:Q", "year:Q", "month:O")
        ).properties(width=240, height=160)
    
    text = chart.mark_text(align="left", baseline="middle", dx = 3).encode(
        text= 'combine:O')
    
    plot = chart + text
    return plot.to_html()
