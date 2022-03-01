from dash import Dash, html

app = Dash()
app.layout = html.Div("Hello world!")
app.run_server()