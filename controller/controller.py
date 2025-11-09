class Controller:
    """Contrôleur : fait le lien entre le modèle et la vue."""

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.update_view()
        self.setup_button_actions()
        self.view.set_compute_lu_callback(self.compute_LU)


    def update_view(self, section=None):
        message = self.model.get_message(section)
        self.view.set_message(message, section)

    def setup_button_actions(self):
        self.view.buttons['systemes_lineaires'].config(command=lambda: self.go_to_section('systemes_lineaires'))
        self.view.buttons['programmation_lineaire'].config(command=lambda: self.go_to_section('programmation_lineaire'))
        self.view.buttons['regression_lineaire'].config(command=lambda: self.go_to_section('regression_lineaire'))

        if 'systemes_lu' in self.view.buttons:
            self.view.buttons['systemes_lu'].config(command=lambda: self.go_to_section('systemes_lu'))
        if 'systemes_gauss' in self.view.buttons:
            self.view.buttons['systemes_gauss'].config(command=lambda: self.go_to_section('systemes_gauss'))

        for section in ['systemes_lineaires', 'programmation_lineaire', 'regression_lineaire']:
            self.view.back_buttons[section].config(command=lambda s=section: self.go_home())

    def go_to_section(self, section):
        self.update_view(section)
        self.view.show_frame(section)

    def go_home(self):
        self.update_view("home")
        self.view.show_frame("home")

    def compute_LU(self):
        # récupérer données LUView
        A,B = self.view.sub_views["systemes_lu"].get_values()

        # --- calcul LU (ton code recollé propre) ---
        n=3
        L=[[0]*n for _ in range(n)]
        U=[[0]*n for _ in range(n)]
        for i in range(n): L[i][i]=1.0

        U[0][0]=A[0][0]
        U[0][1]=A[0][1]
        U[0][2]=A[0][2]

        L[1][0]=A[1][0]/U[0][0]
        L[2][0]=A[2][0]/U[0][0]

        U[1][1]=A[1][1]-(L[1][0]*U[0][1])
        U[1][2]=A[1][2]-(L[1][0]*U[0][2])

        L[2][1]=(A[2][1]-(L[2][0]*U[0][1]))/U[1][1]

        U[2][2]=A[2][2]-(L[2][0]*U[0][2])-(L[2][1]*U[1][2])

        # descente
        Y=[0]*n
        Y[0]=B[0]
        Y[1]=B[1]-(L[1][0]*Y[0])
        Y[2]=B[2]-(L[2][0]*Y[0])-(L[2][1]*Y[1])

        # remontée
        X=[0]*n
        X[2]=Y[2]/U[2][2]
        X[1]=(Y[1]-U[1][2]*X[2])/U[1][1]
        X[0]=(Y[0]-U[0][1]*X[1]-U[0][2]*X[2])/U[0][0]

        txt  = "=== L ===\n"
        txt += "\n".join(str([round(v,4) for v in row]) for row in L)
        txt += "\n\n=== U ===\n"
        txt += "\n".join(str([round(v,4) for v in row]) for row in U)
        txt += "\n\n=== Y ===\n"
        txt += str([round(v,4) for v in Y])
        txt += "\n\n=== X ===\n"
        txt += str([round(v,4) for v in X])

        # afficher
        self.view.sub_views["systemes_lu"].show_result(txt)
