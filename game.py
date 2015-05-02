import random


class Player():
    def __init__(self):
        self.hand = Hand()


class Game():

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.player1 = Player()
        self.player2 = Player()
        self.currentPlayer = random.choice[self.player1, self.player2]
        for i in range(7):
            self.deck.draw(self.player1)
            self.deck.draw(self.player2)


class Deck():
    
    def __init__(self):
        self._deck = [Card(val, color) for val in range(1, 11)
                         for color in ["red", "green",
                                       "blue", "purple",
                                       "yellow", "orange"] ]

    def draw(self, player):
        card = self._deck.pop()
        player.hand.append(card)

    def shuffle(self):
        random.shuffle(self._deck)


class Card():
    def __init__(self, val, color):
        self.val = val
        self.color = color

    def __str__(self):
        return "{} {}".format(self.val, self.color)


class Hand():
    def __init__(self):
        self._hand = []
