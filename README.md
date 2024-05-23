CONTENU DU DEPOT:

le dépot contient :

- un script contenant tout le nécessaire pour jouer au jeu du pendu
- un fichier de mots par défaut utilisé par le script du jeu du pendu 


MANUEL D'UTILISATION DU JEU DU PENDU:

Lors du lancement, le script démarre les étapes consécutives suivantes : 

-> Accueil et demande si l'utilisateur veut lancer une partie, la sélection se fait de la manière suivante :

		- pour OUI saisir : "0"
		- pour NON saisir : "1" ou toute autre entrée

-> Sélection du mode de jeu, l'utilisateur peut choisir son mode de difficulté :

		- en écrivant "normal" il n'aura aucune aide
		- en écrivant "facile" l'utilisateur recevra une aide* lorsqu'il ne lui restera plus qu'une seule vie
		- en ecrivant toute autre chose, le mode par défaut (normal) se lance

* l'aide affiche une lettre jamais proposée qui n'est pas dans le mot. De plus, elle indique toutes les lettres fausses proposées précèdemment par l'utilisateur.

-> Sélection du fichier source pour les mots du jeu :

		-Si l'utilisateur souhaite ajouter son fichier de mots, il doit le mettre sous forme de fichier .txt à la racine du dossier contenant le script JeuDuPendu.py. Il doit alors écrire le nom du fichier avec son extension. 

		-Si l'utilisateur souhaite utiliser le fischier de mots par défaut, il doit cliquer directement sur entrée.

Dans le cas d'une erreur dans le nom du fichier, le fichier par défaut se lance automatiquement.

-> Démarrage du jeu, affichage des informations importantes et demande d'entrée d'une lettre. 

L'utilisateur peut visualiser les chances qu'il lui reste, l'état du mot caché, le mode de jeu et l'avancement du pendu. 

Lors de la saisie d'une lettre, l'utilisateur entrera un caractère sans accent (si des lettres accentuées se cachent dans le mot, le script considèrera la similarité). Si l'utilisateur entre plus qu'un seul caractère, on lui indique d'en inscrire un seul.

-> Ecran de fin, On indique à l'utilisateur s'il a gagné ou non en lui donnant le mot, il a le choix de relancer une partie.


LIMITATIONS : Les mots de plus de 27 lettres sont interdits. (limitation imposée par l'affichage qui s'adapte selon la grandeur du mot)
