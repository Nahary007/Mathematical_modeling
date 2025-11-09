import tkinter as tk

class LUView:
    """Vue spécifique pour la méthode LU."""

    def __init__(self, parent, go_home_callback, compute_callback):
        self.parent = parent
        self.go_home_callback = go_home_callback
        self.compute_callback = compute_callback

        # Titre
        title_label = tk.Label(
            self.parent,
            text="Méthode LU",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1E3A8A"
        )
        title_label.pack(pady=25)

        # FRAME MATRICE A
        frm_A = tk.Frame(self.parent, bg="white")
        frm_A.pack(pady=10)

        tk.Label(frm_A, text="Matrice A (3x3)", bg="white", font=("Arial",14,"bold")).pack()

        self.entriesA = []
        for i in range(3):
            row = []
            rframe = tk.Frame(frm_A, bg="white")
            rframe.pack()
            for j in range(3):
                e = tk.Entry(rframe, width=6, font=("Arial",14))
                e.pack(side="left", padx=5, pady=3)
                row.append(e)
            self.entriesA.append(row)

        # vecteur B
        frm_B = tk.Frame(self.parent, bg="white")
        frm_B.pack(pady=10)

        tk.Label(frm_B, text="Vecteur B", bg="white", font=("Arial",14,"bold")).pack()

        self.entriesB = []
        bframe = tk.Frame(frm_B, bg="white")
        bframe.pack()
        for i in range(3):
            e = tk.Entry(bframe, width=6, font=("Arial",14))
            e.pack(side="left", padx=10, pady=3)
            self.entriesB.append(e)

        # bouton calculer
        calc_btn = tk.Button(
            self.parent,
            text="Calculer LU",
            font=("Arial",14,"bold"),
            bg="#3B82F6",
            fg="white",
            bd=0,
            relief="flat",
            activebackground="#1E40AF",
            cursor="hand2",
            command=self.compute_callback
        )
        calc_btn.pack(pady=15)

        # zone résultat
        self.result_text = tk.Text(self.parent, width=70, height=12, font=("Consolas",12))
        self.result_text.pack(pady=20)

        # bouton retour
        back_btn = tk.Button(
            self.parent,
            text="← Retour",
            font=("Arial", 12, "bold"),
            command=go_home_callback,
            bg="#6B7280",
            fg="white",
            bd=0,
            relief="flat",
            activebackground="#4B5563",
            cursor="hand2"
        )
        back_btn.pack(pady=15)

    # helper pour controller
    def get_values(self):
        A = [[float(self.entriesA[i][j].get()) for j in range(3)] for i in range(3)]
        B = [float(self.entriesB[i].get()) for i in range(3)]
        return A, B

    def show_result(self, text):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
