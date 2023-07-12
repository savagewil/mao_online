import json
import logging
from threading import Thread

import jsonpickle as jsonpickle
from flask import Flask, request

from mao_model.mao_game import MaoGame
from mao_ptui.__main__ import load_rules


def thread_function(game: MaoGame):
    logging.info("Event loop started")
    game.event_loop()
    logging.info("Event loop ended")


game = MaoGame({}, {}, load_rules(["/Users/wsavage/PycharmProjects/mao_online/rules/rules.json"]))
game.start_game()

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("Main    : before creating thread")

x = Thread(target=thread_function, args=(game,))
x.start()
# x.join()

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/game')
def get_game():
    # logging.info(f"Game:{game.to_dict()}")
    return jsonpickle.dumps(game.to_dict())


@app.route('/add_player', methods=['PUT'])
def add_player():
    name = json.loads(request.data)["player_name"]
    logging.info(f"Add player:{name}")
    game.addPlayer(name)
    return {"result": True}


@app.route('/send_chat', methods=['PUT'])
def send_chat():
    name = json.loads(request.data)["player_name"]
    message = json.loads(request.data)["message"]
    logging.info(f"Sending chat for {name}:{message}")
    game.sendChat(name, message)
    return {"result": True}
