from itertools import count
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt

# tsunami_df = pd.read_csv("data/processed/tsunami-events.csv")

cars = data.cars()

def plot_altair(xmax):
    chart = alt.Chart(cars[cars['Horsepower'] < xmax]).mark_bar().encode(
        x='Weight_in_lbs:Q',
        y='Horsepower')
    return chart.to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
        html.Iframe(
            id='bar',
            srcDoc=plot_altair(xmax=0),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Slider(id='xslider', min=0, max=240)])
        
@app.callback(
    Output('bar', 'srcDoc'),
    Input('xslider', 'value'))
def update_output(xmax):
    return plot_altair(xmax)

if __name__ == '__main__':
    app.run_server(debug=True)
