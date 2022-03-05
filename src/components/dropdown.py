import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd

PROCESSED_DATA_PATH = "data/processed/tsunami-events.csv"

def preprocess(year_start, year_end):
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['tsunami_instance'] = range(1, len(df) + 1)
    df['tsunami_instance'] = df.index
    df_daterange = df.query(f"{year_start} <= year <= {year_end}")
    df_daterange = df_daterange.sort_values(by=['tsunami_intensity'], ascending = False)
    df_daterange = df_daterange[0:15]
    return df_daterange

def create_bar_plot(year_start, year_end):
    tsunami_dataframe = preprocess(year_start, year_end)
    chart = alt.Chart(tsunami_dataframe).mark_bar().encode(
        x=alt.X('tsunami_intensity:Q', title = 'Tsunami Intensity', scale=alt.Scale(domain=(0, 12))),
        y=alt.Y('tsunami_instance:N', sort = '-x', title = 'Country', axis = alt.Axis(labelExpr="datum.country")),
        tooltip=("country:O", "location_name:O", "tsunami_intensity:Q", "earthquake_magnitude:Q", "year:Q", "month:O"))
    
    text = chart.mark_text(align="left", baseline="middle", dx = 3).encode(
        text= "country:O")
    
    plot = chart + text
    return plot.to_html()
