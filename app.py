import streamlit as st

st.header("Transform your texts")
from datetime import datetime as dt
from datetime import timedelta as td


# Transform Texts
font_size = "12px"
p_normal = f"<p style='font-size:{font_size};'>"
p_bold = f"<p style='font-size:{font_size}; font-weight: bold'>"
p_bold_underlined = f"<p style='font-size:{font_size}; font-weight: bold;text-decoration:underline'>"
p_close = "</p>"
INPUT_AREA_HEIGHT = 200


raw = st.text_area("Enter Text to remove spaces:", height = INPUT_AREA_HEIGHT)
if raw:
    st.write(raw)
    processed = raw.replace("Befund:", f"{p_bold_underlined}Befund:{p_close}{p_normal}")
    processed = processed.replace("Beurteilung:", f"{p_bold_underlined}Beurteilung:{p_close}{p_normal}")
    st.markdown(processed, unsafe_allow_html=True)


# Kostaufbau
st.header("Kostaufbau")
select_kostaufbau = st.radio("Select Kostaufbau", ("Kostaufbau 1", "Kostaufbau 2", "Kostaufbau 3"))
d = dt.now()
kostaufbau = "Kostaufbau:<br>"

if select_kostaufbau == "Kostaufbau 1":
    kostaufbau += f"Weiche / Faserarme Kost bis einschließlich {(d+td(days=1)).strftime('%d.%m.%Y')}<br>"
elif select_kostaufbau == "Kostaufbau 2":
    kostaufbau += f"Flüssige / Passierte Kost bis einschließlich {(d+td(days=2)).strftime('%d.%m.%Y')}<br>"
    kostaufbau += f"Weiche / Faserarme Kost bis einschließlich {(d+td(days=4)).strftime('%d.%m.%Y')}<br>"
elif select_kostaufbau == "Kostaufbau 3":
    kostaufbau += f"Flüssige / Passierte Kost bis einschließlich {(d+td(days=3)).strftime('%d.%m.%Y')}<br>"
    kostaufbau += f"Weiche / Faserarme Kost bis einschließlich {(d+td(days=6)).strftime('%d.%m.%Y')}<br>"

kostaufbau += "Dann weiterer vorsichtiger Kostaufbau<br>"

st.markdown(kostaufbau, unsafe_allow_html=True)

