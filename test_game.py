from game import Game, Deck, Card, Player
import pytest


def test_card_constructor():
    test_card = Card(10, 'G')
    assert test_card.val == 10
    assert test_card.color == 'G'


def test_deck_constructor():
    test_deck = Deck()
    assert len(test_deck._deck) == 60


