from mao_model.ranks import Ranks
from mao_model.suits import Suits


class Card:
    def __init__(self, suit: Suits, rank: Ranks):
        self.suit = suit
        self.rank = rank

    def to_dict(self):
        return {"suit": self.suit.name, "rank": self.rank.name}
