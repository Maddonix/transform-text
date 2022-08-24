from pydantic import BaseModel
from typing import Optional, List
from utils.formatting import return_bold, return_underlined, return_italic

# B_TYPE_HEADER = {
#     "Koloskopie": [],
#     "Gastroskopie": [],
# }

HEADERS = [
    "Histologie",
    "Befund",
    "Beurteilung",
    "Beurteilung vorläufig",
    "Beurteilung endgültig",
    "Empfehlung"
]

SUBHEADERS = [
    "Indikation",
    "Prämedikation",
    "Colon",
    "Kolon",
    "Magen",
    "Ösophagus",
    "Duodenum",
    "Komplikation"
]



class Befund(BaseModel):
    text: Optional[str]
    date: Optional[str]
    markdown_text: Optional[str]
    b_type: Optional[str]

    def parse(self):
        text = self.text
        text = text.replace("\n", " ")
        for header in HEADERS:
            if header in text:
                text = text.replace(header+":", f"<br><br>{header+':'}<br>")
                text = text.replace(header+":", return_bold(header+':'))
                text = text.replace(header+":", return_underlined(header+':'))

        for subheader in SUBHEADERS:
            if subheader in text:
                text = text.replace(subheader+":", f"<br>{subheader+':'}")
                text = text.replace(subheader+":", return_italic(subheader+':'))
                text = text.replace(subheader+":", return_underlined(subheader+':'))

        self.markdown_text = text

        return text