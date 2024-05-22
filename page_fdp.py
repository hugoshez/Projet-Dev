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
pygame.display.set_caption("Fin de Partie")

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

def show_end_game(score, leaderboard):
    running = True
    while running:
        screen.fill(BG_COLOR)
        display_message("Fin de la Partie", (SCREEN_WIDTH // 2, 50))
        display_message(f"Votre score : {score}", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Affichage du classement des joueurs
        display_message("Classement des Joueurs :", (SCREEN_WIDTH // 2, 250))
        for i, (player, player_score) in enumerate(leaderboard, start=1):
            display_message(f"{i}. {player} - {player_score}", (SCREEN_WIDTH // 2, 250 + i * 40))

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
    leaderboard = [("Joueur1", 1500), ("Joueur2", 1200)]  # Exemple de classement, remplacez-le par le classement réel
    show_end_game(leaderboard)

if __name__ == "__main__":
    main()
