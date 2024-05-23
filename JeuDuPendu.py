# -------------------------------------------------------------------------- #
                            #SCRIPT JEU DU PENDU#
# -------------------------------------------------------------------------- #
# Emilio Scottu
# MGA-802

# Ce script permet à tout utilisateur qui l'exécute de jouer au jeu du pendu
# Le format du fichier de mots accepté est le .txt

# Pour tous les choix proposés au cours du jeu, si l'utilisateur donne une
# réponse non attendue, un mode par défaut est configuré.


# -------------------------------------------------------------------------- #
                            #ZONE D'IMPORTATION#
# -------------------------------------------------------------------------- #
from random import choice
import os.path
import unicodedata


# -------------------------------------------------------------------------- #
                            #FONCTION LAUNCHSCREEN#
# -------------------------------------------------------------------------- #
def accueil_jeu_du_pendu():
    print(" _______________________________________")
    print("|              Bonjour                  |")
    print("|    bienvenue sur le jeu du pendu      |")
    print("|                                       |")
    print("|  Souhaitez vous lancer une partie ?   |")
    print("|                                       |")
    print("|     oui(tapez 0)   non(tapez 1)       |")
    print("|                                       |")
    reponse = input("-->")

    if reponse == "0":
        demarrage_jeu_du_pendu()
    else:
        return

# -------------------------------------------------------------------------- #
               #FONCTION CONTENANT LA BOUCLE PRINCIPALE DU JEU#
# -------------------------------------------------------------------------- #
def demarrage_jeu_du_pendu():
    etat = 0
    compteur_bonne_lettre = 0
    liste_propositions = []

    # BONUS : choix de la difficulté (avec aide ou non)
    print("|   sélectionner votre difficulté       |")
    print("| normal(sans aide)   facile(avec aide) |")
    difficulte = set_difficulte(input("-->"))
    print("┌---------------------------------------┐")
    print(f"| lancement de la partie en mode {difficulte} |")
    print("└---------------------------------------┘")

    # choix d'un mot dans le fichier de jeu (personnel ou par défaut)
    print("|    souhaitez vous utiliser votre      |")
    print("|       propre fichier de mots?         |")
    print("| oui(notez son nom) non(laissez vide)  |")
    mot = selection_mot_fichier(input("-->"))
    nombre_lettres = len(mot)
    mot_sans_accent = unicodedata.normalize('NFD', mot).encode(encoding='ASCII', errors='ignore').decode('utf8')

    # génération du mot caché de la longueur du mot à deviner
    mot_cache = "_" * nombre_lettres
    print("┌---------------------------------------┐")
    print("|         le mot a été choisi           |")
    print("└---------------------------------------┘")

    # Verification s'il y a des tirets ou apostrophe dans le mot + leur affichage (cas particuliers ex :arc-en-ciel)
    if mot_sans_accent.count("-") != 0:
        mot_cache = update_mot_cache(mot, "-", mot_cache)
        compteur_bonne_lettre += mot_sans_accent.count("-")
    if mot_sans_accent.count("'") != 0:
        mot_cache = update_mot_cache(mot, "'", mot_cache)
        compteur_bonne_lettre += mot_sans_accent.count("'")

    # Fin de la configuration, la partie DEMARRE ici
    affichage_pendu(etat, mot_cache, difficulte)

    # On continue la partie tant que l'utilisateur a des chances et qu'il n'a pas trouvé le mot
    while etat < 6 and compteur_bonne_lettre != nombre_lettres:

        # On demande de tenter d'inscrire une lettre
        print("| Tentez de trouver le mot qui se cache |")
        print("|         proposez une lettre           |")
        proposition = input("-->")

        # Si l'utilisateur a bien mis un seul caractère
        if len(proposition) == 1:
            # Si la lettre est dans le mot
            if mot_sans_accent.count(proposition) != 0:
                # Si la lettre n'a pas déja été proposée anciennement
                if mot_cache.count(proposition) == 0:
                    compteur_bonne_lettre += mot_sans_accent.count(proposition)
                    mot_cache = update_mot_cache(mot, proposition, mot_cache)

            # Si la lettre n'est pas dans le mot on diminue le nombre de chances
            # et on ajoute la lettre dans la liste des mauvaises propositions
            else:
                etat += 1
                if liste_propositions.count(proposition) == 0:
                    liste_propositions.append(proposition)

            # A chaque tour de boucle, on affiche : le nombre de chances restantes, l'etat du pendu, l'etat du mot
            # à trouver et le mode de jeu selectionné.
            affichage_pendu(etat, mot_cache, difficulte)

            # BONUS: lorsqu'il ne reste qu'une seule vie et qu'on est en mode facile, on aide l'utilisateur
            # en lui indiquant une lettre qui n'est pas dans le mot et les lettres fausses déjà proposée.
            if etat == 5 and difficulte == "facile":
                print("┌---------------------------------------┐")
                print(f"| Cette lettre n'est pas dans le mot: {aide(liste_propositions, mot)} |")
                print("| Lettres fausses déjà proposées :      |")
                print(f"| {liste_propositions} "+(37-5*len(liste_propositions))*" "+"|")
                print("└---------------------------------------┘\n")

        # Si l'utilisateur a mal inscrit son caractère
        else:
            print("┌---------------------------------------┐")
            print("|   veuillez saisir un seul caractère   |")
            print("└---------------------------------------┘")

    # Si perdu
    if etat == 6:
        rejouer("perdu", mot)
    # Si gagné
    else:
        rejouer("gagné", mot)


