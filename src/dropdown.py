import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd

df = pd.read_csv("data/processed/tsunami-events.csv")
df['tsunami_instance'] = range(1, len(df) + 1)
df['tsunami_instance'] = df.index

def select_year(ymin, ymax):
    return df.loc[(df['year'] >= ymin) & (df['year'] <= ymax)]

def plot_altair(data):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('tsunami_intensity:Q', title = 'Tsunami Intensity', scale=alt.Scale(domain=(0, 10))),
        y=alt.Y('tsunami_instance:N', sort = '-x', title = 'Country', axis = alt.Axis(labelExpr="datum['country']")),
        tooltip=("country:O", "location_name:O", "tsunami_intensity:Q", "earthquake_magnitude:Q", "year:Q", "month:O"))
    return chart.to_html()


app = Dash(__name__, external_stylesheets=[
           'https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    html.Iframe(
        id='bar',
        srcDoc=plot_altair(data=df),
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
    df_daterange = df_daterange.sort_values(by=['tsunami_intensity'], ascending = False)
    df_daterange = df_daterange[0:15]
    return plot_altair(df_daterange)


if __name__ == '__main__':
    app.run_server(debug=True)
