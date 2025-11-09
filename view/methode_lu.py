import tkinter as tk
from tkinter import messagebox

class LUView:
    """Vue pour méthode LU."""

    def __init__(self, parent, back_callback, controller):
        self.parent = parent
        self.back_callback = back_callback
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # Titre
        title_label = tk.Label(self.parent, text="Méthode LU", font=("Arial", 24, "bold"), bg="white", fg="#1E3A8A")
        title_label.pack(pady=25)
        # Frame A
        frm_A = tk.Frame(self.parent, bg="white")
        frm_A.pack(pady=10)
        tk.Label(frm_A, text="Matrice A (3x3)", bg="white", font=("Arial", 14, "bold")).pack(pady=5)
        self.entriesA = []
        for i in range(3):
            row = []
            rframe = tk.Frame(frm_A, bg="white")
            rframe.pack(pady=2)
            for j in range(3):
                e = tk.Entry(rframe, width=8, font=("Arial", 12), justify="center")
                e.pack(side="left", padx=2)
                row.append(e)
            self.entriesA.append(row)
        # Frame B
        frm_B = tk.Frame(self.parent, bg="white")
        frm_B.pack(pady=10)
        tk.Label(frm_B, text="Vecteur B", bg="white", font=("Arial", 14, "bold")).pack(pady=5)
        self.entriesB = []
        bframe = tk.Frame(frm_B, bg="white")
        bframe.pack(pady=2)
        for i in range(3):
            e = tk.Entry(bframe, width=8, font=("Arial", 12), justify="center")
            e.pack(side="left", padx=5)
            self.entriesB.append(e)
        # Bouton calcul
        calc_btn = tk.Button(
            self.parent, text="Calculer LU", font=("Arial", 14, "bold"), bg="#10B981", fg="white",
            bd=0, relief="flat", activebackground="#059669", cursor="hand2", width=15,
            command=self.controller.compute_LU
        )
        calc_btn.pack(pady=15)
        # Résultats
        self.result_text = tk.Text(self.parent, width=80, height=15, font=("Consolas", 11), wrap=tk.NONE)
        self.result_text.pack(pady=20)
        # Bouton retour
        back_btn = tk.Button(
            self.parent, text="← Retour", font=("Arial", 12, "bold"), bg="#6B7280", fg="white",
            bd=0, relief="flat", activebackground="#4B5563", cursor="hand2", command=self.back_callback
        )
        back_btn.pack(pady=15)

    def get_values(self):
        try:
            A = [[float(self.entriesA[i][j].get()) for j in range(3)] for i in range(3)]
            B = [float(self.entriesB[i].get()) for i in range(3)]
            return A, B
        except ValueError:
            raise ValueError("Entrez des valeurs numériques valides dans tous les champs.")

    def show_result(self, text):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)

    def show_error(self, msg):
        messagebox.showerror("Erreur", msg)