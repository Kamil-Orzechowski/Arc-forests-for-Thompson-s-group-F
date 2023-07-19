import dash
from dash import Dash, html, dcc, Output, Input
from domain.plotting.diagram_plot import draw_diagram


app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
