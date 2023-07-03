from abc import ABC

from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class Eval(ABC):
    def get_value(self, event: MaoEvent, game: MaoGame) -> object:
        pass
