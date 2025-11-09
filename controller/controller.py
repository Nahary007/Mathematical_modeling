class Controller:
    """Contrôleur : fait le lien entre le modèle et la vue."""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.update_view()

    def update_view(self):
        """Met à jour la vue selon le modèle."""
        message = self.model.get_message()
        self.view.set_message(message)
