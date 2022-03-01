from dash import Dash, html

app = Dash()
server = app.server

app.layout = html.Div("Hello world!")

app.run_server()