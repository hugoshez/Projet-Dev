import pygame
import sys

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

def show_instructions():
    running = True
    while running:
        screen.fill(BG_COLOR)
        display_message("Instructions", (SCREEN_WIDTH // 2, 50))
        instructions = [
            "1. Le joueur 1 utilise les touches 'ZQSD' pour se déplacer.",
            "2. Le joueur 2 utilise les touches fléchées pour se déplacer.",
            "3. Appuyez sur 'Echap' pour quitter le jeu.",
            "Le pistolet apparait aléatoirement dans la map.",
            "Le joueur qui ramasse le pistolet en premier,",
            "peut tirer avec le clic gauche de la souris.",
            "Le joueur qui n'a pas le pistolet peut frapper avec ses poings",
            "Le joueur qui est touché perd la partie",
            "Le jeu se termine à la fin du niveau 3.",]

        for i, line in enumerate(instructions):
            display_message(line, (SCREEN_WIDTH // 2, 150 + i * 40))
        
        display_message("Appuyez sur 'Retour' pour revenir au menu principal", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False

def main():
    show_instructions()

if __name__ == "__main__":
    main()
