from itertools import count
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt

tsunami_df = pd.read_csv("data/processed/tsunami-events.csv")

bar = html.Iframe(
    id="bar",
    style={
        "border-width": "0",
        "width": "100%",
        "height": "400px",
    })

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
        html.Iframe(
                id="bar",
                style={
                    "border-width": "0",
                    "width": "100%",
                    "height": "400px"})
        
@app.callback(
    Output("bar", "srcDoc"),
    Input("year_slider", "value"))
def plot_bar(year_slider):
    tsunami = tsunami_df
    tsunami = tsunami.sort_values(by = ['tsunami_intensity'])
    tsunami = tsunami[:11]
    chart = (
        alt.Chart(
            tsunami,
            title="Strongest Tsunamis",
        )
        .mark_bar()
        .encode(
            y=alt.Y("country", sort="-x", title="Country"),
            x=alt.X(tsunami_intensity, title="Tsunami Intensity"),
            color=alt.Color(
                "country",
                sort=alt.EncodingSortField("country", order="descending"),
                title="Country",
            ),
            tooltip=("name:O", "tsunami_intensity:Q"),
        )
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=15)
        .configure_legend(labelFontSize=12)
        .properties(width=400, height=300)
    )
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)
