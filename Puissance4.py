
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
        print("🤝 Match nul" )

from tkinter import *
from tkinter import messagebox

LIGNES = 6
COLONNES = 7
TAILLE = 80

grille = [[" " for _ in range(COLONNES)] for _ in range(LIGNES)]
joueur = "X"

fenetre = Tk()
fenetre.title("Puissance 4")

canvas = Canvas(fenetre,
                width=COLONNES * TAILLE,
                height=LIGNES * TAILLE,
                bg="blue")
canvas.pack()


def dessiner_grille():
    canvas.delete("all")

    for ligne in range(LIGNES):
        for colonne in range(COLONNES):

            x1 = colonne * TAILLE
            y1 = ligne * TAILLE
            x2 = x1 + TAILLE
            y2 = y1 + TAILLE

            # Couleur du pion
            couleur = "white"

            if grille[ligne][colonne] == "X":
                couleur = "red"
            elif grille[ligne][colonne] == "O":
                couleur = "yellow"

            canvas.create_oval(
                x1 + 5,
                y1 + 5,
                x2 - 5,
                y2 - 5,
                fill=couleur
            )


def jouer(colonne):
    global joueur

    # Le pion tombe
    for ligne in range(LIGNES - 1, -1, -1):
        if grille[ligne][colonne] == " ":
            grille[ligne][colonne] = joueur

            dessiner_grille()

            if alignement_4():
                messagebox.showinfo(
                    "Fin de partie",
                    f"Le joueur {joueur} a gagné !"
                )
                return

            # Changement de joueur
            if joueur == "X":
                joueur = "O"
            else:
                joueur = "X"

            return


def alignement_4():

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


def clic(event):
    colonne = event.x // TAILLE

    if 0 <= colonne < COLONNES:
        jouer(colonne)


# Quand on clique sur la grille
canvas.bind("<Button-1>", clic)

dessiner_grille()

fenetre.mainloop()
