from re import match


class MaoEvent:
    def __init__(self, **properties):
        self.properties = properties

    def match(self, event) -> bool:
        return MaoEvent.match_dict(self.properties, event.properties)

    @staticmethod
    def match_dict(dict_1: dict, dict_2: dict) -> bool:
        for key, value in dict_1.items():
            if key not in dict_2:
                return False
            else:
                if isinstance(value, dict) and isinstance(dict_2[key], dict):
                    return MaoEvent.match_dict(value, dict_2[key])
                elif isinstance(value, str) and isinstance(dict_2[key], str):
                    return bool(match(value, dict_2[key]))
                else:
                    return False

    def to_dict(self) -> dict:
        return self.properties

    @classmethod
    def from_dict(cls, json_dict: dict):
        return cls(**json_dict)
