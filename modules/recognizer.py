import random

class Recognizer:
    def __init__(self, config, stable_states, kmeans):
        self.config = config
        self.stable_states = stable_states
        self.kmeans = kmeans

    def get_stable_state(self, state):
        '''Given a raw state, return the closest state from stable states.'''
        min_dist = self.kmeans.states_distance(state, self.stable_states[0])
        min_index = 0

        for i in range(1, len(self.stable_states)):
            dist = self.kmeans.states_distance(state, self.stable_states[i])
            if dist < min_dist:
                min_dist = dist
                min_index = i
        return self.stable_states[min_index]
