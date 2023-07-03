from argparse import ArgumentParser

from mao_model.action import Action
from mao_model.action_types import ActionTypes
from mao_model.mao_event import MaoEvent
from mao_model.mao_game import MaoGame
from mao_model.rule import Rule

if __name__ == '__main__':
    parser = ArgumentParser(description="Running mao on the command line")
    parser.add_argument("--players", nargs="+", required=True, dest="players")
    parser.add_argument("--rules", nargs="*", dest="rules", default=[])
    args = parser.parse_args()
    rules = [
        Rule("dict",
             MaoEvent(type="player"),
             positive_action=Action(ActionTypes.SEND_CHAT,
                                    {"player": "{{event.player}}", "message": "I am a dict"})),
        Rule("start deck",
             MaoEvent(type="start"),
             positive_action=Action(ActionTypes.ADD_DECK,
                                    {"deck": "Deck"}))
    ]
    game = MaoGame({}, {}, args.rules + rules)
    for player in args.players:
        game.addPlayer(player)
    game.start_game()
    while not game.over:
        for event in game.dump_queue():
            game.handle_event(event)
        print("\n".join(game.chat))
        input("wait")
