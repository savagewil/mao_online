from typing import List

from mao_model.card import Card


class Hand:
    def __init__(self, cards: List[Card], face_up: bool = False):
        self.face_up = face_up
        self.cards = cards

    def play(self, idx: int):
        return self.cards.pop(idx)

    def peek(self, idx: int):
        return self.cards[idx]

    def add(self, card: Card):
        self.cards.append(card)

    def flip(self):
        self.face_up = not self.face_up
