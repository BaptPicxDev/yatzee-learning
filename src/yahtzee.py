# Import
import numpy as np
import random

# Class
class YahtzeeGame:
    def __init__(self):
        """Initializes the Yahtzee game with settings.
        Call reset() to start a new game.
        """
        self.num_dice = 5
        self.max_rolls = 3
        self.verbose = False
        self.reset()
    
    def reset(self):
        """Resets the entire game to the beginning of a 13-round Yahtzee game.
        :return dict: initial game state.
        """
        self.rounds_played = 0
        self.rolls_left = self.max_rolls
        self.final_score = 0
        self.scores = {}
        self.available_categories = [
            '1', '2', '3', '4', '5', '6',
            'chance',
            'brelan',
            'carre',
            'yahtzee',
            'full',
            'petite_suite',
            'grande_suite',
        ]
        self.current_dice = self.roll_dices(number_of_dice=self.num_dice)
        self.kept = np.zeros(self.num_dice, dtype=bool)  # which dice are kept between rolls
        self.done = False
        return self.get_state()

    def get_state(self):
        """
        Representing the current game state, including dice, scores, available categories.
        :return dict: initial game state.
        """
        return {
            "dice": self.current_dice.copy(),
            "rolls_left": self.rolls_left,
            "rounds_played": self.rounds_played,
            "available_categories": self.available_categories.copy(),
            "scores": self.scores.copy(),
            "final_score": self.final_score,
            "done": self.done
        }
    
    def roll_dices(self, number_of_dice=5):
        """Rolls the specified number of dice and returns the result as a numpy array."""
        return np.random.randint(1, 7, size=number_of_dice)

    def reroll(self, keep_mask):
        """Given a list of 5 booleans (True = keep, False = reroll).
        Rerolls only the dice the player wants to change.
        """
        new_dice = self.current_dice.copy()
        for i in range(5):
            if not keep_mask[i]:
                new_dice[i] = self.roll_dices(number_of_dice=1)[0]
        self.current_dice = new_dice
        self.rolls_left -= 1

    def score_round(self, category):
        score = self.compute_score(category, self.current_dice)
        self.scores[category] = score
        self.final_score += score
        self.available_categories.remove(category)
        self.rounds_played += 1
        self.rolls_left = self.max_rolls
        if self.rounds_played >= 13:
            # Apply upper bonus
            upper_total = sum(self.scores.get(str(i), 0) for i in range(1, 7))
            if upper_total >= 63:
                self.final_score += 35
            self.done = True
        else:
            self.current_dice = self.roll_dices(number_of_dice=self.num_dice)
        return score

    def step(self, action):
        """
        Step logic:
        - action is a tuple of (keep_mask, chosen_category)
        - if rerolls left, apply keep_mask
        - if no rerolls left or player chooses, apply score
        """
        if self.done:
            return self.get_state(), 0, True, {}

        if self.rolls_left > 1:
            keep_mask, category = action
            self.reroll(keep_mask)
            return self.get_state(), 0, False, {}
        else:
            # last roll: must score
            _, category = action
            if category not in self.available_categories:
                raise ValueError("Invalid scoring category selected.")
            reward = self.score_round(category)
            return self.get_state(), reward, self.done, {}

    def compute_score(self, category, dices):
        """Calculates the score for the given category based on the dice rolled, according to Yahtzee rules.

        :return int: Category score.
        """
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
        elif category == 'yahtzee':
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

    def run_game(self):
        """Run a 13 rounds Yahtzee game."""
        if self.verbose:
            print("Starting Yahtzee Game...\n")
        while not self.done:
            if self.verbose:
                print(f"Rolls left: {self.rolls_left}")
                print(f"Dice: {self.current_dice.tolist()}")

            if self.rolls_left > 1:
                # Keep highest dice for simplicity
                keep_mask = [val >= 5 for val in self.current_dice]
                action = (keep_mask, None)
            else:
                category = random.choice(self.available_categories)
                if self.verbose:
                    print(f"Scoring category: {category}")
                action = ([True]*5, category)

            state, reward, done, _ = self.step(action)

    
        if self.verbose:
            print(f"Final Score: {self.final_score}")
            print("Category Scores:")
            for cat, score in sorted(self.scores.items()):
                print(f"  {cat}: {score}")


# Main thread.
if __name__ == "__main__":
    a = YahtzeeGame()
    a.run_game()
    print(a.get_state())
