from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime as dt
from utils.lab_fomatter import get_timestamps, read_text_lab_value
import pandas as pd



REMOVE_LAB_FLAGS = [
    "Akutbestimmungen / TDM / Drogen:",
    "Hämatologie:",
    "Klinische Chemie:",
    "Gerinnung:",
]
RE_TIMESTAMP = r"(\(\d{2}\.\d{2}.\d{4} \d{2}:\d{2}:\d{2}\))"

LOOKUP_UNITS = {
    'Alk. Phosphatase': 'U/l',
    'C-reaktives Protein': 'mg/dl',
    'Calcium': 'mmol/l',
    'Creatinin': 'mg/dl',
    'Erythrozyten': 'n*10E6/µl',
    'GGT': 'U/l',
    'GOT (ASAT)': 'U/l',
    'GPT (ALAT)': 'U/l',
    'Gesamt-Bilirubin': 'mg/dl',
    'Harnstoff': 'mg/dl',
    'Hämatokrit': '%',
    'Hämoglobin': 'g/dl',
    'Kalium': 'mmol/l',
    'Lactat Dehydrogenase': 'U/l',
    'Leukozyten': 'n*1000/µl',
    'Lipase': 'U/l',
    'MCH (HbE)': 'pg',
    'MCHC': 'g/dl',
    'MCV': 'fl',
    'Mittleres Plättchenvolumen': 'fl',
    'Natrium': 'mmol/l',
    'PTT': 's',
    'Ratio int. norm.': '',
    'Thromboplastinzeit n. Quick': '%',
    'Thrombozyten': 'n*1000/µl',
    'anorg. Phosphat': 'mmol/l',
    'glomerul. Filtrationsr. (MDRD)': 'ml/min /1,73qm',
    'glomerul. Filtrationsr. CKD-EP': 'ml/min /1,73qm'
}

LOOKUP_REPLACES = {
    "C-reaktives Protein": [(">", ""), ("<", ""), (" ", "")],
}

class LaborText(BaseModel):
    raw_text: str
    formatted_text: Optional[str]
    text_snippets: Optional[List[str]]
    lab_dicts: Optional[List[dict]]
    timestamps: Optional[List[dt]]


    PLACEHOLDER_DATE: str = "__XX__XX__XX__"
    TEXT_TIMESTAMP_FORMAT: str = "(%d.%m.%Y %H:%M:%S)"

    def remove_lab_flags(self):
        self.get_timestamps()
        text = self.raw_text
        for flag in REMOVE_LAB_FLAGS:
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
                    _new.append(read_text_lab_value(_))
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


        self.df = df.merge(ref_df, left_index=True, right_index=True)
