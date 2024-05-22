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
pygame.display.set_caption("Menu Principal")

# Chargement de l'image de fond
background = pygame.image.load("resources/img/11.09.2001.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

# Création de la table si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT)''')

# Fonction pour insérer un utilisateur dans la base de données
def insert_user(username):
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()

def show_menu():
    while True:
        screen.blit(background, (0, 0))
        display_message("Menu Principal", (300, 50))
        display_message("1. Créer un utilisateur", (300, 150))
        display_message("2. Démarrer le jeu", (300, 250))
        display_message("3. Instructions", (300, 350))
        display_message("4. Quitter", (300, 450))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    user = create_user()
                    if user:
                        insert_user(user.username)
                elif event.key == pygame.K_2:
                    start_game()
                elif event.key == pygame.K_3:
                    show_instructions()
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

def start_game():
    running = True
    while running:
        screen.fill(BG_COLOR)
        display_message("Jeu en cours... Appuyez sur 'Q' pour quitter", (100, 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

    show_end_screen()

def show_end_screen():
    running = True
    while running:
        screen.fill(BG_COLOR)
        display_message("Fin de la partie. Appuyez sur 'M' pour retourner au menu principal", (50, 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    running = False

    show_menu()

def show_instructions():
    running = True
    while running:
        screen.fill(BG_COLOR)
        display_message("Instructions du jeu:", (50, 50))
        display_message("1. Utilisez les flèches du clavier pour déplacer.", (50, 100))
        display_message("2. Appuyez sur 'Q' pour quitter le jeu.", (50, 150))
        display_message("3. Appuyez sur 'M' pour retourner au menu principal.", (50, 200))
        display_message("Appuyez sur 'M' pour retourner au menu principal", (50, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    running = False

    show_menu()

# Fonction principale
def main():
    show_menu()

if __name__ == "__main__":
    main()
