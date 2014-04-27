import random
import unittest

from game import Game
from helper import Helper
from modules.preprocess import Preprocess

class TestPreprocess(unittest.TestCase):

    def setUp(self):
        self.config = Helper.get_config()
        self.preprocess = Preprocess(self.config)
        self.game = Game(self.config, self.preprocess)

    def test_get_state(self):
        # Enlarge prey's perception to have chances of
        # seeing traps/attackers in test.
        x = self.config.getint('game', 'x')
        self.config.set('game', 'pray_perception', x / 3)

        pred_nr = 5
        self.config.set('game', 'pred_nr', pred_nr)
        trap_nr = 3
        self.config.set('game', 'trap_nr', trap_nr)
        self.game.restart_game()

        state = self.preprocess.get_state(self.game.instances)
        self.assertEqual(pred_nr + trap_nr, len(state))
