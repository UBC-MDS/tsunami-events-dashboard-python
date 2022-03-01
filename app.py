from dash import Dash, html

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div("Hello world!")

if __name__ == '__main__':
    app.run_server(debug=True)
