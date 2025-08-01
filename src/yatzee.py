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
            'chance',
            'brelan',
            'carre',
            'yatzee',
            'full',
            'petite_suite',
            'grande_suite',
        ]

    
    def roll_dices(self, number_of_dice=5):
        return np.random.randint(1, 7, size=number_of_dice)

    def compute_score(self, category, dices):
        counts = [np.count_nonzero(dices == i) for i in range(1, 7)]

        if category in ['1', '2', '3', '4', '5', '6']:
            face = int(category)
            return np.sum(dices[dices == face])
        elif category == 'brelan':
            if any(c >= 3 for c in counts):
                return np.sum(dices)
            return 0
        elif category == 'carre':
            if any(c >= 4 for c in counts):
                return np.sum(dices)
            return 0
        elif category == 'yatzee':
            for value in range(1, 7):
                if np.count_nonzero(dices == value) == 5:
                    return 50
            return 0
        elif category == 'chance':
            return np.sum(dices)
        elif category == 'full':
            if 3 in counts and 2 in counts:
                return 25
            if 3 in counts and counts.count(1) == 2:
                return 25
            return 0
        elif category == 'petite_suite':
            # Check all small straight sequences
            straights = [
                {1, 2, 3, 4},
                {2, 3, 4, 5},
                {3, 4, 5, 6}
            ]
            dice_set = set(dices)
            if any(straight.issubset(dice_set) for straight in straights):
                return 30
            return 0
        elif category == 'grande_suite':
            dice_set = set(dices)
            if {1, 2, 3, 4, 5}.issubset(dice_set) or {2, 3, 4, 5, 6}.issubset(dice_set):
                return 40
            return 0
        raise NotImplementedError(f"category {category}")

    def play_round(self):
        # Initial roll of 5 dice -> we simplify so let's say it is my roll
        dices = self.roll_dices()

        # Choose a category randomly
        chosen_category = random.choice(self.available_categories)
        self.available_categories.remove(chosen_category)

        # Score is just a random placeholder for now
        score = self.compute_score(category=chosen_category, dices=dices)
        self.scores[chosen_category] = score
        self.final_score += score
        self.rounds_played += 1

    def play_game(self):
        while self.available_categories:
            self.play_round()
        sum_top = (
            self.scores['1']
            + self.scores['2']
            + self.scores['3']
            + self.scores['4']
            + self.scores['5']
            + self.scores['6']
        )
        if sum_top >= 63:
            self.final_score += 35
        print(f"\nFinal score: {self.final_score}")
        print("Scores by category:")
        for cat, score in self.scores.items():
            print(f"  {cat}: {score}")

# Main thread.
if __name__ == "__main__":
    a = YatzeeGame()
    a.play_game()
