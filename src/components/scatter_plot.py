import altair as alt
from dash import Dash, dcc, html, Input, Output
import pandas as pd

PROCESSED_DATA_PATH = "data/processed/tsunami-events.csv"

def create_scatter_plot(year_start, year_end, countries):
    chart = alt.Chart(get_data(year_start, year_end, countries)).mark_circle(opacity=0.9, size=10).encode(
        x=alt.X('earthquake_magnitude',
                title='Earthquake Magnitude (Richter Scale)',
                scale=alt.Scale(domain=(5.5, 10))),
        y=alt.Y('total_deaths',
                title='Total Deaths (log-transformed), per Event',
                scale=alt.Scale(type='log', base=10)),
        color='country',
        tooltip=['year', 'mercalli_intensity', 'country', 'total_deaths']
    ).interactive(
    )
    return chart.to_html()

def get_data(year_start, year_end, countries):
    
    tsunami_events = pd.read_csv(PROCESSED_DATA_PATH)
    
    if not (year_start and year_end and year_start <= year_end):
        raise ValueError("Invalid value for year start and/or year end")
    
    if not countries and countries != []:
         raise ValueError("Invalid value for countries")

    tsunami_events = tsunami_events.query(
        f"{year_start} <= year <= {year_end}"
    )
    if countries != []:
        tsunami_events = (
            tsunami_events[tsunami_events["country"].isin(countries)]
        )
    
    tsunami_events = tsunami_events[tsunami_events['total_deaths'].notna()]
    tsunami_events['mercalli_intensity'] = pd.cut(tsunami_events['earthquake_magnitude'],
                                      bins=[1, 2, 4, 5, 6, 7, 10],
                                      labels=["I", "II-III", "IV–V", "VI–VII", "VII–IX", "VIII or higher"]).astype(str)
    return tsunami_events