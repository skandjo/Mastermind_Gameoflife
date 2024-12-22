import pygame
import sys
from mastermind import Mastermind
from config import *


class MastermindGUI:
    def __init__(self):
        pygame.init()

        # Configuration initiale
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mastermind")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.initialize_game()

    def initialize_game(self):
        """Réinitialise le jeu."""
        self.mastermind = Mastermind(10)  # Backend avec 10 tentatives max
        self.current_colors = []  # Sélection actuelle
        self.history = []  # Historique des tentatives
        self.running = True  # Indicateur pour maintenir le jeu en cours

    def draw_interface(self):
        """Dessine les éléments de l'interface utilisateur."""
        self.screen.fill(COLORS["white"])

        # Zone de jeu
        pygame.draw.rect(self.screen, COLORS["gray"], (0, 0, SCREEN_WIDTH, GAME_RECT_HEIGHT))
        
        # Dessiner les pastilles de sélection des couleurs
        for i, color in enumerate(self.mastermind.all_colors):
            pygame.draw.circle(self.screen, COLORS[color], (150 + i * 100, SELECTION_PANEL_Y), 20)

        # Historique des tentatives
        for index_line, attempt in enumerate(self.history):
            for index_column, color in enumerate(attempt["sequence"]):
                pygame.draw.circle(self.screen, COLORS[color], (100 + index_column * 100, 100 + index_line * 40), 15)
            feedback = attempt["feedback"]
            feedback_text = f"{feedback[0]} bien placée(s), {feedback[1]} mal placée(s)"
            text_surface = self.font.render(feedback_text, True, COLORS["black"])
            self.screen.blit(text_surface, (500, 85 + index_line * 40))

    def handle_events(self):
        """Gère les événements utilisateur."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Gestion de la sélection des couleurs
                if SELECTION_PANEL_Y - RADIUS <= y <= SELECTION_PANEL_Y + RADIUS:
                    for i, color in enumerate(self.mastermind.all_colors):
                        circle_x = 150 + i * 100
                        if circle_x - 20 <= x <= circle_x + 20:
                            self.current_colors.append(color)

                # Soumettre la séquence si elle est complète
                if len(self.current_colors) == len(self.mastermind.secret_sequence):
                    self.mastermind.current_guess = self.current_colors
                    result, feedback = self.mastermind.handle_guess()
                    self.history.append({"sequence": self.current_colors, "feedback": feedback})

                    self.current_colors = []
                    # Fin de la partie si nécessaire
                    if result is not None:
                        self.running = False

    def display_end_screen(self, message, sequence):
        """Affiche l'écran de fin avec un message."""
        self.screen.fill(COLORS["white"])
        text_surface = self.font.render(message, True, COLORS["black"])
        self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

        # Affiche la séquence secrète
        sequence_text = "Séquence secrète : " + " ".join(sequence)
        sequence_surface = self.font.render(sequence_text, True, COLORS["red"])
        self.screen.blit(sequence_surface, (SCREEN_WIDTH // 2 - sequence_surface.get_width() // 2, SCREEN_HEIGHT // 2))

        # Affiche l'option de rejouer
        replay_text = "Appuyez sur 'R' pour rejouer ou 'Q' pour quitter"
        replay_surface = self.font.render(replay_text, True, COLORS["black"])
        self.screen.blit(replay_surface, (SCREEN_WIDTH // 2 - replay_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    def handle_events_end_screen(self):
        """Gère les événements sur l'écran de fin."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Rejouer
                    self.initialize_game()
                elif event.key == pygame.K_q:  # Quitter
                    pygame.quit()
                    sys.exit()

    def run(self):
        """Boucle principale du jeu."""
        while True:  # Boucle continue pour gérer la rejouabilité
            if self.running:
                self.handle_events()
                self.draw_interface()
                pygame.display.flip()
                self.clock.tick(30)
            else:
                # Partie terminée
                if self.mastermind.attempt_count >= self.mastermind.max_attempts:
                    # Défaite : affiche la séquence secrète
                    secret_sequence = self.mastermind.secret_sequence
                    message = "Vous avez perdu!"
                else:
                    # Victoire
                    secret_sequence = self.mastermind.secret_sequence
                    message = "Félicitations, vous avez gagné!"

                self.display_end_screen(message, secret_sequence)
                self.handle_events_end_screen()

