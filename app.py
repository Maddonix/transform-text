import streamlit as st

st.title("Transform your texts")

font_size = "12px"
p_normal = f"<p style='font-size:{font_size};'>"
p_bold = f"<p style='font-size:{font_size}; font-weight: bold'>"
p_bold_underlined = f"<p style='font-size:{font_size}; font-weight: bold;text-decoration:underline'>"
INPUT_AREA_HEIGHT = 200


raw = st.text_area("Enter Text to remove spaces:", height = INPUT_AREA_HEIGHT)
if raw:
    st.write(raw)