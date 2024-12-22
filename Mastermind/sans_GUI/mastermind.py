import random

class Mastermind:
    def __init__(self, p_max_attempt):
        self.all_colors = ["red", "blue", "green", "black", "yellow", "orange"]

        self.secret_sequence = random.choices(self.all_colors, k=4)

        self.current_guess = []
        self.max_attempts = p_max_attempt
        self.attempt_count = 0

    def get_current_guess(self):
        """
        Demande à l'utilisateur de proposer une séquence de couleurs
        et retourne la liste des couleurs séparées par un espace.
        """

        if self.attempt_count == 0 : 
            print("les couleurs possible sont :", self.all_colors)
            entry = str(input("Proposez votre séquence de "+str(len(self.secret_sequence)) +" couleur en séparant  d'un espace: "))
        else :
            entry = str(input("Proposez votre nouvelle séquence en séparant  d'un espace: "))

        sequence = entry.split()
        self.current_guess = sequence
    
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

    

    def start(self):
        """
        Gère le déroulement des tours, avec limitation des tentatives et messages de victoire/défaite.
        """
        print("=" * 40)
        print("🎉 Bienvenue dans le MASTERMIND 🎉".center(40))
        print("=" * 40)
        while self.attempt_count < self.max_attempts:
            print(f"\nTentative {self.attempt_count + 1}/{self.max_attempts}")

            # Récupérer la saisie du joueur
            self.get_current_guess()

            # Vérifier la validité de la séquence
            while not self.verify_sequence():
                print("\nSéquence invalide. Assurez-vous d'utiliser les bonnes couleurs: \n", self.all_colors, " et de ne pas dépasser la taille requise: ", len(self.secret_sequence),'\n')
                self.get_current_guess()
            
            self.attempt_count += 1  

            # Comparer les séquences
            correct_position, wrong_position = self.compare_sequences()
            # Victoire
            if correct_position == len(self.secret_sequence):
                print(f"Félicitations ! Vous avez deviné la combinaison : {self.secret_sequence}")
                return
            # Tour suivant
            else :
                print(f"Résultat : {correct_position} bien placée(s), {wrong_position} mal placée(s)")
                print("Continuer")
            print("_"*20)

        # Défaite
        print(f"Dommage ! Vous avez utilisé vos {self.max_attempts} tentatives. La combinaison secrète était : {self.secret_sequence}")



