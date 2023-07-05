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
        properties["players"] = self.players
        event = MaoEvent(**properties)
        self.LOG(f"Added event {event}")
        self.eventQueue.append(event)

    def drawCards(self, player: str, deck: str, count: int):
        player_ = self.players[player]
        deck_ = self.decks[deck]
        for _ in range(count):
            card = deck_.draw()
            player_.hand.add(card)
            self.addEvent(type="draw", player=player, player_dict=self.players[player].to_dict(), deck=deck,
                          card=card.to_dict())
        self.chat.append(f"{player} drew {count} cards from {deck}")

    def dealCards(self, deck_from: str, deck_to: str, count: int):
        deck_from_ = self.decks[deck_from]
        deck_to_ = self.decks[deck_to]
        for _ in range(count):
            card = deck_from_.draw()
            deck_to_.add_to_top(card)
            self.addEvent(type="deal", deck_from=deck_from, deck_to=deck_to, card=card.to_dict())
        self.chat.append(f"Dealt {count} cards from {deck_from} to {deck_to}")

    def playCard(self, player: str, deck: str, index: str):
        self.LOG(f"{player} plays {index} on {deck} ")
        player_ = self.players[player]
        deck_ = self.decks[deck]
        card = player_.hand.play(int(index))
        deck_.add_to_top(card)
        self.chat.append(f"{player} played card on {deck}")
        self.addEvent(type="play", player=player, deck=deck, card=card.to_dict(),
                      player_dict=self.players[player].to_dict())

    def addDeck(self, deck_name: str, face_up=False, empty=False):
        self.decks[deck_name] = Deck([], face_up) if empty else Deck.get_shuffled_deck()
        self.decks[deck_name].face_up = face_up
        self.chat.append(f"Deck: {deck_name} added")
        self.addEvent(type="deck", deck=deck_name)

    def addPlayer(self, player_name: str):
        self.players[player_name] = Player(player_name, Hand([]))
        self.chat.append(f"Player: {player_name} added")
        self.addEvent(type="player", player=player_name)

    def setGameProperty(self, property: str, value: str):
        table = self.properties
        variables = property.split(".")
        for var in variables[:-1]:
            if var in table and isinstance(table[var], dict):
                table = table[var]
            else:
                table[var] = {}
                table = table[var]
        table[variables[-1]] = value
        self.chat.append(f"Property: {property} set to {value}")
        self.addEvent(type="property_update", property=property, value=value)

    def sendChat(self, player: str, message: str):
        self.chat.append(f"{player}: {message}")
        if player in self.players:
            self.addEvent(type="chat", player=player, player_dict=self.players[player].to_dict(), message=message)
        else:
            self.addEvent(type="chat", player=player, player_dict={}, message=message)

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
