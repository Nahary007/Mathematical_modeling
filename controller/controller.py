class Controller:
    """Contrôleur : fait le lien entre le modèle et la vue."""

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.update_view()
        self.setup_button_actions()

    def update_view(self, section=None):
        message = self.model.get_message(section)
        self.view.set_message(message, section)

    def setup_button_actions(self):
        self.view.buttons['systemes_lineaires'].config(command=lambda: self.go_to_section('systemes_lineaires'))
        self.view.buttons['programmation_lineaire'].config(command=lambda: self.go_to_section('programmation_lineaire'))
        self.view.buttons['regression_lineaire'].config(command=lambda: self.go_to_section('regression_lineaire'))

        for section in ['systemes_lineaires', 'programmation_lineaire', 'regression_lineaire']:
            self.view.back_buttons[section].config(command=lambda s=section: self.go_home())

    def go_to_section(self, section):
        self.update_view(section)
        self.view.show_frame(section)

    def go_home(self):
        self.update_view("home")
        self.view.show_frame("home")