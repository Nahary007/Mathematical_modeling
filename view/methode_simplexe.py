import tkinter as tk
from tkinter import messagebox

class SimplexeView:
    """Vue pour méthode du Simplexe."""

    def __init__(self, parent, back_callback, controller):
        self.parent = parent
        self.back_callback = back_callback
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # Titre
        title_label = tk.Label(self.parent, text="Méthode du Simplexe", font=("Arial", 24, "bold"), bg="white", fg="#1E3A8A")
        title_label.pack(pady=30)
        # Objectif
        input_frame = tk.Frame(self.parent, bg="white")
        input_frame.pack(pady=20)
        tk.Label(input_frame, text="Maximiser Z =", bg="white", font=("Arial", 14)).grid(row=0, column=0, padx=5)
        self.a1_entry = tk.Entry(input_frame, width=6, font=("Arial", 12), justify="center")
        self.a1_entry.grid(row=0, column=1, padx=2)
        self.a1_entry.insert(0, "3")
        tk.Label(input_frame, text="x1 +", bg="white", font=("Arial", 14)).grid(row=0, column=2)
        self.a2_entry = tk.Entry(input_frame, width=6, font=("Arial", 12), justify="center")
        self.a2_entry.grid(row=0, column=3, padx=2)
        self.a2_entry.insert(0, "2")
        tk.Label(input_frame, text="x2", bg="white", font=("Arial", 14)).grid(row=0, column=4)
        # Contraintes
        constraints_frame = tk.Frame(self.parent, bg="white")
        constraints_frame.pack(pady=10)
        # Contrainte 1
        tk.Label(constraints_frame, text="Constr. 1 :", bg="white", font=("Arial", 14)).grid(row=0, column=0, pady=5)
        self.c1x1_entry = tk.Entry(constraints_frame, width=6, font=("Arial", 12), justify="center")
        self.c1x1_entry.grid(row=0, column=1, padx=2)
        self.c1x1_entry.insert(0, "2")
        tk.Label(constraints_frame, text="x1 +", bg="white", font=("Arial", 14)).grid(row=0, column=2)
        self.c1x2_entry = tk.Entry(constraints_frame, width=6, font=("Arial", 12), justify="center")
        self.c1x2_entry.grid(row=0, column=3, padx=2)
        self.c1x2_entry.insert(0, "1")
        tk.Label(constraints_frame, text="x2 ≤", bg="white", font=("Arial", 14)).grid(row=0, column=4)
        self.c1b_entry = tk.Entry(constraints_frame, width=6, font=("Arial", 12), justify="center")
        self.c1b_entry.grid(row=0, column=5, padx=2)
        self.c1b_entry.insert(0, "10")
        # Contrainte 2
        tk.Label(constraints_frame, text="Constr. 2 :", bg="white", font=("Arial", 14)).grid(row=1, column=0, pady=10)
        self.c2x1_entry = tk.Entry(constraints_frame, width=6, font=("Arial", 12), justify="center")
        self.c2x1_entry.grid(row=1, column=1, padx=2)
        self.c2x1_entry.insert(0, "1")
        tk.Label(constraints_frame, text="x1 +", bg="white", font=("Arial", 14)).grid(row=1, column=2)
        self.c2x2_entry = tk.Entry(constraints_frame, width=6, font=("Arial", 12), justify="center")
        self.c2x2_entry.grid(row=1, column=3, padx=2)
        self.c2x2_entry.insert(0, "2")
        tk.Label(constraints_frame, text="x2 ≤", bg="white", font=("Arial", 14)).grid(row=1, column=4)
        self.c2b_entry = tk.Entry(constraints_frame, width=6, font=("Arial", 12), justify="center")
        self.c2b_entry.grid(row=1, column=5, padx=2)
        self.c2b_entry.insert(0, "15")
        # Bouton résoudre
        solve_btn = tk.Button(
            self.parent, text="Résoudre", font=("Arial", 14, "bold"), bg="#10B981", fg="white",
            bd=0, relief="flat", activebackground="#059669", cursor="hand2", width=15,
            command=self.controller.compute_simplex
        )
        solve_btn.pack(pady=20)
        # Résultats
        self.result_text = tk.Text(self.parent, width=80, height=15, font=("Consolas", 11), wrap=tk.WORD)
        self.result_text.pack(pady=10)
        self.result_text.insert(tk.END, "Entrez les coefficients et résolvez.\n")
        # Bouton retour
        back_btn = tk.Button(
            self.parent, text="← Retour à la programmation linéaire", font=("Arial", 12, "bold"),
            bg="#6B7280", fg="white", bd=0, relief="flat", activebackground="#4B5563", cursor="hand2",
            command=self.back_callback
        )
        back_btn.pack(pady=15)

    def get_params(self):
        try:
            return (
                float(self.a1_entry.get()),
                float(self.a2_entry.get()),
                float(self.c1x1_entry.get()),
                float(self.c1x2_entry.get()),
                float(self.c1b_entry.get()),
                float(self.c2x1_entry.get()),
                float(self.c2x2_entry.get()),
                float(self.c2b_entry.get())
            )
        except ValueError:
            raise ValueError("Entrez des nombres valides dans tous les champs.")

    def show_result(self, text):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)

    def show_error(self, msg):
        messagebox.showerror("Erreur", msg)