from mao_model.evaluation.eval import Eval
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class EvalBinaryOperations(Enum):
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    MULTIPLY = "*"
    MOD = "%"


class EvalBinary(Eval):
    def __init__(self, op: EvalBinaryOperations, eval_0: Eval, eval_1: Eval):
        self.op = op
        self.eval_0 = eval_0
        self.eval_1 = eval_1

    def get_value(self, event: MaoEvent, game: MaoGame) -> object:
        match self.op:
            case EvalBinaryOperations.PLUS:
                return self.eval_0.get_value(event, game) + self.eval_1.get_value(event, game)
            case EvalBinaryOperations.MINUS:
                return self.eval_0.get_value(event, game) - self.eval_1.get_value(event, game)
            case EvalBinaryOperations.DIVIDE:
                return self.eval_0.get_value(event, game) / self.eval_1.get_value(event, game)
            case EvalBinaryOperations.MULTIPLY:
                return self.eval_0.get_value(event, game) * self.eval_1.get_value(event, game)
            case EvalBinaryOperations.MOD:
                return self.eval_0.get_value(event, game) % self.eval_1.get_value(event, game)
