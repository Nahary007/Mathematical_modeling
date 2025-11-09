import tkinter as tk

class View:
    """Vue : gère l'interface graphique."""

    def __init__(self, root):
        self.root = root
        self.root.title("MVC avec Tkinter")
        self.label = tk.Label(self.root, text="", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

    def set_message(self, message: str):
        """Affiche un message dans la fenêtre."""
        self.label.config(text=message)
