import tkinter as tk
from tkinter import messagebox
import pulp


class SimplexeView:
    """Vue spécifique pour la méthode du Simplexe."""

    def __init__(self, parent, go_home_callback):
        self.parent = parent
        self.go_home_callback = go_home_callback

        # Nettoyer le parent avant d'ajouter du contenu
        for widget in self.parent.winfo_children():
            widget.destroy()

        # 🎯 Titre
        title_label = tk.Label(
            self.parent,
            text="Méthode du Simplexe",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1E3A8A"
        )
        title_label.pack(pady=30)

        # 🧮 Section saisie des coefficients
        input_frame = tk.Frame(self.parent, bg="white")
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Maximiser Z = ", bg="white", font=("Arial", 14)).grid(row=0, column=0)
        self.a1_entry = tk.Entry(input_frame, width=5, font=("Arial", 14))
        self.a1_entry.grid(row=0, column=1)
        tk.Label(input_frame, text="x1 +", bg="white", font=("Arial", 14)).grid(row=0, column=2)
        self.a2_entry = tk.Entry(input_frame, width=5, font=("Arial", 14))
        self.a2_entry.grid(row=0, column=3)
        tk.Label(input_frame, text="x2", bg="white", font=("Arial", 14)).grid(row=0, column=4)

        # 🧱 Contraintes
        constraints_frame = tk.Frame(self.parent, bg="white")
        constraints_frame.pack(pady=10)

        tk.Label(constraints_frame, text="Contrainte 1 : ", bg="white", font=("Arial", 14)).grid(row=0, column=0)
        self.c1x1_entry = tk.Entry(constraints_frame, width=5, font=("Arial", 14))
        self.c1x1_entry.grid(row=0, column=1)
        tk.Label(constraints_frame, text="x1 +", bg="white", font=("Arial", 14)).grid(row=0, column=2)
        self.c1x2_entry = tk.Entry(constraints_frame, width=5, font=("Arial", 14))
        self.c1x2_entry.grid(row=0, column=3)
        tk.Label(constraints_frame, text="x2 ≤", bg="white", font=("Arial", 14)).grid(row=0, column=4)
        self.c1b_entry = tk.Entry(constraints_frame, width=5, font=("Arial", 14))
        self.c1b_entry.grid(row=0, column=5)

        tk.Label(constraints_frame, text="Contrainte 2 : ", bg="white", font=("Arial", 14)).grid(row=1, column=0, pady=10)
        self.c2x1_entry = tk.Entry(constraints_frame, width=5, font=("Arial", 14))
        self.c2x1_entry.grid(row=1, column=1)
        tk.Label(constraints_frame, text="x1 +", bg="white", font=("Arial", 14)).grid(row=1, column=2)
        self.c2x2_entry = tk.Entry(constraints_frame, width=5, font=("Arial", 14))
        self.c2x2_entry.grid(row=1, column=3)
        tk.Label(constraints_frame, text="x2 ≤", bg="white", font=("Arial", 14)).grid(row=1, column=4)
        self.c2b_entry = tk.Entry(constraints_frame, width=5, font=("Arial", 14))
        self.c2b_entry.grid(row=1, column=5)

        # 🔘 Bouton Résoudre
        solve_btn = tk.Button(
            self.parent,
            text="Résoudre le problème",
            font=("Arial", 14, "bold"),
            bg="#10B981",
            fg="white",
            bd=0,
            relief="flat",
            activebackground="#059669",
            cursor="hand2",
            command=self.solve_simplexe
        )
        solve_btn.pack(pady=20)

        # 📊 Zone de résultat
        self.result_label = tk.Label(
            self.parent,
            text="Résultats : ",
            font=("Arial", 14),
            bg="white",
            fg="#374151",
            justify="center"
        )
        self.result_label.pack(pady=10)

        # 🔙 Bouton Retour
        back_btn = tk.Button(
            self.parent,
            text="← Retour à la programmation linéaire",
            font=("Arial", 12, "bold"),
            command=go_home_callback,
            bg="#6B7280",
            fg="white",
            bd=0,
            relief="flat",
            activebackground="#4B5563",
            cursor="hand2"
        )
        back_btn.pack(pady=30)

    # --- Fonction de résolution du simplexe ---
    def solve_simplexe(self):
        try:
            # 🔢 Lecture des valeurs entrées
            a1 = float(self.a1_entry.get())
            a2 = float(self.a2_entry.get())
            c1x1 = float(self.c1x1_entry.get())
            c1x2 = float(self.c1x2_entry.get())
            c1b = float(self.c1b_entry.get())
            c2x1 = float(self.c2x1_entry.get())
            c2x2 = float(self.c2x2_entry.get())
            c2b = float(self.c2b_entry.get())

            # 1️⃣ Définir le problème
            prob = pulp.LpProblem("Simplexe_UI", pulp.LpMaximize)

            # 2️⃣ Variables
            x1 = pulp.LpVariable('x1', lowBound=0)
            x2 = pulp.LpVariable('x2', lowBound=0)

            # 3️⃣ Fonction objectif
            prob += a1 * x1 + a2 * x2, "Z"

            # 4️⃣ Contraintes
            prob += c1x1 * x1 + c1x2 * x2 <= c1b
            prob += c2x1 * x1 + c2x2 * x2 <= c2b

            # 5️⃣ Résolution
            prob.solve()

            # 6️⃣ Affichage résultat
            result_text = (
                f"Statut : {pulp.LpStatus[prob.status]}\n"
                f"x1 = {pulp.value(x1):.2f}\n"
                f"x2 = {pulp.value(x2):.2f}\n"
                f"Valeur maximale de Z = {pulp.value(prob.objective):.2f}"
            )
            self.result_label.config(text=result_text)

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides dans tous les champs.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
