import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd

df = pd.read_csv("data/processed/tsunami-events.csv")
df.columns.values[0] = 'tsunami_instance'

def select_year(ymin, ymax):
    return df_all.loc[(df['year'] > ymin) & (df['year'] < ymax)]

def plot_altair(df_daterange):
    chart = alt.Chart(df_daterange).mark_bar().encode(
        x=alt.X('tsunami_intensity:Q'),
        y=alt.Y('tsunami_instance:N'),
        color = alt.Color('country:O'),
        tooltip=("country:O, ""location_name:O", "tsunami_intensity:Q", "earthquake_magnitude:Q", "year:Q", "month:O"))
    return chart.to_html()


app = Dash(__name__, external_stylesheets=[
           'https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    html.Iframe(
        id='bar',
        srcDoc=plot_altair(df_daterange),
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.RangeSlider(1500, 2000, 20, value=[1900, 1990], id='my-range-slider',
                    marks={str(year): str(year)
                           for year in range(1500, 2000, 20)}
                    )])


@ app.callback(
    Output('bar', 'srcDoc'),
    Input('my-range-slider', 'value'))
def update_output(value):
    df_daterange = select_year(value[0], value[1])
    plot_altair(df_daterange)


if __name__ == '__main__':
    app.run_server(debug=True)
