import math
import random
import unittest

from helper import Helper

class TestHelper(unittest.TestCase):

    def test_objects_collide1(self):
        '''Test the objects collision detection w/ multiple scenarios.'''
        pos1, r1 = (0,0), 1
        pos2, r2 = (0,2), 1
        self.assertFalse(Helper.objects_collide(pos1, r1, pos2, r2))

        pos1, r1 = (0,0), 1
        pos2, r2 = (0,1), 0
        self.assertFalse(Helper.objects_collide(pos1, r1, pos2, r2))

        pos1, r1 = (0,0), 1
        pos2, r2 = (0,1), 1
        self.assertTrue(Helper.objects_collide(pos1, r1, pos2, r2))

        pos1, r1 = (0,0), 1
        pos2, r2 = (2,2), 1
        self.assertFalse(Helper.objects_collide(pos1, r1, pos2, r2))

    def test_objects_collide2(self):
        pos1, r1 = (0,0), 10
        r2 = 15
        pos2 = (0, r1 + r2 - 1)
        self.assertTrue(Helper.objects_collide(pos1, r1, pos2, r2))

    def test_get_direction_towards(self):
        direction = Helper.get_direction_towards((0,0), (0,10))
        self.assertEqual(90, direction)

        direction = Helper.get_direction_towards((0,0), (1,1))
        self.assertEqual(45, direction)

        direction = Helper.get_direction_towards((0,0), (-1,-1))
        eps = math.sin(math.radians(225)) - math.sin(math.radians(direction))
        self.assertTrue(eps < 0.001)
