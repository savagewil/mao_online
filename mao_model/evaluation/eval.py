import json
from abc import ABC

from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class Eval(ABC):
    def get_value(self, event: MaoEvent, game: MaoGame):
        pass

    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, json_dict: dict):
        pass

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        json_ = json.loads(json_str)
        if isinstance(json_, dict):
            return cls.from_dict(json_)
        elif isinstance(json_, list):
            return [cls.from_dict(dict_) for dict_ in json_]
