#        PUISSANCE 4

def creer_grille():
    return [[" " for _ in range(7)] for _ in range(6)]


# Affichage de la grille
def afficher_grille(grille):

    print("+---" * 7 + "+")

    for ligne in grille:

        print("|", end="")

        for case in ligne:

            if case == " ":
                print("   |", end="")
            else:
                print(f" {case} |", end="")

        print()
        print("+---" * 7 + "+")

    print("  0   1   2   3   4   5   6")
    print()


# Fait tomber un pion dans une colonne
def jouer(grille, colonne, joueur):

    # On part du bas de la grille
    for ligne in range(5, -1, -1):

        # On cherche la première case vide
        if grille[ligne][colonne] == " ":
            grille[ligne][colonne] = joueur
            return True

    # La colonne est pleine
    return False


# Vérifie s'il y a 4 pions alignés
def alignement_4(grille):

    # Horizontal
    for i in range(6):
        for j in range(4):

            if grille[i][j] != " " and \
               grille[i][j] == grille[i][j + 1] == grille[i][j + 2] == grille[i][j + 3]:

                return True

    # Vertical
    for i in range(3):
        for j in range(7):

            if grille[i][j] != " " and \
               grille[i][j] == grille[i + 1][j] == grille[i + 2][j] == grille[i + 3][j]:

                return True

    # Diagonale ↘
    for i in range(3):
        for j in range(4):

            if grille[i][j] != " " and \
               grille[i][j] == grille[i + 1][j + 1] == grille[i + 2][j + 2] == grille[i + 3][j + 3]:

                return True

    # Diagonale ↙
    for i in range(3):
        for j in range(3, 7):

            if grille[i][j] != " " and \
               grille[i][j] == grille[i + 1][j - 1] == grille[i + 2][j - 2] == grille[i + 3][j - 3]:

                return True

    return False


# Vérifie si la grille est pleine
def grille_pleine(grille):

    for colonne in range(7):

        if grille[0][colonne] == " ":
            return False

    return True


# ==========================
#    PROGRAMME PRINCIPAL
# ==========================
def main():
    grille = creer_grille()

    joueur = "X"

    while not alignement_4(grille) and not grille_pleine(grille):

        afficher_grille(grille)

        try:
            colonne = int(
                input(f"Joueur {joueur}, choisis une colonne (0 à 6) : ")
            )

            if 0 <= colonne <= 6:

                if jouer(grille, colonne, joueur):

                    # Changement de joueur
                    if joueur == "X":
                        joueur = "O"
                    else:
                        joueur = "X"

                else:
                    print("Cette colonne est pleine !")

            else:
                print("Veuillez choisir une colonne entre 0 et 6.")

        except ValueError:
            print("Veuillez entrer un nombre.")

    # ==========================
    #      FIN DE PARTIE
    # ==========================

    afficher_grille(grille)

    if alignement_4(grille):

        # Le joueur a déjà changé après le dernier coup
        if joueur == "X":
            print("🎉 Le joueur O a gagné !")
        else:
            print("🎉 Le joueur X a gagné !")

    else:
        print("🤝 Match nul")


# ============================================================
#   BLOC IA  — AJOUT UNIQUEMENT, CODE ORIGINAL NON MODIFIÉ
# ============================================================

import math
import random
import concurrent.futures

LIGNES_IA  = 6   # nombre de lignes de ta grille
COLONNES_IA = 7  # nombre de colonnes de ta grille
PROFONDEUR_IA = 6  # profondeur de recherche (plus c'est haut = plus fort mais plus lent)


def colonnes_disponibles(grille):
    """Renvoie les colonnes jouables, triées du centre vers les bords."""
    centre = COLONNES_IA // 2
    valides = [c for c in range(COLONNES_IA) if grille[0][c] == " "]
    return sorted(valides, key=lambda c: abs(c - centre))


def copier_grille_ia(grille):
    """Crée une copie indépendante de la grille pour les simulations."""
    return [ligne[:] for ligne in grille]


def simuler_coup(grille, colonne, symbole):
    """Fait tomber un pion dans la copie de la grille (même logique que jouer())."""
    for ligne in range(LIGNES_IA - 1, -1, -1):
        if grille[ligne][colonne] == " ":
            grille[ligne][colonne] = symbole
            return