# -------------------------------------------------------------------------- #
                        #FONCTION D'UPDATE DU MOT CACHE#
            # met à jour le mot caché lorsqu'une lettre est trouvée #
# -------------------------------------------------------------------------- #
def update_mot_cache(mot, proposition, mot_cache):
    # On crée une liste avec des tirets et la proposition correcte à la bonne place
    mot_cache_liste = [x if unicodedata.normalize('NFD', x).encode(encoding='ASCII', errors='ignore').decode('utf8') == proposition else "_" for x in mot]
    tampon = mot_cache
    mot_cache = ''
    # On vient reprendre le mot caché actuel et on y ajoute la/les proposition/s correctes à leurs places.
    for i in range(len(mot)):
        if mot_cache_liste[i] != "_":
            mot_cache += mot_cache_liste[i]
        else:
            mot_cache += tampon[i]
    return mot_cache

# -------------------------------------------------------------------------- #
                    #FONCTION BONUS CHOIX DE LA DIFFICULTE#
# -------------------------------------------------------------------------- #
def set_difficulte(difficulte):
    if difficulte == "facile":
        difficulte_selection = "facile"
    else:
        difficulte_selection = "normal"

    return difficulte_selection


# -------------------------------------------------------------------------- #
                    #FONCTION DEMANDE POUR REJOUER#
# -------------------------------------------------------------------------- #
def rejouer(txt, mot):
    print(" _______________________________________")
    print(f"|          Vous avez {txt}              |")
    print("|           le mot était                |")
    print(f"|            {mot}"+(27-len(mot))*" "+"|")# On suppose que les mots font moins de 28 caractères
                                                        # (qui plus est, serait trop difficile à deviner)
    print("|                                       |")
    print("| Souhaitez vous relancer une partie ?  |")
    print("|                                       |")
    print("|     oui(tapez 0)   non (tapez 1)      |")
    print("|                                       |")
    reponse = input("-->")

    if reponse == "0":
        demarrage_jeu_du_pendu()
    else:
        return

# -------------------------------------------------------------------------- #
                #FONCTION SELECTION D'UN MOT DANS UN FICHIER#
# -------------------------------------------------------------------------- #
def selection_mot_fichier(nom_de_fichier):
    if os.path.isfile(nom_de_fichier):
        with open(nom_de_fichier, 'r', encoding='utf-8') as fio: # ENCODING nécessaire pour lire les accents...
            words = fio.read().splitlines()
    else:
        with open("mots_pendu.txt", 'r', encoding='utf-8') as fio:
            words = fio.read().splitlines()
    word = choice(words)
    return word

# -------------------------------------------------------------------------- #
                          #FONCTION BONUS AIDE#
  #permettant d'afficher la liste des mauvaises propositions déjà proposées
                      # et d'une lettre incorrecte
