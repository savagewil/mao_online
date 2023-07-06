import json
import re
from enum import Enum
from typing import Union

from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame
from mao_model.utils import table_lookup


class EvalOperations(Enum):
    ANY = "any"
    ALL = "all"
    NOT = "not"
    PLUS = "add"
    MINUS = "sub"
    DIVIDE = "div"
    MULTIPLY = "mult"
    MOD = "mod"
    IF = "if"
    IF_ELSE = "if_else"
    LOAD = "load"
    SET = "set"
    INCREMENT = "inc"
    DECREMENT = "dec"
    EQUALS = "equals"
    LESS_THAN = "greater_than"
    GREATER_THAN = "less_than"
    RUN_ALL = "run_all"
    APPEND = "append"
    LENGTH = "len"
    GET_LIST = "get_list"
    GET_DICT = "get_dict"
    MATCH = "match"
    FIND = "find"
    ADD_EVENT = "add_event"
    DRAW_CARDS = "draw_cards"
    DEAL_CARDS = "deal_cards"
    PLAY_CARD = "play_card"
    ADD_DECK = "add_deck"
    ADD_PLAYER = "add_player"
    SEND_CHAT = "send_chat"
    FORMAT = "format"

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
                    table = game.to_dict()
                else:
                    table = event.properties
                return table_lookup(table, self.evals[1].get_value(event, game))
            case EvalOperations.GET_DICT:
                table = self.evals[0].get_value(event, game)
                return table_lookup(table, self.evals[1].get_value(event, game))
            case EvalOperations.SET:
                if len(self.evals) == 2:
                    table_loc, lookup = self.evals[0].get_value(event, game).split(".", 1)
                    if table_loc == "game":
                        game.setGameProperty(lookup, self.evals[2].get_value(event, game))
                    else:
                        table = event.properties
                        variables = lookup.split(".")
                        for var in variables[:-1]:
                            if var in table and isinstance(table[var], dict):
                                table = table[var]
                            else:
                                table[var] = {}
                                table = table[var]
                        table[variables[-1]] = self.evals[2].get_value(event, game)
                else:
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
            case EvalOperations.ALL:
                return all(eval_.get_value(event, game) for eval_ in self.evals)
            case EvalOperations.ANY:
                return any(eval_.get_value(event, game) for eval_ in self.evals)
            case EvalOperations.RUN_ALL:
                return [eval.get_value(event, game) for eval in self.evals]
            case EvalOperations.APPEND:
                return self.evals[0].get_value(event, game) + [self.evals[1].get_value(event, game)]
            case EvalOperations.LENGTH:
                return len(self.evals[0].get_value(event, game))
            case EvalOperations.GET_LIST:
                return self.evals[0].get_value(event, game)[int(self.evals[1].get_value(event, game))]
            case EvalOperations.MATCH:
                return bool(
                    re.match(str(self.evals[0].get_value(event, game)), str(self.evals[1].get_value(event, game))))
            case EvalOperations.FIND:
                return re.findall(self.evals[0].get_value(event, game), self.evals[1].get_value(event, game))[0]
            case EvalOperations.ADD_EVENT:
                values = [eval.get_value(event, game) for eval in self.evals]
                return game.addEvent(**dict(zip(values[::2], values[1::2])))
            case EvalOperations.DRAW_CARDS:
                return game.drawCards(self.evals[0].get_value(event, game), self.evals[1].get_value(event, game),
                                      self.evals[2].get_value(event, game))
            case EvalOperations.DEAL_CARDS:
                return game.dealCards(self.evals[0].get_value(event, game), self.evals[1].get_value(event, game),
                                      self.evals[2].get_value(event, game))
            case EvalOperations.PLAY_CARD:
                return game.playCard(self.evals[0].get_value(event, game), self.evals[1].get_value(event, game),
                                     self.evals[2].get_value(event, game))
            case EvalOperations.ADD_DECK:
                if len(self.evals) == 3:
                    return game.addDeck(self.evals[0].get_value(event, game),
                                        bool(self.evals[1].get_value(event, game)),
                                        bool(self.evals[2].get_value(event, game)))
                elif len(self.evals) == 2:
                    return game.addDeck(self.evals[0].get_value(event, game),
                                        bool(self.evals[1].get_value(event, game)))
                else:
                    return game.addDeck(self.evals[0].get_value(event, game))
            case EvalOperations.ADD_PLAYER:
                return game.addPlayer(self.evals[0].get_value(event, game))
            case EvalOperations.SEND_CHAT:
                return game.sendChat(self.evals[0].get_value(event, game), self.evals[1].get_value(event, game))
            case EvalOperations.FORMAT:
                return self.evals[0].get_value(event, game) % tuple(
                    eval_.get_value(event, game) for eval_ in self.evals[1:])

    def __eq__(self, other):
        return self.op == other.op and len(self.evals) == len(other.evals) and all(
            eval.__eq__(other_eval) for eval, other_eval in zip(self.evals, other.evals))

    def __str__(self):
        return f"Eval({self.op.name}, {', '.join([eval.__str__() for eval in self.evals])})"

    def __repr__(self):
        return self.__str__()

    def serialize(self) -> Union[list, dict, object]:
        return [self.op.value] + [eval.serialize() for eval in self.evals]

    @classmethod
    def deserialize(cls, obj: Union[list, dict, object]):
        if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], str) and EvalOperations.has_string(obj[0]):
            if EvalOperations(obj[0]) == EvalOperations.SET and len(obj) == 3 and bool(
                    re.match("(game|event)\\..*", obj[1])):
                return cls(EvalOperations(obj[0]),
                           [cls.deserialize(eval) for eval in (obj[1].split(".", 1) + [obj[2]])])
            return cls(EvalOperations(obj[0]), [cls.deserialize(eval) for eval in obj[1:]])
        elif isinstance(obj, str) and re.match("(game|event)\\..*", obj):
            split_obj = obj.split(".", 1)
            return cls(EvalOperations.LOAD, [EvalLiteral(split_obj[0]), EvalLiteral(split_obj[1])])
        else:
            return EvalLiteral(obj)

    def handle_event(self, event: MaoEvent, game: MaoGame):
        self.get_value(event, game)

    def to_json(self):
        return json.dumps(self.serialize())

    @classmethod
    def from_json(self, json_str: str):
        return self.deserialize(json.loads(json_str))


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
