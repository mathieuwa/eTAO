import streamlit as st

from parameters.parameters import Parameters
from dashboard.inputs import Demographics, OcularDryness, Eye, Surgery
from dashboard.results import Results, Recommendations


class Patient:
    def __init__(self):
        self.demographics = Demographics()
        self.ocular_dryness = OcularDryness()
        self.surgery = Surgery()
        self.left_eye = Eye("LEFT")
        self.right_eye = Eye("RIGHT")
        self.results = Results()
        self.recommendations = Recommendations()

    def display_patient_information(self):
        self.demographics.display_patient_information()

    def display_main_results(self):
        self.results.display_main_results(self.demographics, self.ocular_dryness, self.left_eye, self.right_eye, self.surgery)

    def display_eye_column(self, side):
        st.subheader(Eye.get_eye_header(side))

        eye = self.left_eye if side == "LEFT" else self.right_eye
        eye.display_recommendations()
        #self.results.display_eye_eTAO(eye)

    def display_recommendations(self):
        self.recommendations.display()

    def get_report(self, report_type):
        data = {
            'demographics': {
                'sex': self.demographics.sex,
                'first_name': self.demographics.first_name,
                'last_name': self.demographics.last_name,
                'birthday': self.demographics.birthday,
                'exam_date': self.demographics.exam_date
            },
            'ocular_dryness': {
                'intensity': self.ocular_dryness.intensity,
                'frequency': self.ocular_dryness.frequency,
            },
            'left_eye': {
                'e': self.left_eye.e_color,
                'T': self.left_eye.T_color,
                'A': self.left_eye.A_color,
                'O': self.left_eye.O_color
            },
            'right_eye': {
                'e': self.right_eye.e_color,
                'T': self.right_eye.T_color,
                'A': self.right_eye.A_color,
                'O': self.right_eye.O_color
            },
            'eTAO': self.results.eTAO,
            'surgery': {
                'lasik': self.surgery.lasik,
                'iso': self.surgery.iso,
                'blepharo': self.surgery.blepharo,
            }
        }

        if report_type == "OCULAR_DRYNESS":
            data['recommendations'] = {
                'light': self.recommendations.light,
                'QMR': self.recommendations.QMR,
                'lipiflow': self.recommendations.lipiflow,
                'lubricant': self.recommendations.lubricant
            }


        return data
