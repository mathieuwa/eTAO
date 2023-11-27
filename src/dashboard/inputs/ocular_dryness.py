import streamlit as st

from parameters.parameters import Parameters


class OcularDryness:
    def __init__(self):
        self.intensity = None
        self.frequency = None

    def display_sidebar(self):
        header = Parameters.text('DRYNESS_HEADER')
        st.header(header)

        text = Parameters.text('DRYNESS_INTENSITY')
        help_text = Parameters.text('DRYNESS_INTENSITY_EXPLANATION')
        self.intensity = st.number_input(text, min_value=0, max_value=10, help=help_text)

        if self.intensity > 0:
            text = Parameters.text('DRYNESS_FREQUENCY')
            help_text = Parameters.text('DRYNESS_FREQUENCY_EXPLANATION')
            self.frequency = st.number_input(text, min_value=1, max_value=10, help=help_text)
        else:
            self.frequency = 0
