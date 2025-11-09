class Model:
    """Modèle : contient les données de l'application."""

    def __init__(self):
        self.messages = {
            "home": "Modélisation Mathématiques",
            "systemes_lineaires": "Systèmes linéaires : Résolvez des équations simultanées avec élégance.",
            "programmation_lineaire": "Programmation linéaire : Optimisez vos ressources comme un pro.",
            "regression_lineaire": "Régression linéaire : Prédisez l'avenir avec des droites intelligentes."
        }
        self.current_section = "home"

    def get_message(self, section=None):
        if section:
            self.current_section = section
        return self.messages.get(self.current_section, self.messages["home"])

    def get_sections(self):
        return list(self.messages.keys())