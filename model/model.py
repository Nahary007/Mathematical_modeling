import numpy as np
import pulp
from sklearn.linear_model import LinearRegression
import itertools

class Model:
    """Modèle : contient les données et la logique métier."""

    def __init__(self):
        self.messages = {
            "home": "Modélisation Mathématiques",
            "systemes_lineaires": "Systèmes linéaires",
            "programmation_lineaire": "Programmation linéaire",
            "regression_lineaire": "Régression linéaire",
            "systemes_lu": "Méthode LU",
            "systemes_gauss": "Méthode de Gauss"
        }
        self.current_section = "home"
        # Données régression
        self.x_reg = None
        self.y_reg = None
        self.reg_model = None
        self.a = None
        self.b = None
        self.r = None

    def get_message(self, section=None):
        if section:
            self.current_section = section
        return self.messages.get(self.current_section, self.messages["home"])

    def get_sections(self):
        return list(self.messages.keys())

    def compute_lu(self, A, B):
        """Décomposition LU et résolution."""
        n = 3
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]
        for i in range(n):
            L[i][i] = 1.0
        U[0] = A[0][:]
        if abs(U[0][0]) < 1e-10:
            raise ValueError("Pivot nul en position (1,1). Échange de lignes requis.")
        L[1][0] = A[1][0] / U[0][0]
        L[2][0] = A[2][0] / U[0][0]
        U[1][1] = A[1][1] - L[1][0] * U[0][1]
        U[1][2] = A[1][2] - L[1][0] * U[0][2]
        if abs(U[1][1]) < 1e-10:
            raise ValueError("Pivot nul en position (2,2).")
        L[2][1] = (A[2][1] - L[2][0] * U[0][1]) / U[1][1]
        U[2][2] = A[2][2] - L[2][0] * U[0][2] - L[2][1] * U[1][2]
        if abs(U[2][2]) < 1e-10:
            raise ValueError("Pivot nul en position (3,3).")
        # Descente (LY = B)
        Y = [0.0] * n
        Y[0] = B[0]
        Y[1] = B[1] - L[1][0] * Y[0]
        Y[2] = B[2] - L[2][0] * Y[0] - L[2][1] * Y[1]
        # Remontée (UX = Y)
        X = [0.0] * n
        X[2] = Y[2] / U[2][2]
        X[1] = (Y[1] - U[1][2] * X[2]) / U[1][1]
        X[0] = (Y[0] - U[0][1] * X[1] - U[0][2] * X[2]) / U[0][0]
        # Format txt
        txt = "=== L ===\n"
        for row in L:
            txt += " ".join(f"{v:7.4f}" for v in row) + "\n"
        txt += "\n=== U ===\n"
        for row in U:
            txt += " ".join(f"{v:7.4f}" for v in [row[0]] + row[1:]) + "\n"  # U sous-diag 0
        txt += "\n=== Y (LY = B) ===\n" + " ".join(f"{v:7.4f}" for v in Y) + "\n"
        txt += "\n=== X (solution) ===\n" + " ".join(f"{v:7.4f}" for v in X) + "\n"
        return txt

    def compute_gauss(self, A, B):
        """Élimination de Gauss avec pivots."""
        A = [row[:] for row in A]
        B = B[:]
        n = 3
        txt = "=== Matrice augmentée initiale ===\n"
        for i in range(n):
            txt += " | ".join(f"{A[i][j]:7.4f}" for j in range(n)) + f" | {B[i]:7.4f}\n"
        txt += "\n"
        # Pivot 1
        if abs(A[0][0]) < 1e-10:
            swapped = False
            for k in range(1, n):
                if abs(A[k][0]) >= 1e-10:
                    A[0], A[k] = A[k], A[0]
                    B[0], B[k] = B[k], B[0]
                    txt += f"--> Échange ligne 1 ↔ {k+1}\n"
                    swapped = True
                    break
            if not swapped:
                raise ValueError("Pivot nul ligne 1, système impossible.")
        # Élimination colonne 1
        for i in range(1, n):
            factor = A[i][0] / A[0][0]
            for j in range(n):
                A[i][j] -= factor * A[0][j]
            B[i] -= factor * B[0]
            txt += f"--> Ligne {i+1} -= {factor:.4f} × ligne 1\n"
        # Pivot 2
        if abs(A[1][1]) < 1e-10:
            if abs(A[2][1]) >= 1e-10:
                A[1], A[2] = A[2], A[1]
                B[1], B[2] = B[2], B[1]
                txt += "--> Échange ligne 2 ↔ 3\n"
            else:
                raise ValueError("Pivot nul ligne 2.")
        # Élimination colonne 2
        factor = A[2][1] / A[1][1]
        for j in range(n):
            A[2][j] -= factor * A[1][j]
        B[2] -= factor * B[1]
        txt += f"--> Ligne 3 -= {factor:.4f} × ligne 2\n"
        # Pivot 3
        if abs(A[2][2]) < 1e-10:
            raise ValueError("Pivot nul ligne 3.")
        txt += "\n=== Matrice triangulaire supérieure ===\n"
        for i in range(n):
            txt += " | ".join(f"{A[i][j]:7.4f}" for j in range(n)) + f" | {B[i]:7.4f}\n"
        # Substitution arrière
        X = [0.0] * n
        X[2] = B[2] / A[2][2]
        X[1] = (B[1] - A[1][2] * X[2]) / A[1][1]
        X[0] = (B[0] - A[0][1] * X[1] - A[0][2] * X[2]) / A[0][0]
        txt += f"\n=== Solution X ===\nx1 = {X[0]:.4f}, x2 = {X[1]:.4f}, x3 = {X[2]:.4f}\n"
        return txt

    def compute_graphic(self, objectif, eq_obj, contraintes_input):
        """Méthode graphique pour PL."""
        # Parsing objectif
        eq_obj = eq_obj.replace("Z=", "").replace(" ", "").upper().replace("-", "+-")
        terms = [t.strip() for t in eq_obj.split("+") if t.strip()]
        aX = 0.0
        aY = 0.0
        for t in terms:
            if "X" in t:
                coef_str = t.replace("X", "").strip()
                aX = 1.0 if coef_str in ["", "+"] else -1.0 if coef_str == "-" else float(coef_str)
            if "Y" in t:
                coef_str = t.replace("Y", "").strip()
                aY = 1.0 if coef_str in ["", "+"] else -1.0 if coef_str == "-" else float(coef_str)
        if aX == 0 and aY == 0:
            raise ValueError("Fonction objectif invalide (ex: 3X + 2Y).")
        # Parsing contraintes
        droites = []
        for c in contraintes_input:
            c = c.replace(" ", "").upper()
            if "<=" in c:
                gauche, droite_str = c.split("<=")
                ineq = "<="
            elif ">=" in c:
                gauche, droite_str = c.split(">=")
                ineq = ">="
            elif "=" in c:
                gauche, droite_str = c.split("=")
                ineq = "="
            else:
                raise ValueError(f"Contrainte invalide : {c}")
            cst = float(droite_str)
            gauche = gauche.replace("-", "+-")
            terms_c = [t.strip() for t in gauche.split("+") if t.strip()]
            a = 0.0
            b = 0.0
            for t in terms_c:
                if "X" in t:
                    coef_str = t.replace("X", "").strip()
                    a = 1.0 if coef_str in ["", "+"] else -1.0 if coef_str == "-" else float(coef_str)
                if "Y" in t:
                    coef_str = t.replace("Y", "").strip()
                    b = 1.0 if coef_str in ["", "+"] else -1.0 if coef_str == "-" else float(coef_str)
            droites.append((a, b, cst, ineq))
        # Intersections
        points = []
        for comb in itertools.combinations(range(len(droites)), 2):
            i, j = comb
            a1, b1, c1, _ = droites[i]
            a2, b2, c2, _ = droites[j]
            det = a1 * b2 - a2 * b1
            if abs(det) > 1e-6:
                px = (c1 * b2 - c2 * b1) / det
                py = (a1 * c2 - a2 * c1) / det
                if px >= 0 and py >= 0:
                    points.append((px, py))
        def respecte_contraintes(px, py):
            for a, b, c, ineq in droites:
                val = a * px + b * py
                if ineq == "<=" and val > c + 1e-6: return False
                if ineq == ">=" and val < c - 1e-6: return False
                if ineq == "=" and abs(val - c) > 1e-6: return False
            return True
        points_valides = [p for p in points if respecte_contraintes(*p)]
        if not points_valides:
            raise ValueError("Aucune région faisable détectée.")
        Z_vals = [aX * px + aY * py for px, py in points_valides]
        idx = np.argmax(Z_vals) if objectif == "max" else np.argmin(Z_vals)
        best_point = points_valides[idx]
        best_val = Z_vals[idx]
        # Text
        text = "=== Sommets faisables ===\n"
        for i, (p, z) in enumerate(zip(points_valides, Z_vals), 1):
            text += f"Point {i} ({p[0]:.2f}, {p[1]:.2f}) → Z = {z:.2f}\n"
        text += f"\n>>> {'Maximum' if objectif == 'max' else 'Minimum'} : Z = {best_val:.2f}\n"
        text += f"au point (X = {best_point[0]:.2f}, Y = {best_point[1]:.2f})\n"
        return {
            'text': text,
            'droites': droites,
            'points_valides': points_valides,
            'best_point': best_point,
            'aX': aX,
            'aY': aY
        }

    def compute_simplex(self, a1, a2, c1x1, c1x2, c1b, c2x1, c2x2, c2b):
        """Résolution Simplexe (2 var, 2 constr)."""
        prob = pulp.LpProblem("Simplexe", pulp.LpMaximize)
        x1 = pulp.LpVariable('x1', lowBound=0)
        x2 = pulp.LpVariable('x2', lowBound=0)
        prob += a1 * x1 + a2 * x2, "Z"
        prob += c1x1 * x1 + c1x2 * x2 <= c1b
        prob += c2x1 * x1 + c2x2 * x2 <= c2b
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        if prob.status != pulp.LpStatusOptimal:
            raise ValueError(f"Problème non optimal : {pulp.LpStatus[prob.status]}")
        return (
            f"Statut : {pulp.LpStatus[prob.status]}\n"
            f"x1 = {x1.value():.2f}\n"
            f"x2 = {x2.value():.2f}\n"
            f"Valeur optimale de Z = {prob.objective.value():.2f}"
        )

    def compute_regression_stats(self, x, y):
        """Statistiques descriptives."""
        mx = np.mean(x)
        my = np.mean(y)
        vx = np.var(x, ddof=1)
        vy = np.var(y, ddof=1)
        cov = np.cov(x, y, ddof=1)[0, 1]
        r = np.corrcoef(x, y)[0, 1]
        return (
            f"Moyenne de x : {mx:.4f}\n"
            f"Moyenne de y : {my:.4f}\n"
            f"Variance de x : {vx:.4f}\n"
            f"Variance de y : {vy:.4f}\n"
            f"Covariance(x, y) : {cov:.4f}\n"
            f"Coefficient de corrélation (r) : {r:.4f}\n"
        )

    def fit_regression_model(self, x, y):
        """Ajustement du modèle linéaire."""
        resh = x.reshape(-1, 1)
        self.reg_model = LinearRegression().fit(resh, y)
        self.a = self.reg_model.coef_[0]
        self.b = self.reg_model.intercept_
        self.r = np.corrcoef(x, y)[0, 1]