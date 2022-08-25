from pydantic import BaseModel
from datetime import datetime as dt
from utils.formatting import font_size
from typing import Optional, List

class Treatment(BaseModel):
    text: str
    date: Optional[dt]
    complications: Optional[List[str]]

    def parse_html(self):
        # print(self)
        text = ""
        if self.date:
            text += self.date.strftime("%m/%Y: ")
        text += self.text

        if self.complications:
            # print(self.complications)
            c_text = ""
            for _ in self.complications:
                c_text+=f"<li style='font-size:{font_size}'>{_}</li>"

            c_text = f"<ul style='font-size:{font_size}'>"+c_text+"</ul>"
            # print(c_text)

            text += c_text

        text = f"<li style='font-size:{font_size}'>" + text + "</li>"

        return text