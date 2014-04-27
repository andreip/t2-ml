#!/usr/bin/env python

import ConfigParser
import io
import math
import random
import sys

from ui.game import Draw
from objects import Pray, Predator, Trap

def get_config(config_file='config.rc'):
    '''Parse config file and return it in a form of dictionary like.'''
    with open(config_file) as f:
        # Read values from config file
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(f.read()))
    return config

def objects_collide(pos1, rad1, pos2, rad2):
    '''Detects if two objects touch another.'''
    (x1, y1), (x2, y2) = pos1, pos2
    actual_dist = math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)
    no_collision_dist = rad1 + rad2
    return actual_dist < no_collision_dist

def generate_without_collision(collision_list, collision_radius):
    '''Generate a new coordinate so that it does not collide with any
    of the coords from collision_list.
    '''
    x,y = config.getint('game','x'), config.getint('game','y')
    while True:
        coord = (random.random()*x, random.random()*y)
        # new generated coord should not conflict w/ collision list.
        for (coord2, collision_radius2) in collision_list:
            if objects_collide(coord2, collision_radius2,
                               coord, collision_radius):
                break
        # did not break, thus no collision w/ any of coords from list.
        else:
            return coord

def get_game_instances(config):
    '''Generate random positions for pray, attackers and traps
    no one collides with another one, initially.
    Instantiate each object with its coordintes and return an
    array of all of them.
    '''
    instances = []

    # generate pray's position
    pray_collide_radius = config.getint('game','pray_collision')
    pray_coord = generate_without_collision([], pray_collide_radius)
    # Create a new Pray instance.
    instances.append(Pray(config, pray_coord))

    # generate all predators w/o collision w/ existing ones.
    pred_coords = []
    pred_collide_radius = config.getint('game','pred_collision')
    while len(pred_coords) < config.getint('game','pred_nr'):
        # Create a list of the form (coord, collision_radius) to pass to
        # coord generator.
        collision_list =\
           [(pray_coord, pray_collide_radius)] +\
           map(lambda c: (c, pred_collide_radius), pred_coords)
        coord = generate_without_collision(collision_list, pred_collide_radius)
        pred_coords.append(coord)
        # Create a new Predator instance.
        instances.append(Predator(config, coord))

    # generate all traps w/o collision w/ pray/predators.
    trap_coords = []
    trap_collide_radius = config.getint('game','trap_collision')
    while len(trap_coords) < config.getint('game','trap_nr'):
        collision_list =\
           [(pray_coord, pray_collide_radius)] +\
           map(lambda c: (c, pred_collide_radius), pred_coords) +\
           map(lambda c: (c, trap_collide_radius), trap_coords)
        coord = generate_without_collision(collision_list, trap_collide_radius)
        trap_coords.append(coord)
        # Create a new Predator instance.
        instances.append(Trap(config, coord))

    return instances

if __name__ == '__main__':
    config = get_config()
    Draw(config, get_game_instances(config))
    #while True:
    #    pass
