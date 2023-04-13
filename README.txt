############### CSGO : Clearly Something GO Oriented ##################

Author : Alexandre Soulié
Group : G1

##### Utilisation #####

CSGO peut être utilisé dans les conditions de l'énoncé, sans paramètres préalables ni modifications à effectuer.
Sont nécessaires comme modules externes de Python : 

> time, random, numpy

Sont nécessaires comme fichiers supplémentaires : 

> Goban.py, localGame.py, playerInterface.py, parce.py, games.json

##### Résumé #####

CSGO est une I.A. permettant de jouer au jeu de GO grâce au système de Goban.py .
CSGO utilise un algorithme AlphaBeta à profondeur adaptative par rapport au temps de jeu restant à heuristique simple avec banque d'ouverture.

##### Heuristique #####

L'heuristique proposée est très simple et basique. Lors du calcul de l'heuristique, selon la couleur de CSGO, on calcule son nombre de
pierres à l'instant donné additioné avec le nombre de pierres capturées. Celà nous donne un entier positif qui sera notre heuristique.
Le problème de cette heuristique dans un AlphaBeta est le suivant : les valeurs d'heuristique sont souvent probablement les mêmes.
Ainsi, l'élagage d'AlphaBeta est réduit à néant, ce qui donne des performances difficilement acceptables. 

Ici intervient le premier choix : à chaque calcul d'heuristique, on choisit d'ajouter un flottant extrèmement petit (de l'ordre de 10^-15) croissant.
Cela donne alors artificiellement un ordre aux heuristique, permettant un élagage un peu articiel de AlphaBeta.

Cette technique à prouvé une efficacité de l'ordre de 50% lors de gros calculs:

AlphaBeta de profondeur 3 sans classement artificiel : ~750 secondes au tour 16
AlphaBeta de profondeur 3 avec classement artificiel : ~500 secondes au tour 16

L'effet sur la compétitivité de l'IA en ouverture semble minime, d'où l'adoption de cette solution.

##### AlphaBeta #####

L'algorithme principal est un AlphaBeta classique. Sa particularité est d'avoir une profondeur adaptative selon le temps qu'il reste à jouer.

L'algorithme démarre par les 15 premiers tours qui sont pris à partir d'une banque d'ouverture. (15 coups de la même ouverture)
Si un coup est illégal (déjà joué précedemment par l'opposant), l'I.A active le "Disturbed Opening Mode" et joue aléatoirement jusqu'au tour 16.
Celà a pour but de vite procéder à l'ouverture avant de commencer les "vrais" calculs.

Vient ensuite un AlphaBeta classique, de profondeur 2.
Pour calculer la profondeur du prochain coup :
Si le temps que l'on a pris pour jouer ce coup est assez court pour que les prochains coups que l'on puisse jouer potentiellement
nous laissent encore la moitié du temps imparti à cet instant, on augmente la profondeur de 1 dans la limite d'une profondeur de 6.

>>> if self._actualDepth < 6 and (2*turnTime*(81-(totalStones+1)))<= (30*60)-self._totalTime:

Si le temps que l'on a pris pour jouer ce coup est trop long a tel point que si on jouait potentiellementà cette vitesse tout les prochains coups, on
dépasserait de 50% du temps imparti à cet instant, alors on diminue la profondeur de 1 dans la limite d'une profondeur de 2.

>>> elif self._actualDepth > 2 and (turnTime*(81-(totalStones+1))) > 1.50*((30*60)-self._totalTime):

On considère aussi deux modes de jeu important :

## Critical Mode :

Il s'active lorsqu'il ne reste plus de 60 secondes. On force alors un AlphaBeta de profondeur 2.

## Ultra Critical Mode :

Il s'active lorsqu'il ne reste plus de 10 secondes. On force alors un AlphaBeta de profondeur 1.

Avec ce modèle, plus le board est rempli, plus on parcours profondément l'arbre de jeu, ce qui nous rend bon en fin de partie.
Il y a malheureusement un faille. Si on arrive en profondeur 6, mais qu'une pierre capture une grande partie des pierres adverses,
alors le parcours sera extrèmement long puisque une branche sera extrèmement grande, ruinant le gain de temps.
On effectue alors une vérification sur la première couche de l'arbre, pour vérifier qu'aucun des premiers moves ne capturera beaucoup d'adversaires.
Si c'est le cas, on préfère alors une profondeur 3.
Sinon, on continue.

Au pire des cas, un gros coup apparaitra en deuxième couche, mais avec un AlphaBeta de profondeur 6, cela laissera maintenant 4 couches au pire à calculer,
ce qu'on estime raisonnable en fin de partie.

