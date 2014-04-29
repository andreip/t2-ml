#!/usr/bin/env python

import random
import sys

from helper import Helper
from ui.game import Draw
from objects import BaseObject, Pray, Predator, Trap
from modules.kmeans import KMeans
from modules.preprocess import Preprocess
from modules.sarsa import Sarsa
from modules.recognizer import Recognizer


class Game:
    '''The game class is dealing with actual manipulation of instances, by
    moving them round by round and detecting when the game has ended.

    One can reset the game and play again, as many times as it wants.
    '''
    def __init__(self, config, preprocess):
        self.config = config
        self.preprocess = preprocess
        self.restart_game()
        self.verbose = self.config.getint('game', 'verbose')

    def play(self):
        ended = False
        while not ended:
            # Extract components from current state.
            self.preprocess.process_state(self.instances)
            self.play_round()
            ended = self.game_ended()
        if self.verbose:
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

    @property
    def pray(self):
        '''Returns the pray instance.'''
        r = filter(lambda o : isinstance(o, Pray), self.instances)
        return r[0] if r else None

    def get_allowed_states(self):
        '''The allowed moves are the directions (in interval [0,360) degrees ).
        '''
        return range(359)

    def game_ended(self):
        '''Check if the game ended:
        - pray and no predators
        - predators and no pray
        - none of them -> bug
        '''
        pray, pred, trap = BaseObject.count_instances(self.instances)
        # At least one of them should remain.
        # TODO checkout why this assert doesn't always hold.
        #assert(pray != 0 or pred != 0)
        if pray == 0 and pred >= 0:
            return Helper.LOST
        elif pray == 1 and pred == 0:
            return Helper.WON
        return False

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
        instances.append(Pray(self.config, pray_coord, self))

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
            instances.append(Predator(self.config, coord, self))

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
            instances.append(Trap(self.config, coord, self))

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
                if Helper.objects_collide(coord, collision_radius,
                                          coord2, collision_radius2):
                    break
            # did not break, thus no collision w/ any of coords from list.
            else:
                return coord

    def __get_dimensions(self):
        return self.config.getint('game','x'), self.config.getint('game','y')

if __name__ == '__main__':
    config = Helper.get_config()
    preprocess = Preprocess(config)
    game = Game(config, preprocess)
    kmeans = KMeans(config, game)
    sarsa = Sarsa(config, game)

    #
    # Preprocess module.
    #
    for i in range(config.getint('algo', 'preprocess_games')):
        # Play w/o gui
        game.play()
        game.restart_game()
    print 'Have ' + str(len(preprocess.states)) + ' states after preprocess.'

    #
    # KMeans module, reduce the number of states.
    #
    cluster_states = kmeans.kmeans(preprocess.states)
    print 'Have ' + str(len(cluster_states)) + ' states after kmeans.'

    # Instantiate the recognizer based on the cluster_states resulted from
    # kmeans.
    recognizer = Recognizer(config, cluster_states)

    #
    # Sarsa learning ; play games and learn.
    #
    # Learn games now, train and build Q.
    game.restart_game()
    learning_games = config.getint('algo', 'learning_games')
    # Filter states produced by preprocessor, so that it's recognized to be
    # one from the kmeans produced stable states.
    state = recognizer.get_stable_state(preprocess.get_state(game.instances))
    action = sarsa.get_action(state, game.get_allowed_states())
    while learning_games > 0:
        game.pray.set_direction(action)
        # Execute the action a from state s, going to state s'.
        game.play_round()

        game_ended = game.game_ended()
        if game_ended:
            game.restart_game()
            learning_games -= 1
            # This will determine the state to not be found in utilities
            # and thus return 0 always, promoting only the reward (as it's a
            # final step in game).
            next_state = next_action = 0
        else:
            next_state = recognizer.get_stable_state(preprocess.get_state(game.instances))
            # Get next action and its reward for s -> s'.
            next_action = sarsa.get_action(next_state, game.get_allowed_states())
        # Update utilities and update (s,a) <- (s', a').
        sarsa.update_utilities(state, action, next_state, next_action, game_ended)
        state, action = next_state, next_action

    # Play with gui
    #Draw(game)
