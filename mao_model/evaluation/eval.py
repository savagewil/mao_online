from enum import Enum
from typing import Union

from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class EvalOperations(Enum):
    OR = "or"
    AND = "and"
    NOT = "!"
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    MULTIPLY = "*"
    MOD = "%"
    IF = "if"
    IF_ELSE = "if-else"
    LOAD = "load"
    SET = "set"
    INCREMENT = "++"
    DECREMENT = "--"
    EQUALS = "="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    RUN_ALL = "run all"
    APPEND = "append"
    LENGTH = "len"
    GET = "get"

    @classmethod
    def has_string(cls, string: str):
        return string in set(entry.value for entry in cls)


class Eval(object):
    def __init__(self, op: EvalOperations, evals: list, name=""):
        self.op = op
        self.evals = evals
        self.name = ""

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
                    return 0
            case EvalOperations.IF_ELSE:
                if self.evals[0].get_value(event, game):
                    return self.evals[1].get_value(event, game)
                else:
                    return self.evals[2].get_value(event, game)
            case EvalOperations.LOAD:
                if self.evals[0].get_value(event, game) == "game":
                    table = game.properties
                else:
                    table = event.properties
                variables = self.evals[1].get_value(event, game).split(".")
                for var in variables:
                    table = table[var]
                return table
            case EvalOperations.SET:
                if self.evals[0].get_value(event, game) == "game":
                    table = game.properties
                    game.setGameProperty(self.evals[1].get_value(event, game), self.evals[2].get_value(event, game))
                else:
                    table = event.properties
                    variables = self.evals[1].get_value(event, game).split(".")
                    for var in variables[:-1]:
                        if var in table and isinstance(table[var], dict):
                            table = table[var]
                        else:
                            table[var] = {}
                            table = table[var]
                    table[variables[-1]] = self.evals[2].get_value(event, game)
                return 1
            case EvalOperations.INCREMENT:
                return self.evals[0].get_value(event, game) + 1
            case EvalOperations.DECREMENT:
                return self.evals[0].get_value(event, game) - 1
            case EvalOperations.EQUALS:
                return self.evals[0].get_value(event, game) == self.evals[1].get_value(event, game)
            case EvalOperations.LESS_THAN:
                return self.evals[0].get_value(event, game) < self.evals[1].get_value(event, game)
            case EvalOperations.GREATER_THAN:
                return self.evals[0].get_value(event, game) > self.evals[1].get_value(event, game)
            case EvalOperations.AND:
                return self.evals[0].get_value(event, game) and self.evals[1].get_value(event, game)
            case EvalOperations.OR:
                return self.evals[0].get_value(event, game) or self.evals[1].get_value(event, game)
            case EvalOperations.RUN_ALL:
                return [eval.get_value(event, game) for eval in self.evals]
            case EvalOperations.APPEND:
                return self.evals[0].get_value(event, game) + [self.evals[1].get_value(event, game)]
            case EvalOperations.LENGTH:
                return len(self.evals[0].get_value(event, game))
            case EvalOperations.GET:
                return self.evals[0].get_value(event, game)[self.evals[1].get_value(event, game)]

    def __eq__(self, other):
        return self.op == other.op and len(self.evals) == len(other.evals) and all(
            eval.__eq__(other_eval) for eval, other_eval in zip(self.evals, other.evals))

    def __str__(self):
        return f"Eval({self.op.name}, {[eval.__str__() for eval in self.evals]})"

    def __repr__(self):
        return self.__str__()

    def serialize(self) -> Union[list, dict, object]:
        return [self.op.value] + [eval.serialize() for eval in self.evals]

    @classmethod
    def deserialize(cls, obj: Union[list, dict, object]):
        if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], str) and EvalOperations.has_string(obj[0]):
            return cls(EvalOperations(obj[0]), [cls.deserialize(eval) for eval in obj[1:]])
        else:
            return EvalLiteral(obj)

    def handle_event(self, event: MaoEvent, game: MaoGame):
        self.get_value(event, game)


class EvalLiteral(Eval):
    def __init__(self, value):
        self.value = value

    def get_value(self, event: MaoEvent, game: MaoGame):
        return self.value

    def serialize(self) -> Union[list, object]:
        return self.value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __str__(self):
        return f"Literal({self.value})"

    def __repr__(self):
        return self.__str__()
