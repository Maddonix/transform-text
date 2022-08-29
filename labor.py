from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime as dt
from utils.lab_fomatter import get_timestamps, read_text_lab_value
import pandas as pd
from options import Options


RE_TIMESTAMP = r"(\(\d{2}\.\d{2}.\d{4} \d{2}:\d{2}:\d{2}\))"

class LaborText(BaseModel):
    raw_text: str
    formatted_text: Optional[str]
    text_snippets: Optional[List[str]]
    lab_dicts: Optional[List[dict]]
    timestamps: Optional[List[dt]]


    options: Options
    PLACEHOLDER_DATE: str = "__XX__XX__XX__"
    TEXT_TIMESTAMP_FORMAT: str = "(%d.%m.%Y %H:%M:%S)"

    class Config:
        arbitrary_types_allowed = True


    def remove_lab_flags(self):
        self.get_timestamps()
        text = self.raw_text
        for flag in self.options.rm_flags:
            text = text.replace(flag, "")

        for timestamp in self.timestamps:
            text = text.replace(timestamp, self.PLACEHOLDER_DATE)

        self.formatted_text = text

    def get_timestamps(self):
        self.timestamps = get_timestamps(self.raw_text)

    def split_text(self):
        text = self.formatted_text
        _text_split = text.split(self.PLACEHOLDER_DATE)
        _text_split = [_.strip() for _ in _text_split if _.strip()]
        self.text_snippets = _text_split
    
    def get_lab_dicts(self):
        lab_dicts = []
        labs = {
            dt.strptime(
                self.timestamps[i],
                "(%d.%m.%Y %H:%M:%S)"
            ): _ for i, _ in enumerate(self.text_snippets)}

        for key, value in labs.items():
            lab_values = value.split(";")
            lab_values = [_.strip() for _ in lab_values if _]
            _new = []
            for _ in lab_values:
                try:
                    _new.append(read_text_lab_value(_, self.options.units))
                    _new[-1].update({"timestamp": key})
                except:
                    print(f"ERROR FOR STRING: {_}")

            lab_dicts.extend(_new)

        self.lab_dicts = lab_dicts

    def export_patient_lab(self):
        self.remove_lab_flags()
        self.split_text()
        self.get_lab_dicts()

        measurements = [Measurement(**_) for _ in self.lab_dicts]
        return measurements
    
import streamlit as st
class Measurement(BaseModel):
    type: str
    value: float
    unit: Optional[str]
    ref_lower: Optional[float]
    ref_upper: Optional[float]
    timestamp: dt
    info: Optional[str]


class PatientLab(BaseModel):
    measurements: List[Measurement]
    df: Optional[pd.DataFrame]

    class Config:
        arbitrary_types_allowed = True

    def get_df(self):
        refs = {}
        dicts = [_.dict() for _ in self.measurements]
        df = pd.DataFrame.from_dict(dicts)
        for _type in df["type"].unique():
            lower = df.loc[df["type"] == _type, "ref_lower"].min()
            upper = df.loc[df["type"] == _type, "ref_upper"].max()
            unit = df.loc[df["type"] == _type, "unit"].unique()[0]
            refs[_type] = {"lower": lower, "upper": upper, "unit": unit}

        df = pd.pivot(df, index="type", columns=["timestamp"], values="value")
        df = df.round(2)
        ref_df = pd.DataFrame.from_dict(refs, orient="index")


        df = df.merge(ref_df, left_index=True, right_index=True)

        new_colnames = []
        for col in df.columns:
            if isinstance(col, dt):
                col = col.strftime("%d.%m.%y %H:%M")
            new_colnames.append(col)

        df.columns = new_colnames

        self.df = df