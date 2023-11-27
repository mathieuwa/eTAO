import plotly.graph_objects as go

from parameters import Parameters

class BarPlot():


    COLORS = Parameters.ETAO_LINE_COLORS

    def __init__(self):
        pass


    @classmethod
    def transform_value_to_barplot(cls, thresholds, value, theta, width):

        if value < thresholds["T1"]:
            r = [value]

        elif value < thresholds["T2"]:
            r = [thresholds["T1"], value-thresholds["T1"]]

        else:
            r = [thresholds["T1"], thresholds["T2"] - thresholds["T1"],  value-thresholds["T2"]]

        colors = cls.COLORS[:len(r)]
        thetas = [theta]*len(r)
        widths = [width]*len(r)

        return r, colors, thetas, widths

    @classmethod
    def plot(cls, eye, thresholds, eTAO=True):

        rs, thetas, widths, colors = [], [], [], []

        if eTAO:
            letters = ["e", "T", "A", "O"]
            angles = [0, 90, 180, 270]
            single_width = 90
        else:
            letters = ["T", "A", "O"]
            angles = [0, 120, 240]
            single_width = 120


        for pb, angle in zip(letters, angles):
            r, color, theta, width = cls.transform_value_to_barplot(thresholds, eye.get_value(pb), angle, single_width)
            rs += r
            colors += color
            thetas += theta
            widths += width


        fig = go.Figure(go.Barpolar(
            r=rs,
            theta=thetas,
            width=widths,
            marker_color=colors,
            marker_line_color="black",
            marker_line_width=1,
            hoverinfo=None,
            opacity=0.8
        ))

        fig.update_layout(
            template=None,
            polar = dict(
                # TODO ASK MAX
                radialaxis = dict(range=[0, 5], showticklabels=True, ticks=''),
                angularaxis = dict(showticklabels=False, ticks=''),

            ),
            polar_radialaxis_gridcolor="#ffffff",
            polar_angularaxis_gridcolor="#ffffff",
        )

        #fig.show()
        return fig
