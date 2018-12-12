# pyCardDeck package by David Jetelina
# Source --> https://github.com/iScrE4m/pyCardDeck


from pyCardDeck import Deck, CardNotFound
from pycd_mods import Card  # , CardType
from rules import POSSIBLE_PLAYS


def double_deck(color1, color2):
    def _double_deck(func):
        def _double():
            deck1 = func(deckcolor=color1)
            deck2 = func(deckcolor=color2)
            return Deck(name='Double Deck', cards=deck1+deck2,
                        reshuffle=False,
                        discard=Deck(name='Discard', reshuffle=False))
        return _double
    return _double_deck


@double_deck('red', 'blue')
def generate_standard(deckcolor=None):
    suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
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
    cards = [Card(suit=s, rank=r, name=n, deck=deckcolor) for s in suits
             for r, n in names.items()]
    cards.extend(2*[Card(name='Joker', suit='', rank='Jk', deck=deckcolor)])
    return cards


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.shown = []
        self.hidden = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def _play_from(self):
        if self.hand:
            return self.hand
        elif self.shown:
            return self.shown
        else:
            return self.hidden

    def draw(self, table):
        '''
        Player draws card from deck.
        '''
        card = table.deck.draw()
        self.hand.append(card)
        return card

    def drop(self, table, card):
        '''
        Player drops card from hand to the discarded.
        '''
        if card not in self._play_from:
            raise CardNotFound('the card {} was not found.'.format(card))

        if len(table.playdeck):
            if card.rank not in POSSIBLE_PLAYS[table.last.rank]:
                raise Exception('Impossible move')  # EXCEPTIONS ON HOLD
        self._play_from.remove(card)
        table.deck.discard(card)


    def take_all(self, deck):
        '''
        Player takes the whole discard deck into their hand.
        *(No se si dejar este o give_playdeck de CarecacaTable)
        '''
        pass


class CarecacaTable:
    def __init__(self, players):
        self.players = players
        self.deck = generate_standard()

        self.deck.shuffle()

    def __repr__(self):
        return "CarecacaTable -> playing: {0}".format(self.players)

    @property
    def playdeck(self):
        return self.deck._discard_pile

    @property
    def last(self):
        return self.playdeck[0]

    def _burn(self):
        self.playdeck.clear()

    def deal(self):
        # Deal 3 hidden cards to each player
        for _ in range(3):
            for p in self.players:
                p.hidden.append(self.deck.draw())
        # Deal 3 shown cards
        for _ in range(3):
            for p in self.players:
                p.shown.append(self.deck.draw())
        # Deal 3 hand cards
        for _ in range(3):
            for p in self.players:
                p.hand.append(self.deck.draw())

    def give_playdeck(self, player):
        if player not in self.players:
            raise Exception  # EXCEPTIONS ON HOLD
        for card in self.playdeck:
            player.hand.append(card)

        self._burn()



if __name__ == '__main__':
    pass
