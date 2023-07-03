import json

from mao_model.action import Action, NONE_ACTION
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class Rule:
    def __init__(self, name: str, eventSchema: MaoEvent,
                 positive_action: Action = NONE_ACTION,
                 negative_action: Action = NONE_ACTION):
        self.name = name
        self.eventSchema: MaoEvent = eventSchema
        self.positive_action: Action = positive_action
        self.negative_action: Action = negative_action

    def handle_event(self, event: MaoEvent, game: MaoGame):
        if self.eventSchema.match(event):
            self.positive_action.run(event, game)
        else:
            self.negative_action.run(event, game)

    def to_dict(self):
        return {"name": self.name,
                "eventSchema": self.eventSchema.to_dict(),
                "positive_action": self.positive_action.to_dict(),
                "negative_action": self.negative_action.to_dict()}

    @classmethod
    def from_dict(cls, json_dict):
        return cls(name=json_dict["name"], eventSchema=MaoEvent.from_dict(json_dict["eventSchema"]),
                   positive_action=Action.from_dict(json_dict["positive_action"]),
                   negative_action=Action.from_dict(json_dict["negative_action"]))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        json_ = json.loads(json_str)
        if isinstance(json_, dict):
            return cls.from_dict(json_)
        elif isinstance(json_, list):
            return [cls.from_dict(dict_) for dict_ in json_]
