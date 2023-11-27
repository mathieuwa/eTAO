import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as COLOOO
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


# from https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html


def radar_factory(num_vars, NAME, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = NAME
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta




def plot_unique():

    colors = ['b', 'r', 'g', 'm', 'y']

    eTAO = [0, 0, 1, 3]

    fig = plt.figure(figsize=(9, 9))
    #fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    ### AX1
    theta_3 = radar_factory(3, NAME="radar_3", frame='polygon')
    ax = fig.add_subplot(3, 2, 1, projection='radar_3')
    ax.set_rgrids([1, 2, 3, 4, 5])
    ax.set_title('TAO', weight='bold', size='medium', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip([eTAO[1:]], colors):
        ax.plot(theta_3, d, color=color)
        poly = ax.fill(theta_3, d, facecolor=color, alpha=0.25, label='_nolegend_')
    ax.set_varlabels(['T', 'A', 'O'])
    ax.set_ylim(-1, 6)



    xmin, xmax = 0, 1
    ymin, ymax = 0, 1

    cmap = COLOOO.LinearSegmentedColormap.from_list('black_to_red', ['black', 'red'])
    grad = np.atleast_2d(np.linspace(0, 4, 256)).T
    #img = ax.imshow(grad, extent=[xmin, xmax, ymin, ymax],interpolation='nearest', cmap=cmap)


    #print(poly)
    #img.set_clip_path(poly[0])



    theta_4 = radar_factory(4, NAME="radar_4", frame='polygon')
    ax = fig.add_subplot(3, 2, 2, projection='radar_4')
    ax.set_rgrids([1, 2, 3, 4, 5])
    ax.set_title('eTAO', weight='bold', size='medium', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip([eTAO], colors):
        ax.plot(theta_4, d, color=color)
        ax.fill(theta_4, d, facecolor=color, alpha=0.25, label='_nolegend_')
    ax.set_varlabels(['e', 'T', 'A', 'O'])
    ax.set_ylim(-1, 6)


    # Plot the four cases from the example data on separate axes


    #ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    #labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
    #legend = axs[0].legend(labels, loc=(0.9, .95),
    #                              labelspacing=0.1, fontsize='small')


    return fig


class SpiderPlot():

    def __init__(self):
        pass

    @classmethod
    def plot(cls, eye):
        e = eye.get_value("e")
        T = eye.get_value("T")
        A = eye.get_value("A")
        O = eye.get_value("O")

        return plot_unique()
