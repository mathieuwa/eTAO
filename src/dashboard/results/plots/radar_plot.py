import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from parameters.parameters import Parameters

# Possible avec Plotly https://plotly.com/python/wind-rose-charts/

class RadarPlot():

    def __init__(self):
        pass

    @classmethod
    def _convert_to_thetas_radii_widths_colors(cls, values):
        radii, thetas, widths, colors = [], [], [], []

        width = 2*np.pi/len(values) - 2*np.pi*Parameters.PERCENT_GUTTER
        step = 2*np.pi/len(values)
        possible_thetas = [i*step for i in range(len(values))]

        for i, (name, value) in enumerate(values):
            rs = list(range(1, value+1))
            ws = [width] * len(rs)
            ts = [possible_thetas[i]] * len(rs)
            color = Parameters.RADAR_PLOT_COLORS[:len(rs)]

            rs.reverse()
            color.reverse()

            radii += rs
            thetas += ts
            widths += ws
            colors += color

        return thetas, radii, widths, colors

    @classmethod
    def _plot_eye_barplot(cls, ax, values):
        thetas, radii, widths, colors = cls._convert_to_thetas_radii_widths_colors(values)
        ax.bar(thetas, radii, widths, bottom=0.0, color=colors, alpha=1)
        ax.set_ylim(0, Parameters.MAX_HEIGHT)

    def _convert_naming(ticks, eye=None):
        
        side = 'D' if eye.side == "RIGHT" else "G"

        return [Parameters.BARPLOT_CORRESPONDANCE[_]+side for _ in ticks]

    @classmethod
    def plot_eye(cls, eye):

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # Plot
        values = [(_, eye.get_bar_height(_)) for _ in "eTAO"]
        cls._plot_eye_barplot(ax, values)

        # Ticks
        ticks = cls._convert_naming(["O", "e", "T", "A"], eye)
        ax.set_xticks([-2*np.pi/4, 0, 2*np.pi/4, np.pi], ticks)
        ax.set_thetalim(-np.pi, np.pi)

        # Other configs
        ax.set_yticklabels([])
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.grid(False)

        cls._add_graduation(ax, 'eTAO-eye')

        return fig

    @classmethod
    def _plot_eyes_single(cls, ax, left_eye, right_eye, name):
        left_values = [(_, left_eye.get_bar_height(_)) for _ in name]
        right_values = [(_, right_eye.get_bar_height(_)) for _ in name]

        values = left_values + right_values

        cls._plot_eye_barplot(ax, values)


    @classmethod
    def plot_eyes(cls, left_eye, right_eye):

        fig, ax = plt.subplots( subplot_kw={'projection': 'polar'})

        cls._plot_eyes_single(ax, left_eye, right_eye, "eTAO")
        ax.set_title("eTAO", fontsize=22)

        labels = cls._convert_naming(["e", "T", "A", "O"], left_eye) + cls._convert_naming(["e", "T", "A", "O"], right_eye)

        labels = labels[-3:] + labels[:-3]
        ticks = [-(6-2*i)*np.pi/8 for i in range(len(labels))]

        ax.set_xticks(ticks, labels, fontsize=14)
        ax.set_thetalim(-np.pi, np.pi)

        ax.set_yticklabels([])
        #ax.set_xticklabels([])
        ax.set_theta_zero_location('S')
        ax.set_theta_direction(-1)
        ax.grid(False)

        cls._add_graduation(ax, 'eTAO')

        return fig

    @classmethod
    def _add_graduation(cls, ax, display):

        if display == "eTAO":
            directions = np.linspace(0, 2*np.pi, 9)
        elif display == "TAO":
            directions = np.linspace(0, 2*np.pi, 7)
        elif display == "eTAO-eye":
            directions = np.linspace(0, 2*np.pi, 5)
        elif display == "TAO-eye":
            directions = np.linspace(0, 2*np.pi, 4)
        else:
            directions = [0]


        for d in directions:
            ax.arrow(d, 0, 0, 2.8, color='#0b0b0b', zorder=3, head_width=0.1, linewidth=0.5)
            for i in range(Parameters.NUMBER_OF_GRADUATION):
                SIZE = Parameters.TICK_SIZE
                thetas = [d-SIZE/(i+1), d+SIZE/(i+1)]
                r = [i/Parameters.NUMBER_OF_GRADUATION*3]*2
                ax.plot(thetas, r, color='#0b0b0b')

