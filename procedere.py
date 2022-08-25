from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime as dt
from datetime import timedelta as td
import streamlit as st
from utils.formatting import return_bold, return_underlined, return_italic, font_size

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
        _dict = KOSTAUFBAU_DICT[self.category]
        for key, value in _dict.items():
            if key == "Kostaufbau": pass
            if self.start_date == (self.start_date+value): pass
            else: 
                self.texts.append(f"{key}: {(self.start_date + value).strftime('%d.%m.%Y')}")

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
            text = f"Bitte bringen Sie aktuelle (max. 7 Tage, {lab}) mit"
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



class Procedere(BaseModel):
    appointments: List[Appointment] = []
    kostaufbau: Kostaufbau = Kostaufbau(category=0)


    def get_procedere(self):
        stay_title = st.text_input("Termin Grund")
        if st.button("Add appointment"):
            self.appointments.append(Appointment(stay_title = stay_title, number = len(self.appointments)))

        for i, a in enumerate(self.appointments):
            st.markdown(a.inputs(), unsafe_allow_html=True)

        kost_cat = st.radio("Kostaufbau", KOSTAUFBAU_DICT.keys(), key = "kost_cat")
        self.kostaufbau=Kostaufbau(category=kost_cat)
        self.kostaufbau.get_kostaufbau()

    def parse(self):
        procedere = ""
        proc_elements = []
        appointments = []
        kostaufbau = []

        for appointment in self.appointments:
            if isinstance(appointment.date, str):
                date = dt.strptime(appointment.date, "%d.%m.%Y")
            else: date = appointment.date

            text = f"<li>Bitte erscheinen Sie am {date.strftime('%d.%m.%Y')} ({appointment.stay_type}) {appointment.prepare} im {appointment.location}</li>"
            for _ in appointment.comments:
                text += f"<li>{_}</li>"

            text = f"<li>Termin {appointment.number} {appointment.stay_title}:<ul>{text}</ul></li>"
            appointments.append(text)
        
        # procedere_text = return_bold(return_underlined("Procedere:"))+"<br>"
        procedere_text = f"<ul style='font-size:{font_size};'>"
        procedere_text += f"<li style='font-size:{font_size};'>{return_bold('Sofortige Vorstellung in der Notaufnahme bei Auftreten von Fieber, SChüttelfrost, ausgeprägten abdominellen Schmerzen oder Blutungszeichen')}</li>"

        if appointments:
            app_text = f"<ul style='font-size:{font_size};'>"+"".join(appointments)+"</ul>"
            app_text = f"<li style='font-size:{font_size};'><b><u>Wiedervorstellung:</b></u><br>{app_text}</li>"

            procedere_text += app_text

        text = ""
        for k in self.kostaufbau.texts:
            text += f"<li style='font-size:{font_size};'>{k}</li>"

        if text:
            text = return_bold(return_underlined(f"<li style='font-size:{font_size};'>Kostaufbau:"))+"<br>" f"<ul>{text}</ul></li>"
            procedere_text += text
        
        
        procedere_text += "</ul>"
        procedere_text = f"<div style='font-size:{font_size};'>" + procedere_text + "</div>"

        return procedere_text