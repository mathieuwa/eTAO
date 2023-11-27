import base64
import streamlit as st

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

def export_as_pdf(collection):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)


    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
    	plt.savefig(tmpfile.name, format="png")

    pdf.cell(40, 10, collection["eTAO"])
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

    st.markdown(html, unsafe_allow_html=True)