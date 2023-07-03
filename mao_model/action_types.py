from enum import Enum


class ActionTypes(Enum):
    NONE = 0
    ADD_EVENT = 1
    DRAW_CARDS = 2
    PLAY_CARD = 3
    ADD_DECK = 4
    ADD_PLAYER = 5
    SEND_CHAT = 6
    SET_PROPERTY = 7
