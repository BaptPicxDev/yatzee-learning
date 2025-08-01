# Import
import numpy as np
import random

# Class
class YatzeeGame:
    def __init__(self):
        self.final_score = 0
        self.rounds_played = 0
        self.scores = {}
        self.available_categories = [
            '1', '2', '3', '4', '5', '6',
            'brelan', 'carre', 'full',
            'petite_suite', 'grande_suite',
            'yahtzee', 'chance'
        ]
        self.play_game()

    
    def roll_dices(self, number_of_dice=5):
        return np.random.randint(1, 7, size=number_of_dice)

    def play_round(self):
        # Initial roll of 5 dice -> we simplify so let's say it is my roll
        dices = self.roll_dices()

        # Choose a category randomly
        chosen_category = random.choice(self.available_categories)
        self.available_categories.remove(chosen_category)

        # Score is just a random placeholder for now
        score = np.sum(dices)
        self.scores[chosen_category] = score
        self.final_score += score
        self.rounds_played += 1

    def play_game(self):
        while self.available_categories:
            self.play_round()
        print(f"\nFinal score: {self.final_score}")
        print("Scores by category:")
        for cat, score in self.scores.items():
            print(f"  {cat}: {score}")

# Main thread.
if __name__ == "__main__":
    a = YatzeeGame()
