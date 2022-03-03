import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd

data = pd.read_csv("data/processed/tsunami-events.csv")
df_all = pd.DataFrame(data.groupby("year").size()).rename(
    columns={0: "tsunami_count"}).reset_index()

df = pd.DataFrame(data.groupby(
    ["year", "country"]).size()).rename(columns={0: "tsunami_count"}).reset_index()


def select_year(ymin, ymax):
    return df_all.loc[(df_all['year'] > ymin) & (df_all['year'] < ymax)]

def plot_altair(df):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('tsunami_intensity:Q'),
        y=alt.Y('country:O'),
        color = alt.Color('country:O'),
        tooltip=("location_name:O", "tsunami_intensity:Q", "earthquake_magnitude:Q", "year:Q", "month:O"))
    return chart.to_html()


app = Dash(__name__, external_stylesheets=[
           'https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    html.Iframe(
        id='bar',
        srcDoc=plot_altair(df),
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.RangeSlider(1500, 2000, 20, value=[1900, 1990], id='my-range-slider',
                    marks={str(year): str(year)
                           for year in range(1500, 2000, 20)}
                    )])


# @ app.callback(
#     Output('line', 'srcDoc'),
#     Input('my-range-slider', 'value'))
# def update_output(value):
#     return plot_altair(value[0], value[1])


if __name__ == '__main__':
    app.run_server(debug=True)
