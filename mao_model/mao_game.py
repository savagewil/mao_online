from typing import Dict, List

from mao_model.deck import Deck
from mao_model.hand import Hand
from mao_model.mao_event import MaoEvent
from mao_model.player import Player


class MaoGame:
    def __init__(self, players: Dict[str, Player], decks: Dict[str, Deck], rules: Dict[str, object], properties={},
                 verbose=False):
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
        properties["game"] = self.to_dict()
        event = MaoEvent(**properties)
        self.LOG(f"Added event {event}")
        self.eventQueue.append(event)

    def drawCards(self, player: str, deck: str, count: int):
        player_ = self.players[player]
        deck_ = self.decks[deck]
        cards = deck_.draw(count)
        for card in cards:
            player_.hand.add(card)
            self.addEvent(type="draw", player=player, player_dict=self.players[player].to_dict(), deck=deck,
                          deck_dict=deck_.to_dict(),
                          card=card.to_dict())
        self.chat.append(f"{player} drew {count} cards from {deck}")

    def dealCards(self, deck_from: str, deck_to: str, count: int, shuffled=False, bottom=False):
        deck_from_ = self.decks[deck_from]
        deck_to_ = self.decks[deck_to]
        cards = deck_from_.draw(count, not bottom)
        for card in cards:
            deck_to_.add_to_top(card)
            self.addEvent(type="deal", deck_from=deck_from, deck_to=deck_to, card=card.to_dict())
        if shuffled:
            deck_to_.shuffle()
        if count > 1:
            self.chat.append(f"Dealt {count} cards from {deck_from} to {deck_to}")
        else:
            self.chat.append(f"Dealt {cards[0]} from {deck_from} to {deck_to}")

    def playCard(self, player: str, deck: str, index: str):
        self.LOG(f"{player} plays {index} on {deck} ")
        player_ = self.players[player]
        deck_ = self.decks[deck]
        card = player_.hand.play(int(index))
        deck_.add_to_top(card)
        self.chat.append(f"{player} played {card} on {deck}")
        self.addEvent(type="play", player=player, deck=deck, card=card.to_dict(),
                      player_dict=self.players[player].to_dict())

    def addDeck(self, deck_name: str, face_up=False, empty=False):
        self.decks[deck_name] = Deck([], face_up) if empty else Deck.get_shuffled_deck()
        self.decks[deck_name].face_up = face_up
        self.LOG(f"Deck: {deck_name} added")
        self.addEvent(type="deck", deck=deck_name)

    def addPlayer(self, player_name: str):
        self.players[player_name] = Player(player_name, Hand([]))
        self.LOG(f"Player: {player_name} added")
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
        self.LOG(f"Property: {property} set to {value}")
        self.addEvent(type="property_update", property=property, value=value)

    def sendChat(self, player: str, message: str):
        self.chat.append(f"{player}: {message}")
        if player in self.players:
            self.addEvent(type="chat", player=player, player_dict=self.players[player].to_dict(), message=message)
        else:
            self.addEvent(type="chat", player=player, player_dict={}, message=message)

    def handle_event(self, event: MaoEvent):
        self.LOG(f"Handled event {event}")
        for rule in self.rules.values():
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
        limit = 1000
        for _ in range(limit):
            if self.eventQueue:
                self.handle_event(self.eventQueue.pop(0))
            else:
                return

    def to_dict(self):
        return dict(
            players={player_name: player.to_dict() for player_name, player in self.players.items()},
            decks={deck_name: deck.to_dict() for deck_name, deck in self.decks.items()},
            chat=self.chat,
            **self.properties
        )


if __name__ == '__main__':
    game = MaoGame()
    game.main()
