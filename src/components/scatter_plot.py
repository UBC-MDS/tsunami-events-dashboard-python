import altair as alt
from dash import Dash, dcc, html, Input, Output
import pandas as pd

PROCESSED_DATA_PATH = "data/processed/tsunami-events.csv"

def create_scatter_plot(year_start=1900, year_end=2022, countries=[]):
    chart = alt.Chart(get_data(year_start, year_end, countries)).mark_point(opacity=0.65, size=20).encode(
        x=alt.X('earthquake_magnitude',
                title='Earthquake Magnitude (Richter Scale)',
                scale=alt.Scale(domain=(5.5, 10))),
        y=alt.Y('total_deaths',
                title='Total Deaths (log-transformed), per Event',
                scale=alt.Scale(type='log')),
        color='country',
        tooltip=['year', 'mercalli_intensity', 'country', 'total_deaths']
    ).interactive(
    ).properties(width=400, height=220)
    return chart.to_html()


def get_data(year_start=1802, year_end=2022, countries=[]):

    tsunami_events = pd.read_csv(PROCESSED_DATA_PATH)

    if not (year_start and year_end and year_start <= year_end):
        raise ValueError("Invalid value for year start and/or year end")

    if not countries and countries != []:
        raise ValueError("Invalid value for countries")

    tsunami_events = tsunami_events.query(
        f"{year_start} <= year <= {year_end}"
    )
    if countries == []:
        countries = tsunami_events.sort_values(by="earthquake_magnitude", ascending=False)[
            "country"].drop_duplicates().tolist()[:10]

    tsunami_events = tsunami_events[tsunami_events['total_deaths'].notna()]
    tsunami_events['mercalli_intensity'] = pd.cut(tsunami_events['earthquake_magnitude'],
                                                  bins=[1, 2, 4, 5, 6, 7, 10],
                                                  labels=["I", "II-III", "IV–V", "VI–VII", "VII–IX", "VIII or higher"]).astype(str)

    if len(countries) > 10:
        countries_top10 = [x for x in tsunami_events.sort_values(by="earthquake_magnitude", ascending=False)[
            "country"].drop_duplicates().tolist() if x in countries][:10]

        return tsunami_events.loc[(tsunami_events['year'] > year_start) &
                                  (tsunami_events['year'] < year_end) &
                                  (tsunami_events['country'].isin(countries)) &
                                  (tsunami_events['country'].isin(countries_top10))]
    else:
        return tsunami_events.loc[(tsunami_events['year'] > year_start) &
                                  (tsunami_events['year'] < year_end) &
                                  (tsunami_events['country'].isin(countries))]