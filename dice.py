from random import randint

class Dice:
    def __init__(self):
        self._sides = 6
        self._min = 1
    
    def roll(self):
        return randint(self._min, self._sides)