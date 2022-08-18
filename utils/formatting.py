REPORT_HEADERS = [
    "Histologie:",
    "Beurteilung:",
    "Beurteilung vorläufig:",
    "Beurteilung endgültig:",
]

font_size = "12px"
p_normal = f"<p style='font-size:{font_size};' align='justify'>"
p_bold = f"<p style='font-size:{font_size}; font-weight: bold' align='justify'>"
p_bold_underlined = f"<p style='font-size:{font_size}; font-weight: bold;text-decoration:underline' align='justify'>"
p_close = "</p>"

def format_header(text, header_list = REPORT_HEADERS):
    for header in header_list:
        text = text.replace(header, f"{p_bold_underlined}{header}{p_close}{p_normal}")
    return text