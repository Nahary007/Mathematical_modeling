import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

class GraphicView:
    """Vue spécifique pour la méthode graphique de programmation linéaire."""

    def __init__(self, parent, go_home_callback):
        self.parent = parent
        self.go_home_callback = go_home_callback

        # Effacer tout contenu précédent
        for widget in self.parent.winfo_children():
            widget.destroy()

        # ===== Titre =====
        title_label = tk.Label(
            self.parent,
            text="Méthode Graphique (Programmation Linéaire)",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#1E3A8A"
        )
        title_label.pack(pady=30)

        # ===== Section Objectif =====
        obj_frame = tk.Frame(self.parent, bg="white")
        obj_frame.pack(pady=10)

        tk.Label(obj_frame, text="Objectif :", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10)
        self.obj_choice = tk.StringVar(value="max")
        tk.Radiobutton(obj_frame, text="Maximiser", variable=self.obj_choice, value="max", bg="white").grid(row=0, column=1)
        tk.Radiobutton(obj_frame, text="Minimiser", variable=self.obj_choice, value="min", bg="white").grid(row=0, column=2)

        tk.Label(obj_frame, text="Fonction Z =", font=("Arial", 14), bg="white").grid(row=1, column=0, pady=5)
        self.eq_entry = tk.Entry(obj_frame, width=25, font=("Arial", 14))
        self.eq_entry.insert(0, "3X + 2Y")  # valeur par défaut
        self.eq_entry.grid(row=1, column=1, columnspan=2, pady=5)

        # ===== Section Contraintes =====
        tk.Label(self.parent, text="Contraintes :", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        self.contraintes_text = tk.Text(self.parent, height=6, width=50, font=("Arial", 12))
        self.contraintes_text.insert("1.0", "2X + Y <= 10\nX + 2Y <= 15\nX >= 0\nY >= 0")
        self.contraintes_text.pack(pady=5)

        # ===== Boutons =====
        btn_frame = tk.Frame(self.parent, bg="white")
        btn_frame.pack(pady=20)

        tracer_btn = tk.Button(
            btn_frame,
            text="Tracer et résoudre",
            font=("Arial", 14, "bold"),
            bg="#10B981",
            fg="white",
            width=20,
            command=self.tracer_solution,
            cursor="hand2",
            relief="flat"
        )
        tracer_btn.grid(row=0, column=0, padx=10)

        retour_btn = tk.Button(
            btn_frame,
            text="← Retour",
            font=("Arial", 12, "bold"),
            bg="#6B7280",
            fg="white",
            width=12,
            command=self.go_home_callback,
            cursor="hand2",
            relief="flat"
        )
        retour_btn.grid(row=0, column=1, padx=10)

        # ===== Zone Résultats =====
        self.result_box = tk.Text(self.parent, height=10, width=70, font=("Courier", 11), wrap="word")
        self.result_box.pack(pady=10)
        self.result_box.insert("end", "Résultats affichés ici...\n")

    # ====================================================
    #  MÉTHODE PRINCIPALE : TRACÉ + RÉSOLUTION
    # ====================================================
    def tracer_solution(self):
        objectif = self.obj_choice.get()
        eq_obj = self.eq_entry.get().replace(" ", "").upper()
        contraintes_input = self.contraintes_text.get("1.0", "end").strip().splitlines()
        contraintes = [c for c in contraintes_input if c]

        try:
            eq_obj = eq_obj.replace("Z=", "")
            aX = float(eq_obj.split("X")[0])
            aY = float(eq_obj.split("X")[1].split("Y")[0])
        except Exception:
            messagebox.showerror("Erreur", "Format incorrect pour la fonction objectif (ex: Z = 3X + 2Y)")
            return

        # Parsing des contraintes
        droites = []
        for c in contraintes:
            c = c.replace(" ", "").upper()
            if "<=" in c:
                gauche, droite = c.split("<=")
                ineq = "<="
            elif ">=" in c:
                gauche, droite = c.split(">=")
                ineq = ">="
            elif "=" in c:
                gauche, droite = c.split("=")
                ineq = "="
            else:
                messagebox.showerror("Erreur", f"Contrainte invalide : {c}")
                return

            gauche = gauche.replace("-", "+-")
            terms = gauche.split("+")
            a, b = 0, 0
            for t in terms:
                if "X" in t:
                    coef = t.replace("X", "")
                    a = float(coef) if coef not in ["", "+"] else 1.0
                    if coef == "-":
                        a = -1.0
                elif "Y" in t:
                    coef = t.replace("Y", "")
                    b = float(coef) if coef not in ["", "+"] else 1.0
                    if coef == "-":
                        b = -1.0
            cst = float(droite)
            droites.append((a, b, cst, ineq))

        # Tracé
        x_vals = np.linspace(0, 20, 400)
        plt.figure(figsize=(8, 6))
        plt.title(f"{'Maximisation' if objectif == 'max' else 'Minimisation'} de Z = {aX}X + {aY}Y")
        plt.xlabel("X")
        plt.ylabel("Y")

        for (a, b, cst, ineq) in droites:
            if b != 0:
                y = (cst - a * x_vals) / b
                plt.plot(x_vals, y, label=f"{a}X+{b}Y{ineq}{cst}")
            else:
                plt.axvline(cst / a, label=f"{a}X{ineq}{cst}")

        # Intersections
        points = []
        for i in range(len(droites)):
            for j in range(i + 1, len(droites)):
                a1, b1, c1, _ = droites[i]
                a2, b2, c2, _ = droites[j]
                det = a1 * b2 - a2 * b1
                if det != 0:
                    x = (c1 * b2 - c2 * b1) / det
                    y = (a1 * c2 - a2 * c1) / det
                    if x >= 0 and y >= 0:
                        points.append((x, y))

        def respecte_contraintes(x, y):
            for (a, b, c, ineq) in droites:
                val = a * x + b * y
                if ineq == "<=" and val > c + 1e-6:
                    return False
                if ineq == ">=" and val < c - 1e-6:
                    return False
            return True

        points_valides = [p for p in points if respecte_contraintes(p[0], p[1])]

        self.result_box.delete("1.0", "end")
        if not points_valides:
            self.result_box.insert("end", "⚠️ Aucune zone faisable trouvée.\n")
            plt.legend()
            plt.grid(True)
            plt.show()
            return

        Z_vals = [aX * px + aY * py for (px, py) in points_valides]
        idx = np.argmax(Z_vals) if objectif == "max" else np.argmin(Z_vals)
        best_point = points_valides[idx]
        best_val = Z_vals[idx]

        # Affichage texte
        self.result_box.insert("end", f"=== Sommets faisables ===\n")
        for p, z in zip(points_valides, Z_vals):
            self.result_box.insert("end", f"Point {p} → Z = {z:.2f}\n")

        self.result_box.insert("end", f"\n>>> Valeur {'maximale' if objectif=='max' else 'minimale'} : Z = {best_val:.2f}\n")
        self.result_box.insert("end", f"au point (X={best_point[0]:.2f}, Y={best_point[1]:.2f})\n")

        # Tracé graphique
        Xv, Yv = zip(*points_valides)
        plt.scatter(Xv, Yv, color='green', label='Sommets faisables')
        plt.scatter(best_point[0], best_point[1], color='gold', s=100, edgecolor='black', label='Optimum')
        plt.legend()
        plt.grid(True)
        plt.show()
