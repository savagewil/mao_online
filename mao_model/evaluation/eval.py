from enum import Enum
from typing import Union, List, Self

from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class EvalOperations(Enum):
    NOT = "!"
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    MULTIPLY = "*"
    MOD = "%"
    IF = "if"

    @classmethod
    def has_string(cls, string: str):
        return string in set(entry.value for entry in cls)


class Eval(object):
    def __init__(self, op: EvalOperations, evals: List[Self]):
        self.op = op
        self.evals = evals

    def get_value(self, event: MaoEvent, game: MaoGame) -> object:
        match self.op:
            case EvalOperations.NOT:
                return not self.evals[0].get_value(event, game)
            case EvalOperations.PLUS:
                return self.evals[0].get_value(event, game) + self.evals[1].get_value(event, game)
            case EvalOperations.MINUS:
                return self.evals[0].get_value(event, game) - self.evals[1].get_value(event, game)
            case EvalOperations.DIVIDE:
                return self.evals[0].get_value(event, game) / self.evals[1].get_value(event, game)
            case EvalOperations.MULTIPLY:
                return self.evals[0].get_value(event, game) * self.evals[1].get_value(event, game)
            case EvalOperations.MOD:
                return self.evals[0].get_value(event, game) % self.evals[1].get_value(event, game)
            case EvalOperations.IF:
                if self.evals[0].get_value(event, game):
                    return self.evals[1].get_value(event, game)
                else:
                    return self.evals[1].get_value(event, game)

    def serialize(self) -> Union[list, dict, object]:
        return [self.op.name] + [eval.serialize() for eval in self.evals]

    @classmethod
    def deserialize(cls, obj: Union[list, dict, object]) -> Self:
        if isinstance(obj, list):
            if isinstance(obj[0], str) and EvalOperations.has_string(obj[0]):
                return cls(EvalOperations(obj[0]), [cls.deserialize(eval) for eval in obj[1:]])
            else:
                return EvalLiteral(obj)
        else:
            return EvalLiteral(obj)


class EvalLiteral(Eval):
    def __init__(self, value):
        self.value = value

    def get_value(self, event: MaoEvent, game: MaoGame):
        return self.value

    def serialize(self) -> Union[list, object]:
        return self.value
