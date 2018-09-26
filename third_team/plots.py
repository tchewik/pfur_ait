import logging
import plotly.graph_objs as go
from plotly.offline import plot
from py_expression_eval import Parser

logger = logging.getLogger(__name__)


def plot_function(x, f_str, quadratic=False):
    def get_y():
        parser = Parser()
        y = []
        try:
            expr = parser.parse(f_str)
            for _x in x:
                y.append(expr.evaluate({'x': _x}))
            return y
        except Exception:
            return [0] * len(x)

    data = [go.Scatter(
        x=x,
        y=get_y(),
        name='y = %s' % f_str
        )]

    if quadratic:
        data.append(go.Scatter(
            x=x,
            y=[0] * len(x),
            name='y = 0'
        ))

    layout = go.Layout(
        autosize=True,
        xaxis=dict(autorange=True),
        yaxis=dict(autorange=True),
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div
