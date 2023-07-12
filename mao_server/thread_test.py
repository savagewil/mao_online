import logging
from threading import Thread

from mao_model.mao_game import MaoGame


def thread_function(game: MaoGame):
    game.event_loop()
    logging.info("Game finished")


game = MaoGame({}, {}, {})
format = "%(asctime)s: %(message)s"

logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("Main    : before creating thread")

x = Thread(target=thread_function, args=(game,))
logging.info("Main    : before running thread")
x.start()
logging.info("Main    : wait for the thread to finish")
game.addPlayer("Bob Ross")
game.end_game()
# x.join()
logging.info(f"Game:{game.to_dict()}")
logging.info("Main    : all done")
