from argparse import ArgumentParser

from mao_model.evaluation.eval import Eval
from mao_model.mao_game import MaoGame
from mao_ptui.rendering_utils import render_hand, render_deck

if __name__ == '__main__':
    parser = ArgumentParser(description="Running mao on the command line")
    parser.add_argument("--players", nargs="+", required=True, dest="players")
    parser.add_argument("--rules", nargs="*", dest="rules", default=[])
    parser.add_argument("--verbose", dest="verbose", action="store_true")
    args = parser.parse_args()
    rules = [
        Eval.deserialize(["if", ["equals", "start", "event.type"],
                          ["run_all",
                           ["set", "game.turn", 0],
                           ["set", "game.player_order", []],
                           ["add_deck", "Deck"],
                           ["add_deck", "play", "False", "True"],
                           ["deal_cards", "Deck", "play", 49],
                           ["set", "game.drew", False]
                           ]]),

        Eval.deserialize(["if", ["equals", "player", "event.type"],
                          ["run_all",
                           ["set", "game.player_order",
                            ["append", "game.player_order", "event.player"]],
                           ["draw_cards", "event.player", "Deck", 1]]]),
        Eval.deserialize(
            ["if",
             ["all",
              ["equals",
               "chat", "event.type"],
              [["equals", "event.player",
                ["get_list", "game.player_order", "game.turn"]]],
              ["match", "play \d+", "event.message"]],
             ["if_else", ["any",
                          ["equals",
                           ["get_dict", ["get_list", "event.player_dict.hand", ["find", "\d+", "event.message"]],
                            "suit"], "game.decks.play.top_card.suit"],
                          ["equals",
                           ["get_dict", ["get_list", "event.player_dict.hand", ["find", "\d+", "event.message"]],
                            "rank"], "game.decks.play.top_card.rank"]],
              ["run_all",
               ["play_card", "event.player", "play",
                ["find", "\d+", "event.message"]],
               ["set", "game.turn",
                ["mod", ["inc", "game.turn"], ["len", "game.player_order"]]]],
              ["run_all",
               ["send_chat", "computer", "That card is not legal"]]]]),
        Eval.deserialize(
            ["if",
             ["all",
              ["equals",
               "chat", "event.type"],
              [["equals", "event.player",
                ["get_list", "game.player_order", "game.turn"]]],
              ["match", "draw", "event.message"]],
             ["run_all",
              ["draw_cards", "event.player", "Deck", 1],
              ["set", "game.drew", True]]]),
        Eval.deserialize(
            ["if",
             ["all",
              ["equals",
               "chat", "event.type"],
              [["equals", "event.player",
                ["get_list", "game.player_order", "game.turn"]]],
              ["equals", "pass", "event.message"]],
             ["if_else",
              "game.drew",
              ["run_all",
               ["set", "game.turn",
                ["mod", ["inc", "game.turn"], ["len", "game.player_order"]]]],
              ["send_chat", "computer", "You must draw before passing"]]]),
        Eval.deserialize(
            ["if",
             ["all",
              ["equals",
               "property_update", "event.type"],
              ["equals", "turn", "event.property"]],
             ["run_all",
              ["set", "game.drew", False]
              ]]),
        Eval.deserialize(
            ["if",
             ["all",
              ["equals",
               "play", "event.type"],
              ["not", "event.player_dict.hand"]],
             ["run_all",
              ["send_chat", "computer", ["format", "%s has won the game", "event.player"]],
              ["draw_cards", "event.player", "Deck", 7]]]),
        Eval.deserialize(
            ["if",
             ["all",
              ["equals",
               "draw", "event.type"],
              ["equals", "Deck", "event.deck"],
              ["equals", 0, "event.deck_dict.card_count"]],
             ["run_all",
              ["send_chat", "computer", "Deck Empty"],
              ["move_and_shuffle", "play", "Deck", ["sub", "game.decks.play.card_count", 1]]]]),

    ]
    game = MaoGame({}, {}, args.rules + rules, verbose=args.verbose)
    game.start_game()
    for player in args.players:
        game.addPlayer(player)
    while not game.over:
        game.handle_events()
        print("\n" * 20)
        print("\t" + "\n\t".join(game.chat))

        if len(game.decks['play'].cards):
            print(f"Top card {render_deck(game.decks['play'])}")
        else:
            print(f"Top card {render_deck(game.decks['play'])}")
        print(render_hand(game.players[game.properties['player_order'][game.properties['turn']]].hand))
        text = input(f"{game.properties['player_order'][game.properties['turn']]} send chat:")
        game.sendChat(game.properties['player_order'][game.properties['turn']], text)
