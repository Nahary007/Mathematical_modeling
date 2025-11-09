import tkinter as tk
from tkinter import messagebox

class Controller:
    """Contrôleur : lien Model-View, logique d'application."""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        # Plus besoin de setup_button_actions() : les commands sont définies directement dans View

    # Callbacks pour LU/Gauss (inchangés)
    def compute_LU(self):
        view = self.view.sub_views["systemes_lu"]
        try:
            A, B = view.get_values()
            txt = self.model.compute_lu(A, B)
            view.show_result(txt)
        except ValueError as e:
            view.show_error(str(e))

    def compute_GAUSS(self):
        view = self.view.sub_views["systemes_gauss"]
        try:
            A, B = view.get_values()
            txt = self.model.compute_gauss(A, B)
            view.show_result(txt)
        except ValueError as e:
            view.show_error(str(e))

    # Callbacks pour programmation linéaire (inchangés)
    def compute_graphic(self):
        view = self.view.sub_views["programmation_graphique"]
        objectif = view.obj_choice.get()
        eq_obj = view.eq_entry.get()
        contraintes_input = [c.strip() for c in view.contraintes_text.get("1.0", tk.END).splitlines() if c.strip()]
        try:
            data = self.model.compute_graphic(objectif, eq_obj, contraintes_input)
            view.show_solution(**data, objectif=objectif)
        except ValueError as e:
            view.show_error(str(e))

    def compute_simplex(self):
        view = self.view.sub_views["programmation_simplexe"]
        try:
            params = view.get_params()
            txt = self.model.compute_simplex(*params)
            view.show_result(txt)
        except ValueError as e:
            view.show_error(str(e))

    # Callbacks pour régression (inchangés)
    def set_regression_data(self, x, y):
        self.model.x_reg = x
        self.model.y_reg = y

    def compute_regression(self):
        if self.model.x_reg is None or self.model.y_reg is None:
            self.view.sub_views["regression_lineaire"].show_error("Chargez d'abord un fichier CSV.")
            return
        stats = self.model.compute_regression_stats(self.model.x_reg, self.model.y_reg)
        self.model.fit_regression_model(self.model.x_reg, self.model.y_reg)
        text = stats + f"\nÉquation de la droite : y = {self.model.a:.4f}x + {self.model.b:.4f}"
        self.view.sub_views["regression_lineaire"].show_result(text)

    def plot_regression(self):
        if self.model.x_reg is None or self.model.reg_model is None:
            self.view.sub_views["regression_lineaire"].show_error("Effectuez d'abord le calcul de régression.")
            return
        view = self.view.sub_views["regression_lineaire"]
        view.plot_graph(self.model.x_reg, self.model.y_reg, self.model.reg_model)

    def go_to_section(self, section):
        """Navigation vers une section."""
        self.model.current_section = section
        self.view.show_frame(section)

    def go_home(self):
        """Retour à l'accueil."""
        self.model.current_section = "home"
        self.view.show_frame("home")