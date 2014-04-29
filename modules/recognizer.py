import random

class Recognizer:
    def __init__(self, config, stable_states):
        self.config = config
        self.stable_states = stable_states

    def get_stable_state(self, state):
        '''Given a raw state, return the closest state from stable states.'''
        # TODO check which is closest
        return random.choice(self.stable_states)
