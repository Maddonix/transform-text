from utils.formatting import font_size

def generate_epikrise(male:bool, az:str):
    if male:
        epikrise = f"""
            Die elektive stationäre Aufnahme des Patienten erfolgt zur [#Eingriff#] bei [#Indikation#].
            Bei Aufnahme besteht ein [#AZ#] Allgemeinzustand.<p style='font-size:{font_size}';>
            Es bestehen keine Fragen zum geplanten Procedere.  
            Nach zeitgerecht erfolgter Aufklärung sowie Ausschluss von Kontraindikationen
            konnte der oben genannte Eingriff [#primär komplikationslos#] durchgeführt werden.
            Hier zeigte sich [#BEFUND#]. [#Leichte postinterventionell aufgetretene Schmerzen konnten
            analgetisch therapiert werden#]. Postinterventionell präsentierte sich der Patient
            zu jedem Zeitpunkt kardiorespiratorisch stabil. [#Weder klinisch noch laborchemisch
            ergab sich der Hinweis auf eine signifikante Nachblutung oder Infektsituation.#]<br>
            [#Unsere weiteren Handlungsempfehlungen und Hinweise sind unter dem Punkt 
            Procedere zusammengefasst. #]<p style='font-size:{font_size}';>
            Wir entlassen den Patienten in gutem internistischen Allgemeinzustand in 
            Ihre geschätzte ambulante Weiterversorgung.
        """
    else:
        epikrise = f"""
            Die elektive stationäre Aufnahme der Patientin erfolgt zur [#Eingriff#] bei [#Indikation#].
            Bei Aufnahme besteht ein [#AZ#] Allgemeinzustand.
            Es bestehen keine Fragen zum geplanten Procedere.<p style='font-size:{font_size}';>
            Nach zeitgerecht erfolgter Aufklärung sowie Ausschluss von Kontraindikationen
            konnte der oben genannte Eingriff [#primär komplikationslos#] durchgeführt werden.
            Hier zeigte sich [#BEFUND#]. [#Leichte postinterventionell aufgetretene Schmerzen konnten
            analgetisch therapiert werden#]. Postinterventionell präsentierte sich die Patientin
            zu jedem Zeitpunkt kardiorespiratorisch stabil. [#Weder klinisch noch laborchemisch
            ergab sich der Hinweis auf eine signifikante Nachblutung oder Infektsituation.#]<br>
            [#Unsere weiteren Handlungsempfehlungen und Hinweise sind unter dem Punkt 
            Procedere zusammengefasst. #]<p style='font-size:{font_size}';>
            Wir entlassen die Patientin in gutem internistischen Allgemeinzustand in 
            Ihre geschätzte ambulante Weiterversorgung.
        """

    epikrise = epikrise.replace("[#AZ#]", az)

    return epikrise