# -------------------------------------------------------------------------- #
def aide(liste_propositions, mot):
    lettres = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
               "v", "w", "x", "y", "z"]
    # De la liste des lettres, on enlève celles du mot (pour enlever les lettres bonnes)
    for x in mot:
        if lettres.count(x) != 0:
            del lettres[lettres.index(x)]
    # De la liste des lettres, on enlève celles fausses déjà proposée (pour éviter de donner en
    # aide une lettre déjà proposée)
    for y in liste_propositions:
        if lettres.count(y) != 0:
            del lettres[lettres.index(y)]
    # Retourner une lettre au hasard qui n'est pas dans le mot
    return choice(lettres)

# -------------------------------------------------------------------------- #
                          #FONCTION D'AFFICHAGE#
            # Affiche les chances, le mot caché, le pendu, le mode de jeu
# -------------------------------------------------------------------------- #
def affichage_pendu(etat, mot, difficulte):
    if etat == 0:
        print("┌---------------------------------------┐")
        print("│vies:6❤"+(31-len(mot))*" "+f"{mot}▕")
        print("└---------------------------------------┘")
        print("|               .---.                   |")
        print("|               |   |                   |")
        print("|                   |                   |")
        print("|                   |                   |")
        print("|                   |                   |")
        print(f"| {difficulte}       _____|_____              |")
        print("└---------------------------------------┘")
    elif etat == 1:
        print("┌---------------------------------------┐")
        print(f"│vies:5❤"+(31-len(mot))*" "+f"{mot}▕")
        print("└---------------------------------------┘")
        print("|               .---.                   |")
        print("|               |   |                   |")
        print("|               O   |                   |")
        print("|                   |                   |")
        print("|                   |                   |")
        print(f"| {difficulte}       _____|_____              |")
        print("└---------------------------------------┘")
    elif etat == 2:
        print("┌---------------------------------------┐")
        print(f"│vies:4❤"+(31-len(mot))*" "+f"{mot}▕")
        print("└---------------------------------------┘")
        print("|               .---.                   |")
        print("|               |   |                   |")
        print("|               O   |                   |")
        print("|               |   |                   |")
        print("|                   |                   |")
        print(f"| {difficulte}       _____|_____              |")
        print("└---------------------------------------┘")
    elif etat == 3:
        print("┌---------------------------------------┐")
        print(f"│vies:3❤"+(31-len(mot))*" "+f"{mot}▕")
        print("└---------------------------------------┘")
        print("|               .---.                   |")
        print("|               |   |                   |")
        print("|               O   |                   |")
        print("|              ┌|   |                   |")
        print("|                   |                   |")
        print(f"| {difficulte}       _____|_____              |")
        print("└---------------------------------------┘")
    elif etat == 4:
        print("┌---------------------------------------┐")
        print(f"│vies:2❤"+(31-len(mot))*" "+f"{mot}▕")
        print("└---------------------------------------┘")
        print("|               .---.                   |")
        print("|               |   |                   |")
        print("|               O   |                   |")
        print("|              ┌|┐  |                   |")
        print("|                   |                   |")
        print(f"| {difficulte}       _____|_____              |")
        print("└---------------------------------------┘")
    elif etat == 5:
        print("┌---------------------------------------┐")
        print(f"│vies:1❤"+(31-len(mot))*" "+f"{mot}▕")
        print("└---------------------------------------┘")
        print("|               .---.                   |")
        print("|               |   |                   |")
        print("|               O   |                   |")
        print("|              ┌|┐  |                   |")
        print("|              ┌    |                   |")
        print(f"| {difficulte}       _____|_____              |")
        print("└---------------------------------------┘")
    elif etat == 6:
        print("┌---------------------------------------┐")
        print(f"│vie:0❤"+(31-len(mot))*" "+f"{mot}▕")
        print("└---------------------------------------┘")
        print("|               .---.                   |")
        print("|               |   |                   |")
        print("|               O   |                   |")
        print("|              ┌|┐  |                   |")
        print("|              ┌ ┐  |                   |")
        print(f"| {difficulte}       _____|_____              |")
        print("└---------------------------------------┘")



#Permet de lancer le jeu au RUN du script.
accueil_jeu_du_pendu()
