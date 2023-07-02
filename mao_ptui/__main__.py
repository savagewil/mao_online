from argparse import ArgumentParser

from mao_model.deck import Deck
from mao_model.mao_game import MaoGame

if __name__ == '__main__':
    parser = ArgumentParser(description="Running mao on the command line")
    parser.add_argument("--players", nargs="+", required=True, dest="players")
    args = parser.parse_args()
    game = MaoGame({}, {}, [])
    for player in args.players:
        game.addPlayer(player)
    game.addDeck(deck_name="Deck", deck=Deck.get_shuffled_deck())
    game.start_game()
    while not game.over:
        for event in game.dump_queue():
            game.handle_event(event)
        print("\n".join(game.chat))
        input("wait")
