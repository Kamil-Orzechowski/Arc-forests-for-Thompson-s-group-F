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
            Each diagram has its *essential part*, i.e. there is a minimal range $[x_{min}, x_{max}]$ such that
            the basepoint is between $x_{min}$ and $x_{max}$, and each arc with one of its ends outside this interval
            is *trivial*, which means it connects two consecutive integer points on the $x$ axis.
            
            The expected input is a word $w$ over the alphabet $\{a, A, b, B\}$, where $a, b$ represent the standard generators
            of $F$ in the finite presentation
            $$\left<a,b \;|\; [ab^{-1}, a^{-1}ba], \, [ab^{-1}, a^{-2}ba^{2}\right>$$
            and $A=a^{-1}$, $B=b^{-1}$ stand for their inverses.
            The application returns the arc forest diagram for the element of $F$ given by $w$. The maximal arcs, i.e those having
            no other arcs above them in the plane, are distinguished by a thicker line. The basepoint is marked by a dot on the $x$ axis.
            In a trivial case $w$ may be the empty word, which will result in showing the trivial diagram representing the
            identity element of $F$.
            
            In this interpretation, the letters $a, A, b, B$ act on group elements from the right in an especially nice way.
            Applying $a$ moves the basepoint to the left, one step along the left maximal arc containing the basepoint, similarly
            $A$ moves the basepoint to the right.
            The action of $b$ removes the right maximal arc containing the basepoint (with the additional insertion of two arcs in a
            special situation if there were no arcs below the deleted one).
            The action of $B$ joins the right maximal arc containing the basepoint with the subsequent maximal arc one step to the right,
            covering them from above (if the arcs involved were also minimal ones of the same diameter, they are removed afterwards).       
        ''', mathjax=True),
        html.Div(children=[
            'For a more detailed mathematical description of all the notions mentioned above we refer to the page ',
            dcc.Link('mathematical details.',
                     href=dash.page_registry['pages.math-details']['path']),
            html.P()
        ]
        ),
        html.Div(
            'Enter a string consisting of letters from the set {a, A, b, B}. For example, \"aaABabBaBBBbA\" is a valid input.'),
        dcc.Input(id='word', type='text',
                  pattern=r'[aAbB]*', value='', autoFocus=True),
        html.P(),
        html.Div(
            children='Specify the number of trivial arcs appended to each end of the essential part of the diagram.'),
        dcc.Input(id='tail_length', type='number', min=0, value=100),
        html.P(),
        html.Div(
            children='Specify how far from the center the initial range on the x axis should be.'),
        dcc.Input(id='range_around_center', type='number', min=0, value=5),
        dcc.Graph(id='diagram', figure={}),
        html.Div(children='Center the visible part of the diagram at:'),
        dcc.RadioItems(id='center', options={
            'zero': 'zero,', 'basepoint': 'the basepoint.'}, value='zero'),
        html.P(),
        html.Div(children='Select number format:'),
        dcc.RadioItems(id='format', options={
            'decimal': 'decimal,', 'dyadic': 'dyadic fraction.'}, value='decimal'),
    ],
        style={'marginLeft': 25, 'marginRight': 25, 'marginTop': 15, 'marginBottom': 15, 'font-size': '1.1rem'})


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
