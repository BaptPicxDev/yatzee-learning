# Import
import numpy as np

# Variables
available_categories = [
    '1', '2', '3', '4', '5', '6',
    'chance',
    'brelan',
    'carre',
    'yahtzee',
    'full',
    'petite_suite',
    'grande_suite',
]

# functions
def compute_score(category, dices):
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