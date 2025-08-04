# Import
import numpy as np
import random
from src.utils import compute_score

# Class
class YahtzeeStrategy:
    """
    Baseline strategy (without strategy or with strategy=None) achieves 50 points mean score.
    Out of 100K games.
    """
    def __init__(self):
        self.memory = []  # optional: store game data

    def choose_dice_to_keep(self, dice, rolls_left, available_categories):
        """Returns a mask (list of bool) indicating which dice to keep."""
        raise NotImplementedError

    def choose_category(self, dice, available_categories):
        """Returns a category from the available ones to score."""
        # Default baseline: random choice
        raise NotImplementedError


class NaiveStrategy(YahtzeeStrategy):
    """
    Naive strategy achieves 140 points mean score.
    Out of 100K games.
    We only keep 5 & 6.
    """
    def choose_dice_to_keep(self, dice, rolls_left, available_categories):
        # Garde tous les dés >= 5
        return [d >= 5 for d in dice]

    def choose_category(self, dice, available_categories):
        # Choisit la catégorie qui donne le meilleur score immédiat
        best_score = -1
        best_cat = None
        for cat in available_categories:
            score = compute_score(cat, np.array(dice))
            if score > best_score:
                best_score = score
                best_cat = cat
        return best_cat

if __name__ == "__main__":
    strategy = NaiveStrategy()
