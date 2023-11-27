import matplotlib.pyplot as plt
import matplotlib.patches as patches

from parameters.parameters import Parameters

class eTAOLine:

    COLORS = Parameters.ETAO_LINE_COLORS
    #ORDER_COLORS = Parameters.ORDER_COLORS

    def __init__(self):
        pass


    @classmethod
    def plot(cls, eTAO):

        fig = plt.figure(figsize=(6, 0.5))

        # Plot the axis
        x_values = Parameters.ETAO_LINE_THRESHOLDS
        y_values = [0]*len(x_values)

        plt.text(0-0.05, -0.010, "0", color="black", fontsize=11, weight="bold")
        plt.plot([-0.02, -0.02], [-0.005, 0.005], lw=2, solid_capstyle='round', zorder=10, color="black")
        plt.text(10-0.05, -0.010, "10", color="black", fontsize=11, weight="bold")
        plt.plot([10+0.03, 10+0.03], [-0.005, 0.005], lw=2, solid_capstyle='round', zorder=10, color="black")

        for i in range(len(x_values)-1):
            X = x_values[i:i+2]
            Y = y_values[i:i+2]
            plt.plot(X, Y, color=cls.COLORS[i], linestyle="-", linewidth=6)

        # Plot the eTAO arrow
        plt.plot([eTAO-0.02, eTAO-0.02], [-0.005, 0.007], lw=4, solid_capstyle='round', zorder=100, color="black")
        plt.text(eTAO-0.15, 0.012, f"{eTAO:.2f}", color="black", fontsize=13, weight="bold")

        plt.axis('off')
        return fig
