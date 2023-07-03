from enum import Enum

from mao_model.evaluation.eval import Eval
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class EvalBinaryOperations(Enum):
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    MULTIPLY = "*"
    IF = "if"
    MOD = "%"


class EvalBinary(Eval):
    def __init__(self, op: EvalBinaryOperations, eval_0: Eval, eval_1: Eval):
        self.op = op
        self.eval_0 = eval_0
        self.eval_1 = eval_1

    def get_value(self, event: MaoEvent, game: MaoGame):
        return self.value

    def to_dict(self) -> dict:
        return self.value

    @classmethod
    def from_dict(cls, obj: object):
        cls(obj)
