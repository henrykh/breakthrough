import random


class Player():
    def __init__(self):
        self.hand = []


class Game():

    def __init__(self):
        self.won = False
        self.deck = Deck()
        self.deck.shuffle()

        # Init players, pick start player
        self.player1 = Player()
        self.player2 = Player()
        self.currentPlayer = random.choice([self.player1, self.player2])

        # Deal hands
        for i in range(7):
            self.deck.draw(self.player1)
            self.deck.draw(self.player2)

        # initialize flags, flag control tracking
        self.flags = [[[], []] for i in range(7)]
        self.flag_control = []*7

    # print out the board state
    def display(self):
        for flag in self.flags:
            for stack in flag:
                print " ".join(stack) + " | "


class Deck():

    def __init__(self):
        self._deck = [Card(val, color) for val in range(1, 11)
                      for color in ["R", "G",
                                    "B", "P",
                                    "Y", "O"]]

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
        return "{}{}".format(self.val, self.color)

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    game = Game()
