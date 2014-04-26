import random
import unittest

from game import objects_collide

class TestGame(unittest.TestCase):

    def test_objects_collide1(self):
        '''Test the objects collision detection w/ multiple scenarios.'''
        pos1, r1 = (0,0), 1
        pos2, r2 = (0,2), 1
        self.assertFalse(objects_collide(pos1, r1, pos2, r2))

        pos1, r1 = (0,0), 1
        pos2, r2 = (0,1), 0
        self.assertFalse(objects_collide(pos1, r1, pos2, r2))

        pos1, r1 = (0,0), 1
        pos2, r2 = (0,1), 1
        self.assertTrue(objects_collide(pos1, r1, pos2, r2))

        pos1, r1 = (0,0), 1
        pos2, r2 = (2,2), 1
        self.assertFalse(objects_collide(pos1, r1, pos2, r2))
