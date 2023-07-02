from mao_model.action import Action
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class Rule:
    def __init__(self, eventSchema: MaoEvent, postive_action: Action, negative_action: Action):
        self.eventSchema: MaoEvent = eventSchema
        self.postive_action: Action = postive_action
        self.negative_action: Action = negative_action

    def handle_event(self, event: MaoEvent, game: MaoGame):
        if self.eventSchema.match(event):
            self.postive_action.run(event, game)
        else:
            self.negative_action.run(event, game)