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
            print "\n{}'s Turn".format(self.currentPlayer)

            # flag selection
            flag = self.flagValid()
            # card selection
            card = self.cardValid()

            self.playCard(flag, card)

            self.endTurn()

    def flagValid(self):
        flag = None

        while flag is None or flag == 'd' or flag == 'h':
            flag = raw_input(
                "Where would you like to play (Enter a flag number 1-7 or type 'd' to display the field or 'h' to show your hand)? ")
            if flag == 'd':
                self.display()
            elif flag == 'h':
                print self.currentPlayer.hand
            else:
                try:
                    flag = int(flag) - 1
                except ValueError:
                    flag = None
                    print "Flag must be a number between 1-7"
                    continue

                if flag not in range(0, 7):
                    flag = None
                    print "Not a valid flag."
                elif self. flag_control[flag]:
                    flag = None
                    print "That flag has already been taken."
                elif len(self.flags[flag][self.currentPlayer.playerNumber-1]) == 3:
                    flag = None
                    print "You have already placed three cards there."

        return flag

    def cardValid(self):
        played_card = ""
        while not played_card or played_card == 'h' or played_card == 'd':
            played_card = raw_input("Which card would you like to play (Enter 'h' to see your cards or 'd' to show the field)? ")
            if played_card == 'h':
                print self.currentPlayer.hand
            elif played_card == 'd':
                self.display()
            else:
                for card in self.currentPlayer.hand:
                    if played_card.upper() == card.__str__():
                        played_card = card
                        break
                else:
                    print "Hmm you don't have that card..."
                    played_card = None

        return played_card

    # TODO: clean up the logic here, reduce redundancy
    def playCard(self, flag, played_card):
        currentPlayersSide = self.flags[flag][self.currentPlayer.playerNumber-1]

        self.currentPlayer.hand.remove(played_card)

        currentPlayersSide.append(played_card)
        if len(currentPlayersSide) == 3:
            winner = self.check_flag_control(self.flags[flag])
            if winner:
                print winner.__str__() + " takes flag " + flag
                self.flag_control[flag] = winner

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
        print self.player1.__str__() + " | " + self.player2.__str__()
        for i, flag in enumerate(self.flags):
            flag_repr = flag[0].__str__() + " " + str(i+1) + " " + flag[1].__str__()
            if self.flag_control[i]:
                if self.flag_control[i] == self.player1:
                    flag_repr = "Player 1 Control " + flag_repr
                else:
                    flag_repr = flag_repr + " Player 2 Control"
            print flag_repr

    def check_flag_control(self, flag):
        player_1_side, player_2_side = flag[0], flag[1]
        if len(player_1_side) == 3 and len(player_2_side) == 3:
            if(self.get_side_strength(player_1_side) > (
               self.get_side_strength(player_2_side))):
                return self.player1
            # bugged when sides are equal
            else:
                return self.player2

        # does player2 beat player1's best possible side?
        elif len(player_1_side) == 2:
            if(self.get_side_strength(player_2_side) > (
               self.get_best_possible_strength(player_1_side))):
                return self.player2
            else:
                return None
        # does player1 beat player2's best possible side?
        elif len(player_2_side) == 2:
            if(self.get_side_strength(player_1_side) > (
               self.get_best_possible_strength(player_2_side))):
                return self.player1
            else:
                return None

        # still need to test 3 cards vs 1 card, reduce best possible based on cards in play


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

    def get_best_possible_strength(self, side):
        strength = 0
        side.sort(key=lambda x: x.val)

        for card in side:
            strength += card.val
        if side[1].val == side[0].val + 1:
            strength += 100
        elif side[0].color == side[1].color:
            strength += 200
        elif side[0].val == side[1].val:
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
