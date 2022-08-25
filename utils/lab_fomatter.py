import re
from datetime import datetime as dt

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
    "Magnesium": "mmol/l",
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

def get_timestamps(text, re_timestamp = RE_TIMESTAMP):
    return re.findall(re_timestamp, text)

def split_lab_text_by_date(text, re_timestamp = RE_TIMESTAMP):
    timestamps = get_timestamps(text, re_timestamp)
    return {timestamp: text.split(timestamp)[1] for timestamp in timestamps}

def get_ref_range(value):
    result = {
        "ref_lower": None,
        "ref_upper": None,
        "info": None
    }

    if "<=" in value:
        value = value.replace("<=", "0 -")
    if "<" in value:
        value = value.replace("<=", "0 -")

    if not "-" in value:
        result["info"] = value
        return result

    ref = re.findall(r"(\[.+\])", value)[0].replace("[", "").replace("]", "").strip()
    ref = ref.split("-")
    result["ref_lower"] = float(ref[0])
    result["ref_upper"] = float(ref[1])

    return result

def read_text_lab_value(value):
    result = {
        "type": None,
        "value": None,
        "unit": None,
        "ref_lower": None,
        "ref_upper": None,
        "info": None
    }

    l_type = value.split(":")[0]
    result["type"] = l_type
    if l_type in LOOKUP_UNITS:
        result["unit"] = LOOKUP_UNITS[l_type]
    else:
        result["unit"] = "NOT DEFINED YET"
    #     result["info"] = value
        
        # return result

    

    
    
    _ref_str = value.split(":")[1]

    result.update(get_ref_range(_ref_str))
    v_in = value.replace("<", "").replace(">","")
    v = re.findall(r"(:\s*\d*\.*\d*\s*)", value)[0].replace(": ", "").replace("[", "").strip()
    result["value"] = float(v)

    return result