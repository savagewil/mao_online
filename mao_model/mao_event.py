from re import match
from typing import Self


class MaoEvent:
    def __init__(self, **properties):
        self.properties = properties

    def match(self, event: Self) -> bool:
        pass

    @staticmethod
    def match_dict(dict_1: dict, dict_2: dict) -> bool:
        for key, value in dict_1:
            if key not in dict_2:
                return False
            else:
                if isinstance(value, dict) and isinstance(dict_2[key], dict):
                    MaoEvent.match_dict(value, dict_2[key])
                elif isinstance(value, str) and isinstance(dict_2[key], str):
                    return bool(match(value, dict_2[key]))
                else:
                    return False
