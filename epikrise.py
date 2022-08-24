def generate_epikrise(male:bool, az:str):
    if male:
        epikrise = """
            Die elektive stationäre Aufnahme des Patienten erfolgt zur [#Eingriff#] bei [#Indikation#].
            Bei Aufnahme besteht ein [#AZ#] Allgemeinzustand.
            Es bestehen keine Fragen zum geplanten Procedere.<br><br>
            Nach zeitgerecht erfolgter Aufklärung sowie Ausschluss von Kontraindikationen
            konnte der oben genannte Eingriff [#primär komplikationslos#] durchgeführt werden.
            Hier zeigte sich [#BEFUND#]. [#Leichte postinterventionell aufgetretene Schmerzen konnten
            analgetisch therapiert werden#]. Postinterventionell präsentierte sich der Patient
            zu jedem Zeitpunkt kardiorespiratorisch stabil. [#Weder klinisch noch laborchemisch
            ergab sich der Hinweis auf eine signifikante Nachblutung oder Infektsituation.#]<br>
            [#Unsere weiteren Handlungsempfehlungen und Hinweise sind unter dem Punkt 
            Procedere zusammengefasst. #]<br><br>
            Wir entlassen den Patienten in gutem internistischen Allgemeinzustand in 
            Ihre geschätzte ambulante Weiterversorgung.
        """
    else:
        epikrise = """
            Die elektive stationäre Aufnahme der Patientin erfolgt zur [#Eingriff#] bei [#Indikation#].
            Bei Aufnahme besteht ein [#AZ#] Allgemeinzustand.
            Es bestehen keine Fragen zum geplanten Procedere.<br><br>
            Nach zeitgerecht erfolgter Aufklärung sowie Ausschluss von Kontraindikationen
            konnte der oben genannte Eingriff [#primär komplikationslos#] durchgeführt werden.
            Hier zeigte sich [#BEFUND#]. [#Leichte postinterventionell aufgetretene Schmerzen konnten
            analgetisch therapiert werden#]. Postinterventionell präsentierte sich die Patientin
            zu jedem Zeitpunkt kardiorespiratorisch stabil. [#Weder klinisch noch laborchemisch
            ergab sich der Hinweis auf eine signifikante Nachblutung oder Infektsituation.#]<br>
            [#Unsere weiteren Handlungsempfehlungen und Hinweise sind unter dem Punkt 
            Procedere zusammengefasst. #]<br><br>
            Wir entlassen ie Patientin in gutem internistischen Allgemeinzustand in 
            Ihre geschätzte ambulante Weiterversorgung.
        """

    epikrise = epikrise.replace("[#AZ#]", az)

    return epikrise