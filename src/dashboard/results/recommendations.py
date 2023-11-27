import streamlit as st
from parameters.parameters import Parameters

class Recommendations:

    def __init__(self):
        self.light = None
        self.QMR = None
        self.lipiflow = None
        self.lubricant = None


    def display(self):

        st.subheader(Parameters.text("RECOMMENDATIONS", capitalize=False))
        self.lubricant = st.toggle(Parameters.text("LUBRICANT", capitalize=False), value=True)
        self.light = st.radio(Parameters.text("LIGHT", capitalize=False), [0, 1, 2, 3, 4])
        self.QMR = st.radio(Parameters.text("QMR", capitalize=False), [0, 1, 2, 3, 4])
        self.lipiflow = st.radio(Parameters.text("LIPIFLOW"), [0, 1, 2])




