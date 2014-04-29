from collections import defaultdict
import random

from helper import Helper

class Sarsa:
    '''Learning algorithm, based on playing multiple games, by updating
    a utility function and getting an action policy.
    '''
    def __init__(self, config, game, preprocess, recognizer, maps=defaultdict(int)):
        # By default return a score of 0 for unknown.
        self.config = config
        self.game = game
        self.preprocess = preprocess
        self.recognizer = recognizer
        self.maps = maps
        self.reward_maps = defaultdict(int)
        # Parameters determined empirically.
        self.alpha = config.getfloat('algo', 'learning_alpha')
        self.eps = config.getfloat('algo', 'learning_eps')
        self.gamma = config.getfloat('algo', 'learning_gamma')

        self.fill_reward_maps()

    def begin_episode(self):
        self.state, self.action = self.get_state_and_action()

    def step(self):
        self.game.pray.set_direction(self.action)
        # Execute the action a from state s, going to state s'.
        self.game.play_round()

        game_ended = self.game.game_ended()
        if game_ended:
            # This will determine the state to not be found in utilities
            # and thus return 0 always, promoting only the reward (as it's a
            # final step in game).
            next_state = next_action = 0
        else:
            # Get next action after s -> s'.
            next_state, next_action = self.get_state_and_action()
        # Update utilities and update (s,a) <- (s', a').
        self.update_utilities(self.state, self.action, next_state, next_action, game_ended)
        self.state, self.action = next_state, next_action

    def get_state_and_action(self):
        # Filter states produced by preprocessor, so that it's recognized to be
        # one from the kmeans produced stable states.
        state = self.recognizer.get_stable_state(
            self.preprocess.get_state(self.game.instances))
        action = self.get_action(state, self.game.get_allowed_states())
        return state, action

    def fill_reward_maps(self):
        '''Win -> 1, loose -> -1, else just 0.'''
        self.reward_maps[Helper.WON] = 1
        self.reward_maps[Helper.LOST] = -1

    def get_action(self, state, legal_actions):
        # Choose among the legal actions with a strategy.
        if random.random() > self.eps:
            return self.__get_action_greedy(state, legal_actions)
        # Else pick a random action from all possible actions.
        return self.__get_action_random(legal_actions)

    def update_utilities(self, state, action, next_state, next_action, result):
        '''Update the utity self.maps based on the current and next move.'''
        state_key = (state, action)
        next_state_key = (next_state, next_action)
        reward = self.reward_maps[result]

        # Update the utilities based from state_key based on next_state_key.
        self.maps[state_key] = (1-self.alpha) * self.maps[state_key] +\
            self.alpha * (reward + self.gamma * self.maps[next_state_key])

    def __get_action_greedy(self, state, legal_actions):
        '''Choose the move that best maximises our utility function
        (forever greedy muhaha).
        '''
        max_action = legal_actions[0]
        max_score = self.maps[(state, max_action)]

        for action in legal_actions[1:]:
            score = self.maps[(state, action)]
            if score > max_score:
                max_score = score
                max_action = action
        return max_action

    def __get_action_random(self, legal_actions):
        '''Simply returns a random action from the given ones.'''
        return random.choice(legal_actions)

