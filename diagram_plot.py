import plotly.graph_objects as go
from arc_plot import semicircle_path
from model import Diagram, trivial_diagram


def draw_diagram(word: str, trivial_tail_length=100, range_around_center=5, center='zero'):
    diagram = trivial_diagram.apply_word(word)
    basepoint = diagram.basepoint
    intervals = diagram.get_intervals()
    left_end, right_end = intervals[0][0], intervals[len(intervals) - 1][1]
    trivial_head = [(left_end - trivial_tail_length + i, left_end - trivial_tail_length + i + 1)
                    for i in range(trivial_tail_length)]
    trivial_tail = [(right_end + i, right_end + i + 1) for i in range(trivial_tail_length)]
    intervals = trivial_head + intervals + trivial_tail
    arcs = [dict(type="path",
                 path=semicircle_path(interval[0], interval[1])) for interval in intervals]
    x_ticks = [intervals[0][0]] + [interval[1] for interval in intervals]
    x_center = basepoint if center == 'the basepoint' else 0
    x_range = [x_center - range_around_center, x_center + range_around_center]
    fig = go.Figure()
    fig.update_layout(shapes=arcs)
    fig.update_layout(xaxis= {
                        'tickmode': 'array',
                        'tickvals': x_ticks,
                        'ticktext': x_ticks,
                        'range': x_range
                    },
                      yaxis={
                        'scaleanchor': 'x',
                        'scaleratio': 1,
                        'showticklabels': False,
                    })
    fig.add_trace(go.Scatter(x=[basepoint], y=[0], mode='markers'))
    return fig
