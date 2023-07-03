from mao_model.action_types import ActionTypes
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class Action:
    def __init__(self, action_type: ActionTypes, properties: dict = {}):
        self.action_type = action_type
        self.properties = properties

    def run(self, event: MaoEvent, game: MaoGame):
        if self.action_type == ActionTypes.ADD_EVENT:
            event_properties = {}
            for key, val in self.properties:
                event_properties[key] = self.get_property(event, key)
            game.addEvent(MaoEvent(**event_properties))
        elif self.action_type == ActionTypes.DRAW_CARDS:
            game.drawCards(self.get_property(event, "player"),
                           self.get_property(event, "deck"),
                           int(self.get_property(event, "count")))
        elif self.action_type == ActionTypes.PLAY_CARD:
            game.playCard(self.get_property(event, "player"),
                          self.get_property(event, "deck"),
                          int(self.get_property(event, "index")))
        elif self.action_type == ActionTypes.ADD_DECK:
            game.addDeck(self.get_property(event, "deck"),
                         bool(self.get_property(event, "face_up", False)))
        elif self.action_type == ActionTypes.ADD_PLAYER:
            game.addPlayer(self.get_property(event, "player"))
        elif self.action_type == ActionTypes.SEND_CHAT:
            game.sendChat(game.players[self.get_property(event, "player")], self.get_property(event, "message"))
        else:
            pass

    def get_property(self, event: MaoEvent, game: MaoGame, name: str, default=None):
        if name in self.properties:
            if self.properties[name][:2] == "{{":
                variables = self.properties[name][2:-2].split(".")
                source = variables[0]
                variables = variables[1:]
                table = None
                if source == "game":
                    table = game.properties
                    for var in variables:
                        table = table[var]
                else:
                    table = event.properties
                    for var in variables:
                        table = table[var]
                assert isinstance(table, str)
                return table
            else:
                return self.properties[name]
        return default

    def to_dict(self) -> dict:
        return {
            "properties": self.properties,
            "action_type": self.action_type.name
        }

    @classmethod
    def from_dict(cls, json_dict: dict):
        return cls(action_type=ActionTypes[json_dict["action_type"]], properties=json_dict["properties"])


NONE_ACTION = Action(ActionTypes.NONE, {})
