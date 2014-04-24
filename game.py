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
    pass

def random_generate_game(config):
    # generate pray's position
    x,y = config.getint('game','x'), config.getint('game','y')

    pray_coord = (random.random()*x, random.random()*y)
    pred_coord = []
    #while len(pred_coord) < config.getint('game','pred_nr'):
    #    coord = (random.random()*x, random.random()*y)
    #    pred_coord += coord

    config.set('game','pray_coord', pray_coord)

if __name__ == '__main__':
    config = get_config()
    random_generate_game(config)
    Draw(config)
    #while True:
    #    pass
