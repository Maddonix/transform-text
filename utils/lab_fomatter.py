import re
from datetime import datetime as dt

import json





RE_TIMESTAMP = r"(\(\d{2}\.\d{2}.\d{4} \d{2}:\d{2}:\d{2}\))"

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

def read_text_lab_value(value, units):
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
    if l_type in units:
        result["unit"] = units[l_type]
    else:
        result["unit"] = "NOT DEFINED YET"
    
    _ref_str = value.split(":")[1]

    result.update(get_ref_range(_ref_str))
    v_in = value.replace("<", "").replace(">","")
    v = re.findall(r"(:\s*\d*\.*\d*\s*)", v_in)[0].replace(": ", "").replace("[", "").strip()
    result["value"] = float(v)

    return result