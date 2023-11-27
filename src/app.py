import streamlit as st
from parameters.parameters import Parameters

from dashboard.dashboard import Dashboard
from export.pdf import PDFGenerator
from streamlit.components.v1 import html

def main():

    # Streamit Configs
    st.set_page_config(layout="wide")

    # CSS and JS Files
    css_file = "static/css/streamlit.css"
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Accounts with passwords
    pwd_container = st.sidebar.empty()
    pwd = pwd_container.text_input("Password:", value="")

    if pwd in Parameters.PASSWORDS.keys():
        pwd_container.empty()
    else:
        return

    # Add practitionners !
    practitioner = Parameters.PASSWORDS[pwd]
    st.session_state['practitioner'] = practitioner

    # Dashboard
    dashboard = Dashboard()
    dashboard.display()

    pg = PDFGenerator()
    data = dashboard.get_report_data(practitioner)
    pg.generate(data, save=False)

    js_file = "static/js/streamlit.js"
    with open(js_file) as f:
        html(f'<script>{f.read()}</script>')

if __name__ == '__main__':
    main()

