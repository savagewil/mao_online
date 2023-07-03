from mao_model.hand import Hand


class Player:
    def __init__(self, name: str, hand: Hand):
        self.name = name
        self.hand = hand
