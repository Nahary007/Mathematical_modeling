import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

class GraphicView:
    """Vue pour méthode graphique."""

    def __init__(self, parent, back_callback, controller):
        self.parent = parent
        self.back_callback = back_callback
        self.controller = controller
        self.obj_choice = None
        self.eq_entry = None
        self.contraintes_text = None
        self.result_box = None
        self.setup_ui()

    def setup_ui(self):
        # Titre
        title_label = tk.Label(self.parent, text="Méthode Graphique (Programmation Linéaire)", font=("Arial", 22, "bold"), bg="white", fg="#1E3A8A")
        title_label.pack(pady=30)
        # Section objectif
        obj_frame = tk.Frame(self.parent, bg="white")
        obj_frame.pack(pady=10)
        tk.Label(obj_frame, text="Objectif :", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10, sticky="w")
        self.obj_choice = tk.StringVar(value="max")
        tk.Radiobutton(obj_frame, text="Maximiser", variable=self.obj_choice, value="max", bg="white", selectcolor="#3B82F6").grid(row=0, column=1, padx=10)
        tk.Radiobutton(obj_frame, text="Minimiser", variable=self.obj_choice, value="min", bg="white", selectcolor="#3B82F6").grid(row=0, column=2, padx=10)
        tk.Label(obj_frame, text="Fonction Z =", font=("Arial", 14), bg="white").grid(row=1, column=0, pady=10, sticky="w")
        self.eq_entry = tk.Entry(obj_frame, width=25, font=("Arial", 12))
        self.eq_entry.insert(0, "3X + 2Y")
        self.eq_entry.grid(row=1, column=1, columnspan=2, pady=10, sticky="w")
        # Contraintes
        tk.Label(self.parent, text="Contraintes :", font=("Arial", 14, "bold"), bg="white").pack(pady=(20, 5))
        self.contraintes_text = tk.Text(self.parent, height=6, width=60, font=("Arial", 11), wrap=tk.WORD)
        self.contraintes_text.insert("1.0", "2X + Y <= 10\nX + 2Y <= 15\nX >= 0\nY >= 0")
        self.contraintes_text.pack(pady=5)
        # Boutons
        btn_frame = tk.Frame(self.parent, bg="white")
        btn_frame.pack(pady=20)
        tracer_btn = tk.Button(
            btn_frame, text="Tracer et résoudre", font=("Arial", 14, "bold"), bg="#10B981", fg="white",
            bd=0, relief="flat", activebackground="#059669", cursor="hand2", width=18,
            command=self.controller.compute_graphic
        )
        tracer_btn.grid(row=0, column=0, padx=10)
        retour_btn = tk.Button(
            btn_frame, text="← Retour", font=("Arial", 12, "bold"), bg="#6B7280", fg="white",
            bd=0, relief="flat", activebackground="#4B5563", cursor="hand2", command=self.back_callback
        )
        retour_btn.grid(row=0, column=1, padx=10)
        # Résultats
        self.result_box = tk.Text(self.parent, height=15, width=80, font=("Consolas", 11), wrap=tk.WORD)
        self.result_box.pack(pady=10)
        self.result_box.insert("end", "Entrez les données et cliquez sur 'Tracer et résoudre'.\n")

    def show_solution(self, text, droites, points_valides, best_point, aX, aY, objectif):
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert("end", text)
        # Graphique
        x_vals = np.linspace(0, 20, 400)
        plt.figure(figsize=(10, 7))
        plt.title(f"{'Maximisation' if objectif == 'max' else 'Minimisation'} de Z = {aX}X + {aY}Y")
        plt.xlabel("X")
        plt.ylabel("Y")
        for a, b, cst, ineq in droites:
            if abs(b) > 1e-10:
                y_vals = (cst - a * x_vals) / b
                plt.plot(x_vals, y_vals, label=f"{a}X + {b}Y {ineq} {cst}")
            else:
                plt.axvline(x=cst / a, label=f"{a}X {ineq} {cst}")
        if points_valides:
            Xv, Yv = zip(*points_valides)
            plt.scatter(Xv, Yv, color='green', s=50, label='Sommets faisables', zorder=5)
            plt.scatter(best_point[0], best_point[1], color='gold', s=150, edgecolor='black', label='Optimum', zorder=6)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def show_error(self, msg):
        messagebox.showerror("Erreur", msg)