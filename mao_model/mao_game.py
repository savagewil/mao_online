from typing import Dict, List

from mao_model.deck import Deck
from mao_model.hand import Hand
from mao_model.mao_event import MaoEvent
from mao_model.player import Player


class MaoGame:
    def __init__(self, players: Dict[str, Player], decks: Dict[str, Deck], rules: List, properties={}, verbose=False):
        self.players = players
        self.decks = decks
        self.rules = rules
        self.chat: List[str] = []
        self.eventQueue: List[MaoEvent] = []
        self.properties = properties
        self.over = False
        self.verbose = verbose

    def LOG(self, message: str):
        if self.verbose:
            print(message)

    def addEvent(self, **properties):
        properties["game_properties"] = self.properties
        event = MaoEvent(**properties)
        self.LOG(f"Added event {event}")
        self.eventQueue.append(event)

    def drawCards(self, player: str, deck: str, count: int):
        player_ = self.players[player]
        deck_ = self.decks[deck]
        for _ in range(count):
            card = deck_.draw()
            player_.hand.add(card)
            self.addEvent(type="draw", player=player, deck=deck, card=card.to_dict())
        self.chat.append(f"{player} drew {count} cards from {deck}")

    def playCard(self, player: str, deck: str, index: int):
        player_ = self.players[player]
        deck_ = self.decks[deck]
        card = player_.hand.play(index)
        deck_.add_to_top(card)
        self.chat.append(f"{player} played card on {deck}")
        self.addEvent(type="play", player=player, deck=deck, card=card.to_dict())

    def addDeck(self, deck_name: str, face_up=False, deck=None):
        self.decks[deck_name] = deck if deck is not None else Deck.get_shuffled_deck()
        self.decks[deck_name].face_up = face_up
        self.chat.append(f"Deck: {deck_name} added")
        self.addEvent(type="deck", deck=deck)

    def addPlayer(self, player_name: str):
        self.players[player_name] = Player(player_name, Hand([]))
        self.chat.append(f"Player: {player_name} added")
        self.addEvent(type="player", player=player_name)

    def setGameProperty(self, property: str, value: str):
        self.properties[property] = value
        self.chat.append(f"Property: {property} set to {value}")
        self.addEvent(type="property_update", property=property, value=value)

    def sendChat(self, player: str, message: str):
        assert player in self.players
        self.chat.append(f"{player}: {message}")
        self.addEvent(type="chat", player=player, message=message)

    def handle_event(self, event: MaoEvent):
        for rule in self.rules:
            rule.handle_event(event, self)

    def start_game(self):
        self.addEvent(type="start")

    def end_game(self):
        self.over = True
        self.addEvent(type="end")

    def dump_queue(self):
        queue, self.eventQueue = self.eventQueue, []
        return queue

    def handle_events(self):
        for event in self.dump_queue():
            self.handle_event(event)


if __name__ == '__main__':
    game = MaoGame()
    game.main()
