import pygame
from gameoflife import GameOfLife
from config import *

class GameOfLifeGUI:
    def __init__(self, grid_size, fps):
        self.grid_size = grid_size  # exemple 20*20
        self.fps = fps
        self.game = GameOfLife(grid_size, fps)
        self.paused = False  # Indique si le jeu est en pause


        # Initialisation de l'interface Pygame
        self.window_size = (grid_size * CELL_SIZE, grid_size * CELL_SIZE)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Jeu de la vie")
        self.clock = pygame.time.Clock()

    @staticmethod 
    def show_rules():
        """Affiche les règles du jeu de manière stylée."""
        print("\n" + "=" * 50)
        print("              Bienvenue dans le Jeu de la Vie")
        print("=" * 50)
        print("\nRègles :")
        print("1. Appuyez sur ESPACE pour mettre en pause ou reprendre le jeu.")
        print("2. En pause, cliquez sur une cellule pour inverser son état (vivante/morte).")
        print("3. Le jeu avance automatiquement selon les règles classiques de Conway :")
        print("   - Une cellule vivante avec 2 ou 3 voisins reste vivante.")
        print("   - Une cellule morte avec exactement 3 voisins devient vivante.")
        print("   - Toutes les autres cellules meurent ou restent mortes.")
        print("\nAmusez-vous bien !")
        print("=" * 50 + "\n")

    def draw_grid(self):
        """Dessine la grille et les cellules."""
        cell_border_color = (120, 120, 120)

        # PARCOURS DE LA FRAME
        for index_line in range(self.grid_size):
            for index_column in range(self.grid_size):
                cell_color = (0, 255, 0) if self.game.frame[index_line, index_column] == 1 else (30, 30, 30)   # Mettre en vert les cellules vivantes
                rect = pygame.Rect(index_column * CELL_SIZE, index_line * CELL_SIZE, CELL_SIZE, CELL_SIZE) 
                pygame.draw.rect(self.screen, cell_color, rect)  # soit vert soit (30, 30, 30)
                pygame.draw.rect(self.screen, cell_border_color, rect, 1)  # Bordure de cellule

    def handle_events(self):
        """
        Gère les événements utilisateur, notamment les interactions via le clavier et la souris.
            - Ferme l'application si l'utilisateur clique sur le bouton de fermeture de la fenêtre.
            - Permet de mettre en pause ou de reprendre avec la touche espace.
            - Autorise des modifications manuelles de l'état des cellules en cliquant dessus avec la souris
            lorsque l'exécution est en pause. Le clic inverse l'état de la cellule (vivante/morte).
            """
        for event in pygame.event.get():  # Parcourt tous les événements
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                return False  # Quitte le programme


            # Alterne entre pause et reprise avec la touche espace
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_SPACE:  
                    self.paused = not self.paused  

            # Changer etat de cellules en cliquant ( pendant la pause )
            if event.type == pygame.MOUSEBUTTONDOWN and self.paused :
                mouse_x, mouse_y = event.pos  
                cell_column, cell_line = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE   
                # Si le clic est dans les limites de la grille
                if 0 <= cell_column < self.grid_size and 0 <= cell_line < self.grid_size:
                    self.game.frame[cell_line, cell_column] ^= 1   

        return True  

    def run(self):
        self.show_rules()
        while self.handle_events():  # tant que il y'a les événements sont traités
            self.draw_grid()  
            pygame.display.flip()  
            
            if not self.paused:  
                self.game.compute_next_frame()  # Calcul de la génération suivante
            self.clock.tick(self.fps)  

        pygame.quit()  
