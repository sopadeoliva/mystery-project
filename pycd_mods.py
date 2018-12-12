# pyCardDeck package by David Jetelina
# Source --> https://github.com/iScrE4m/pyCardDeck
from pyCardDeck import BaseCard, PokerCard
from typing import Union


class Card(BaseCard):

    suits = {'h': 'Hearts', 's': 'Spades', 'd': 'Diamonds', 'c': 'Clubs'}
    names = {'A': 'Ace',
             '2': 'Two',
             '3': 'Three',
             '4': 'Four',
             '5': 'Five',
             '6': 'Six',
             '7': 'Seven',
             '8': 'Eight',
             '9': 'Nine',
             '10': 'Ten',
             'J': 'Jack',
             'Q': 'Queen',
             'K': 'King'}


    def __init__(self, name: str, suit: str, rank: str, deck: str = None):
        if name == 'Joker':
            super().__init__(name)
            self.suit = None
        else:
            super().__init__("{} of {}".format(name, suit))
            self.suit = suit
        self.rank = rank
        # Deck color -> for use in double decks
        self._deck = deck

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        if self._deck:
            return '{} ({})'.format(self.name, self._deck)
        return self.name

    @staticmethod
    def alias():
        dic = {num+suit: '{} of {}'.format(Card.names[num], Card.suits[suit])
               for num in Card.names for suit in Card.suits}
        dic.update({'JK': 'Joker'})
        return dic


CardType = Union[Card, BaseCard, PokerCard, object, str, int]
