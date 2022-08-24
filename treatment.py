from pydantic import BaseModel
from datetime import datetime as dt
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
                c_text+=f"<li>{_}</li>"

            c_text = "<ul>"+c_text+"</ul>"
            # print(c_text)

            text += c_text

        text = "<li>" + text + "</li>"

        return text