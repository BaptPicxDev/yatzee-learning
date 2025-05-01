# Import
import numpy as np


# Class
class YatzeeGame:
    def __init__(self):
        pass
    
    def roll_dice(self, number_of_dice=5):
        return np.random.randint(1, 7, size=number_of_dice)
    

# Main thread.
if __name__ == "__main__":
    a = YatzeeGame()
    print(a.roll_dice())
