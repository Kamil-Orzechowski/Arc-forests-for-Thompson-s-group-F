import plotly.graph_objects as go
from arc_plot import semicircle_path
from model import Diagram, trivial_diagram


def draw_diagram(word: str):
    diagram = trivial_diagram.apply_word(word)
    intervals = diagram.get_intervals()
    arcs = [dict(type="path",
                 path=semicircle_path(interval[0], interval[1])) for interval in intervals]
    fig = go.Figure()
    fig.update_layout(shapes=arcs)
    return fig
