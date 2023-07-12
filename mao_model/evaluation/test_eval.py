import json
from unittest import TestCase

from mao_model.card import Card
from mao_model.deck import Deck
from mao_model.evaluation.eval import Eval, EvalOperations, EvalLiteral
from mao_model.hand import Hand
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame
from mao_model.player import Player
from mao_model.ranks import Ranks
from mao_model.suits import Suits


class TestEval(TestCase):
    def setUp(self):
        self.eval_ = Eval(EvalOperations.PLUS, [EvalLiteral(2), EvalLiteral(2)])
        self.event = MaoEvent(player="Bob", nest={"other": 5})
        self.game = MaoGame({}, {}, [], {"turn": 5})
        self.serialized = ['add', 2, 2]

    def test_get_value(self):
        self.assertEqual(4, self.eval_.get_value(self.event, self.game), "Eval should run")

    def test_serialize(self):
        self.assertEqual(self.serialized, self.eval_.serialize(), "Eval should serialize")

    def test_deserialize(self):
        eval_ = Eval.deserialize(self.serialized)
        self.assertEqual(eval_, self.eval_, "Eval should deserialize")
        self.assertEqual(eval_.get_value(self.event, self.game), self.eval_.get_value(self.event, self.game),
                         "Deserialized eval should produce the same result")

    def test_large_eval(self):
        eval_ = ["if", ["add", 2, 2], "4 is more than 0"]
        eval_ = Eval.deserialize(eval_)
        self.assertEqual("4 is more than 0", eval_.get_value(self.event, self.game),
                         "Deserialized eval should produce the same result")

    def test_if_and_ifelse(self):
        event = MaoEvent()
        eval_ = ["if_else", 1, ["set", "event", "true", 1], ["set", "event", "false", 0]]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(event, self.game)
        self.assertEqual(1, event.properties["true"],
                         "If_else true should eval if condition is true ")
        self.assertFalse("false" in self.game.properties,
                         "If_else false should not eval if condition is true")

        event = MaoEvent()
        eval_ = ["if", 1, ["set", "event", "true", 1]]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(event, self.game)
        self.assertEqual(1, event.properties["true"],
                         "If true should eval if condition is true ")

        event = MaoEvent()
        eval_ = ["if_else", 0, ["set", "event", "true", 1], ["set", "event", "false", 0]]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(event, self.game)
        self.assertFalse("true" in self.game.properties,
                         "If-else false should not eval if condition is true")
        self.assertEqual(0, event.properties["false"],
                         "If-else false should eval if condition is false")

        event = MaoEvent()
        eval_ = ["if", 0, ["set", "event", "true", 1]]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(event, self.game)
        self.assertFalse("true" in event.properties,
                         "If true should not eval if condition is false ")

    def test_any(self):
        eval_one_true = Eval.deserialize(["any", True, False, False])
        self.assertTrue(eval_one_true.get_value(self.event, self.game),
                        "Any should be true is any value is true")

        eval_all_true = Eval.deserialize(["any", True, True, True])
        self.assertTrue(eval_all_true.get_value(self.event, self.game),
                        "Any should be true is all are true")

        eval_all_false = Eval.deserialize(["any", False, False, False])
        self.assertFalse(eval_all_false.get_value(self.event, self.game),
                         "Any should be false is all values are false")

    def test_all(self):
        eval_one_true = Eval.deserialize(["all", True, False, False])
        self.assertFalse(eval_one_true.get_value(self.event, self.game),
                         "All should be false is any value is false")

        eval_all_true = Eval.deserialize(["all", True, True, True])
        self.assertTrue(eval_all_true.get_value(self.event, self.game),
                        "All should be true is all are true")

        eval_all_false = Eval.deserialize(["all", False, False, False])
        self.assertFalse(eval_all_false.get_value(self.event, self.game),
                         "All should be false is all values are false")

    def test_not(self):
        eval_false = Eval.deserialize(["not", False])
        self.assertTrue(eval_false.get_value(self.event, self.game),
                        "False should be true")

        eval_true = Eval.deserialize(["not", True])
        self.assertFalse(eval_true.get_value(self.event, self.game),
                         "True should be false")

    def test_add(self):
        eval_two_plus_two = Eval.deserialize(["add", 2, 2])
        self.assertEqual(4, eval_two_plus_two.get_value(self.event, self.game),
                         "Two sub two equals 0")

    def test_sub(self):
        eval_two_sub_two = Eval.deserialize(["sub", 2, 2])
        self.assertEqual(0, eval_two_sub_two.get_value(self.event, self.game),
                         "Two sub two equals 0")

    def test_div(self):
        eval_two_div_two = Eval.deserialize(["div", 2, 2])
        self.assertEqual(1, eval_two_div_two.get_value(self.event, self.game),
                         "Two div two equals 1")

    def test_mult(self):
        eval_two_div_two = Eval.deserialize(["mult", 2, 2])
        self.assertEqual(4, eval_two_div_two.get_value(self.event, self.game),
                         "Two times two equals 4")

    def test_mod(self):
        eval_two_mod_two = Eval.deserialize(["mod", 2, 2])
        self.assertEqual(0, eval_two_mod_two.get_value(self.event, self.game),
                         "Two mod two equals zero")

        eval_zero_mod_two = Eval.deserialize(["mod", 0, 2])
        self.assertEqual(0, eval_zero_mod_two.get_value(self.event, self.game),
                         "Two mod two equals zero")

        eval_one_mod_two = Eval.deserialize(["mod", 1, 2])
        self.assertEqual(1, eval_one_mod_two.get_value(self.event, self.game),
                         "One mod two equals one")

        eval_three_mod_two = Eval.deserialize(["mod", 3, 2])
        self.assertEqual(1, eval_three_mod_two.get_value(self.event, self.game),
                         "Three mod two equals one")

    def test_load(self):
        eval_ = ["load", "game", "turn"]
        eval_ = Eval.deserialize(eval_)
        self.assertEqual(5, eval_.get_value(self.event, self.game),
                         "Load should get values from game")
        eval_ = ["load", "event", "player"]
        eval_ = Eval.deserialize(eval_)
        self.assertEqual("Bob", eval_.get_value(self.event, self.game),
                         "Load should get values from event")
        eval_ = ["load", "event", "nest.other"]
        eval_ = Eval.deserialize(eval_)
        self.assertEqual(5, eval_.get_value(self.event, self.game),
                         "Load should get nested values")

    def test_set(self):
        eval_ = ["set", "game", "turn2", 5]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(self.event, self.game)
        self.assertEqual(5, self.game.properties["turn2"],
                         "Set should set values in game")

        eval_ = ["set", "event", "player2", "Bob"]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(self.event, self.game)
        self.assertEqual("Bob", self.event.properties["player2"],
                         "Set should set values in event")

        eval_ = ["set", "event", "nest.other2", 5]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(self.event, self.game)
        self.assertEqual(5, self.event.properties["nest"]["other2"],
                         "Set should set values in a nested dict")

        eval_ = ["set", "event", "nest2.other2", 5]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(self.event, self.game)
        self.assertEqual(5, self.event.properties["nest2"]["other2"],
                         "Set should create a nested dict if one is needed")

    def test_set_event(self):
        eval_ = ["set", "game", "turn2", 5]
        eval_ = Eval.deserialize(eval_)
        eval_.get_value(self.event, self.game)
        self.assertTrue(len(self.game.eventQueue) > 0,
                        "Set game should trigger and event")

    def test_inc(self):
        eval_inc_two = Eval.deserialize(["inc", 2])
        self.assertEqual(3, eval_inc_two.get_value(self.event, self.game),
                         "Two incremented equals three")

    def test_dec(self):
        eval_dec_two = Eval.deserialize(["dec", 2])
        self.assertEqual(1, eval_dec_two.get_value(self.event, self.game),
                         "Two decremented equals one")

    def test_equals(self):
        eval_two_equals_two = Eval.deserialize(["equals", 2, 2])
        self.assertEqual(1, eval_two_equals_two.get_value(self.event, self.game),
                         "Two equals two")

        eval_two_equals_three = Eval.deserialize(["equals", 2, 3])
        self.assertFalse(eval_two_equals_three.get_value(self.event, self.game),
                         "Two does not equal three")

    def test_less_than(self):
        eval_two_less_than_two = Eval.deserialize(["less_than", 2, 2])
        self.assertFalse(eval_two_less_than_two.get_value(self.event, self.game),
                         "Two is not less than two")

        eval_two_less_than_one = Eval.deserialize(["less_than", 2, 1])
        self.assertFalse(eval_two_less_than_one.get_value(self.event, self.game),
                         "Two is not less than one")

        eval_two_less_than_three = Eval.deserialize(["less_than", 2, 3])
        self.assertTrue(eval_two_less_than_three.get_value(self.event, self.game),
                        "Two is less than three")

    def test_greate_than(self):
        eval_two_greater_than_two = Eval.deserialize(["greater_than", 2, 2])
        self.assertFalse(eval_two_greater_than_two.get_value(self.event, self.game),
                         "Two is not greater than two")

        eval_two_greater_than_one = Eval.deserialize(["greater_than", 2, 1])
        self.assertTrue(eval_two_greater_than_one.get_value(self.event, self.game),
                        "Two is greater than one")

        eval_two_greater_than_three = Eval.deserialize(["greater_than", 2, 3])
        self.assertFalse(eval_two_greater_than_three.get_value(self.event, self.game),
                         "Two is not greater than three")

    def test_run_all(self):
        eval_run = Eval.deserialize(["run_all", 2, 2, 2, 2])
        self.assertEqual([2, 2, 2, 2], eval_run.get_value(self.event, self.game),
                         "run all runs all children")

    def test_append(self):
        eval_append = Eval.deserialize(["append", [], 2])
        self.assertEqual([2], eval_append.get_value(self.event, self.game),
                         "Append adds value to list")

    def test_length(self):
        eval_len_0 = Eval.deserialize(["len", []])
        self.assertEqual(0, eval_len_0.get_value(self.event, self.game),
                         "Gets length of empty list")

        eval_len_2 = Eval.deserialize(["len", [1, 1]])
        self.assertEqual(2, eval_len_2.get_value(self.event, self.game),
                         "gets length of non empty list")

    def test_get(self):
        eval_get_list = Eval.deserialize(["get_list", [1, 2, 3], 1])
        self.assertEqual(2, eval_get_list.get_value(self.event, self.game),
                         "Gets entries in list")

        eval_get_dict = Eval.deserialize(["get_dict", {"test": 2}, "test"])
        self.assertEqual(2, eval_get_dict.get_value(self.event, self.game),
                         "Gets entries in dictionary")

    def test_match(self):
        eval_match = Eval.deserialize(["match", ".*", "test"])
        self.assertTrue(eval_match.get_value(self.event, self.game),
                        "Matches on regex match")

        eval_not_match = Eval.deserialize(["match", "Hello", "test"])
        self.assertFalse(eval_not_match.get_value(self.event, self.game),
                         "Does not match")

    def test_find(self):
        eval_find = Eval.deserialize(["find", "\\d+", "40"])
        self.assertEqual("40", eval_find.get_value(self.event, self.game),
                         "Finds regex match")

    def test_add_event(self):
        game = MaoGame({}, {}, {})
        eval_find = Eval.deserialize(["add_event", "type", "test"])
        eval_find.get_value(self.event, game)
        self.assertEqual(1, len(game.eventQueue),
                         "Adds events to game")

    def test_draw_cards(self):
        deck = Deck.get_shuffled_deck()
        hand = Hand([])
        player = Player("bob", hand=hand)
        game = MaoGame({"bob": player}, {"Deck": deck}, {})

        self.assertEqual(0, len(hand.cards),
                         "Hand should start empty")

        eval_draw = Eval.deserialize(["draw_cards", "bob", "Deck", 2])
        eval_draw.get_value(self.event, game)
        self.assertEqual(2, len(hand.cards),
                         "Hand drew two cards")

    def test_deal_cards(self):
        deck1 = Deck.get_shuffled_deck()
        deck2 = Deck([])
        game = MaoGame({}, {"Deck1": deck1, "Deck2": deck2}, {})

        self.assertEqual(0, len(deck2.cards),
                         "Deck should start empty")

        eval_deal = Eval.deserialize(["deal_cards", "Deck1", "Deck2", 2])
        eval_deal.get_value(self.event, game)
        self.assertEqual(2, len(deck2.cards),
                         "Deck was dealt two cards")

    def test_play_cards(self):
        deck2 = Deck([])
        hand = Hand([Card(Suits.SPADES, Ranks.ACE)])
        player = Player("bob", hand=hand)
        game = MaoGame({"bob": player}, {"Deck2": deck2}, {})

        self.assertEqual(0, len(deck2.cards),
                         "Deck2 should start empty")

        eval_play = Eval.deserialize(["play_card", "bob", "Deck2", 0])
        eval_play.get_value(self.event, game)

        self.assertEqual(1, len(deck2.cards),
                         "One Card was played on deck2")
        self.assertEqual(0, len(player.hand.cards),
                         "One Card was removed from bob")

    def test_add_deck(self):
        deck2 = Deck([])
        game = MaoGame({}, {}, {})

        self.assertEqual(0, len(game.decks.items()),
                         "Game should have no decks")

        eval_add_deck = Eval.deserialize(["add_deck", "Deck", deck2])
        eval_add_deck.get_value(self.event, game)

        self.assertEqual(1, len(game.decks.items()),
                         "One deck was added to the game")
        self.assertIn("Deck", game.decks,
                      "Deck was added")

    def test_add_player(self):
        player = Player("bob", Hand([]))
        game = MaoGame({}, {}, {})

        self.assertEqual(0, len(game.players.items()),
                         "Game should have no players")

        eval_add_deck = Eval.deserialize(["add_player", "Bob", player])
        eval_add_deck.get_value(self.event, game)

        self.assertEqual(1, len(game.players.items()),
                         "One player was added to the game")
        self.assertIn("Bob", game.players,
                      "Bob was added")

    def test_add_rule(self):
        game = MaoGame({}, {}, {})

        self.assertEqual(0, len(game.rules.items()),
                         "Game should have no rules")

        eval_add_deck = Eval.deserialize(["add_rule", "test_rule", ["function", "boop"]])
        eval_add_deck.get_value(self.event, game)

        self.assertEqual(1, len(game.rules.items()),
                         "One player was added to the game")
        self.assertIn("test_rule", game.rules,
                      "test_rule was added")
        self.assertEqual(EvalLiteral("boop"), game.rules["test_rule"],
                         "test_rule is correct")

    def test_send_chat(self):
        game = MaoGame({}, {}, {})

        self.assertEqual(0, len(game.chat),
                         "Game should have no chats")

        eval_add_deck = Eval.deserialize(["send_chat", "computer", "message_text"])
        eval_add_deck.get_value(self.event, game)

        self.assertEqual(1, len(game.chat),
                         "Chat was sent")
        self.assertIn("computer", game.chat[0],
                      "Player name was included in chat")
        self.assertIn("message_text", game.chat[0],
                      "message_text was included in chat")

    def test_format(self):
        eval_format = Eval.deserialize(["format", "test %d", 2])
        self.assertEqual("test 2", eval_format.get_value(self.event, self.game),
                         "String format added worked with one int")

        eval_format = Eval.deserialize(["format", "test %s %s", "5", "6"])
        self.assertEqual("test 5 6", eval_format.get_value(self.event, self.game),
                         "String format added worked with one int")

    def test_move_and_shuffle(self):
        deck1 = Deck.get_shuffled_deck()
        deck1_top = deck1.peek()
        deck2 = Deck([])
        game = MaoGame({}, {"Deck1": deck1, "Deck2": deck2}, {})

        self.assertEqual(0, len(deck2.cards),
                         "Deck should start empty")

        eval_deal = Eval.deserialize(["move_and_shuffle", "Deck1", "Deck2", 2])
        eval_deal.get_value(self.event, game)

        self.assertEqual(2, len(deck2.cards),
                         "Deck was dealt two cards")
        self.assertEqual(deck1_top, deck1.peek(),
                         "Deck top should stay the same")

    def test_end_game(self):
        game = MaoGame({}, {}, {})

        self.assertFalse(game.over,
                         "Game should start no over")

        eval_deal = Eval.deserialize(["end_game"])
        eval_deal.get_value(self.event, game)

        self.assertTrue(game.over,
                        "Game end should set over to true")

    def test_function_and_eval(self):
        eval_deal = Eval.deserialize(["function", ["add", 2, 2]])
        self.assertEqual(Eval.deserialize(["add", 2, 2]), eval_deal.get_value(self.event, self.game),
                         "function should return an eval")

        eval_deal = Eval.deserialize(['eval', ["function", ["add", 2, 2]]])
        self.assertEqual(4, eval_deal.get_value(self.event, self.game),
                         "eval should run function")

        eval_deal = Eval.deserialize(['eval', ["function", ["add", "event.arg_1", "event.arg_1"]], 2, 2])
        self.assertEqual(4, eval_deal.get_value(self.event, self.game),
                         "eval should take arguments")

    def test_serialize_and_deserialize_eval(self):
        eval_ = Eval.deserialize(["deserialize", json.dumps(['add', 2, 2])])
        self.assertEqual(self.eval_, eval_.get_value(self.event, self.game), "Eval should deserialize")

        eval_ = Eval.deserialize(["serialize", ['function', ['add', 2, 2]]])
        self.assertEqual(json.dumps(['add', 2, 2]), eval_.get_value(self.event, self.game), "Eval should deserialize")

    def test_eval_json(self):
        eval_ = Eval.deserialize(['add', 2, 2])
        print(eval_)
        print(json.dumps(eval_))
