from enum import Enum

from mao_model.evaluation.eval import Eval
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class EvalUnaryOperations(Enum):
    NOT = "!"


class EvalUnary(Eval):
    def __init__(self, op: EvalUnaryOperations, eval_0: Eval):
        self.op = op
        self.eval_0 = eval_0

    def get_value(self, event: MaoEvent, game: MaoGame) -> object:
        match self.op:
            case EvalUnaryOperations.NOT:
                return not self.eval_0.get_value(event, game)
