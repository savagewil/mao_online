from typing import Dict, List

from mao_model.deck import Deck
from mao_model.hand import Hand
from mao_model.mao_event import MaoEvent
from mao_model.player import Player


class MaoGame:
    def __init__(self, players: Dict[str, Player], decks: Dict[str, Deck], rules: List, properties={}):
        self.players = players
        self.decks = decks
        self.rules = rules
        self.chat: List[str] = []
        self.eventQueue: List[MaoEvent] = []
        self.properties = properties
        self.over = False

    def addEvent(self, event: MaoEvent):
        self.eventQueue.append(event)

    def drawCards(self, player: str, deck: str, count: int):
        player_ = self.players[player]
        deck_ = self.decks[deck]
        for _ in range(count):
            card = deck_.draw()
            player_.hand.add(card)
            self.addEvent(MaoEvent(type="draw", player=player, deck=deck, card=card.to_dict()))
        self.chat.append(f"{player} drew cards from {deck}")

    def playCard(self, player: str, deck: str, index: int):
        player_ = self.players[player]
        deck_ = self.decks[deck]
        card = player_.hand.play(index)
        deck_.add_to_top(card)
        self.chat.append(f"{player} played card on {deck}")
        self.addEvent(MaoEvent(type="play", player=player, deck=deck, card=card.to_dict()))

    def addDeck(self, deck_name: str, face_up=False, deck=None):
        self.decks[deck_name] = deck if deck is not None else Deck.get_full_deck()
        self.decks[deck_name].face_up = face_up
        self.chat.append(f"Deck: {deck_name} added")
        self.addEvent(MaoEvent(type="deck", deck=deck))

    def addPlayer(self, player_name: str):
        self.players[player_name] = Player(Hand([]))
        self.chat.append(f"Player: {player_name} added")
        self.addEvent(MaoEvent(type="player", deck=player_name))

    def setGameProperty(self, property: str, value: str):
        self.properties[property] = value
        self.chat.append(f"Property: {property} set to {value}")
        self.addEvent(MaoEvent(type="property_update", property=property, value=value))

    def sendChat(self, player: Player, message: str):
        self.chat.append(message)
        self.addEvent(MaoEvent(type="chat", player=player, message=message))

    def handle_event(self, event: MaoEvent):
        for rule in self.rules:
            rule.handle_event(event, self)

    def start_game(self):
        self.addEvent(MaoEvent(type="start"))

    def end_game(self):
        self.over = True
        self.addEvent(MaoEvent(type="end"))

    def dump_queue(self):
        queue, self.eventQueue = self.eventQueue, []
        return queue


if __name__ == '__main__':
    game = MaoGame()
    game.main()
