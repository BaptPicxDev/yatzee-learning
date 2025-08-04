# Import
import numpy as np
import random
from src.utils import compute_score

# Class
class YahtzeeGame:
    def __init__(self, strategy=None):
        """Initializes the Yahtzee game with settings.
        Call reset() to start a new game.
        """
        self.num_dice = 5
        self.max_rolls = 3
        self.verbose = False
        self.strategy = strategy
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
        score = compute_score(category, self.current_dice)
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

    def run_game(self):
        """Run a 13 rounds Yahtzee game."""
        if self.verbose:
            print("Starting Yahtzee Game...\n")
        while not self.done:
            if self.verbose:
                print(f"Rolls left: {self.rolls_left}")
                print(f"Dice: {self.current_dice.tolist()}")

            if self.rolls_left > 1:
                if self.strategy is not None:
                    keep_mask = self.strategy.choose_dice_to_keep(
                        dice=self.current_dice.copy(),
                        rolls_left=self.rolls_left,
                        available_categories=self.available_categories.copy()
                    )
                else:
                    keep_mask = [True] * 5  # default fallback
    
                action = (keep_mask, None)
            else:
                if self.strategy is not None:
                    category = self.strategy.choose_category(
                        dice=self.current_dice.copy(),
                        available_categories=self.available_categories.copy()
                    )
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
