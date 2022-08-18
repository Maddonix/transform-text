from utils.formatting import format_header

import streamlit as st

def letter_app():
    st.header("Arztbrief Helfer")
    st.subheader("Befunde Formatieren")
    b_cols = st.columns(2)
    b_in = b_cols[0].text_area("Befund:", height = 200)
    b_out = format_header(b_in)
    b_cols[1].markdown(b_out, unsafe_allow_html=True)