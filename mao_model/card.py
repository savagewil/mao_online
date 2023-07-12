from mao_model.ranks import Ranks
from mao_model.suits import Suits


class Card:
    def __init__(self, suit: Suits, rank: Ranks):
        self.suit = suit
        self.rank = rank

    def to_dict(self):
        return {"suit": self.suit.name, "rank": self.rank.name}

    def __str__(self):
        return F"Card[{self.rank.name} of {self.suit.name}]"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, card):
        print(card["suit"], card["rank"])
        return cls(Suits[card["suit"]], Ranks[card["rank"]])
