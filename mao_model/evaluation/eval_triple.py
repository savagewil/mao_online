from enum import Enum

from mao_model.evaluation.eval import Eval
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class EvalTripleOperations(Enum):
    IF = "if"


class EvalTriple(Eval):
    def __init__(self, op: EvalTripleOperations, eval_0: Eval, eval_1: Eval, eval_2: Eval):
        self.op = op
        self.eval_0 = eval_0
        self.eval_1 = eval_1
        self.eval_2 = eval_2

    def get_value(self, event: MaoEvent, game: MaoGame) -> object:
        match self.op:
            case EvalTripleOperations.IF:
                if self.eval_0.get_value(event, game):
                    return self.eval_1.get_value(event, game)
                else:
                    return self.eval_2.get_value(event, game)
