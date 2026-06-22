#        PUISSANCE 4 — Interface Graphique + IA

import math
import random
import concurrent.futures
from tkinter import *
from tkinter import messagebox

# ============================================================
#   CONSTANTES
# ============================================================

LIGNES      = 6
COLONNES    = 7
TAILLE      = 100          # taille d'une case en pixels
RAYON       = TAILLE // 2 - 8

COULEUR_GRILLE  = "#1565C0"
COULEUR_VIDE    = "#E3F2FD"
COULEUR_X       = "#E53935"   # rouge  pour X (joueur 1)
COULEUR_O       = "#FFD600"   # jaune pour O (joueur 2 / IA)
COULEUR_FOND    = "#0D47A1"

PROFONDEUR_IA = 5

# ============================================================
#   LOGIQUE DU JEU (ton code original)
# ============================================================

def creer_grille():
    return [[" " for _ in range(COLONNES)] for _ in range(LIGNES)]


def jouer_pion(grille, colonne, joueur):
    for ligne in range(LIGNES - 1, -1, -1):
        if grille[ligne][colonne] == " ":
            grille[ligne][colonne] = joueur
            return True
    return False


def alignement_4(grille):

    # Horizontal
    for i in range(LIGNES):
        for j in range(COLONNES - 3):
            if grille[i][j] != " " and \
               grille[i][j] == grille[i][j+1] == grille[i][j+2] == grille[i][j+3]:
                return True

    # Vertical
    for i in range(LIGNES - 3):
        for j in range(COLONNES):
            if grille[i][j] != " " and \
               grille[i][j] == grille[i+1][j] == grille[i+2][j] == grille[i+3][j]:
                return True

    # Diagonale ↘
    for i in range(LIGNES - 3):
        for j in range(COLONNES - 3):
            if grille[i][j] != " " and \
               grille[i][j] == grille[i+1][j+1] == grille[i+2][j+2] == grille[i+3][j+3]:
                return True

    # Diagonale ↙
    for i in range(LIGNES - 3):
        for j in range(3, COLONNES):
            if grille[i][j] != " " and \
               grille[i][j] == grille[i+1][j-1] == grille[i+2][j-2] == grille[i+3][j-3]:
                return True

    return False


def grille_pleine(grille):
    return all(grille[0][c] != " " for c in range(COLONNES))


# ============================================================
#   INTELLIGENCE ARTIFICIELLE (minimax + alpha-bêta)
# ============================================================

def colonnes_disponibles(grille):
    centre = COLONNES // 2
    valides = [c for c in range(COLONNES) if grille[0][c] == " "]
    return sorted(valides, key=lambda c: abs(c - centre))


def copier_grille(grille):
    return [ligne[:] for ligne in grille]


def simuler_coup(grille, colonne, symbole):
    for ligne in range(LIGNES - 1, -1, -1):
        if grille[ligne][colonne] == " ":
            grille[ligne][colonne] = symbole
            return


def evaluer_fenetre(fenetre, symbole_ia, symbole_adverse):
    score = 0
    if fenetre.count(symbole_ia) == 4:
        score += 1000
    elif fenetre.count(symbole_ia) == 3 and fenetre.count(" ") == 1:
        score += 10
    elif fenetre.count(symbole_ia) == 2 and fenetre.count(" ") == 2:
        score += 2
    if fenetre.count(symbole_adverse) == 3 and fenetre.count(" ") == 1:
        score -= 80
    return score


