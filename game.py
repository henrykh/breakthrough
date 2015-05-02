import random


class Deck():
    
    def __init__(self):
        self._deck = [Card(val, color) for val in range(1, 11)
                         for color in ["red", "green",
                                       "blue", "purple",
                                       "yellow", "orange"] ]

    def draw(self):
        return self._deck.pop()

    def shuffle(self):
        random.shuffle(self._deck)


class Card():
    def __init__(self, val, color):
        self.val = val
        self.color = color

    def __str__(self):
        return "{} {}".format(self.val, self.color)
