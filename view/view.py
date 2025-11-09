import tkinter as tk
from tkinter import ttk

class View:
    """Vue principale : gère les frames et sous-vues."""

    def __init__(self, root):
        self.root = root
        self.root.title("Modélisation Mathématiques")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")
        self.buttons = {}
        self.back_buttons = {}
        self.sub_views = {}
        self.controller = None
        self.show_frame("home")

    def set_controller(self, controller):
        self.controller = controller

    def clear_root(self):
        """Nettoie le root."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_frame(self, section):
        """Affiche une frame selon la section."""
        self.clear_root()
        if section in ["home", "systemes_lineaires", "programmation_lineaire"]:
            self.create_main_frame(section)
        else:
            # Sous-sections ou régression
            if section == "regression_lineaire":
                back_cb = self.controller.go_home
            elif section.startswith("systemes_"):
                back_cb = lambda: self.show_frame("systemes_lineaires")
            elif section.startswith("programmation_"):
                back_cb = lambda: self.show_frame("programmation_lineaire")
            else:
                back_cb = self.controller.go_home
            self.create_subview_frame(section, back_cb)

    def create_main_frame(self, section):
        """Crée frame pour sections principales avec boutons."""
        # Titre
        title_label = tk.Label(self.root, text=self.get_section_title(section), font=("Arial", 24, "bold"), bg="white", fg="#1E3A8A")
        title_label.pack(pady=30)
        # Description
        # Frame boutons
        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(expand=True, pady=50)
        # Boutons spécifiques
        if section == "home":
            self.create_home_buttons(btn_frame)
        elif section == "systemes_lineaires":
            self.create_systemes_buttons(btn_frame)
        elif section == "programmation_lineaire":
            self.create_programmation_buttons(btn_frame)
        # Bouton retour
        if section != "home":
            back_btn = tk.Button(self.root, text="← Retour", font=("Arial", 12, "bold"), bg="#6B7280", fg="white", bd=0, relief="flat", activebackground="#4B5563", cursor="hand2", command=self.controller.go_home)
            back_btn.pack(pady=20)
            self.back_buttons[section] = back_btn

    def create_subview_frame(self, section, back_cb):
        """Crée frame pour sous-vue."""
        sub_frame = tk.Frame(self.root, bg="white")
        sub_frame.pack(fill="both", expand=True, padx=20, pady=20)
        if section == "systemes_lu":
            from view.methode_lu import LUView
            self.sub_views[section] = LUView(sub_frame, back_cb, self.controller)
        elif section == "systemes_gauss":
            from view.methode_gauss import GaussView
            self.sub_views[section] = GaussView(sub_frame, back_cb, self.controller)
        elif section == "programmation_graphique":
            from view.methode_graphique import GraphicView
            self.sub_views[section] = GraphicView(sub_frame, back_cb, self.controller)
        elif section == "programmation_simplexe":
            from view.methode_simplexe import SimplexeView
            self.sub_views[section] = SimplexeView(sub_frame, back_cb, self.controller)
        elif section == "regression_lineaire":
            from view.regression_lineaire import RLView
            self.sub_views[section] = RLView(sub_frame, back_cb, self.controller)

    def create_home_buttons(self, frame):
        btn_config = {"font": ("Arial", 18, "bold"), "bg": "#3B82F6", "fg": "white", "bd": 0, "relief": "flat", "activebackground": "#1E40AF", "cursor": "hand2", "width": 25, "height": 2}
        sys_btn = tk.Button(frame, text="Systèmes Linéaires", command=lambda: self.controller.go_to_section('systemes_lineaires'), **btn_config)
        sys_btn.pack(pady=20)
        self.buttons["systemes_lineaires"] = sys_btn
        prog_btn = tk.Button(frame, text="Programmation Linéaire", command=lambda: self.controller.go_to_section('programmation_lineaire'), **btn_config)
        prog_btn.pack(pady=20)
        self.buttons["programmation_lineaire"] = prog_btn
        reg_btn = tk.Button(frame, text="Régression Linéaire", command=lambda: self.controller.go_to_section('regression_lineaire'), **btn_config)
        reg_btn.pack(pady=20)
        self.buttons["regression_lineaire"] = reg_btn

    def create_systemes_buttons(self, frame):
        btn_config = {"font": ("Arial", 16, "bold"), "bg": "#3B82F6", "fg": "white", "bd": 0, "relief": "flat", "activebackground": "#1E40AF", "cursor": "hand2", "width": 20, "height": 2}
        lu_btn = tk.Button(frame, text="Méthode LU", command=lambda: self.controller.go_to_section('systemes_lu'), **btn_config)
        lu_btn.pack(pady=20)
        self.buttons["systemes_lu"] = lu_btn
        gauss_btn = tk.Button(frame, text="Méthode de Gauss", command=lambda: self.controller.go_to_section('systemes_gauss'), **btn_config)
        gauss_btn.pack(pady=20)
        self.buttons["systemes_gauss"] = gauss_btn

    def create_programmation_buttons(self, frame):
        btn_config = {"font": ("Arial", 16, "bold"), "bg": "#3B82F6", "fg": "white", "bd": 0, "relief": "flat", "activebackground": "#1E40AF", "cursor": "hand2", "width": 20, "height": 2}
        graph_btn = tk.Button(frame, text="Méthode Graphique", command=lambda: self.controller.go_to_section('programmation_graphique'), **btn_config)
        graph_btn.pack(pady=20)
        self.buttons["programmation_graphique"] = graph_btn
        simp_btn = tk.Button(frame, text="Méthode du Simplexe", command=lambda: self.controller.go_to_section('programmation_simplexe'), **btn_config)
        simp_btn.pack(pady=20)
        self.buttons["programmation_simplexe"] = simp_btn

    def get_section_title(self, section):
        titles = {
            "home": "Modélisation Mathématiques",
            "systemes_lineaires": "Systèmes Linéaires",
            "programmation_lineaire": "Programmation Linéaire"
        }
        return titles.get(section, section.replace("_", " ").title())
