import pygame
import os
import sys
import sqlite3

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 255)

# Initialisation de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Page d'accueil de jeux")

# Chargement de l'image de fond
background = pygame.image.load("resources/img/son_of_the_forest.JPG").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

users = []


# Police de caractères
font = pygame.font.Font(None, 36)

def display_message(message, pos):
    # Créer le texte en rouge
    text_red = font.render(message, True, (255, 0, 0))
    text_rect = text_red.get_rect(topleft=pos)
    
    # Créer le contour noir
    offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for dx, dy in offsets:
        text_outline = font.render(message, True, (0, 0, 0))
        screen.blit(text_outline, (text_rect.x + dx, text_rect.y + dy))

    # Afficher le texte rouge par-dessus le contour
    screen.blit(text_red, text_rect)

class User:
    def __init__(self, username):
        self.username = username
        self.scores = 0

def create_user():
    input_box = pygame.Rect(300, 400, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    username = ''
    active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return User(username)
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

        screen.blit(background, (0, 0))
        display_message("Entrez votre pseudo:", (300, 350))
        pygame.draw.rect(screen, color, input_box, 2)

        # Affichage du texte avec contour noir et texte rouge
        text_surface = font.render(username, True, (255, 0, 0))
        outline_positions = [(input_box.x + 4, input_box.y + 5),
                             (input_box.x + 6, input_box.y + 5),
                             (input_box.x + 5, input_box.y + 4),
                             (input_box.x + 5, input_box.y + 6)]
        for outline_pos in outline_positions:
            outline_text = font.render(username, True, (0, 0, 0))
            screen.blit(outline_text, outline_pos)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        input_box.w = max(200, text_surface.get_width() + 10)
        pygame.display.flip()

# Création ou connexion à la base de données SQLite
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas (avec la colonne scores)
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, scores INTEGER)''')

# Fonction pour insérer un utilisateur avec son score dans la base de données
def insert_user(username, scores):
    cursor.execute("INSERT INTO users (username, scores) VALUES (?, ?)", (username, scores))
    conn.commit()






# Fonction principale
def main():
    running = True

    while running:
        screen.blit(background, (0, 0))
        display_message("Appuyez sur 'C' pour créer un utilisateur,", (50, 50))
        display_message("Appuyez sur 'E' pour exécuter le jeu", (50, 100))


        # Affichage des utilisateurs créés
        if users:
            display_message("Utilisateurs créés :", (50, 200))
            for i, user in enumerate(users):
                display_message(f"{i + 1}. {user.username}", (50, 250 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    user = create_user()
                    users.append(user)
                    insert_user(user.username, user.scores)
                elif event.key == pygame.K_e:
                    if len(users) > 0:
                        # Exécuter le fichier main.py
                        os.system('python3 main.py')
                        running = False
                    else:
                        print("Aucun utilisateur créé. Veuillez créer un utilisateur avant de démarrer le jeu.")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
