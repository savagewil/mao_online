from argparse import ArgumentParser

from mao_model.deck import Deck
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame
from mao_model.rule import Rule

if __name__ == '__main__':
    parser = ArgumentParser(description="Running mao on the command line")
    parser.add_argument("--players", nargs="+", required=True, dest="players")
    parser.add_argument("--rules", nargs="*", dest="rules")
    args = parser.parse_args()
    game = MaoGame({}, {}, args.rules + [Rule("test", MaoEvent(player=".*"))])
    for player in args.players:
        game.addPlayer(player)
    game.addDeck(deck_name="Deck", deck=Deck.get_shuffled_deck())
    game.start_game()
    while not game.over:
        for event in game.dump_queue():
            game.handle_event(event)
        print("\n".join(game.chat))
        input("wait")
