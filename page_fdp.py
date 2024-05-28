import pygame
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
pygame.display.set_caption("Instructions")

# Police de caractères
font = pygame.font.Font(None, 36)

def display_message(message, pos):
    # Créer le texte en rouge
    text_red = font.render(message, True, (255, 0, 0))
    text_rect = text_red.get_rect(center=pos)
    
    # Créer le contour noir
    offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for dx, dy in offsets:
        text_outline = font.render(message, True, (0, 0, 0))
        screen.blit(text_outline, (text_rect.x + dx, text_rect.y + dy))

    # Afficher le texte rouge par-dessus le contour
    screen.blit(text_red, text_rect)

def get_scores(username):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()


    return str(cursor.execute("SELECT scores FROM users WHERE username = ?", (username,)).fetchone()[0])



def show_fdp():
    running = True
    db = sqlite3.connect("users.db")
    cursor = db.cursor()

    res = cursor.execute('''SELECT username FROM users ORDER BY id DESC LIMIT 2''').fetchall()


    while running:
        screen.fill(BG_COLOR)
        display_message("Fin De Partie", (SCREEN_WIDTH // 2, 50))
        
        # Mettre à jour la liste `fdp` avec les noms d'utilisateur
        fdp = [
            f"1. {res[0][0]}" + " : " + get_scores(res[0][0]) if len(res) > 0 else "1.",
            f"2. {res[1][0]}" + " : " + get_scores(res[1][0])  if len(res) > 1 else "2.",
        ]

        # Afficher les noms d'utilisateur
        display_message(fdp[0]  , (SCREEN_WIDTH // 2, 100))
        display_message(fdp[1] , (SCREEN_WIDTH // 2, 150))
        
             # Afficher le message de retour
        display_message("Appuyez sur 'Retour' pour revenir au menu principal", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False

    db.close()

def main():
    show_fdp()

if __name__ == "__main__":
    main()
