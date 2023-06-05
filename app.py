from dash import Dash, html, dcc, callback, Output, Input
from diagram_plot import draw_diagram


app = Dash(__name__)

app.layout = html.Div([
    html.Div(
        children='Please enter a string consisting of letters from the set {a, A, b, B}:'),
    dcc.Input(id='word', type='text', pattern=r'[aAbB]*', value=''),
    dcc.Graph(id='diagram', figure={})
])


@app.callback(
    Output('diagram', 'figure'),
    Input('word', 'value')
)
def update_diagram(input_word):
    return draw_diagram(input_word)


if __name__ == '__main__':
    app.run_server(debug=True)
