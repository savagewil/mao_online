from typing import Dict, List

from mao_model.deck import Deck
from mao_model.mao_event import MaoEvent
from mao_model.player import Player


class MaoGame:
    def __init__(self, players: Dict[str, Player], decks: Dict[str, Deck], rules: List):
        self.players = players
        self.decks = decks
        self.rules = rules
        self.chat: List[str] = []
        self.eventQueue: List[MaoEvent] = []

    def addEvent(self, event: MaoEvent):
        self.eventQueue.append(event)

    def drawCards(self, player: Player, deck: Deck, count: int):
        pass

    def playCard(self, player: Player, deck: Deck, index: int):
        pass

    def addDeck(self, deck_name: str, face_up=False, deck=None):
        pass

    def addPlayer(self, player_name: str):
        pass

    def sendChat(self, player: Player, message: str):
        pass


if __name__ == '__main__':
    game = MaoGame()
    game.main()
