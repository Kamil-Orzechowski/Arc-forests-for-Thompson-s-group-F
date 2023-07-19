import dash
from dash import html, dcc, callback, Output, Input
from domain.plotting.diagram_plot import draw_diagram

dash.register_page(__name__, path='/',
                   title="Arc forests for Thompson's group F — application")


def layout():
    return html.Div([
        dcc.Markdown(r'''
            # Arc forests for Thompson's group $F$
            
            This application helps visualize the elements of Thompson's group $F$
            using *arc forest diagrams*. Any such diagram is a collection of semicircles joining some points
            on the $x$ axis whose coordinates are dyadic rationals, together with a distinguished *basepoint*.
            Each diagram has its *essential part*, i.e. there is minimal range $[x_{min}, x_{max}]$ such that
            the basepoint is between $x_{min}$ and $x_{max}$, and all arcs with the $x$ coordinate outside this interval
            are *trivial*, which means they connect two consecutive integer points on the $x$ axis.
            
            The expected input is a word $w$ over the alphabet $\{a, A, b, B\}$, where $a, b$ represent the standard generators
            of $F$ in the finite presentation
            $$\left<a,b \;|\; [ab^{-1}, a^{-1}ba], \, [ab^{-1}, a^{-2}ba^{2}\right>$$
            and $A=a^{-1}$, $B=b^{-1}$ stand for their inverses.
            The application returns the arc forest diagram for the element of $F$ given by $w$.
            In a trivial case $w$ may be the empty word, which will result showing the trivial diagram representing the
            identity element of $F$.
        ''', mathjax=True),
        html.Div(children=[
            'For a more detailed mathematical desription of all the notions mentioned above we refer to the page ',
            dcc.Link('mathematical details.',
                     href=dash.page_registry['pages.math-details']['path']),
            html.P()
        ]
        ),
        html.Div(
            'Enter a string consisting of letters from the set {a, A, b, B}'),
        dcc.Input(id='word', type='text',
                  pattern=r'[aAbB]*', value='', autoFocus=True),
        html.P(),
        html.Div(
            children='Specify the number of trivial arcs appended to each end of the essential part of the diagram'),
        dcc.Input(id='tail_length', type='number', min=0, value=100),
        html.P(),
        html.Div(
            children='Specify how far from the center the initial range on the x axis should be'),
        dcc.Input(id='range_around_center', type='number', min=0, value=5),
        html.P(),
        html.Div(children='Center the visible part of the diagram at'),
        dcc.RadioItems(id='center', options=[
            'zero', 'the basepoint'], value='zero'),
        html.P(),
        html.Div(children='Select number format'),
        dcc.RadioItems(id='format', options=[
            'decimal', 'dyadic fraction'], value='decimal'),
        dcc.Graph(id='diagram', figure={})
    ])


@callback(
    Output('diagram', 'figure'),
    Input('word', 'value'),
    Input('tail_length', 'value'),
    Input('range_around_center', 'value'),
    Input('center', 'value'),
    Input('format', 'value')
)
def update_diagram(input_word, tail_length, range_around_center, center, format):
    return draw_diagram(input_word, tail_length, range_around_center, center, format)
