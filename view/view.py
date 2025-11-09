import tkinter as tk

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

        self.create_home_frame()
        self.create_content_frame("systemes_lineaires")
        self.create_content_frame("programmation_lineaire")
        self.create_content_frame("regression_lineaire")

        self.show_frame("home")

    def create_home_frame(self):
        home_frame = tk.Frame(self.root, bg="#E8F4FD")
        self.frames["home"] = home_frame
        home_frame.pack(expand=True, fill="both")

        self.title_label = tk.Label(
            home_frame,
            text="",
            font=("Arial", 32, "bold"),
            bg="#E8F4FD",
            fg="#1E3A8A"
        )
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
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 16, "bold"),
                command=None,
                width=20,
                height=2,
                bg=bg_color,
                fg="white",
                bd=0,
                relief="flat",
                activebackground=active_color,
                cursor="hand2"
            )
            btn.pack(pady=15)

            key = buttons_map[text]
            self.buttons[key] = btn

    def create_content_frame(self, section):
        content_frame = tk.Frame(self.root, bg="white")
        self.frames[section] = content_frame

        section_label = tk.Label(
            content_frame,
            text=f"{section.replace('_', ' ').title()}",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1E3A8A"
        )
        section_label.pack(pady=40)

        message_label = tk.Label(
            content_frame,
            text="Contenu détaillé à venir... Explorez les concepts ici !",
            font=("Arial", 14),
            bg="white",
            fg="#4B5563",
            wraplength=500,
            justify="center"
        )
        message_label.pack(pady=20, padx=50)

        back_btn = tk.Button(
            content_frame,
            text="← Retour à l'accueil",
            font=("Arial", 12, "bold"),
            command=None,
            bg="#6B7280",
            fg="white",
            bd=0,
            relief="flat",
            activebackground="#4B5563",
            cursor="hand2"
        )
        back_btn.pack(pady=30)

        self.message_labels[section] = message_label
        self.back_buttons[section] = back_btn

    def set_message(self, message: str, section=None):
        if section == "home":
            self.title_label.config(text=message)
        elif section in self.message_labels:
            self.message_labels[section].config(text=message)

    def show_frame(self, frame_name):
        for name, frame in self.frames.items():
            if name == frame_name:
                frame.pack(expand=True, fill="both")
            else:
                frame.pack_forget()