from argparse import ArgumentParser

from mao_model.action import Action
from mao_model.action_types import ActionTypes
from mao_model.evaluation.eval import Eval
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame
from mao_model.rule import Rule
from mao_ptui.rendering_utils import render_hand, render_deck

if __name__ == '__main__':
    parser = ArgumentParser(description="Running mao on the command line")
    parser.add_argument("--players", nargs="+", required=True, dest="players")
    parser.add_argument("--rules", nargs="*", dest="rules", default=[])
    parser.add_argument("--verbose", dest="verbose", action="store_true")
    args = parser.parse_args()
    rules = [
        Eval.deserialize(["if", ["equals", "start", ["load", "event", "type"]],
                          ["run all",
                           ["set", "game", "turn", 0],
                           ["set", "game", "players", []],
                           ["add_deck", "Deck"],
                           ["add_deck", "play", "False", "True"],
                           ["deal_cards", "Deck", "play", 1]
                           ]]),
        Rule("draw first hand",
             MaoEvent(type="player"),
             positive_action=Action(ActionTypes.DRAW_CARDS,
                                    {"player": "{{event.player}}", "deck": "Deck", "count": "7"})),

        Eval.deserialize(["if", ["equals", "player", ["load", "event", "type"]],
                          ["run all", ["set", "game", "players",
                                       ["append", ["load", "game", "players"], ["load", "event", "player"]]]]]),
        Eval.deserialize(
            ["if",
             ["and", ["and",
                      ["equals",
                       "chat",
                       ["load", "event", "type"]],
                      [["equals",
                        ["load", "event", "player"],
                        ["get", ["load", "game", "players"], ["load", "game", "turn"]]]]],
              ["match", "play \d+", ["load", "event", "message"]]],
             ["if_else",
              ["load", "event", "player_dict."],
              ["run all",
               ["play_card", ["load", "event", "player"], "play",
                ["find", "\d+", ["load", "event", "message"]]]],
              ["send_chat", "computer", "bonk"]]]),
        Eval.deserialize(
            ["if",
             ["and",
              ["equals",
               "chat",
               ["load", "event", "type"]],
              [["equals",
                ["load", "event", "player"],
                ["get", ["load", "game", "players"], ["load", "game", "turn"]]]]],
             ["run all",
              ["set", "game", "turn",
               ["mod", ["inc", ["load", "game", "turn"]], ["len", ["load", "game", "players"]]]]]])
    ]
    game = MaoGame({}, {}, args.rules + rules, verbose=args.verbose)
    game.start_game()
    for player in args.players:
        game.addPlayer(player)
    while not game.over:
        game.handle_events()
        print("\n".join(game.chat))
        if len(game.decks['play'].cards):
            print(f"Top card {render_deck(game.decks['play'])}")
        else:
            print(f"Top card {render_deck(game.decks['play'])}")
        print(render_hand(game.players[game.properties['players'][game.properties['turn']]].hand))
        text = input(f"{game.properties['players'][game.properties['turn']]} send chat:")
        game.sendChat(game.properties['players'][game.properties['turn']], text)
