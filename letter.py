from utils.formatting import format_header
from utils.lab_fomatter import *
import pandas as pd
import streamlit as st

def letter_app():
    st.header("Arztbrief Helfer")
    st.subheader("Befunde Formatieren")
    b_cols = st.columns(2)
    b_in = b_cols[0].text_area("Befund:", height = 200)
    b_out = format_header(b_in)
    b_cols[1].markdown(b_out, unsafe_allow_html=True)


    st.subheader("Laborwerte Formatieren")
    lab_dicts = []
    l_cols = st.columns(2)
    l_in = l_cols[0].text_area("Laborwerte:", height = 200)
    for flag in REMOVE_LAB_FLAGS:
        l_in = l_in.replace(flag, "")
    
    timestamps = get_timestamps(l_in)
    for timestamp in timestamps:
        l_in = l_in.replace(timestamp, "__XX__XX__XX__")

    _text_split = l_in.split("__XX__XX__XX__")
    _text_split = [_.strip() for _ in _text_split if _ ]
    labs = {dt.strptime(timestamps[i], "(%d.%m.%Y %H:%M:%S)"): _ for i, _ in enumerate(_text_split)}

    for key, value in labs.items():
        lab_values = value.split(";")
        lab_values = [_.strip() for _ in lab_values if _]
        _new = []
        for _ in lab_values:
            _new.append(read_text_lab_value(_))
            _new[-1].update({"timestamp": key})

        lab_dicts.extend(_new)

    df = pd.DataFrame.from_dict(lab_dicts)
    st.write(df)
    refs = {}
    for _type in df["type"].unique():
        lower = df.loc[df["type"] == _type, "ref_lower"].min()
        upper = df.loc[df["type"] == _type, "ref_upper"].max()
        unit = df.loc[df["type"] == _type, "unit"].unique()[0]
        refs[_type] = {"lower": lower, "upper": upper, "unit": unit}

    df = pd.pivot(df, index="type", columns=["timestamp"], values="value")
    ref_df = pd.DataFrame.from_dict(refs, orient="index")


    df = df.merge(ref_df, left_index=True, right_index=True)
    l_cols[1] = st.table(df)

