from pydantic import BaseModel
from typing import Optional, List
from utils.formatting import return_bold, return_underlined, return_italic
import re
from datetime import datetime as dt
# B_TYPE_HEADER = {
#     "Koloskopie": [],
#     "Gastroskopie": [],
# }
from options import Options




class Befund(BaseModel):
    text: Optional[str]
    date: Optional[str]
    markdown_text: Optional[str]
    b_type: Optional[str]
    options: Options

    def parse(self):
        title_line = self.text.split(":")[0]
        date = re.findall("(/d+\./d+\.d+)", title_line)
        text = self.text
        text = text.replace("\n", " ")
        if len(date):
            date=date[0]
            _ = date.split(".")
            date = dt(_[-1], _[-2], [-3])
            
            text.replace(title_line, return_italic(return_underlined(title_line))+"<p>")
        for header in self.options.befund_headers:
            if header in text:
                text = text.replace(header+":", f"<br><br>{header+':'}<br>")
                text = text.replace(header+":", return_bold(header+':'))
                text = text.replace(header+":", return_underlined(header+':'))

        for subheader in self.options.befund_subheaders:
            if subheader in text:
                text = text.replace(subheader+":", f"<br>{subheader+':'}")
                text = text.replace(subheader+":", return_italic(subheader+':'))
                text = text.replace(subheader+":", return_underlined(subheader+':'))

        self.markdown_text = text

        return text