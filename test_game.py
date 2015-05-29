from game import Game, Deck, Card, Player
import pytest

@pytest.fixture
def test_game():
    test_game = Game()
    test_game.flags[1] = ([Card(5, 'O'), Card(6, 'O'), Card(7, 'O')],
                          [Card(10, 'P'), Card(10, 'O')])

    return test_game


def test_card_constructor():
    test_card = Card(10, 'G')
    assert test_card.val == 10
    assert test_card.color == 'G'


def test_deck_constructor():
    test_deck = Deck()
    assert len(test_deck._deck) == 60


def test_run_game():
    test_game = Game()
    test_game.run_game()


# checks that straight flush beats two of a kind
def test_flag_control_straight_flush_vs_2of(test_game):
    assert test_game.check_flag_control(test_game.flags[1]) == (
        test_game.player1)


# checks that straight flush beats three of a kind
def test_flag_control_straight_flush_vs_3of(test_game):
    test_game.flags[1][1].append(Card(10, 'G'))
    assert test_game.check_flag_control(test_game.flags[1]) == (
        test_game.player1)
