import altair as alt
import pandas as pd
from vega_datasets import data

PROCESSED_DATA_PATH = "data/processed/tsunami-events.csv"
COUNTRY_CODES_FILE_PATH = "data/processed/country_codes.csv"

def create_map_plot(year_start, year_end, countries,
                    magnitude_start, magnitude_end):
    """Create a world map plot with countries colored by no. of tsunami
    hits and with origin points.

    Parameters
    ----------
    year_start : int
        the lower bound of the range of years selected by the user
    year_end : int
        the upper bound of the range of years selected by the user
    countries : list
        the list of countries to filter as selected by the user
    magnitude_start : int
        the lower bound of the earthquake magnitude selected by the user
    magnitude_end : int
        the upper bound of the earthquake magnitude selected by the user
    
    Returns
    -------
    LayerChart:
        a world map plot with countries colored by no. of tsunami
        hits and with origin points
    """
    
    world_map = alt.topo_feature(data.world_110m.url, 'countries')
    counts, tsunami_events = preprocess_data(year_start, year_end, countries,
                                             magnitude_start, magnitude_end)
    mean_count = tsunami_events.groupby("country").size().mean()

    map_click = alt.selection_single(fields=['name'])
    map = (
        alt.Chart(world_map)
        .mark_geoshape(stroke="grey", strokeWidth=0.3)
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(counts, "country-code", ["name", "count"])
        )
        .encode(
            color=alt.condition(
                "datum.count>0.0",
                alt.Color("count:Q",
                        scale=alt.Scale(scheme='blues',
                                        domainMin=1,
                                        domainMid=mean_count),
                        legend=alt.Legend(orient='bottom-left'),
                        title="Total Tsuanami Hits"),
                alt.ColorValue("white")
            ),
            tooltip=[alt.Tooltip("name:N", title="Country"),
                     alt.Tooltip("count:Q", title="Total Tsunami Hits")],
            opacity=alt.condition(map_click, alt.value(1), alt.value(0.2))
        )
        .add_selection(map_click)
        .project("naturalEarth1")
        .properties(width=730, height=350)
    )

    tsunami_events["legend"] = "Tsunami Origin"

    tsunami_spots = (
        alt.Chart(tsunami_events)
        .mark_circle(size=5, opacity=0.35)
        .encode(
            latitude="latitude:Q",
            longitude="longitude:Q",
            color=alt.Color("legend:N",
                            scale=alt.Scale(range=["red"]),
                            legend=alt.Legend(title="",
                                              orient='top-left')),
            tooltip=[alt.Tooltip("earthquake_magnitude:Q",
                                 title="Earthquake Magnitude"),
                     alt.Tooltip("year:Q",
                                 title="Event Year")]
        )
        .properties(width=300, height=100)
    )

    return (map + tsunami_spots).to_html()

def preprocess_data(year_start, year_end, countries,
                    magnitude_start, magnitude_end):
    """Reads and preprocesses the data for the map plot.

    Parameters
    ----------
    year_start : int
        the lower bound of the range of years selected by user
    year_end : int
        the upper bound of the range of years selected by user
    countries : list
        the list of countries to filter as selected by the user
    magnitude_start : int
        the lower bound of the earthquake magnitude selected by the user
    magnitude_end : int
        the upper bound of the earthquake magnitude selected by the user
    
    Returns
    -------
    counts:
        a dataframe which has the number of tsunami hits by countries
    tsunami_events:
        a dataframe of filtered tsunami events
    """

    tsunami_events = pd.read_csv(PROCESSED_DATA_PATH)
    country_codes = pd.read_csv(COUNTRY_CODES_FILE_PATH)

    if not (year_start and year_end and year_start <= year_end):
        raise ValueError("Invalid value for year start and/or year end")
    
    if not countries and countries != []:
         raise ValueError("Invalid value for countries")

    tsunami_events = tsunami_events.query(
        f"({year_start} <= year <= {year_end}) &"
        f"({magnitude_start} <= earthquake_magnitude <= {magnitude_end})"
    )
    if countries != []:
        tsunami_events = (
            tsunami_events[tsunami_events["country"].isin(countries)]
        )
    
    counts = tsunami_events.groupby("country").size().reset_index(name='count')
    counts = counts.merge(country_codes,
                          how="right",
                          left_on="country",
                          right_on="name")
    counts["count"] = counts["count"].fillna(0)

    return counts, tsunami_events
