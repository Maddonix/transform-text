from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime as dt
from datetime import timedelta as td
import streamlit as st
from utils.formatting import return_bold, return_underlined, return_italic, font_size, return_list_element, return_list
from options import Options

KOSTAUFBAU_DICT={
    0: {
        # "Kostaufbau": "1",
        "Klare Flüssigkeiten bis einschließlich": td(0),
        "Flüssige / Passierte Kost bis einschließlich": td(days=0),
        "Weiche / Faserarme Kost bis einschließlich": td(days=0),
        "Weiterer vorsichtiger Kostaufbau ab": td(days=0)
    },
    1: {
        # "Kostaufbau": "2",
        "Klare Flüssigkeiten bis einschließlich": td(0),
        "Flüssige / Passierte Kost bis einschließlich": td(days=0),
        "Weiche / Faserarme Kost bis einschließlich": td(days=0),
        "Weiterer vorsichtiger Kostaufbau ab": td(days=1)
    },
    2: {
        # "Kostaufbau": "3",
        "Klare Flüssigkeiten bis einschließlich": td(0),
        "Flüssige / Passierte Kost bis einschließlich": td(days=0),
        "Weiche / Faserarme Kost bis einschließlich": td(days=1),
        "Weiterer vorsichtiger Kostaufbau ab": td(days=2)
    },
    3: {
        # "Kostaufbau": "4",
        "Klare Flüssigkeiten bis einschließlich": td(0),
        "Flüssige / Passierte Kost bis einschließlich": td(days=2),
        "Weiche / Faserarme Kost bis einschließlich": td(days=4),
        "Weiterer vorsichtiger Kostaufbau ab": td(days=5)
    },
    4: {
        # "Kostaufbau": "5",
        "Klare Flüssigkeiten bis einschließlich": td(1),
        "Flüssige / Passierte Kost bis einschließlich": td(days=3),
        "Weiche / Faserarme Kost bis einschließlich": td(days=6),
        "Weiterer vorsichtiger Kostaufbau ab": td(days=7)
    },
}

class Kostaufbau(BaseModel):
    category:int=0
    start_date: dt = dt.now()
    texts: List[str] = []

    def get_kostaufbau(self):
        self.texts = []
        _dict = KOSTAUFBAU_DICT[self.category]
        for key, value in _dict.items():
            if key == "Kostaufbau": pass
            if self.start_date == (self.start_date+value): pass
            else: 
                self.texts.append(f"{key}: {(self.start_date + value).strftime('%d.%m.%Y')}")
                

    def parse(self):
        st.write(self.texts)
        self.get_kostaufbau()
        text = ""
        for _ in self.texts:
            text+=return_list_element(_)
        text = return_list(text)
        text = return_bold("Kostaufbau")+return_list(text)
        return text

class Appointment(BaseModel):
    stay_type: str = "ambulant"
    stay_title: Optional[str]
    number: int
    date: Union[dt, str] = dt.now() + td(14)

    location: Optional[str] = "Zentrum Innere Medizin, Haus A4, Ebene -1, Anmeldung 18"
    location_options: List[str] = [
        "Zentrum Innere Medizin, Haus A4, Ebene -1, Anmeldung 18",
    ]

    prepare: str =""
    prepare_options = ["", "nüchtern", "nüchtern und abgeführt"]

    comments: List[str] = []

    def add_lab(self, lab = "Blutbild, Gerinnung"):
        if st.button("Add Lab", key=f"add_lab_{self.number}"):
            text = f"Bitte bringen Sie aktuelle Laborwerte mit (max. 7 Tage, {lab})"
            self.comments.append(text)

    def add_appointment_prep(self):
        self.prepare = st.radio(
            "Vorbereitung", self.prepare_options, self.prepare_options.index(self.prepare),
            key = f"add_appointment_prep_{self.number}"
        )

    def add_date(self):
        self.date = st.date_input("Datum", self.date, key = f"add_date_{self.number}")

    def add_location(self):
        self.location = st.selectbox(
            "Wo?", self.location_options, self.location_options.index(self.location),
            key = f"add_location_{self.number}")

    def add_comment(self, text):
        new = st.text_input(text, key = f"add_comment_{self.number}_input")
        if st.button("Add comment", key = f"add_comment_{self.number}"):
            self.comments.append(new)

    def drop_last_comment(self):
        if st.button("Drop last comment", key = f"drop_last_comment_{self.number}"):
            if len(self.comments) > 0:
                self.comments.pop()

    def inputs(self):
        st.subheader(f"Termin {self.number}")
        self.add_appointment_prep()
        self.add_date()
        self.add_location()
        self.add_lab()
        self.add_comment("Bemerkungen")
        self.drop_last_comment()

    def parse(self):
        if isinstance(self.date, str):
            date = dt.strptime(self.date, "%d.%m.%Y")
        else: date = self.date

        header = f"Termin ({self.stay_title}):"
        text = f"Bitte erscheinen Sie am {date.strftime('%d.%m.%Y')} ({self.stay_type}) {self.prepare} im {self.location}"
        text = return_list_element(text)
        comments = ""
        for _ in self.comments:
            comments += return_list_element(_)
        # comments = return_list(comments)
        text = return_list(text+comments)

        # text = return_list(text)
        text = header+ text
        
        return text

class Procedere(BaseModel):
    appointments: List[Appointment] = []
    kostaufbau: Kostaufbau = Kostaufbau(category=0)
    

    options: Options
    bausteine: List[str] = []

    def get_procedere(self):
        stay_title = st.text_input("Termin Grund")
        if st.button("Add appointment"):
            self.appointments.append(Appointment(stay_title = stay_title, number = len(self.appointments)))

        for i, a in enumerate(self.appointments):
            st.markdown(a.inputs(), unsafe_allow_html=True)

        kost_cat = st.radio("Kostaufbau", KOSTAUFBAU_DICT.keys(), key = "kost_cat")
        self.kostaufbau=Kostaufbau(category=kost_cat)
        self.kostaufbau.get_kostaufbau()
        
        self.bausteine = st.multiselect("Bausteine", list(self.options.procedere_bausteine.keys()), key = "bausteine")

    def parse(self):
        appointments = self.appointments

        procedere_elements = []
        
        # procedere_text = return_bold(return_underlined("Procedere:"))+"<br>"
        procedere_elements.append(return_bold('Sofortige Vorstellung in der Notaufnahme bei Auftreten von Fieber, Schüttelfrost, ausgeprägten abdominellen Schmerzen oder Blutungszeichen'))
        for a in appointments:
            _a = a.parse()
            procedere_elements.append(_a)

        if self.kostaufbau.category > 0:
            procedere_elements.append(self.kostaufbau.parse())


        for _ in self.bausteine:
            procedere_elements.append(self.options.procedere_bausteine[_])
        procedere_text = ""
        for _ in procedere_elements:
            if not _.startswith("<ul>"):
                procedere_text += return_list_element(_)
            else: procedere_text += _
        procedere_text = return_list(procedere_text)

        return procedere_text