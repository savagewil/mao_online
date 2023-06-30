import random
from typing import List, Self

from mao_model.card import Card
from mao_model.ranks import Ranks
from mao_model.suits import Suits


class Deck:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    @classmethod
    def get_full_deck(cls):
        cards = []
        for suit in Suits:
            for rank in Ranks:
                cards.append(Card(suit, rank))
        return cls(cards)

    @classmethod
    def get_shuffled_deck(cls):
        deck = cls.get_full_deck()
        deck.shuffle()
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0)

    def peek(self):
        return self.cards[0]

    def add_to_bottom(self, card: Card):
        self.cards.append(card)

    def add_to_top(self, card: Card):
        self.cards.insert(0, card)

    def shuffle_in(self, deck: Self):
        self.cards.extend(deck.cards)
        self.shuffle()
        deck.cards = []
