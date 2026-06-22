"""
Jeu Puissance 4 - Joueur humain VS IA (algorithme Minimax + élagage alpha-bêta)
Grille : 6 colonnes x 7 lignes
"""

import math

LIGNES = 7
COLONNES = 6
PROFONDEUR_IA = 7  # plus c'est grand, plus l'IA est forte (et lente)


# ---------------------------------------------------------
# GESTION DE LA GRILLE
# ---------------------------------------------------------

def creer_grille():
    return [['.' for _ in range(COLONNES)] for _ in range(LIGNES)]


def afficher_grille(grille):
    print()
    print(" " + " ".join(str(c) for c in range(COLONNES)))
    for ligne in grille:
        print("|" + "|".join(ligne) + "|")
    print()


def colonnes_valides(grille):
    return [c for c in range(COLONNES) if grille[0][c] == '.']


def colonnes_valides_triees(grille):
    """
    Renvoie les colonnes jouables, triées du centre vers les bords.
    Explorer les bonnes colonnes en premier rend l'élagage alpha-bêta
    beaucoup plus efficace (on coupe plus de branches, plus vite).
    """
    centre = COLONNES // 2
    valides = colonnes_valides(grille)
    return sorted(valides, key=lambda c: abs(c - centre))


def copier_grille(grille):
    return [ligne[:] for ligne in grille]


def jouer_coup(grille, col, symbole):
    """Place le pion dans la première case libre en partant du bas (gravité)."""
    for ligne in range(LIGNES - 1, -1, -1):
        if grille[ligne][col] == '.':
            grille[ligne][col] = symbole
            return


# ---------------------------------------------------------
# VERIFICATION DE VICTOIRE
# ---------------------------------------------------------

def verifier_victoire(grille, symbole):
    # Horizontal
    for l in range(LIGNES):
        for c in range(COLONNES - 3):
            if all(grille[l][c + i] == symbole for i in range(4)):
                return True

    # Vertical
    for l in range(LIGNES - 3):
        for c in range(COLONNES):
            if all(grille[l + i][c] == symbole for i in range(4)):
                return True

    # Diagonale descendante (\)
    for l in range(LIGNES - 3):
        for c in range(COLONNES - 3):
            if all(grille[l + i][c + i] == symbole for i in range(4)):
                return True

    # Diagonale montante (/)
    for l in range(3, LIGNES):
        for c in range(COLONNES - 3):
            if all(grille[l - i][c + i] == symbole for i in range(4)):
                return True

    return False


def partie_terminee(grille):
    return (
        verifier_victoire(grille, 'X')
        or verifier_victoire(grille, 'O')
        or len(colonnes_valides(grille)) == 0
    )


# ---------------------------------------------------------
# INTELLIGENCE ARTIFICIELLE (MINIMAX + ALPHA-BETA)
# ---------------------------------------------------------

def evaluer_fenetre(fenetre, symbole_ia, symbole_adverse):
    score = 0

    if fenetre.count(symbole_ia) == 4:
        score += 1000
    elif fenetre.count(symbole_ia) == 3 and fenetre.count('.') == 1:
        score += 10
    elif fenetre.count(symbole_ia) == 2 and fenetre.count('.') == 2:
        score += 2

    if fenetre.count(symbole_adverse) == 3 and fenetre.count('.') == 1:
        score -= 80

    return score


def evaluer_grille(grille, symbole_ia, symbole_adverse):
    score = 0

    # Bonus pour le centre
    colonne_centrale = [grille[l][COLONNES // 2] for l in range(LIGNES)]
    score += colonne_centrale.count(symbole_ia) * 3

    # Horizontal
    for l in range(LIGNES):
        for c in range(COLONNES - 3):
            fenetre = [grille[l][c + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, symbole_ia, symbole_adverse)

    # Vertical
    for c in range(COLONNES):
        for l in range(LIGNES - 3):
            fenetre = [grille[l + i][c] for i in range(4)]
            score += evaluer_fenetre(fenetre, symbole_ia, symbole_adverse)

    # Diagonale descendante (\)
    for l in range(LIGNES - 3):
        for c in range(COLONNES - 3):
            fenetre = [grille[l + i][c + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, symbole_ia, symbole_adverse)

    # Diagonale montante (/)
    for l in range(3, LIGNES):
        for c in range(COLONNES - 3):
            fenetre = [grille[l - i][c + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, symbole_ia, symbole_adverse)

    return score


def minimax(grille, profondeur, alpha, beta, maximisant, symbole_ia, symbole_adverse):
    valides = colonnes_valides_triees(grille)
    fini = partie_terminee(grille)

    if profondeur == 0 or fini:
        if fini:
            if verifier_victoire(grille, symbole_ia):
                return (None, 10_000_000)
            elif verifier_victoire(grille, symbole_adverse):
                return (None, -10_000_000)
            else:
                return (None, 0)
        else:
            return (None, evaluer_grille(grille, symbole_ia, symbole_adverse))

    if maximisant:
        meilleur_score = -math.inf
        meilleure_col = valides[0]
        for col in valides:
            copie = copier_grille(grille)
            jouer_coup(copie, col, symbole_ia)
            _, score = minimax(copie, profondeur - 1, alpha, beta, False,
                                symbole_ia, symbole_adverse)
            if score > meilleur_score:
                meilleur_score = score
                meilleure_col = col
            alpha = max(alpha, meilleur_score)
            if alpha >= beta:
                break
        return meilleure_col, meilleur_score

    else:
        meilleur_score = math.inf
        meilleure_col = valides[0]
        for col in valides:
            copie = copier_grille(grille)
            jouer_coup(copie, col, symbole_adverse)
            _, score = minimax(copie, profondeur - 1, alpha, beta, True,
                                symbole_ia, symbole_adverse)
            if score < meilleur_score:
                meilleur_score = score
                meilleure_col = col
            beta = min(beta, meilleur_score)
            if alpha >= beta:
                break
        return meilleure_col, meilleur_score


def meilleur_coup_ia(grille, symbole_ia, symbole_adverse, profondeur=PROFONDEUR_IA):
    valides = colonnes_valides_triees(grille)

    # 1. Si l'IA peut gagner immédiatement, elle le fait (pas besoin de minimax)
    for col in valides:
        copie = copier_grille(grille)
        jouer_coup(copie, col, symbole_ia)
        if verifier_victoire(copie, symbole_ia):
            return col

    # 2. Si l'adversaire peut gagner au prochain coup, on bloque immédiatement
    for col in valides:
        copie = copier_grille(grille)
        jouer_coup(copie, col, symbole_adverse)
        if verifier_victoire(copie, symbole_adverse):
            return col

    # 3. Sinon, on lance le minimax complet pour trouver le meilleur coup stratégique
    col, _ = minimax(grille, profondeur, -math.inf, math.inf, True,
                      symbole_ia, symbole_adverse)
    return col


# ---------------------------------------------------------
# BOUCLE DE JEU
# ---------------------------------------------------------

def demander_colonne_humain(joueur, grille):
    while True:
        choix = input(f"Joueur {joueur}, choisis une colonne (0-{COLONNES-1}) : ")
        if not choix.isdigit():
            print("Merci d'entrer un nombre valide.")
            continue
        col = int(choix)
        if col < 0 or col >= COLONNES:
            print(f"La colonne doit être entre 0 et {COLONNES-1}.")
            continue
        if grille[0][col] != '.':
            print("Cette colonne est déjà pleine, choisis-en une autre.")
            continue
        return col
    