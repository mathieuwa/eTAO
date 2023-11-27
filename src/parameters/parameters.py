import os
import json
import streamlit as st
import numpy as np

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Parameters:

    LANGUAGE = "FR"
    LANGUAGES = {
        "Français": "FR",
        "English": "EN",
        "Español": "ES",

    }

    with open(os.path.join(CURRENT_DIRECTORY, 'translations.json')) as json_file:
        TRANSLATIONS = json.load(json_file)

    @staticmethod
    def set_language(language):
        Parameters.LANGUAGE = Parameters.LANGUAGES[language]

    @classmethod
    def text(cls, part, capitalize=True):
        txt = cls.TRANSLATIONS[part][cls.LANGUAGE]
        if capitalize:
            txt = txt.capitalize()
        return txt

    @classmethod
    def get_intensity_recommendation(cls, intensity):
        return cls.TRANSLATIONS['PDF_DRYNESS_EXPLANATION'][intensity][cls.LANGUAGE]

    @classmethod
    def get_eye_recommendation(cls, letter, color):
        recommendation = cls.TRANSLATIONS['EYE_RECOMMENDATION']
        recommendation = recommendation[letter][color]
        return recommendation[cls.LANGUAGE]

    @classmethod
    def sex_to_naming(cls, sex):
        if cls.LANGUAGE == "FR":
            if sex == "homme":
                return "M."
            else:
                return "Mme"
        elif cls.LANGUAGE == "EN":
            if sex == "man":
                return "Mr."
            else:
                return "Mrs."
        elif cls.LANGUAGE == "ES":
            if sex == "senior":
                return "Sr."
            else:
                return "Sra."

    @classmethod
    def get_dashboard_title(cls, gender, fn, ln, age):
        naming = cls.sex_to_naming(gender)
        if cls.LANGUAGE == "FR":
            title = "eTAO de {} {} {}, {:.0f} "
        elif cls.LANGUAGE == "EN":
            title = "eTAO of {} {} {}, {:.0f} "
        elif cls.LANGUAGE == "ES":
            title = "eTAO de {} {} {}, {:.0f} "
        title += Parameters.text('AGE')
        return title.format(naming, fn, ln, np.floor(age))


    @classmethod
    def get_img_path(cls, name):
        practitioner = st.session_state['practitioner']
        last_name, first_name = practitioner
        return os.path.join(CURRENT_DIRECTORY, '..', '..', f'static/img/{name}_{last_name.capitalize()}_{first_name}.png')

    ETAO_VALUE_CORRESPONDANCE = {
        "e": {
            "🟢": 0.4,
            "🟡": 4,
            "🟠": 7,
            "🔴": 13
        },
        "T": {
            "🟢": 0.4,
            "🟡": 5,
            "🟠": 9,
            "🔴": 14
        },
        "A": {
            "🟢": 0.4,
            "🟡": 5,
            "🟠": 8,
            "🔴": 15
        },
        "O": {
            "🟢": 0.4,
            "🟡": 7,
            "🟠": 11,
            "🔴": 15
        },
    }

    @classmethod
    def get_eTAO_value_correspondance(cls, letter, value):
        return cls.ETAO_VALUE_CORRESPONDANCE[letter][value]

    MAX_HEIGHT = 4

    @classmethod
    def get_eTAO_bar_height(cls, letter, value):
        heights = {"🟢": 1, "🟡": 2, "🟠": 3, "🔴": 4}
        # Remove letter usage
        return heights[value]

    # Line colors
    ETAO_LINE_COLORS = [
        "#069C56",  # Green
        "#ffd60a",  # Yellow
        "#FF980E",  # Orange
        "#D3212C",  # Red
        "#540b0e"  # Dark red
    ]

    ETAO_LINE_THRESHOLDS = [0, 2, 4, 6, 8, 10]

    # Radar plot colors
    RADAR_PLOT_COLORS = [
        "#069C56",  # Green
        "#ffd60a",  # Yellow
        "#FF980E",  # Orange
        "#D3212C",  # Red
    ]


    PASSWORDS = {
        "granium93": ("COLLET", "Benoit"),
        "fermin32": ("FISCH", "Anne Laure"),
        "provost89": ("MARTY", "Anne Sophie "),
        "drupal23": ("SCHOLTES", "Frederic"),
        "frondus88": ("CASSE", "Guillaume"),
        "drusse43": ("CHENAL", "Hervé"),
        "fresin21": ("BLOT", "Julie"),
        "armustre08": ("DEBATZ", "Mathieu"),
        "argotier62": ("CASTELLARIN", "Sylvie"),
        "milper34": ("EL SAMMAK", "Khaled"),
        "alafat90": ("ELMALEH", "Valérie"),
        "dripome21": ("ASSOULINE", "Julia"),
        "astolier32": ("MOUCHEL", "Romain"),
        "merfutal83": ("WEISSROCK", "Marie"),
        "rimotora26": ("PAIRE", "Vincent"),
        "volpetit11": ("CHAMMAS", "Jimmy"),
        "ophtalmo1235789": ("DIGHIERO", "Pablo"),
        "user1": ("Poste", "1"),
        "user2": ("Poste", "2"),
        "user3": ("Poste", "3"),
        "user4": ("Poste", "4"),
    }

    SHORTEN = {
        "e": "eO",
        "T": "TO",
        "A": "AO",
        "O": "OO"
    }

    @classmethod
    def get_shorten(cls, letter, side):
        side = "G" if side == "LEFT" else "D"
        return "[" + cls.SHORTEN[letter] + side + "]"

    PERCENT_GUTTER = 0.02  # % of gutter in bar plot
    NUMBER_OF_GRADUATION = 5
    TICK_SIZE = 0.1

    BARPLOT_CORRESPONDANCE = {
        "e": "eO",
        "T": "TO",
        "A": "AO",
        "O": "OO"
    }

    ## Display order
    DEFAULT_ORDER = ["e", "T", "A", "O"]
    BUTTON_ORDER = DEFAULT_ORDER