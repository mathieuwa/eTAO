import streamlit as st
import numpy as np

from parameters.parameters import Parameters
from .etao_score import eTAOScore
from .plots.etao_line import eTAOLine
from .plots.radar_plot import RadarPlot


class Results:
    def __init__(self):
        self.eTAO = None

    def display_main_results(self, demographics, ocular_dryness, left_eye, right_eye, surgery):

        fn = demographics.first_name.capitalize()
        ln = demographics.last_name.upper()
        age = demographics.age
        title = Parameters.get_dashboard_title(demographics.sex, fn, ln, age)
        st.subheader(title)
        self.eTAO = eTAOScore.compute(ocular_dryness, left_eye, right_eye, surgery)

        col1, col2 = st.columns([65, 35])
        with col1:
            st.image('static/img/logo.png', width=300)
            fig = eTAOLine.plot(self.eTAO)
            fig.savefig(Parameters.get_img_path('etao'), bbox_inches='tight')
            st.pyplot(fig)

        with col2:
            fig = RadarPlot.plot_eyes(left_eye, right_eye)
            fig.savefig(Parameters.get_img_path('main_barplot'), bbox_inches='tight')
            st.pyplot(fig)


    def display_eye_eTAO(self, eye):
        # Display eye barplot
        fig = RadarPlot.plot_eye(eye)
        #fig.savefig(Parameters.get_img_path(f'{self.side}_barplot'), bbox_inches='tight')
        st.pyplot(fig)