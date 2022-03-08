import altair as alt
import pandas as pd

PROCESSED_DATA_PATH = "data/processed/tsunami-events.csv"

def preprocess(year_start, year_end):
    """The function to return the processed dataframe with a new index column
    and combination column of the country and year. Also filters the df
    based on the callback year slider for tsunamis occurring between
    specific dates, then reorders by tsunami intensity.
    Parameters
    ----------
    year_start : int
        the lower bound of the range of years selected by user
    year_end : int
        the upper bound of the range of years selected by user
    Returns
    -------
    df:
        a processed dataframe with additional columns and filtered
        data
    """
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
    """The function to create a bar graph of the highest intensity
    tsunamis between the year_start and year_end.
    Parameters
    ----------
    year_start : int
        the lower bound of the range of years selected by user
    year_end : int
        the upper bound of the range of years selected by user
    Returns
    -------
    bar plot object
        horizontal bar graph of greatest intensity tsunamis with tooltip
        to glean further information when hovering over each bar.
    """
    df = preprocess(year_start, year_end)
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('tsunami_intensity:Q', title = 'Tsunami Intensity', scale=alt.Scale(domain=(0, 12))),
        y=alt.Y('tsunami_instance:N', sort = '-x', title = 'Country', axis = alt.Axis(labelExpr="datum.country")),
        color=alt.Color('country:O', legend=alt.Legend(title="Countries (Top 10)")),
        tooltip=("country:O", "location_name:O", "tsunami_intensity:Q", "earthquake_magnitude:Q", "year:Q", "month:O")
        ).properties(width=250, height=180)
    
    chart.configure_legend(padding=10,
                            cornerRadius=10,
                            orient='top-right')

    text = chart.mark_text(align="left", baseline="middle", dx = 3).encode(
        text= 'combine:O')
    
    plot = chart + text
    return plot.to_html()
