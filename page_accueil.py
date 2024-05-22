import pygame
import sys
import os

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 255)

# Initialisation de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Page d'accueil")

# Chargement de l'image de fond
background = pygame.image.load("resources/img/11.09.2001.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

def show_welcome_screen():
    running = True
    while running:
        screen.blit(background, (0, 0))
        display_message("Appuyez sur Entrer pour commencer", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

def show_main_menu():
    running = True
    while running:
        screen.fill(BG_COLOR)
        display_message("Menu Principal", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        display_message("1. Commencer le jeu", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        display_message("2. Instructions", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        display_message("3. Quitter", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("Démarrer le jeu")  # Remplacez par la fonction de démarrage du jeu
                    os.system('python3 page.py')
                elif event.key == pygame.K_2:
                    print("Afficher les instructions")  # Remplacez par la fonction d'affichage des instructions
                    os.system('python3 page_instruction.py')
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def main():
    show_welcome_screen()
    show_main_menu()

if __name__ == "__main__":
    main()
