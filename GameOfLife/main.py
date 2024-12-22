
from gameoflife import GameOfLife  # Import du backend
from gameoflifeGUI import GameOfLifeGUI  # Import du frontend

if __name__ == "__main__":
    # Initialisation
    game_gui = GameOfLifeGUI(grid_size=30, fps=5)  # Instancie l'interface graphique

    # Exemple de configuration initiale (un oscillateur "blinker")
    game_gui.game.frame[10, 9] = 1
    game_gui.game.frame[10, 10] = 1
    game_gui.game.frame[10, 11] = 1

    
    game_gui.run()  # Lance la boucle principale