def evaluer_grille_ia(grille, symbole_ia, symbole_adverse):
    score = 0
    col_centre = [grille[l][COLONNES // 2] for l in range(LIGNES)]
    score += col_centre.count(symbole_ia) * 3

    for l in range(LIGNES):
        for c in range(COLONNES - 3):
            score += evaluer_fenetre([grille[l][c+i] for i in range(4)],
                                     symbole_ia, symbole_adverse)
    for c in range(COLONNES):
        for l in range(LIGNES - 3):
            score += evaluer_fenetre([grille[l+i][c] for i in range(4)],
                                     symbole_ia, symbole_adverse)
    for l in range(LIGNES - 3):
        for c in range(COLONNES - 3):
            score += evaluer_fenetre([grille[l+i][c+i] for i in range(4)],
                                     symbole_ia, symbole_adverse)
    for l in range(3, LIGNES):
        for c in range(COLONNES - 3):
            score += evaluer_fenetre([grille[l-i][c+i] for i in range(4)],
                                     symbole_ia, symbole_adverse)
    return score


def minimax(grille, profondeur, alpha, beta, maximisant, symbole_ia, symbole_adverse):
    valides = colonnes_disponibles(grille)
    fini = alignement_4(grille) or len(valides) == 0

    if profondeur == 0 or fini:
        if fini:
            copie_ia = copier_grille(grille)
            for l in range(LIGNES):
                for c in range(COLONNES):
                    if copie_ia[l][c] == symbole_adverse:
                        copie_ia[l][c] = " "
            if alignement_4(copie_ia):
                return (None, 10_000_000)
            elif alignement_4(grille):
                return (None, -10_000_000)
            else:
                return (None, 0)
        return (None, evaluer_grille_ia(grille, symbole_ia, symbole_adverse))

    if maximisant:
        meilleur_score, meilleure_col = -math.inf, valides[0]
        for col in valides:
            copie = copier_grille(grille)
            simuler_coup(copie, col, symbole_ia)
            _, score = minimax(copie, profondeur-1, alpha, beta, False,
                               symbole_ia, symbole_adverse)
            if score > meilleur_score:
                meilleur_score, meilleure_col = score, col
            alpha = max(alpha, meilleur_score)
            if alpha >= beta:
                break
        return meilleure_col, meilleur_score
    else:
        meilleur_score, meilleure_col = math.inf, valides[0]
        for col in valides:
            copie = copier_grille(grille)
            simuler_coup(copie, col, symbole_adverse)
            _, score = minimax(copie, profondeur-1, alpha, beta, True,
                               symbole_ia, symbole_adverse)
            if score < meilleur_score:
                meilleur_score, meilleure_col = score, col
            beta = min(beta, meilleur_score)
            if alpha >= beta:
                break
        return meilleure_col, meilleur_score


def _calcul_coup(grille, symbole_ia, symbole_adverse):
    valides = colonnes_disponibles(grille)
    for col in valides:
        copie = copier_grille(grille)
        simuler_coup(copie, col, symbole_ia)
        if alignement_4(copie):
            return col
    for col in valides:
        copie = copier_grille(grille)
        simuler_coup(copie, col, symbole_adverse)
        if alignement_4(copie):
            return col
    col, _ = minimax(grille, PROFONDEUR_IA, -math.inf, math.inf,
                     True, symbole_ia, symbole_adverse)
    return col


def coup_ia(grille, symbole_ia, symbole_adverse):
    valides = colonnes_disponibles(grille)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futur = executor.submit(_calcul_coup, grille, symbole_ia, symbole_adverse)
        try:
            col = futur.result(timeout=5)
        except concurrent.futures.TimeoutError:
            col = random.choice(valides)
    return col


# ============================================================
#   INTERFACE GRAPHIQUE TKINTER
# ============================================================

class Puissance4App:

    def __init__(self, fenetre, mode):
        self.fenetre  = fenetre
        self.mode     = mode          # "hvh", "hvia", "iavia"
        self.grille   = creer_grille()
        self.joueur   = "X"
        self.partie_finie = False

        fenetre.title("Puissance 4")
        fenetre.configure(bg=COULEUR_FOND)
        fenetre.resizable(False, False)

        # --- Bandeau du haut ---
        self.label_tour = Label(
            fenetre,
            text=self._texte_tour(),
            font=("Arial", 16, "bold"),
            bg=COULEUR_FOND,
            fg="white",
            pady=10
        )
        self.label_tour.pack()

        # --- Canvas (grille) ---
        self.canvas = Canvas(
            fenetre,
            width=COLONNES * TAILLE,
            height=LIGNES  * TAILLE,
            bg=COULEUR_GRILLE,
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=(0, 10))
        self.canvas.bind("<Button-1>", self.clic)

        # --- Bouton rejouer ---
        self.btn_rejouer = Button(
            fenetre,
            text="🔄  Rejouer",
            font=("Arial", 13),
            bg="#1E88E5",
            fg="white",
            relief=FLAT,
            padx=20, pady=8,
            cursor="hand2",
            command=self.rejouer
        )
        self.btn_rejouer.pack(pady=(0, 15))

        self.dessiner_grille()

        # Si l'IA joue en premier (ia_vs_ia), on lance son coup
        if self.mode == "iavia":
            self.fenetre.after(500, self.tour_ia)

    # ----------------------------------------------------------
    def _texte_tour(self):
        if self.partie_finie:
            return ""
        noms = {"hvh": f"Joueur {'Rouge' if self.joueur == 'X' else 'Jaune'}",
                "hvia": "Ton tour" if self.joueur == "X" else "L'IA réfléchit…",
                "iavia": f"IA {'1 (Rouge)' if self.joueur == 'X' else '2 (Jaune)'} réfléchit…"}
        return noms[self.mode]

    def _couleur(self, case):
        if case == "X":
            return COULEUR_X
        if case == "O":
            return COULEUR_O
        return COULEUR_VIDE

    # ----------------------------------------------------------
    def dessiner_grille(self):
        self.canvas.delete("all")
        for l in range(LIGNES):
            for c in range(COLONNES):
                x1 = c * TAILLE + 8
                y1 = l * TAILLE + 8
                x2 = x1 + TAILLE - 16
                y2 = y1 + TAILLE - 16
                self.canvas.create_oval(
                    x1, y1, x2, y2,
                    fill=self._couleur(self.grille[l][c]),
                    outline=""
                )

    # ----------------------------------------------------------
    def clic(self, event):
        """Appelé quand le joueur humain clique sur la grille."""
        if self.partie_finie:
            return
        # Seul le joueur humain peut cliquer
        if self.mode == "hvia" and self.joueur == "O":
            return
        if self.mode == "iavia":
            return

        colonne = event.x // TAILLE
        if 0 <= colonne < COLONNES:
            self.jouer_colonne(colonne)

    # ----------------------------------------------------------
    def jouer_colonne(self, colonne):
        """Fait tomber le pion du joueur actuel dans la colonne choisie."""
        if self.grille[0][colonne] != " ":
            return   # colonne pleine

        jouer_pion(self.grille, colonne, self.joueur)
        self.dessiner_grille()

        # Victoire ?
        if alignement_4(self.grille):
            self.partie_finie = True
            nom = "Rouge" if self.joueur == "X" else "Jaune"
            self.label_tour.config(text=f"🎉 {nom} a gagné !")
            messagebox.showinfo("Fin de partie", f"Le joueur {nom} a gagné !")
            return

        # Match nul ?
        if grille_pleine(self.grille):
            self.partie_finie = True
            self.label_tour.config(text="🤝 Match nul !")
            messagebox.showinfo("Fin de partie", "Match nul !")
            return

        # Changer de joueur
        self.joueur = "O" if self.joueur == "X" else "X"
        self.label_tour.config(text=self._texte_tour())

        # Si le prochain joueur est une IA, on déclenche son tour
        if self.mode == "hvia" and self.joueur == "O":
            self.fenetre.after(400, self.tour_ia)
        elif self.mode == "iavia":
            self.fenetre.after(400, self.tour_ia)

    # ----------------------------------------------------------
    def tour_ia(self):
        """Calcule et joue le coup de l'IA."""
        if self.partie_finie:
            return

        if self.joueur == "O":
            col = coup_ia(self.grille, symbole_ia="O", symbole_adverse="X")
        else:
            col = coup_ia(self.grille, symbole_ia="X", symbole_adverse="O")

        self.jouer_colonne(col)

    # ----------------------------------------------------------
    def rejouer(self):
        """Remet le jeu à zéro."""
        self.grille       = creer_grille()
        self.joueur       = "X"
        self.partie_finie = False
        self.label_tour.config(text=self._texte_tour())
        self.dessiner_grille()

        if self.mode == "iavia":
            self.fenetre.after(500, self.tour_ia)


# ============================================================
#   FENÊTRE DE SÉLECTION DU MODE
# ============================================================

def choisir_mode():
    """Affiche une petite fenêtre pour choisir le mode de jeu."""
    menu = Tk()
    menu.title("Puissance 4 — Mode de jeu")
    menu.configure(bg=COULEUR_FOND)
    menu.resizable(False, False)

    mode_choisi = [None]   # liste pour pouvoir modifier depuis les lambdas

    Label(menu, text="Puissance 4", font=("Arial", 24, "bold"),
          bg=COULEUR_FOND, fg="white").pack(pady=(30, 5))
    Label(menu, text="Choisis un mode de jeu",
          font=("Arial", 13), bg=COULEUR_FOND, fg="#90CAF9").pack(pady=(0, 25))

    style = {"font": ("Arial", 13), "bg": "#1E88E5", "fg": "white",
             "relief": FLAT, "padx": 30, "pady": 12, "cursor": "hand2",
             "width": 22}

    def choisir(mode):
        mode_choisi[0] = mode
        menu.destroy()

    Button(menu, text="👥  Humain vs Humain",
           command=lambda: choisir("hvh"),  **style).pack(pady=6)
    Button(menu, text="🤖  Humain vs IA",
           command=lambda: choisir("hvia"), **style).pack(pady=6)
    Button(menu, text="🤖🤖  IA vs IA",
           command=lambda: choisir("iavia"),**style).pack(pady=6)

    Label(menu, text="", bg=COULEUR_FOND).pack(pady=10)

    menu.mainloop()
    return mode_choisi[0]


# ============================================================
#   LANCEMENT
# ============================================================

if __name__ == "__main__":
    mode = choisir_mode()
    if mode:
        fenetre = Tk()
        Puissance4App(fenetre, mode)
        fenetre.mainloop()