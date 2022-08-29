from pydantic import BaseModel
from utils.lab_fomatter import RE_TIMESTAMP
import streamlit as st
from typing import Optional, Type, List
import json

class Options(BaseModel):
    units: Optional[dict]
    rm_flags: Optional[list] 
    replace_unit_values: Optional[dict]
    befund_headers: Optional[List]
    befund_subheaders: Optional[List]
    procedere_bausteine: Optional[dict]
    
    re_timestamp: str = RE_TIMESTAMP

    form: Optional[Type[st.form]]

    class Config:
        arbitrary_types_allowed = True

    def load(self, path="utils/lab_options.json"):
        with open(path) as f:
            OPTIONS = json.load(f)

        self.units = OPTIONS["units"]
        self.rm_flags = OPTIONS["rm_flags"]
        self.replace_unit_values = OPTIONS["replace_unit_values"]
        self.befund_headers = OPTIONS["befund_headers"]
        self.befund_subheaders = OPTIONS["befund_subheaders"]
        self.procedere_bausteine = OPTIONS["procedere_bausteine"]

    def save(self):
        with open("utils/lab_options.json", "w") as f:
            d = self.dict(exclude = {"form", "re_timestamp"})
            json.dump(d, f, indent = 4)


    def get_unit_form(self):
        e_units = st.expander("Units")
        with e_units:
            rm_unit_keys = []
            add_units = []
            for key, value in self.units.items():
                _cols = st.columns((3,3,1))
                _rm = _cols[2].checkbox("Löschen", key = f"rm_unit_{key}")
                if _rm:
                    rm_unit_keys.append(key)
                _cols[0].write(key)
                _cols[1].write(value)
                st.markdown("""---""")
            
            _cols = st.columns((3,3,1))
            new_key = _cols[0].text_input("Neuer Wert", key = f"new_lab_key_{len(add_units)}")
            new_value = _cols[1].text_input("Neue Einheit", key = f"new_lab_value_{len(add_units)}")
            
            add = st.button("Hinzufügen", key = "add_unit", on_click = lambda: self.units.update({new_key: new_value}))

            if add:
                self.units[new_key] = new_value


            if st.button("Speichern", key = "save_units"):
                for key, value in add_units:
                    self.units[key] = value
                for key in rm_unit_keys:
                    del self.units[key]
                self.save_lab()

    def get_rm_flags_form(self):
        flags = self.rm_flags
        rm_flags = []
        e = st.expander("Aus Labor Entfernen")
        with e:
            for flag in flags:
                _cols = st.columns((5,1))
                _cols[0].write(flag)
                _rm = _cols[1].checkbox("Löschen", key = f"rm_flag_{flag}")
                st.markdown("""---""")
                if _rm:
                    rm_flags.append(flag)
            
            new_flag = st.text_input("Neuer Wert", key = f"new_flag_{len(flags)}")
            add = st.button("Hinzufügen", key = "add_flag", on_click = lambda: flags.append(new_flag))
        
        if e.button("Speichern", key = "save_rm_flags"):
            for flag in rm_flags:
                flags.remove(flag)
            
            self.save_lab()

    def get_replace_unit_values_form(self):
        replace_unit_values = self.replace_unit_values
        e = st.expander("Einheiten ersetzen")
        with e:
            for key, value in replace_unit_values.items():
                _cols = st.columns((3,3,1))
                _cols[0].write(key)
                _cols[1].write(value)
                _rm = _cols[2].checkbox("Löschen", key = f"rm_replace_unit_value_{key}")
                st.markdown("""---""")
                if _rm:
                    del replace_unit_values[key]
            
            new_key = st.text_input("Neuer Wert", key = f"new_replace_unit_key_{len(replace_unit_values)}")
            new_value = st.text_input("Neue Einheit", key = f"new_replace_unit_value_{len(replace_unit_values)}")
            add = st.button("Hinzufügen", key = "add_replace_unit_value", on_click = lambda: replace_unit_values.update({new_key: new_value}))
        
        if e.button("Speichern", key = "save_replace_unit_values"):
            for key, value in replace_unit_values.items():
                self.replace_unit_values[key] = value
            self.save()

    def get_befund_header_form(self):
        e = st.expander("Befund Header")
        with e:
            for header in self.befund_headers:
                _cols = st.columns((5,1))
                _cols[0].write(header)
                _rm = _cols[1].checkbox("Löschen", key = f"rm_befund_header_{header}")
                st.markdown("""---""")
                if _rm:
                    self.befund_headers.remove(header)
            
            new_header = st.text_input("Neuer Wert", key = f"new_befund_header_{len(self.befund_headers)}")
            add = st.button("Hinzufügen", key = "add_befund_header", on_click = lambda: self.befund_headers.append(new_header))
        
        if e.button("Speichern", key = "save_befund_headers"):
            for header in self.befund_headers:
                self.befund_headers.remove(header)
            self.save()

    def get_befund_subheader_form(self):
        e = st.expander("Befund Subheader")
        with e:
            for subheader in self.befund_subheaders:
                _cols = st.columns((5,1))
                _cols[0].write(subheader)
                _rm = _cols[1].checkbox("Löschen", key = f"rm_befund_subheader_{subheader}")
                st.markdown("""---""")
                if _rm:
                    self.befund_subheaders.remove(subheader)
            
            new_subheader = st.text_input("Neuer Wert", key = f"new_befund_subheader_{len(self.befund_subheaders)}")
            add = st.button("Hinzufügen", key = "add_befund_subheader", on_click = lambda: self.befund_subheaders.append(new_subheader))
        
        if e.button("Speichern", key = "save_befund_subheaders"):
            for subheader in self.befund_subheaders:
                self.befund_subheaders.remove(subheader)
            self.save()

    def get_procedere_bausteine_form(self):
        e = st.expander("Procedere Bausteine")
        with e:
            for key, value in self.procedere_bausteine.items():
                _cols = st.columns((3,3,1))
                _cols[0].write(key)
                _cols[1].write(value)
                _rm = _cols[2].checkbox("Löschen", key = f"rm_procedere_bausteine_{key}")
                st.markdown("""---""")
                if _rm:
                    del self.procedere_bausteine[key]
            
            new_key = st.text_input("Name", key = f"new_procedere_bausteine_key_{len(self.procedere_bausteine)}")
            new_value = st.text_input("Baustein", key = f"new_procedere_bausteine_value_{len(self.procedere_bausteine)}")
            add = st.button("Hinzufügen", key = "add_procedere_bausteine", on_click = lambda: self.procedere_bausteine.update({new_key: new_value}))
                
            if e.button("Speichern", key = "save_procedere_bausteine"):
                for key, value in self.procedere_bausteine.items():
                    self.procedere_bausteine[key] = value
                self.save()

    def get_form(self):
        st.subheader("Options")
        self.get_unit_form()
        self.get_rm_flags_form()
        self.get_befund_header_form()
        self.get_befund_subheader_form()
        self.get_procedere_bausteine_form()

        # self.get_replace_unit_values_form()

        
            
