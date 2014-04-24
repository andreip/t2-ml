#!/usr/bin/env python

import ConfigParser
import io
import random
import sys

from ui.game import Draw

def get_config(config_file='config.rc'):
    '''Parse config file and return it in a form of dictionary like.'''
    with open(config_file) as f:
        # Read values from config file
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(f.read()))
    return config

def objects_collide(pos1, rad1, pos2, rad2):
    '''Detects if two objects touch another.'''
    # TODO
    return False

def set_initial_positions(config):
    '''Generate random positions for pray and attackers so that
    no one collides with another one, initially.
    '''
    x,y = config.getint('game','x'), config.getint('game','y')

    # generate pray's position
    pray_coord = (random.random()*x, random.random()*y)
    pray_collide_radius = config.getint('game','pray_collision')
    config.set('game','pray_coord', pray_coord)

    # generate all predators w/o collision w/ existing ones.
    pred_coords = []
    pred_collide_radius = config.getint('game','pred_collision')
    while len(pred_coords) < config.getint('game','pred_nr'):
        coord = (random.random()*x, random.random()*y)
        # new generated coord should not conflict w/ prey.
        if objects_collide(pray_coord, pray_collide_radius,
                            coord, pred_collide_radius):
            continue
        # new generated coord should not conflict w/ generated pred.
        is_collision = False
        for coord2 in pred_coords:
            if objects_collide(coord2, pred_collide_radius,
                               coord, pred_collide_radius):
                is_collision = True
                break
        if not is_collision:
            pred_coords.append(coord)

    config.set('game','pred_coords', pred_coords)

if __name__ == '__main__':
    config = get_config()
    set_initial_positions(config)
    Draw(config)
    #while True:
    #    pass
