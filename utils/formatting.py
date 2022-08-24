REPORT_HEADERS = [
    "Histologie:",
    "Befund:",
    "Beurteilung:",
    "Beurteilung vorläufig:",
    "Beurteilung endgültig:",
]

font_size = "12px"
p_normal = f"<p style='font-size:{font_size};' align='justify'>"
p_bold = f"<p style='font-size:{font_size}; font-weight: bold' align='justify'>"
p_bold_underlined = f"<p style='font-size:{font_size}; font-weight: bold;text-decoration:underline'>"
p_close = "</p>"

def return_bold(text):
    return f"<b>{text}</b>"

def return_italic(text):
    return f"<i>{text}</i>"

def return_underlined(text):
    return f"<u>{text}</u>"

def set_font_size(text, size):
    return f"<font size={size}px>{text}</font>"


def header(text):
    return f"{return_bold(return_underlined(text))}:<br>"

def paragraph(title, text):
    return f"{header(title)}{text}<br><br>"