import tkinter as tk

class GaussView:
    """Vue spécifique pour la méthode de Gauss."""

    def __init__(self, parent, go_home_callback):
        self.parent = parent
        self.go_home_callback = go_home_callback

        # Titre
        title_label = tk.Label( self.parent, text="Méthode de Gauss", font=("Arial", 24, "bold"), bg="white", fg="#1E3A8A")
        title_label.pack(pady=40)

        # Message placeholder
        message_label = tk.Label( self.parent, text="Implémentez ici l'élimination de Gauss. Entrez votre matrice augmentée pour résoudre le système.", font=("Arial", 14), bg="white", fg="#4B5563", wraplength=500, justify="center" )
        message_label.pack(pady=20, padx=50)

        # Bouton Retour (utilise le callback global)
        back_btn = tk.Button( self.parent, text="← Retour aux systèmes linéaires", font=("Arial", 12, "bold"), command=go_home_callback, bg="#6B7280", fg="white", bd=0, relief="flat", activebackground="#4B5563", cursor="hand2" )
        back_btn.pack(pady=30)