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
background = pygame.image.load("resources/img/pomme.webp").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Police de caractères
font = pygame.font.Font(None, 36)

def display_message(message, pos):
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(topleft=pos)
    screen.blit(text, text_rect)

class User:
    def __init__(self, username):
        self.username = username

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
        text_surface = font.render(username, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, text_surface.get_width() + 10)
        pygame.display.flip()

# Création ou connexion à la base de données SQLite
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT)''')

# Fonction pour insérer un utilisateur dans la base de données
def insert_user(username):
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()

# Fonction principale
def main():
    users = []
    running = True

    while running:
        screen.blit(background, (0, 0))
        display_message("Appuyez sur 'C' pour créer un utilisateur ou 'E' pour exécuter le jeu", (50, 50))

        # Affichage des utilisateurs créés
        if users:
            display_message("Utilisateurs créés :", (50, 100))
            for i, user in enumerate(users):
                display_message(f"{i + 1}. {user.username}", (50, 150 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    user = create_user()
                    users.append(user)
                    insert_user(user.username)
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
