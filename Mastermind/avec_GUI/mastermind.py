import random

class Mastermind:
    def __init__(self, p_max_attempt):
        self.all_colors = ["red", "blue", "green", "black", "yellow", "orange"]
        self.secret_sequence = random.choices(self.all_colors, k=4)
        self.current_guess = []

        self.max_attempts = p_max_attempt
        self.attempt_count = 0

    
    def verify_sequence(self):
        """ verifie si la saisie est acceptée mais ne compare pas  ( nombre + choix couleur )"""

        return len(self.current_guess) == len(self.secret_sequence) and all(c in self.all_colors for c in self.current_guess)
    
    def compare_sequences(self):
        """ Compare la séquence tentée avec la séquence correcte
        et retourne le résultat en tenant compte des doublons. """
        correct_position = 0
        wrong_position = 0

        # Comptage des occurrences dans les séquences
        secret_counts = {}
        guess_counts = {}

        # Première boucle : comptage des positions correctes
        for secret_color, player_color in zip(self.secret_sequence, self.current_guess):
            if player_color == secret_color:
                correct_position += 1
            else:
                # Comptage des couleurs restantes
                secret_counts[secret_color] = secret_counts.get(secret_color, 0) + 1
                guess_counts[player_color] = guess_counts.get(player_color, 0) + 1

        # Deuxième boucle : comptage des positions incorrectes sans surcomptage
        for color in guess_counts:
            if color in secret_counts:
                wrong_position += min(secret_counts[color], guess_counts[color])
        return [correct_position, wrong_position]


    def handle_guess(self):
        """
        Gère le déroulement des tours, avec limitation des tentatives et messages de victoire/défaite.
        """

        # Vérifier la validité de la séquence
        if not self.verify_sequence():           
            return False, "Séquence invalide. Assurez-vous d'utiliser les bonnes couleurs et de ne pas dépasser la taille requise: "
            
        # Comparer les séquences
        correct_position, wrong_position = self.compare_sequences()
        self.attempt_count += 1

        # Victoire
        if correct_position == len(self.secret_sequence):
            return True, [correct_position, wrong_position]
        # Défaite
        elif self.attempt_count >= self.max_attempts:
            return False, [correct_position, wrong_position]
        
        return None, [correct_position, wrong_position] # Continuer à deviner
    
