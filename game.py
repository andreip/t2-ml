#!/usr/bin/env python

import ConfigParser
import io
import math
import random
import sys

from ui.game import Draw
from objects import BaseObject, Pray, Predator, Trap

class Game:
    '''The game class is dealing with actual manipulation of instances, by
    moving them round by round and detecting when the game has ended.

    One can reset the game and play again, as many times as it wants.
    '''
    def __init__(self, config_file='config.rc'):
        self.config = self.__open_config(config_file)
        self.restart_game()

    def play(self):
        ended = False
        while not ended:
            self.play_round()
            ended = self.game_ended()
        print 'game ended: ' + ended

    def play_round(self):
        for instance in self.instances:
            instance.move()
        self.instances = BaseObject.resolve_collisions(self.instances)

    def restart_game(self):
        self.instances = self.__get_initial_game_instances()

    @property
    def instances(self):
        return self.instances

    @property
    def config(self):
        return self.config

    def game_ended(self):
        '''Check if the game ended:
        - pray and no predators
        - predators and no pray
        - none of them -> bug
        '''
        pray, pred, trap = BaseObject.count_instances(self.instances)
        # At least one of them should remain.
        assert(pray != 0 or pred != 0)
        if pray == 0 and pred > 0:
            return 'GAME OVER'
        elif pray == 1 and pred == 0:
            return 'YOU WIN'
        return False

    @staticmethod
    def objects_collide(pos1, rad1, pos2, rad2):
        '''Detects if two objects touch another.'''
        (x1, y1), (x2, y2) = pos1, pos2
        actual_dist = math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)
        no_collision_dist = rad1 + rad2
        return actual_dist < no_collision_dist

    def __get_initial_game_instances(self):
        '''Generate random positions for pray, attackers and traps
        no one collides with another one, initially.
        Instantiate each object with its coordintes and return an
        array of all of them.
        '''
        instances = []

        # generate pray's position
        pray_collide_radius = self.config.getint('game','pray_collision')
        pray_coord = self.__generate_coord_without_collision([], pray_collide_radius)
        # Create a new Pray instance.
        instances.append(Pray(self.config, pray_coord))

        # generate all predators w/o collision w/ existing ones.
        pred_coords = []
        pred_collide_radius = self.config.getint('game','pred_collision')
        while len(pred_coords) < self.config.getint('game','pred_nr'):
            # Create a list of the form (coord, collision_radius) to pass to
            # coord generator.
            collision_list =\
               [(pray_coord, pray_collide_radius)] +\
               map(lambda c: (c, pred_collide_radius), pred_coords)
            coord = self.__generate_coord_without_collision(collision_list,
                                                            pred_collide_radius)
            pred_coords.append(coord)
            # Create a new Predator instance.
            instances.append(Predator(self.config, coord))

        # generate all traps w/o collision w/ pray/predators.
        trap_coords = []
        trap_collide_radius = self.config.getint('game','trap_collision')
        while len(trap_coords) < self.config.getint('game','trap_nr'):
            collision_list =\
               [(pray_coord, pray_collide_radius)] +\
               map(lambda c: (c, pred_collide_radius), pred_coords) +\
               map(lambda c: (c, trap_collide_radius), trap_coords)
            coord = self.__generate_coord_without_collision(collision_list,
                                                            trap_collide_radius)
            trap_coords.append(coord)
            # Create a new Predator instance.
            instances.append(Trap(self.config, coord))

        return instances

    def __generate_coord_without_collision(self, collision_list, collision_radius):
        '''Generate a new coordinate so that it does not collide with any
        of the coords from collision_list.
        '''
        x,y = self.__get_dimensions()
        while True:
            coord = (random.random()*x, random.random()*y)
            # new generated coord should not conflict w/ collision list.
            for (coord2, collision_radius2) in collision_list:
                if Game.objects_collide(coord, collision_radius,
                                        coord2, collision_radius2):
                    break
            # did not break, thus no collision w/ any of coords from list.
            else:
                return coord

    def __get_dimensions(self):
        return self.config.getint('game','x'), self.config.getint('game','y')

    def __open_config(self, config_file):
        with open(config_file) as f:
            # Read values from config file
            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(io.BytesIO(f.read()))
        return config

if __name__ == '__main__':
    game = Game()
    while True:
        # Play w/o gui
        game.play()
        game.restart_game()
        # Play with gui
        Draw(game)
        break
