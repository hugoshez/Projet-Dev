# Projet-Dev

    les deux joueurs sont positionnés chacun à une extrémité de la map,
    L'un des joueurs sera le chasseur, et l'autre sera le lapin.
    Le rôle de chacun sera définit par rapport à la position de l'arme qui est aléatoire, le premier à attraper l'arme sera le chasseur.

    Bonne chance.

## Fonctionnalités

    cinq écrans :
    - L'écran de démarrage avec le nom du jeu.


    modèle de données :
        - [x] une différenciation joueur 1 / joueur 2 --> chasseur / lapin 
        - [x] une vitesse de déplacement
        - [x] des points de vie --> une balle un mort
        - [x] une puissance de tir --> une balle un mort
        - [x] un délai de tir --> instantané un clic une balle
        - [x] une vitesse de projectile --> le projectile se déplace à une vitesse donnée

    Scores possédants :
        - [x] un pseudo --> enregistrement d'un pseudo pour chaque joueur
        - [x] un score --> un score pour chaque joueur
    
    déroulement d’une partie :
        - [x] les deux joueurs apparaissent de part et d’autre de l’écran ---> un joueur est le chasseur et l’autre le lapin
        - [x] l’espace de jeu se limite à l’écran, pas de physique, la vue caméra est dite “topdown” --> vue de dessus
        - [x] le Joystick doit permettre au joueur de pivoter à 360° et d’avancer vers l’avant --> déplacement du joueur
        - [x] un des boutons doit permettre au joueur de tirer un projectile --> tir du joueur
        - [x] un Joueur perd des points de vie quand un projectile le touche --> 1 balle = 1 mort

    fin d’une partie :
        - [x] la partie se termine quand un joueur n’a plus de points de vie --> changer de scène
        - [x] le logiciel bascule alors sur l’écran de fin de partie, où le score du gagnant s’affiche ainsi que sa position dans les meilleurs scores
        - [ ] pour le score, vous devez créer une formule prenant en compte la différence de points de vie, le temps passé sur la partie ainsi que la différence sur les données de BDD du joueur 1 et 2 (un joueur peut gagner un plus gros score en baissant sa vitesse de rotation par rapport à son adversaire par exemple)
        
    écran d’option :
        - [ ] il devra permettre aux joueurs de modifier toutes leurs données (puissance de tir, vitesses ...) 
        - [ ] ces données devront être stockées dans une base de données, afin de pouvoir les réutilisées même après fermeture du logiciel 




timer

score

écran de fin