from typing import List

from mao_model.card import Card


class Hand:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def play(self, idx: int):
        return self.cards.pop(idx)

    def peek(self, idx: int):
        return self.cards[idx]

    def add(self, card: Card):
        self.cards.append(card)