def evaluer_fenetre(fenetre, symbole_ia, symbole_adverse):
    """
    Donne un score à une suite de 4 cases.
    Plus le score est élevé, mieux c'est pour l'IA.
    """
    score = 0

    if fenetre.count(symbole_ia) == 4:
        score += 1000                                          # victoire IA
    elif fenetre.count(symbole_ia) == 3 and fenetre.count(" ") == 1:
        score += 10                                            # 3 pions IA alignés
    elif fenetre.count(symbole_ia) == 2 and fenetre.count(" ") == 2:
        score += 2                                             # 2 pions IA alignés

    if fenetre.count(symbole_adverse) == 3 and fenetre.count(" ") == 1:
        score -= 80                                            # l'adversaire menace

    return score


def evaluer_grille_ia(grille, symbole_ia, symbole_adverse):
    """Calcule un score global de la grille du point de vue de l'IA."""
    score = 0

    # Bonus pour les pions au centre (le centre offre plus de possibilités)
    colonne_centre = [grille[l][COLONNES_IA // 2] for l in range(LIGNES_IA)]
    score += colonne_centre.count(symbole_ia) * 3

    # Analyse de toutes les fenêtres horizontales
    for l in range(LIGNES_IA):
        for c in range(COLONNES_IA - 3):
            fenetre = [grille[l][c + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, symbole_ia, symbole_adverse)

    # Analyse de toutes les fenêtres verticales
    for c in range(COLONNES_IA):
        for l in range(LIGNES_IA - 3):
            fenetre = [grille[l + i][c] for i in range(4)]
            score += evaluer_fenetre(fenetre, symbole_ia, symbole_adverse)

    # Analyse de toutes les diagonales ↘
    for l in range(LIGNES_IA - 3):
        for c in range(COLONNES_IA - 3):
            fenetre = [grille[l + i][c + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, symbole_ia, symbole_adverse)

    # Analyse de toutes les diagonales ↙
    for l in range(3, LIGNES_IA):
        for c in range(COLONNES_IA - 3):
            fenetre = [grille[l - i][c + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, symbole_ia, symbole_adverse)

    return score


def minimax(grille, profondeur, alpha, beta, maximisant, symbole_ia, symbole_adverse):
    """
    Explore tous les coups possibles en avance et renvoie (meilleure_colonne, meilleur_score).
    """
    valides = colonnes_disponibles(grille)
    partie_finie = alignement_4(grille) or len(valides) == 0

    # --- Cas d'arrêt ---
    if profondeur == 0 or partie_finie:
        if partie_finie:
            if alignement_4(grille):
                # On regarde qui a gagné en cherchant le dernier symbole joué
                if any(grille[l][c] == symbole_ia
                       for l in range(LIGNES_IA) for c in range(COLONNES_IA)
                       if grille[l][c] == symbole_ia):
                    # Pour savoir qui a gagné, on teste chacun
                    copie_test = copier_grille_ia(grille)
                    if alignement_4(copie_test):
                        # on vérifie en retirant temporairement les pions adverses
                        pass
                # Simplification : si la partie est finie avec alignement,
                # on renvoie un grand score positif si l'IA a aligné 4, négatif sinon
                grille_sans_adverse = copier_grille_ia(grille)
                for l in range(LIGNES_IA):
                    for c in range(COLONNES_IA):
                        if grille_sans_adverse[l][c] == symbole_adverse:
                            grille_sans_adverse[l][c] = " "
                if alignement_4(grille_sans_adverse):
                    return (None, 10_000_000)   # l'IA a gagné
                else:
                    return (None, -10_000_000)  # l'adversaire a gagné
            else:
                return (None, 0)  # grille pleine, match nul
        else:
            return (None, evaluer_grille_ia(grille, symbole_ia, symbole_adverse))

    # --- Tour de l'IA (elle maximise son score) ---
    if maximisant:
        meilleur_score = -math.inf
        meilleure_col  = valides[0]
        for col in valides:
            copie = copier_grille_ia(grille)
            simuler_coup(copie, col, symbole_ia)
            _, score = minimax(copie, profondeur - 1, alpha, beta,
                               False, symbole_ia, symbole_adverse)
            if score > meilleur_score:
                meilleur_score = score
                meilleure_col  = col
            alpha = max(alpha, meilleur_score)
            if alpha >= beta:
                break   # élagage : on coupe les branches inutiles
        return meilleure_col, meilleur_score

    # --- Tour de l'adversaire (il minimise le score de l'IA) ---
    else:
        meilleur_score = math.inf
        meilleure_col  = valides[0]
        for col in valides:
            copie = copier_grille_ia(grille)
            simuler_coup(copie, col, symbole_adverse)
            _, score = minimax(copie, profondeur - 1, alpha, beta,
                               True, symbole_ia, symbole_adverse)
            if score < meilleur_score:
                meilleur_score = score
                meilleure_col  = col
            beta = min(beta, meilleur_score)
            if alpha >= beta:
                break   # élagage
        return meilleure_col, meilleur_score


def _calcul_coup(grille, symbole_ia, symbole_adverse):
    """
    Calcul interne du meilleur coup (tourne dans un thread séparé avec limite de temps).
    """
    valides = colonnes_disponibles(grille)

    # 1. L'IA peut-elle gagner immédiatement ?
    for col in valides:
        copie = copier_grille_ia(grille)
        simuler_coup(copie, col, symbole_ia)
        if alignement_4(copie):
            return col

    # 2. L'adversaire va-t-il gagner au prochain coup ? On bloque.
    for col in valides:
        copie = copier_grille_ia(grille)
        simuler_coup(copie, col, symbole_adverse)
        if alignement_4(copie):
            return col

    # 3. Sinon on lance minimax pour trouver le meilleur coup stratégique
    col, _ = minimax(grille, PROFONDEUR_IA, -math.inf, math.inf,
                     True, symbole_ia, symbole_adverse)
    return col


def coup_ia(grille, symbole_ia, symbole_adverse):
    """
    Lance le calcul dans un thread avec une limite de 5 secondes.
    Si l'IA ne répond pas à temps → elle joue une colonne aléatoire.
    """
    valides = colonnes_disponibles(grille)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futur = executor.submit(_calcul_coup, grille, symbole_ia, symbole_adverse)
        try:
            col = futur.result(timeout=5)        # attend max 5 secondes
        except concurrent.futures.TimeoutError:
            col = random.choice(valides)         # temps écoulé → coup aléatoire
            print("⏱️ L'IA a dépassé les 5 secondes, elle joue au hasard !")

    return col


# ============================================================
#   BOUCLE DE JEU AVEC IA (mode console)
# ============================================================

def play(grille, mode="humain_vs_ia"):
    """
    Lance une partie en console.
    mode = "humain_vs_ia"  → joueur 1 (X) humain, joueur 2 (O) IA
    mode = "ia_vs_ia"      → les deux joueurs sont des IA
    mode = "humain_vs_humain" → deux joueurs humains
    """
    joueur = "X"

    while not alignement_4(grille) and not grille_pleine(grille):

        afficher_grille(grille)

        # --- Choix de la colonne selon qui joue ---
        if mode == "humain_vs_humain":
            col = int(input(f"Joueur {joueur}, choisis une colonne (0-6) : "))

        elif mode == "humain_vs_ia":
            if joueur == "X":
                col = int(input(f"Joueur {joueur}, choisis une colonne (0-6) : "))
            else:
                print("L'IA réfléchit...")
                col = coup_ia(grille, symbole_ia="O", symbole_adverse="X")
                print(f"L'IA joue la colonne {col}")

        elif mode == "ia_vs_ia":
            if joueur == "X":
                print("IA 1 (X) réfléchit...")
                col = coup_ia(grille, symbole_ia="X", symbole_adverse="O")
                print(f"IA 1 joue la colonne {col}")
            else:
                print("IA 2 (O) réfléchit...")
                col = coup_ia(grille, symbole_ia="O", symbole_adverse="X")
                print(f"IA 2 joue la colonne {col}")

        # --- On fait tomber le pion ---
        jouer(grille, col, joueur)

        # --- On change de joueur ---
        joueur = "O" if joueur == "X" else "X"

    # --- Fin de partie ---
    afficher_grille(grille)

    if alignement_4(grille):
        gagnant = "O" if joueur == "X" else "X"
        print(f"🎉 Le joueur {gagnant} a gagné !")
    else:
        print("🤝 Match nul !")


# ============================================================
#   LANCEMENT
# ============================================================

if __name__ == "__main__":
    print("=== PUISSANCE 4 ===")
    print("1 - Humain vs Humain")
    print("2 - Humain vs IA")
    print("3 - IA vs IA")
    choix = input("Choisis un mode (1, 2 ou 3) : ")

    grille = creer_grille()

    if choix == "1":
        play(grille, mode="humain_vs_humain")
    elif choix == "2":
        play(grille, mode="humain_vs_ia")
    elif choix == "3":
        play(grille, mode="ia_vs_ia")
    else:
        print("Choix invalide.")
