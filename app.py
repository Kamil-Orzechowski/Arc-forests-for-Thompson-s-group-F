from dash import Dash, html, dcc, Output, Input
from diagram_plot import draw_diagram


app = Dash(__name__)

app.layout = html.Div([
    html.Div(
        children='Enter a string consisting of letters from the set {a, A, b, B}'),
    dcc.Input(id='word', type='text', pattern=r'[aAbB]*', value=''),
    html.Div(children='Specify the number of trivial arcs appended to each end of the essential part of the diagram'),
    dcc.Input(id='tail_length', type='number', min=0, value=100),
    html.Div(
        children='Specify how far from the center the initial range on the x axis should be'),
    dcc.Input(id='range_around_center', type='number', min=0, value=5),
    html.Div(children='Center the visible part of the diagram at'),
    dcc.RadioItems(id='center', options=[
                   'zero', 'the basepoint'], value='zero'),
    html.Div(children='Select number format'),
    dcc.RadioItems(id='format', options=[
                   'decimal', 'dyadic fraction'], value='decimal'),
    dcc.Graph(id='diagram', figure={})
])


@app.callback(
    Output('diagram', 'figure'),
    Input('word', 'value'),
    Input('tail_length', 'value'),
    Input('range_around_center', 'value'),
    Input('center', 'value'),
    Input('format', 'value')
)
def update_diagram(input_word, tail_length, range_around_center, center, format):
    return draw_diagram(input_word, tail_length, range_around_center, center, format)


if __name__ == '__main__':
    app.run_server(debug=True)
