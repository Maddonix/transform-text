from pydantic import BaseModel

from utils.formatting import return_bold, return_italic, return_underlined


letter_content = {
    "Diagnosen": "Diagnosen einfügen",
    "Medikamente": "Medikamente einfügen",
    "Epikrise": "Epikrise einfügen",
    "Procedere": "Procedere einfügen",
    "Befunde": "Befunde einfügen",
    "Labor": "Labor einfügen"
}

# letter_template = "".join([paragraph(key, value) for key, value in letter_content.items()])

# letter_template = f"""\
#     {header("Diagnosen")}
#     INSERT DIAGNOSES<br>
#     {header("Medikamente")}
#     """