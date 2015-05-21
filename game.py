import random


class Player(object):
    def __init__(self, playerNumber):
        self.hand = []
        self.playerNumber = playerNumber

    def __str__(self):
        return "Player " + str(self.playerNumber)

    def __repr__(self):
        return self.__str__()


class Game(object):

    def __init__(self):
        self.won = False
        self.deck = Deck()
        self.deck.shuffle()

        # Init players, pick start player
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.currentPlayer = random.choice([self.player1, self.player2])

        # Deal hands
        for i in range(7):
            self.deck.draw(self.player1)
            self.deck.draw(self.player2)

        # initialize flags, flag control tracking
        self.flags = [([], []) for i in range(7)]
        self.flag_control = [None for i in range(7)]

    def run_game(self):
        while not self.won:
            print "{}'s Turn".format(self.currentPlayer)


            # flag selection
            valid_move = False
            while not valid_move:
                flag = None

                while flag is None or flag == 'display':
                    flag = raw_input(
                        "Where would you like to play (Enter a flag number, 1-7)? ")
                    if flag == 'display':
                        self.display()
                    else:
                        try:
                            flag = int(flag) - 1
                        except ValueError:
                            flag = None
                            print "Flag must be a number between 1-7"

                # card selection
                played_card = ""
                while not played_card or played_card == 'hand':
                    played_card = raw_input("Which card would you like to play (Enter 'hand' to see your cards)? ")
                    if played_card == 'hand':
                        print self.currentPlayer.hand
                valid_move = self.playCard(flag, played_card)

            self.endTurn()

    # TODO: clean up the logic here, reduce redundancy
    def playCard(self, flag, played_card):
        currentPlayersSide = self.flags[flag][self.currentPlayer.playerNumber-1]
        # is the card in the players hand
        # how to validate their input ?
        for card in self.currentPlayer.hand:
            if played_card == card.__str__():
                played_card = card
                break
        else:
            played_card = raw_input("Hmm you don't have that card. Try again (Enter 'hand' to see your cards)? ")
            return self.playCard(flag, played_card)

        # make sure the flag number is in the correct range
        if flag not in range(0, 7):
            flag = raw_input("Not a valid flag. Try again (Enter a number, 1-7) ")
            return self.playCard(flag, played_card)

        # make sure the flag hasn't already been claimed
        elif self.flag_control[flag]:
            flag = raw_input("That flag has already been taken. Try again (Enter a number, 1-7")
            return self.playCard(flag, played_card)

        # make sure the player hasn't already played three cards there
        elif len(currentPlayersSide) == 3:
            flag = raw_input("You have already placed three cards there. Try again (Enter a number, 1-7")
            return self.playCard(flag, played_card)
        else:
            # remove the card from the player's hand
            self.currentPlayer.hand.remove(played_card)

            currentPlayersSide.append(played_card)
            if len(currentPlayersSide) == 3:
                winner = self.check_flag_control(self.flags[flag])
                if winner:
                    self.flag_control[flag] = winner
            return True

    # current player draws
    # switch active player
    # check game end
    def endTurn(self):
        self.deck.draw(self.currentPlayer)

        # make this better
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

        # Check if game is over


    # print out the board state
    def display(self):
        for flag in self.flags:
            print flag[0].__str__() + " | " + flag[1].__str__()

    def check_flag_control(self, flag):
        player_1_side, player_2_side = flag[0], flag[1]
        if len(player_1_side) == 3 and len(player_2_side) == 3:
            if(self.get_side_strength(player_1_side) > (
               self.get_side_strength(player_2_side))):
                return self.player1
            # bugged when sides are equal
            else:
                return self.player2
        else:
            # if one player has fewer than three can it be claimed?
            pass

    # give side a numerical value for comparison
    def get_side_strength(self, side):
        strength = 0
        side.sort(key=lambda x: x.val)

        # get sum of side
        for card in side:
            strength += card.val

        # is straight?
        if side[1].val == side[0].val + 1 and side[2].val == side[1].val + 1:
            strength += 100

        # is flush?
        if side[0].color == side[1].color == side[2].color:
            strength += 200

        # is three of a kind
        elif side[0].val == side[1].val == side[2].val:
            strength += 250

        return strength


class Deck(object):

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


class Card(object):
    def __init__(self, val, color):
        self.val = val
        self.color = color

    def __str__(self):
        return "{}{}".format(self.val, self.color)

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    game = Game()
    game.run_game()
