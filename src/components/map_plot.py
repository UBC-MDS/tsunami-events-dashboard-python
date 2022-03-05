import altair as alt
import pandas as pd
from vega_datasets import data

PROCESSED_DATA_PATH = "data/processed/tsunami-events.csv"
COUNTRY_IDS_FILE_PATH = "data/processed/world-110m-country-names.tsv"

def create_map_plot(year_start, year_end, countries):
    
    world_map = alt.topo_feature(data.world_110m.url, 'countries')
    counts, tsunami_events = preprocess_data(year_start, year_end, countries)
    mean_count = tsunami_events.groupby("country").size().mean()

    map = (
        alt.Chart(world_map)
        .mark_geoshape(stroke="grey", strokeWidth=0.3)
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(counts, "id", ["name", "count"])
        )
        .encode(color=alt.condition(
            "datum.count>0.0",
            alt.Color("count:Q",
                    scale=alt.Scale(scheme='blues',
                                    domainMin=1,
                                    domainMid=mean_count),
                    legend=alt.Legend(orient='bottom-left'),
                    title="Total Tsuanami Hits"),
            alt.ColorValue("white")),
                tooltip=[alt.Tooltip("name:N", title="Country"),
                         alt.Tooltip("count:Q", title="Total Tsunami Hits")])
        .project("naturalEarth1")
        .properties(width=730, height=350)
    )

    tsunami_events["legend"] = "Tsunami Origin"

    tsunami_spots = (
        alt.Chart(tsunami_events)
        .mark_circle(size=5)
        .encode(
            latitude="latitude",
            longitude="longitude",
            color=alt.Color("legend:N",
                            scale=alt.Scale(range=["red"]),
                            legend=alt.Legend(title="",
                                              orient='top-left')),
            tooltip=[alt.Tooltip("earthquake_magnitude",
                    title="Earthquake Magnitude")]
        ).properties(width=300, height=100)
    )

    return (map + tsunami_spots).to_html()

def preprocess_data(year_start, year_end, countries):

    tsunami_events = pd.read_csv(PROCESSED_DATA_PATH)
    country_ids = pd.read_csv(COUNTRY_IDS_FILE_PATH, sep="\t")

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
    
    counts = tsunami_events.groupby("country").size().reset_index(name='count')
    counts = counts.merge(country_ids,
                          how="right",
                          left_on="country",
                          right_on="name")
    counts["count"] = counts["count"].fillna(0)

    return counts, tsunami_events
