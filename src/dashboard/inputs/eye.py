import streamlit as st

from parameters.parameters import Parameters

class Eye():

    def __init__(self, side):
        self.side = side
        self.color_selected = {}

    def value(self, letter):
        return Parameters.get_eTAO_value_correspondance(letter, self.color_selected[letter])

    @property
    def e_color(self):
        return self.color_selected["e"]

    @property
    def T_color(self):
        return self.color_selected["T"]

    @property
    def A_color(self):
        return self.color_selected["A"]

    @property
    def O_color(self):
        return self.color_selected["O"]

    @property
    def e_value(self):
        return Parameters.get_eTAO_value_correspondance("e", self.color_selected["e"])

    @property
    def T_value(self):
        return Parameters.get_eTAO_value_correspondance("T", self.color_selected["T"])

    @property
    def A_value(self):
        return Parameters.get_eTAO_value_correspondance("A", self.color_selected["A"])

    @property
    def O_value(self):
        return Parameters.get_eTAO_value_correspondance("O", self.color_selected["O"])

    def get_bar_height(self, letter):
        value = self.color_selected[letter]
        return Parameters.get_eTAO_bar_height(letter, value)

    @staticmethod
    def get_eye_header(side):
        header = Parameters.text(f"{side.upper()}_EYE")
        header = Parameters.text("EYE_HEADER").format(header)
        return header


    def display_sidebar(self):
        st.header(self.get_eye_header(self.side))

        format_func = lambda x: ""

        for letter, options in [
            ("e", ["🟢", "🟡", "🟠", "🔴"]),
            ("T", ["🟢", "🟡", "🟠", "🔴"]),
            ("A", ["🟢", "🟡", "🟠", "🔴"]),
            ("O", ["🟢", "🟡", "🟠", "🔴"]),
        ]:

            full_name = Parameters.TRANSLATIONS['EYE_SIDEBAR_NAMING'][letter][Parameters.LANGUAGE]  # TODO - Change to function
            short = Parameters.get_shorten(letter, self.side)
            help_text = Parameters.TRANSLATIONS['EYE_SIDEBAR_EXPLANATION'][letter][Parameters.LANGUAGE]  # TODO - Change to function
            self.color_selected[letter] = st.radio(
                short + " " + full_name,
                options=options,
                key=self.side + "_"+full_name,
                help=help_text,
                horizontal=True,
                format_func=format_func
            )

    def display_recommendations(self):

        for letter in Parameters.BUTTON_ORDER:
            color = self.color_selected[letter]
            short = Parameters.get_shorten(letter, self.side)
            recommendation = Parameters.get_eye_recommendation(letter, color)

            st.write("{} {} {}".format(color, short, recommendation))
