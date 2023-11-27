import pandas as pd
import streamlit as st
from datetime import date, datetime

from parameters.parameters import Parameters
from dashboard.patient import Patient


class Dashboard:
    """
    Dashboard manager, including a Patient object (that olds all computations) and
    a DashboardSidebar and DashboardMain that display the patients properties
    """
    def __init__(self):
        self.patient = Patient()
        self.report = None

    def display(self):
        with st.sidebar:
            self._display_sidebar()
        self._display_main()

    def get_report_data(self, practitioner):

        data = self.patient.get_report(self.report)
        data['report_type'] = self.report
        data['practitioner'] = practitioner

        return data

    def _display_sidebar(self):
        self.patient.demographics.display_sidebar()  # Display demographics
        report = st.radio(Parameters.text('REPORT'),
                               [Parameters.text("OCULAR_DRYNESS"),
                                Parameters.text("OCULAR_SURGERY")],
                                horizontal=True,
                                label_visibility="collapsed")
        if report in Parameters.TRANSLATIONS['OCULAR_DRYNESS'].values():
            self.report = "OCULAR_DRYNESS"
        else:
            self.report = "OCULAR_SURGERY"

        if self.report == "OCULAR_DRYNESS":
            self.patient.ocular_dryness.display_sidebar()  # Display ocular dryness
        self.patient.surgery.display_sidebar()  # Display surgeries
        self.patient.right_eye.display_sidebar()  # Display right eye
        self.patient.left_eye.display_sidebar()  # Display left eye


    def _display_main(self):
        self.patient.display_main_results()

        col1, col2 = st.columns(2)
        with col1:
            self.patient.display_eye_column('RIGHT')
        with col2:
            self.patient.display_eye_column('LEFT')

        if self.report == "OCULAR_DRYNESS":
            self.patient.display_recommendations()
