import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import numpy as np
import matplotlib.pyplot as plt

class RLView:
    """Vue pour régression linéaire."""

    def __init__(self, parent, back_callback, controller):
        self.parent = parent
        self.back_callback = back_callback
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.parent.configure(bg="white")
        # Titre
        title_label = tk.Label(self.parent, text="Régression Linéaire", font=("Arial", 24, "bold"), bg="white", fg="#1E3A8A")
        title_label.pack(pady=40)
        # Boutons
        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)
        load_btn = tk.Button(
            button_frame, text="📂 Charger CSV", font=("Arial", 14, "bold"), bg="#3B82F6", fg="white",
            bd=0, relief="flat", activebackground="#1D4ED8", cursor="hand2", width=20,
            command=self.load_csv_file
        )
        load_btn.grid(row=0, column=0, padx=10, pady=10)
        calc_btn = tk.Button(
            button_frame, text="⚙️ Calculer", font=("Arial", 14, "bold"), bg="#10B981", fg="white",
            bd=0, relief="flat", activebackground="#059669", cursor="hand2", width=20,
            command=self.controller.compute_regression
        )
        calc_btn.grid(row=0, column=1, padx=10, pady=10)
        plot_btn = tk.Button(
            button_frame, text="📈 Graphique", font=("Arial", 14, "bold"), bg="#F59E0B", fg="white",
            bd=0, relief="flat", activebackground="#D97706", cursor="hand2", width=20,
            command=self.controller.plot_regression
        )
        plot_btn.grid(row=1, column=0, columnspan=2, pady=10)
        # Résultats
        self.result_text = tk.Text(self.parent, width=80, height=15, font=("Consolas", 11), wrap=tk.WORD)
        self.result_text.pack(pady=20)
        self.result_text.insert(tk.END, "Chargez un CSV avec colonnes 'x' et 'y', puis calculez.\n")
        # Bouton retour
        back_btn = tk.Button(
            self.parent, text="← Retour", font=("Arial", 12, "bold"), bg="#6B7280", fg="white",
            bd=0, relief="flat", activebackground="#4B5563", cursor="hand2", command=self.back_callback
        )
        back_btn.pack(pady=20)

    def load_csv_file(self):
        filepath = filedialog.askopenfilename(title="Sélectionner CSV", filetypes=[("CSV", "*.csv")])
        if not filepath:
            return
        try:
            x_vals, y_vals = [], []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if 'x' not in reader.fieldnames or 'y' not in reader.fieldnames:
                    raise ValueError("Colonnes 'x' et 'y' obligatoires.")
                for row in reader:
                    x_vals.append(float(row['x']))
                    y_vals.append(float(row['y']))
            x = np.array(x_vals)
            y = np.array(y_vals)
            self.controller.set_regression_data(x, y)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Données chargées : {len(x)} points.\nPrêt pour calcul.\n")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de lecture : {e}")

    def show_result(self, text):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)

    def plot_graph(self, x, y, model):
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='blue', label='Données', alpha=0.7)
        x_sort = np.sort(x)
        y_pred = model.predict(x_sort.reshape(-1, 1))
        plt.plot(x_sort, y_pred, color='red', linewidth=2, label=f'Droite : y = {self.controller.model.a:.2f}x + {self.controller.model.b:.2f}')
        plt.title("Régression Linéaire")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def show_error(self, msg):
        messagebox.showerror("Erreur", msg)