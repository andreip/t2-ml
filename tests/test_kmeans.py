import random
import unittest

from objects import *
from game import Game
from helper import Helper
from modules.kmeans import KMeans
from modules.preprocess import Preprocess

class TestObjects(unittest.TestCase):
    def setUp(self):
        self.config = Helper.get_config()
        self.kmeans = KMeans(self.config)
        self.preprocess = Preprocess(self.config)
        self.game = Game(self.config, self.preprocess)
        self.pred_nr = self.config.getint('game', 'pred_nr')
        self.trap_nr = self.config.getint('game', 'trap_nr')

    def test_states_distance(self):
        '''Test distance between same state with shuffled predators
        and traps (should find an exact match => 0 distance).
        '''
        # Enlarge prey's perception to have chances of
        # seeing traps/attackers in test.
        x = self.config.getint('game', 'x')
        self.config.set('game', 'pray_perception', x / 3)
        state1 = self.preprocess.get_state(self.game.instances)

        # Keep the same values, just shuffle them up a bit
        predator_coord = list(state1[:self.pred_nr])
        trap_coord = list(state1[self.pred_nr:])
        random.shuffle(predator_coord)
        random.shuffle(trap_coord)
        state2 = tuple(predator_coord + trap_coord)

        self.assertEqual(0, self.kmeans.states_distance(state1, state2))
