from argparse import ArgumentParser

import requests
from inputimeout import inputimeout, TimeoutOccurred

from mao_model.mao_game import MaoGame
from mao_ptui.rendering_utils import render_hand, render_deck

ADD_PLAYER = "http://%s/add_player"
parser = ArgumentParser(description="Running mao client on the command line")
parser.add_argument("--player-name", required=True, dest="player_name")
parser.add_argument("--server", dest="server", default="127.0.0.1:5000")
parser.add_argument("--verbose", dest="verbose", action="store_true")


def send_add_player(server, player_name):
    requests.put('http://%s/add_player' % server, json={'player_name': player_name})


def send_chat(server, player_name, message):
    requests.put('http://%s/send_chat' % server, json={'player_name': player_name, "message": message})


def get_game(server):
    response = requests.get('http://%s/game' % server)
    # print(response.json())
    return MaoGame.from_dict(response.json())


if __name__ == '__main__':
    args = parser.parse_args()
    send_add_player(args.server, args.player_name)
    game = get_game(args.server)
    while not game.over:
        game = get_game(args.server)
        print("\n" * 20)
        print("\t" + "\n\t".join(game.chat))

        if len(game.decks['play'].cards):
            print(f"Top card {render_deck(game.decks['play'])}")
        else:
            print(f"Top card {render_deck(game.decks['play'])}")
        print(render_hand(game.players[args.player_name].hand))
        try:
            text = inputimeout(f"{args.player_name} send chat:", 10)
            send_chat(args.server, args.player_name, text)
        except TimeoutOccurred as e:
            print(e)
            pass
