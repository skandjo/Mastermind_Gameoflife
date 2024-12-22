import numpy as np
import time

class GameOfLife :
    def __init__(self, p_grid_size, p_fps):
        self.grid_size = p_grid_size
        self.frame = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.fps = p_fps  # Définir les FPS (images par seconde)
        self.generation = 0
    
    @staticmethod
    def compute_number_neigh(paded_frame, index_line, index_col):
        """ prend en parametre une matrice paded , ligne et colone de la celule
            ----> retourne le nombre de voisins de la cellules"""
        # Extraitre une matrice 3*3 avec la celule (index_line, index_col) comme centre . Pour pouvoir appliquer np.sum
        cell = paded_frame[index_line, index_col]
        neighbors = paded_frame[index_line-1:index_line+2, index_col-1:index_col+2]

        # Faire la somme :
        number_neighbors = np.sum(neighbors) if cell == 0 else np.sum(neighbors) - 1

        return number_neighbors
    
    def compute_next_frame(self):
        """ Retourne la frame de la prochaine generation apres avoir appliquer les regles du jeu de la vie """
        paded_frame = np.pad(self.frame, 1, mode='constant') # 0 PADDING 

        n, m = paded_frame.shape # limite de la frame (n ,m)  mais ici on va travailler de (1, 1) ---> (n-2, m-2)  : padding

        # PARCOURS DE LA MATRICE : 
        for l in range(1, n-1):           # n-1 pour qu il s'arrete a n-2
            for c in range(1, m-1):

                current_cell = paded_frame[l, c]
                number_neighbors = self.compute_number_neigh(paded_frame, l, c) 

                # BORN 
                if (current_cell == 0) and (number_neighbors == 3):
                    self.frame [l-1, c-1] = 1   # on met le -1 a cause du padding
                # DEAD
                if (current_cell == 1) and ( (number_neighbors < 2) or (number_neighbors > 3) ):
                    self.frame [l-1, c-1] = 0
        self.generation += 1

    def start(self):
        
        while True:
            print("-" * 10 + str(self.generation) + "-" * 10)
            print(self.frame)
            self.compute_next_frame() 
            time.sleep(1/self.fps)  # Pause pour atteindre les FPS souhaités








