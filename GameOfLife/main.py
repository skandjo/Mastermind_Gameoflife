from gameoflife import GameOfLife

if __name__ == "__main__":
    """ executer sans interface graphique, 
        directement sur le terminal"""
    # Initialisation 
    grid_size=7
    fps = 2
    game_of_life = GameOfLife(grid_size, fps) # SIZE = 7*7 

    # Frame de depart
    game_of_life.frame[3, 2] = 1
    game_of_life.frame[3, 3] = 1
    game_of_life.frame[3, 4] = 1

    # Boucle de jeu
    game_of_life.start()


