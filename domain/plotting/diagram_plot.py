import plotly.graph_objects as go
from domain.plotting.arc_plot import semicircle_path
from fractions import Fraction
from domain.model import trivial_diagram


def draw_diagram(word: str, trivial_tail_length=100, range_around_center=5, center='zero', format='decimal'):
    diagram = trivial_diagram.apply_word(word)
    basepoint = diagram.basepoint
    intervals = diagram.get_intervals()
    maximal_intervals = diagram.get_intervals(maximal_only=True)

    left_end, right_end = maximal_intervals[0][0], maximal_intervals[- 1][1]
    trivial_head = [(left_end - trivial_tail_length + i, left_end - trivial_tail_length + i + 1)
                    for i in range(trivial_tail_length)]
    trivial_tail = [(right_end + i, right_end + i + 1)
                    for i in range(trivial_tail_length)]
    intervals, maximal_intervals = [
        trivial_head + arr + trivial_tail for arr in (intervals, maximal_intervals)]

    arcs = [dict(type="path",
                 path=semicircle_path(interval[0], interval[1]),
                 line_width=3 if interval in maximal_intervals else 2,
                 line_color='green') for interval in intervals
            ]
    x_ticks = [intervals[0][0]] + [interval[1] for interval in intervals]
    x_center = basepoint if center == 'the basepoint' else 0
    x_range = [x_center - range_around_center, x_center + range_around_center]
    x_labels = [str(Fraction(number))
                for number in x_ticks] if format == 'dyadic fraction' else x_ticks

    fig = go.Figure()
    fig.update_layout(shapes=arcs)
    fig.update_layout(xaxis={
        'tickmode': 'array',
        'tickvals': x_ticks,
        'ticktext': x_labels,
        'range': x_range
    },
        yaxis={
        'scaleanchor': 'x',
        'scaleratio': 1,
        'showticklabels': False,
    },
        legend={
        'orientation': 'h',
        'x': 0.0,
        'y': -0.25,
        'xanchor': 'center',
        'yanchor': 'bottom',
    },
        title={'text': 'Arc forest diagram',
               'x': 0.5,
               'font_size': 25})
    fig.add_trace(go.Scatter(x=[basepoint], y=[0],
                             mode='markers',
                             marker_size=10,
                             name='basepoint',
                             hoverinfo='x',
                             showlegend=True))
    return fig
