import tkinter as tk
from view.methode_lu import LUView
from view.methode_gauss import GaussView
from view.methode_graphique import GraphicView
from view.methode_simplexe import SimplexeView

class View:
    """Vue : gère l'interface graphique."""

    def __init__(self, root):
        self.root = root
        self.root.title("Modélisation Mathématiques")
        self.root.geometry("700x500")
        self.root.config(bg="#E8F4FD")

        self.frames = {}
        self.buttons = {}
        self.message_labels = {}
        self.back_buttons = {}
        self.sub_views = {}
        self.titles = {
            "home": "Modélisation Mathématiques",
            "systemes_lineaires": "Systèmes Linéaires",
            "programmation_lineaire": "Programmation Linéaire",
            "regression_lineaire": "Régression Linéaire"
        }

        self.create_home_frame()
        self.create_content_frame("systemes_lineaires")
        self.create_content_frame("programmation_lineaire")
        self.create_content_frame("regression_lineaire")

        self.show_frame("home")

    def create_home_frame(self):
        home_frame = tk.Frame(self.root, bg="#E8F4FD")
        self.frames["home"] = home_frame
        home_frame.pack(expand=True, fill="both")

        self.title_label = tk.Label(home_frame,text="", font=("Arial", 32, "bold"), bg="#E8F4FD", fg="#1E3A8A")
        self.title_label.pack(pady=60)

        button_frame = tk.Frame(home_frame, bg="#E8F4FD")
        button_frame.pack(expand=True)

        buttons_data = [
            ("Systèmes linéaires", "#3B82F6", "#1E40AF"),
            ("Programmation linéaire", "#10B981", "#059669"),
            ("Régression linéaire", "#F59E0B", "#D97706")
        ]

        buttons_map = {
            "Systèmes linéaires": "systemes_lineaires",
            "Programmation linéaire": "programmation_lineaire",
            "Régression linéaire": "regression_lineaire"
        }

        for i, (text, bg_color, active_color) in enumerate(buttons_data):
            btn = tk.Button( button_frame, text=text, font=("Arial", 16, "bold"), command=None, width=20, height=2, bg=bg_color, fg="white", bd=0, relief="flat", activebackground=active_color, cursor="hand2" )
            btn.pack(pady=15)

            key = buttons_map[text]
            self.buttons[key] = btn

    def create_content_frame(self, section):
        content_frame = tk.Frame(self.root, bg="white")
        self.frames[section] = content_frame

        title_text = self.titles.get(section, section.replace('_', ' ').title())
        section_label = tk.Label( content_frame, text=title_text, font=("Arial", 24, "bold"), bg="white", fg="#1E3A8A" )
        section_label.pack(pady=40)

        if section == "systemes_lineaires":
            button_frame = tk.Frame(content_frame, bg="white")
            button_frame.pack(expand=True, pady=20)

            # Méthode LU
            lu_btn = tk.Button(button_frame,text="Méthode LU",font=("Arial", 16, "bold"),command=None,width=20,height=2,bg="#8B5CF6",fg="white",bd=0,relief="flat",activebackground="#7C3AED",cursor="hand2")
            lu_btn.pack(pady=10)
            self.buttons['systemes_lu'] = lu_btn

            # Méthode de Gauss
            gauss_btn = tk.Button( button_frame, text="Méthode de Gauss", font=("Arial", 16, "bold"), command=None, width=20, height=2, bg="#EF4444", fg="white", bd=0, relief="flat", activebackground="#DC2626", cursor="hand2" )
            gauss_btn.pack(pady=10)
            self.buttons['systemes_gauss'] = gauss_btn

        elif section == "programmation_lineaire":
            button_frame = tk.Frame(content_frame, bg="white")
            button_frame.pack(expand=True, pady=20)

            # Méthode graphique
            graphique_btn = tk.Button(
                button_frame,
                text="Méthode graphiques",
                font=("Arial", 16, "bold"),
                command=lambda: self.show_frame("methode_graphique"),  # 🟢 redirection ici
                width=20,
                height=2,
                bg="#8B5CF6",
                fg="white",
                bd=0,
                relief="flat",
                activebackground="#7C3AED",
                cursor="hand2"
            )
            graphique_btn.pack(pady=10)
            self.buttons['methode_graphique'] = graphique_btn

            # Méthode Simplexe
            simplexe_btn = tk.Button(
                button_frame,
                text="Méthode Simplexe",
                font=("Arial", 16, "bold"),
                command=lambda: self.show_frame("methode_simplexe"),  # ✅ affiche la vue
                width=20,
                height=2,
                bg="#EF4444",
                fg="white",
                bd=0,
                relief="flat",
                activebackground="#DC2626",
                cursor="hand2"
            )
            simplexe_btn.pack(pady=10)
            self.buttons['methode_simplexe'] = simplexe_btn


        else:
            message_label = tk.Label( content_frame, text="Contenu détaillé à venir... Explorez les concepts ici !", font=("Arial", 14), bg="white", fg="#4B5563", wraplength=500, justify="center" )
            message_label.pack(pady=20, padx=50)
            self.message_labels[section] = message_label

        back_btn = tk.Button( content_frame, text="← Retour à l'accueil", font=("Arial", 12, "bold"), command=None, bg="#6B7280", fg="white", bd=0, relief="flat", activebackground="#4B5563", cursor="hand2" )
        back_btn.pack(pady=30)

        self.back_buttons[section] = back_btn

    def create_sub_view_frame(self, section):
        if section in self.sub_views:
            return

        content_frame = self.frames.get(section)
        if not content_frame:
            content_frame = tk.Frame(self.root, bg="white")
            self.frames[section] = content_frame

        if section == "systemes_lu":
            self.sub_views[section] = LUView(content_frame, self.go_home_callback, self.compute_lu_callback)

        elif section == "systemes_gauss":
            self.sub_views[section] = GaussView(content_frame, self.go_home_callback, self.compute_gauss_callback)

        elif section == "methode_graphique":
            self.sub_views[section] = GraphicView(content_frame, self.go_home_callback)
        elif section == "methode_simplexe":
            self.sub_views[section] = SimplexeView(content_frame, self.go_home_callback)


    def set_message(self, message: str, section=None):
        if section == "home":
            self.title_label.config(text=message)
        elif section in self.message_labels:
            self.message_labels[section].config(text=message)

    def show_frame(self, frame_name):
        self.create_sub_view_frame(frame_name)
        for name, frame in self.frames.items():
            if name == frame_name:
                frame.pack(expand=True, fill="both")
            else:
                frame.pack_forget()

    def go_home_callback(self):
        self.show_frame("home")

    # Exposer pour le controller
    def get_go_home_callback(self):
        return self.go_home_callback
    
    def set_compute_lu_callback(self, cb):
        self.compute_lu_callback = cb

    def set_compute_gauss_callback(self, cb):
        self.compute_gauss_callback = cb
