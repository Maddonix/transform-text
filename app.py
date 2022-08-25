from re import T
import streamlit as st
st.set_page_config(
    page_title = "Xulutions Clinic Helpers",layout="wide"
)

from diagnose import DiagnosenText
from patient import Patient
from labor import LaborText, PatientLab
from utils.formatting import header, font_size

st.markdown("""
<style>
table {
  font-size: 13px;
}
</style>
""", unsafe_allow_html=True
)

TEST_LAB_TEXT = """
(18.08.2022 12:29:00)

Hämatologie: Leukozyten: 5.2 [4.37 - 9.68] n*1000/µl; Erythrozyten: 4.01 [3.92 - 5.08] n*10E6/µl; Hämoglobin: 11.6 [12.0 - 14.6] g/dl; Hämatokrit: 33.9 [36.6 - 44.0] %; MCV: 84.5 [77.70 - 93.70] fl; MCH (HbE): 28.9 [25.30 - 30.90] pg; MCHC: 34.2 [31.00 - 34.10] g/dl; Thrombozyten: 256 [186 - 353] n*1000/µl; Mittleres Plättchenvolumen: 9.5 [9.6 - 12.0] fl;

(18.08.2022 09:28:00)

Klinische Chemie: Natrium: 144 [135 - 145] mmol/l; Kalium: 4.3 [3.5 - 5.1] mmol/l; Calcium: 2.5 [2.0 - 2.7] mmol/l; anorg. Phosphat: 1.26 [0.87 - 1.45] mmol/l; glomerul. Filtrationsr. CKD-EP: 102 ml/min /1,73qm; glomerul. Filtrationsr. (MDRD): 92 ml/min /1,73qm; Creatinin: 0.80 [0 - 0.95] mg/dl; Harnstoff: 23.0 [10 - 50] mg/dl; Gesamt-Bilirubin: 0.2 [0.1 - 1.2] mg/dl; GOT (ASAT): 24.3 [10 - 35] U/l; GPT (ALAT): 20.5 [10 - 35] U/l; GGT: 12.0 [<= 40] U/l; Alk. Phosphatase: 90 [35 - 105] U/l; Lactat Dehydrogenase: 211 [<= 250] U/l; Lipase: 12 [13 - 60] U/l;

Gerinnung: Thromboplastinzeit n. Quick: 87 [80 - 126] %; Ratio int. norm.: 1.06 [0.85 - 1.18] ; PTT: 18.0 [21 - 31] s;

Hämatologie: Leukozyten: 5.7 [4.37 - 9.68] n*1000/µl; Erythrozyten: 4.74 [3.92 - 5.08] n*10E6/µl; Hämoglobin: 13.8 [12.0 - 14.6] g/dl; Hämatokrit: 40.1 [36.6 - 44.0] %; MCV: 84.6 [77.70 - 93.70] fl; MCH (HbE): 29.1 [25.30 - 30.90] pg; MCHC: 34.4 [31.00 - 34.10] g/dl; Thrombozyten: 301 [186 - 353] n*1000/µl; Mittleres Plättchenvolumen: 10.0 [9.6 - 12.0] fl;

Akutbestimmungen / TDM / Drogen: C-reaktives Protein: < 0.10 [0 - 0.5] mg/dl;

 
"""

TEST_DIAGNOSEN_TEXT = """
diagnose text Kolonpolypen; typ haupt; 
therapie text fraktionierte schlingenresektion! datum 21.03.1234!; 
therapie text clip applikation! diagnose text arterielle hypertonie; 
diagnose text Coxarthrose beidseits; therapie 2004 Hüft TEP li; 
therapie text hüft tep re! komplikation Peroneusparese;"""

cols = st.columns(3)

with cols[0]:
    e_general = st.expander("Allgemein", expanded=True)
    e_diagnosen = st.expander("Diagnosen", expanded=True)
    e_befunde = st.expander("Befunde", expanded=True)
with cols[1]:
    e_laborwerte = st.expander("Laborwerte", expanded=True)
    e_epicrisis = st.expander("Epicrisis", expanded=True)
    e_procedere = st.expander("Procedere", expanded=True)

if not "patient" in st.session_state:
    st.session_state.patient = Patient()
patient = st.session_state.patient

with e_general:
    patient.get_general_attributes()

with e_diagnosen:
    d_text_input = st.text_area("Diagnosen", TEST_DIAGNOSEN_TEXT, height = 200)
    diagnose_text = DiagnosenText(text=d_text_input)
    patient.diagnoses = diagnose_text.get_diagnose_list()
    d_html = [_.parse_html() for _ in patient.diagnoses]
    d_html = "<ul>"+"".join(d_html)+"</ul>"

with e_befunde:
    patient.get_befunde()

with e_laborwerte:
    lab_in = st.text_area("Laborwerte (Freitext)", TEST_LAB_TEXT, height=200)
    lab_text = LaborText(raw_text = lab_in)
    measurements = lab_text.export_patient_lab()
    patient.lab = PatientLab(measurements=measurements)
    patient.lab.get_df()



with e_procedere:
    patient.get_procedere()
    text = patient.procedere.parse()
    
letter = patient.generate_letter()
st.markdown(letter, unsafe_allow_html=True)
st.markdown(header(f"<div style='font-size:{font_size};'>Labor"+ "</div>"), unsafe_allow_html=True) 
st.table(patient.lab.df.style.format({"font-size": 12}, precision=2, na_rep="-"))
# st.markdown(letter, unsafe_allow_html=True)

