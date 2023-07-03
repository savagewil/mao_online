from unittest import TestCase

from mao_model.evaluation.eval import Eval, EvalOperations, EvalLiteral
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame


class TestEval(TestCase):
    def setUp(self):
        self.eval = Eval(EvalOperations.PLUS, [EvalLiteral(2), EvalLiteral(2)])
        self.event = MaoEvent(player="Bob", nest={"other": 5})
        self.game = MaoGame({}, {}, [], {"turn": 5})
        self.serialized = ['+', 2, 2]

    def test_get_value(self):
        self.assertEqual(4, self.eval.get_value(self.event, self.game), "Eval should run")

    def test_serialize(self):
        self.assertEqual(self.serialized, self.eval.serialize(), "Eval should serialize")

    def test_deserialize(self):
        eval = Eval.deserialize(self.serialized)
        # print(eval)
        self.assertEqual(eval, self.eval, "Eval should deserialize")
        self.assertEqual(eval.get_value(self.event, self.game), self.eval.get_value(self.event, self.game),
                         "Deserialized eval should produce the same result")

    def test_large_eval(self):
        eval = ["if", ["+", 2, 2], "4 is more than 0"]
        eval = Eval.deserialize(eval)
        self.assertEqual("4 is more than 0", eval.get_value(self.event, self.game),
                         "Deserialized eval should produce the same result")

    def test_load(self):
        eval = ["load", "game", "turn"]
        eval = Eval.deserialize(eval)
        self.assertEqual(5, eval.get_value(self.event, self.game),
                         "Load should get values from game")
        eval = ["load", "event", "player"]
        eval = Eval.deserialize(eval)
        self.assertEqual("Bob", eval.get_value(self.event, self.game),
                         "Load should get values from event")
        eval = ["load", "event", "nest.other"]
        eval = Eval.deserialize(eval)
        self.assertEqual(5, eval.get_value(self.event, self.game),
                         "Load should get nested values")

    def test_set(self):
        eval = ["set", "game", "turn2", 5]
        eval = Eval.deserialize(eval)
        eval.get_value(self.event, self.game)
        self.assertEqual(5, self.game.properties["turn2"],
                         "Set should set values in game")

        eval = ["set", "event", "player2", "Bob"]
        eval = Eval.deserialize(eval)
        eval.get_value(self.event, self.game)
        self.assertEqual("Bob", self.event.properties["player2"],
                         "Set should set values in event")

        eval = ["set", "event", "nest.other2", 5]
        eval = Eval.deserialize(eval)
        eval.get_value(self.event, self.game)
        self.assertEqual(5, self.event.properties["nest"]["other2"],
                         "Set should set values in a nested dict")

        eval = ["set", "event", "nest2.other2", 5]
        eval = Eval.deserialize(eval)
        eval.get_value(self.event, self.game)
        self.assertEqual(5, self.event.properties["nest2"]["other2"],
                         "Set should create a nested dict if one is needed")

    def test_set_event(self):
        eval = ["set", "game", "turn2", 5]
        eval = Eval.deserialize(eval)
        eval.get_value(self.event, self.game)
        self.assertTrue(len(self.game.eventQueue) > 0,
                        "Set game should trigger and event")

    def test_if_and_ifelse(self):
        event = MaoEvent()
        eval = ["if-else", 1, ["set", "event", "true", 1], ["set", "event", "false", 0]]
        eval = Eval.deserialize(eval)
        eval.get_value(event, self.game)
        self.assertEqual(1, event.properties["true"],
                         "If-else true should eval if condition is true ")
        self.assertFalse("false" in self.game.properties,
                         "If-else false should not eval if condition is true")

        event = MaoEvent()
        eval = ["if", 1, ["set", "event", "true", 1]]
        eval = Eval.deserialize(eval)
        eval.get_value(event, self.game)
        self.assertEqual(1, event.properties["true"],
                         "If true should eval if condition is true ")

        event = MaoEvent()
        eval = ["if-else", 0, ["set", "event", "true", 1], ["set", "event", "false", 0]]
        eval = Eval.deserialize(eval)
        eval.get_value(event, self.game)
        self.assertFalse("true" in self.game.properties,
                         "If-else false should not eval if condition is true")
        self.assertEqual(0, event.properties["false"],
                         "If-else false should eval if condition is false")

        event = MaoEvent()
        eval = ["if", 0, ["set", "event", "true", 1]]
        eval = Eval.deserialize(eval)
        eval.get_value(event, self.game)
        self.assertFalse("true" in event.properties,
                         "If true should not eval if condition is false ")
