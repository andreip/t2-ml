import math

class KMeans:
    def __init__(self, config):
        self.config = config
        self.pred_nr = self.config.getint('game', 'pred_nr')
        self.trap_nr = self.config.getint('game', 'trap_nr')
        self.k = self.config.getint('algo', 'k')

    def states_distance(self, state1, state2):
        predator_coords1 = state1[:self.pred_nr]
        predator_coords2 = state2[:self.pred_nr]
        trap_coords1 = state1[self.pred_nr:]
        assert(len(trap_coords1) == self.trap_nr)
        trap_coords2 = state2[self.pred_nr:]
        assert(len(trap_coords2) == self.trap_nr)

        return self.__states_distance(predator_coords1, predator_coords2) +\
               self.__states_distance(trap_coords1, trap_coords2)

    def __states_distance(self, state1, state2):
        '''Compute the actual distance between two states, s1 {a1,a2}
        and s2 {a3,a4}, trying to link
        a1-a3 and a2-a4 if this is the minimum distance between them, or
        a1-a4 and a2-a3.
        '''
        # Make a copy of the old list, so we don't modify the initial one.
        state2 = list(state2[:])

        # TODO in case this is not that good, try and calculate all combinations
        # and find the combination with the smallest total distance between
        # state characteristics.
        total_dist = 0
        for c1 in state1:
            min_d = self.__euclidian_distance(c1, state2[0])
            min_point = state2[0]
            for c2 in state2[1:]:
                d = self.__euclidian_distance(c1, c2)
                if min_d > d:
                    min_d = d
                    min_point = c2
            total_dist += min_d
            state2.remove(min_point)
        return total_dist

    def __euclidian_distance(self, p1, p2):
        '''Euclidian distance between two points.'''
        assert(len(p1) == len(p2))
        s = 0
        for i in range(len(p1)):
            s += (p1[i] - p2[i])**2
        return math.sqrt(s)
