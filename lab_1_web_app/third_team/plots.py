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


def get_str_quadr_y(a, b, c):
    y = ''
    y += str(a) * (a not in [0, 1]) + '*' * (a not in [0, 1]) + 'x^2' * (a != 0)
    y += '+' * (b != 0) + str(b) * (b not in [0, 1]) + '*' * (b not in [0, 1]) + 'x' * (b != 0)
    y += ('+' + str(c)) * (c != 0)
    y = y.replace('+-', '-')

    return y