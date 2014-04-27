import random
import unittest

from objects import *
from game import get_config

class TestObjects(unittest.TestCase):

    def setUp(self):
        self.config = get_config()

    def test_objects_collide(self):
        pray_r = self.config.getint('game', 'pray_collision')
        pred_r = self.config.getint('game', 'pred_collision')

        o1 = Pray(self.config, (0, 0))
        self.assertEqual(o1.coord, (0,0))
        self.assertEqual(o1.collision_radius, pray_r)

        o2 = Predator(self.config, (0, pray_r + pred_r - 1))
        self.assertEqual(o2.coord, (0, pray_r + pred_r - 1))
        self.assertEqual(o2.collision_radius, pred_r)

        self.assertTrue(BaseObject.objects_collide(o1, o2))

    def test_move_loop(self):
        '''Infinite recursion test in move() call.
        It's added because it was a bug that was happening.
        '''
        self.config.set('game', 'x', '300')
        self.config.set('game', 'y', '300')
        self.config.set('game', 'pray_collision', '15')
        coord_pray = (128.83141588437942, 294.753514205884)
        Pray(self.config, coord_pray).move()

    def test_resolve_collision_pray_predator(self):
        '''Test collision resolution between multiple predators
        and a pray. (between one and three prays, randomly)
        '''
        pray_r = self.config.getint('game', 'pray_collision')
        pred_r = self.config.getint('game', 'pred_collision')

        pray = Pray(self.config, (0, 0))
        instances = [pray]

        nr_pred = random.randint(1,3)
        predators = []
        for i in range(nr_pred):
            pred = Predator(self.config, (0, pray_r + pred_r - 1))
            self.assertTrue(BaseObject.objects_collide(pray, pred))
            predators.append(pred)
            instances.append(pred)

        instances = BaseObject.resolve_collisions(instances)
        if nr_pred == 1:
            # Pray should survive, predator should die.
            self.assertEqual(instances, [pray])
            self.assertFalse(pray.is_dead())
            self.assertTrue(all(pred.is_dead() for pred in predators))
        elif nr_pred > 1:
            # Pray should die, all predators should survive.
            self.assertEqual(nr_pred, len(instances))
            self.assertTrue(pray.is_dead())
            self.assertTrue(all(not pred.is_dead() for pred in predators))

    def test_resolve_collision_trap_objects(self):
        '''Test both the trap and the object die after collision.'''
        trap_r = self.config.getint('game', 'trap_collision')
        pray_r = self.config.getint('game', 'pray_collision')
        pred_r = self.config.getint('game', 'pred_collision')

        trap = Trap(self.config, (0,0))
        instances = [trap]
        if random.random() < 0.5:
            o = Pray(self.config, (0, trap_r + pray_r - 1))
        else:
            o = Predator(self.config, (0, trap_r + pred_r - 1))
        instances.append(o)

        self.assertTrue(BaseObject.objects_collide(trap, o))

        instances = BaseObject.resolve_collisions(instances)
        self.assertEqual([], instances)
        self.assertTrue(o.is_dead())
        self.assertTrue(trap.is_dead())

    def test_resolve_collision_predators(self):
        '''Test both the predators survive if they collide.'''
        pred_r = self.config.getint('game', 'pred_collision')

        o1 = Predator(self.config, (0, 0))
        o2 = Predator(self.config, (0, pred_r + pred_r - 1))
        self.assertTrue(BaseObject.objects_collide(o1, o2))

        self.assertEqual([o1, o2], BaseObject.resolve_collisions([o1, o2]))
        self.assertFalse(o1.is_dead())
        self.assertFalse(o2.is_dead())
