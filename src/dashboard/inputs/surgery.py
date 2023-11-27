import streamlit as st

from parameters.parameters import Parameters


class Surgery:
    def __init__(self):
        self.lasik = None
        self.iso = None
        self.blepharo = None


    def display_sidebar(self):
        st.header(Parameters.text("CONTEXT"))

        self.lasik = st.toggle(Parameters.text("LASIK"))
        self.iso = st.toggle(Parameters.text("ISOTRETINOIN"))
        self.blepharo = st.toggle(Parameters.text("BLEPHAROPLASTY"))


