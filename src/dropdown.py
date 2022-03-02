from itertools import count
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

tsunami_df = pd.read_csv("data/processed/tsunami-events.csv")

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

table_cols = ["Country", "Location Name", "Year", "Month", "Tsunami Intensity", "Earthquake Magnitude"]

app.layout = html.Div([
              dash_table.DataTable(
                id = "tsunami_table",
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in table_cols
                ],
                data = tsunami_df.to_dict('records'),
                editable=True,
                sort_action="native",
                sort_mode="multi",
                column_selectable=False,
                row_selectable=False,
                row_deletable=True,
                filter_action="native",
                page_action="native",
                page_current= 0,
                page_size= 10),
html.Button('Add Row', id='editing-rows-button', n_clicks=0)])

@app.callback(
    Output('tsunami_table', 'data'),
    Input('editing-rows-button', 'n_clicks'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

# @app.callback(
#     Output('tsunami_table', 'data'),
#     Input('top_dropdown', 'value'),
# #     Input('year_slider', 'value')
# )
# def update_table():
#   tsunami = tsunami_df
#   tsunami = tsunami.sort_values(by = ['tsunami_intensity'])
#   return tsunami.to_dict('records')
  
