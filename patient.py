from pydantic import BaseModel
from typing import List
import streamlit as st
from diagnose import Diagnose
import pandas as pd
from befund import Befund
from procedere import Procedere
from labor import PatientLab
from typing import Optional
from utils.formatting import header, paragraph, font_size
from epikrise import generate_epikrise

class Patient(BaseModel):
    age: int = 60           # General attributes

    male: bool = False      # General attributes

    az: str = "guter"         # General attributes
    az_options = ["guter", "adäquater", "reduzierter"]

    cvrf: List[str] = []    # General attributes
    cvrf_options = ["Rauchen", "art. Hypertonie", "Adipositas", "Z.n. MI", "Z.n. Apoplex"]

    diagnoses: List[Diagnose] = []
    lab: Optional[PatientLab]

    befunde: List[Befund] = []

    procedere: Procedere = Procedere()


    def get_general_attributes(self):
        self.age = st.number_input("Alter", value=self.age)

        if self.male: _g_select = 0
        else: _g_select = 1
        gender = st.radio("Geschlecht", ("Männlich", "Weiblich"), _g_select)
        if gender == "Männlich":
            self.male = True
        else:
            self.male = False

        _az_index = self.az_options.index(self.az)
        self.az = st.radio("Allgemeinzustand", self.az_options, _az_index)
        self.cvrf = st.multiselect("CVRF", self.cvrf_options, self.cvrf)

    def diagnoses_df(self):
        records = [_.dict() for _ in self.diagnoses]
        df = pd.DataFrame.from_records(records)
        return df

    def get_befunde(self):
        befunde = []        
        if st.button("Befund hinzufügen"):
            self.befunde.append(Befund(text=""))

        for i, b in enumerate(self.befunde):
            befunde.append(st.text_area(f"Befund {i}", value=b.text))

        self.befunde = [Befund(text=_) for _ in befunde]

        return self.befunde

    def get_procedere(self):
        return self.procedere.get_procedere()


    def generate_letter(self):
        content = {
            "Diagnosen": "Diagnosen einfügen",
            "Medikamente": "Medikamente einfügen",
            "Epikrise": "Epikrise einfügen",
            "Procedere": "Procedere einfügen",
            "Befunde": "Befunde einfügen",
            "Labor": "Labor einfügen"
        }


        # Diagnosen
        _ = [_.parse_html() for _ in self.diagnoses]
        # _ = "<ul>"+"".join(_)+"</ul>" #f"<div style='font-size:{font_size}px;><ul>"+"".join(_)+"</ul></div>"
        _ = f"<ul style='font-size:{font_size}'>"+"".join(_)+"</ul>"
        content["Diagnosen"] = _

        # Epikrise
        content["Epikrise"] = generate_epikrise(self.male, self.az)

        # Procedere
        content["Procedere"] = self.procedere.parse()

        # Befunde
        [_.parse() for _ in self.befunde]
        content["Befunde"] = "<\n>".join([_.markdown_text for _ in self.befunde])

        # Labor
        self.lab.get_df()
        content["Labor"] = self.lab.df.to_markdown()

        letter = "".join([paragraph(key, value) for key, value in content.items() if key !="Labor"])
        # letter+= "<br><br>"+content["Labor"]
        return letter




