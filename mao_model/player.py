from mao_model.hand import Hand


class Player:
    def __init__(self, name: str, hand: Hand):
        self.name = name
        self.hand = hand

    def __str__(self):
        dict_ = {"name": self.name, "hand": self.hand}
        return f"Player {dict_}"

    def __repr__(self):
        return self.__str__()
