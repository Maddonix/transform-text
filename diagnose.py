from pydantic import BaseModel
from datetime import datetime as dt
from typing import Optional, List
from treatment import Treatment
import re
from utils.formatting import return_underlined, return_bold, return_italic, font_size
import streamlit as st

FLAG_DIAGNOSE_DATE = [
    "ED",
    "PD",
    "Erstdiagnose",
    "Primärdiagnose"
]

DATE_FORMATS = [
    "%m.%Y",
    "%m.%y",
    "%m/%Y",
    "%m/%y",
    "%d.%m.%Y"
]

RE_DATE_FORMATS = [

]



def get_diagnose_date(text):
    for flag in FLAG_DIAGNOSE_DATE:
        if flag in text:
            text.replace(flag, "X_X_X_X_X")

    if "X_X_X_X_X" in text:
        return dt.strptime(text.split("X_X_X_X_X")[0], "%d.%m.%Y")
    return None

def parse_verlauf(text):
    snippets = text.split("!")
    new = {"text": None, "date": None, "complications": []}
    pattern = "datum (.*)|komplikation (.*)|text (.*)"

    for snippet in snippets:
        r = re.findall(pattern, snippet, re.IGNORECASE)
        for _ in r:
            if _[2]: new["text"] = _[2]
            if _[0]:
                _date = _[0]
                for pattern in DATE_FORMATS:
                    try:
                        _date = dt.strptime(_date, pattern)
                        new["date"] = _date
                    except:
                        pass
            if _[1]: new["complications"].append(_[1])

    return new

def split_snippet(snippet, pattern):
    return re.findall(pattern, snippet, re.IGNORECASE)

class DiagnosenText(BaseModel):
    text: str
    snippets: List[str] = []

    snippet_pattern: str = "text (?P<text>[^;]*);|typ (?P<typ>haupt);|verlauf(?P<verlauf>[^;]*);"
    snippet_order: List[str] = ["text", "typ", "verlauf"]

    def text_to_snippets(self):
        self.snippets = self.text.replace("diagnose", "Diagnose").split("Diagnose")
        self.snippets = [_ for _ in self.snippets if _.strip()]

    def snippets_to_jsons(self):
        snippets = self.snippets
        jsons = []

        for snippet in snippets:
            r = split_snippet(snippet, self.snippet_pattern)
            new = {"text": None, "primary": False, "verlauf": []}
            for match_tuple in r:
                if match_tuple[0]: new["text"] = match_tuple[0].strip()
                if match_tuple[1]: new["primary"] = True
                if match_tuple[2]:
                    _v = match_tuple[2].strip()
                    _v = parse_verlauf(_v)
                    # _v = Treatment(**_v)
                    if _v["text"]: new["verlauf"].append(_v)
                    
            jsons.append(new)

        return jsons

    def get_diagnose_list(self):
        self.text_to_snippets()
        jsons = self.snippets_to_jsons()
        _list = []
        for _ in jsons:
            _list.append(Diagnose(**_))
        return _list

class Diagnose(BaseModel):
    text: Optional[str]
    diagnose_date: Optional[dt]
    primary: bool = False
    icd: Optional[str]
    icd_text: Optional[str]
    verlauf: List[Treatment] = []

    def parse_html(self):

        text = self.text
        if self.diagnose_date:
            text += f" [{self.diagnose_date.strftime('%m/%Y: ')}]"
        
        verlauf = ""
        for _ in self.verlauf:
            verlauf+= _.parse_html()
            # print(verlauf)
        
        verlauf = f"<ul style='font-size:{font_size}'>"+verlauf+"</ul>"
        text+=verlauf
        text = f"<li style='font-size:{font_size}'>"+text+"</li>"

        return text
        
