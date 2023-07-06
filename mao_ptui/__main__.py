import json
from argparse import ArgumentParser
from typing import List

from mao_model.evaluation.eval import Eval
from mao_model.mao_game import MaoGame
from mao_ptui.rendering_utils import render_hand, render_deck


def load_rules(rule_files: List[str]):
    rules = {}
    for rule_file_path in rule_files:
        rules = dict(**rules, **json.load(open(rule_file_path, 'r')))
    return {rule_name: Eval.deserialize(rule) for rule_name, rule in rules.items()}


if __name__ == '__main__':
    parser = ArgumentParser(description="Running mao on the command line")
    parser.add_argument("--players", nargs="+", required=True, dest="players")
    parser.add_argument("--rules", nargs="*", dest="rules", default=[])
    parser.add_argument("--verbose", dest="verbose", action="store_true")
    args = parser.parse_args()

    game = MaoGame({}, {}, load_rules(args.rules), verbose=args.verbose)
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
