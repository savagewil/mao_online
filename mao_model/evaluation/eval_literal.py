from mao_model.evaluation.eval import Eval
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class EvalLiteral(Eval):
    def __init__(self, value):
        self.value = value

    def get_value(self, event: MaoEvent, game: MaoGame):
        return self.value

    def to_dict(self) -> dict:
        return self.value

    @classmethod
    def from_dict(cls, obj: object):
        cls(obj)
