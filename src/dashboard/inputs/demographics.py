import streamlit as st
from datetime import date, datetime

from parameters.parameters import Parameters


class Demographics:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.birthday = None
        self.sex = None
        self.exam_date = None

    @property
    def age(self):
        if self.exam_date == None or self.birthday == None:
            return None
        return (self.exam_date - self.birthday).days/365.25

    def display_sidebar(self):
        col1, col2 = st.columns(2)
        with col1:
            languages = list(Parameters.LANGUAGES.keys())
            language = st.selectbox("Language", languages)
            Parameters.set_language(language)
        with col2:
            self.exam_date = st.date_input(Parameters.text('DATE'),
                                           value=date.today(),
                                           min_value=datetime.strptime('1/1/2008', '%d/%m/%Y'),
                                           max_value=date.today(),
                                           format="DD/MM/YYYY")

        col1, col2 = st.columns(2)
        with col1:
            self.first_name = st.text_input(Parameters.text('FIRST_NAME'))
        with col2:
            self.last_name = st.text_input(Parameters.text('LAST_NAME'))

        col1, col2 = st.columns(2)
        with col1:
            self.sex = st.selectbox(Parameters.text('SEX'), [Parameters.text('MALE'), Parameters.text('FEMALE')])
        with col2:
            self.birthday = st.date_input(Parameters.text('BIRTHDAY'),
                                          value=datetime.strptime('1/1/1960', '%d/%m/%Y'),
                                          min_value=datetime.strptime('1/1/1900', '%d/%m/%Y'),
                                          max_value=date.today(),
                                          format="DD/MM/YYYY")

    def display_patient_information(self):
        st.subheader('Patient')

        col1, col2 = st.columns(2)
        with col1:
            text = Parameters.text('LAST_NAME')
            last_name = self.last_name.upper()
            st.write("{} : {}".format(text, last_name))

        with col2:
            text = Parameters.text('FIRST_NAME')
            first_name = self.first_name.capitalize()
            st.write("{} : {}".format(text, first_name))
