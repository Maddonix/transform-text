import streamlit as st
st.set_page_config(
    page_title = "Xulutions Clinic Helpers",layout="wide"
)

from datetime import datetime as dt
from datetime import timedelta as td

from letter import letter_app

letter_app()


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

