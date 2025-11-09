import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class RLView:
    """Vue spécifique pour la régression linéaire."""

    def __init__(self, parent, go_home_callback):
        self.parent = parent
        self.go_home_callback = go_home_callback

        self.parent.config(bg="white")

        # --- Titre principal ---
        title_label = tk.Label(
            self.parent,
            text="Régression Linéaire",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1E3A8A"
        )
        title_label.pack(pady=40)

        # --- Zone de boutons ---
        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        # Bouton pour charger un fichier CSV
        load_btn = tk.Button(
            button_frame,
            text="📂 Charger un fichier CSV",
            font=("Arial", 14, "bold"),
            bg="#3B82F6",
            fg="white",
            width=25,
            relief="flat",
            cursor="hand2",
            activebackground="#1D4ED8",
            command=self.load_csv_file
        )
        load_btn.grid(row=0, column=0, padx=10, pady=10)

        # Bouton pour calculer la régression
        calc_btn = tk.Button(
            button_frame,
            text="⚙️ Calculer la régression",
            font=("Arial", 14, "bold"),
            bg="#10B981",
            fg="white",
            width=25,
            relief="flat",
            cursor="hand2",
            activebackground="#059669",
            command=self.compute_regression
        )
        calc_btn.grid(row=0, column=1, padx=10, pady=10)

        # Bouton pour afficher le graphique
        plot_btn = tk.Button(
            button_frame,
            text="📈 Afficher le graphique",
            font=("Arial", 14, "bold"),
            bg="#F59E0B",
            fg="white",
            width=25,
            relief="flat",
            cursor="hand2",
            activebackground="#D97706",
            command=self.plot_graph
        )
        plot_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # --- Zone d'affichage des résultats ---
        self.result_label = tk.Label(
            self.parent,
            text="Aucun calcul effectué.",
            font=("Arial", 13),
            bg="white",
            fg="#374151",
            justify="left"
        )
        self.result_label.pack(pady=20)

        # --- Bouton retour ---
        back_btn = tk.Button(
            self.parent,
            text="← Retour à l'accueil",
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

        # Variables pour stocker les données
        self.x = None
        self.y = None
        self.modele = None
        self.a = None
        self.b = None
        self.r = None

    # --- Charger un fichier CSV ---
    def load_csv_file(self):
        filepath = filedialog.askopenfilename(
            title="Sélectionner un fichier CSV",
            filetypes=[("Fichiers CSV", "*.csv")]
        )
        if not filepath:
            return

        try:
            x_vals, y_vals = [], []
            with open(filepath, 'r') as fichier_csv:
                lecteur = csv.DictReader(fichier_csv)
                if 'x' not in lecteur.fieldnames or 'y' not in lecteur.fieldnames:
                    raise ValueError("Le fichier doit contenir des colonnes nommées 'x' et 'y'.")
                for ligne in lecteur:
                    x_vals.append(float(ligne['x']))
                    y_vals.append(float(ligne['y']))

            self.x = np.array(x_vals)
            self.y = np.array(y_vals)

            messagebox.showinfo("Fichier chargé", f"{len(self.x)} valeurs importées depuis {filepath}")

        except Exception as e:
            messagebox.showerror("Erreur de lecture", f"Impossible de lire le fichier :\n{e}")

    # --- Calcul de la régression ---
    def compute_regression(self):
        if self.x is None or self.y is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger un fichier CSV.")
            return

        try:
            moyenne_x = np.mean(self.x)
            moyenne_y = np.mean(self.y)
            variance_x = np.var(self.x, ddof=1)
            variance_y = np.var(self.y, ddof=1)
            covariance = np.cov(self.x, self.y, ddof=1)[0, 1]
            self.r = np.corrcoef(self.x, self.y)[0, 1]

            x_reshape = self.x.reshape(-1, 1)
            self.modele = LinearRegression()
            self.modele.fit(x_reshape, self.y)

            self.a = self.modele.coef_[0]
            self.b = self.modele.intercept_

            # Mise à jour du texte affiché
            result_text = (
                f"Moyenne de x : {moyenne_x:.4f}\n"
                f"Moyenne de y : {moyenne_y:.4f}\n"
                f"Variance de x : {variance_x:.4f}\n"
                f"Variance de y : {variance_y:.4f}\n"
                f"Covariance(x, y) : {covariance:.4f}\n"
                f"Coefficient de corrélation (r) : {self.r:.4f}\n\n"
                f"Équation de la droite : y = {self.a:.4f}x + {self.b:.4f}"
            )

            self.result_label.config(text=result_text)

        except Exception as e:
            messagebox.showerror("Erreur de calcul", f"Une erreur est survenue :\n{e}")

    # --- Tracé du graphique ---
    def plot_graph(self):
        if self.modele is None or self.x is None or self.y is None:
            messagebox.showwarning("Attention", "Veuillez d'abord effectuer le calcul.")
            return

        plt.scatter(self.x, self.y, color='blue', label='Données')
        plt.plot(self.x, self.modele.predict(self.x.reshape(-1, 1)), color='red', label='Droite de régression')
        plt.title("Droite des Moindres Carrés")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        plt.show()
