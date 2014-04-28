from collections import defaultdict
import random

from helper import Helper

class KMeans:
    def __init__(self, config, game):
        self.config = config
        self.game = game
        self.pred_nr = self.config.getint('game', 'pred_nr')
        self.trap_nr = self.config.getint('game', 'trap_nr')
        self.coord_nr = self.pred_nr + self.trap_nr
        self.k = self.config.getint('algo', 'k')

    def kmeans(self, instances):
        # Select k random centroids out of instances at first.
        centroids = random.sample(instances, self.k)
        # For each instance, check in which cluster does each
        # one fit (min distance to centroid).
        clusters = self.kmeans_clusters(instances, centroids)

        # Recalculate new centroids based on clusters and then
        # recalculate centroids until they don't change any more.
        while True:
            centroids = self.kmeans_centroids(clusters)
            new_clusters = self.kmeans_clusters(instances, centroids)
            # When the clusters/centroids converge, we can exit.
            if clusters == new_clusters:
                break
            clusters = new_clusters
        from nose.tools import set_trace; set_trace()
        return centroids

    def kmeans_centroids(self, clusters):
        '''Calculate centroids based on clusters by doing a mean between
        all states within the same cluster.
        '''
        self.pretty_print_clusters(clusters)
        new_centroids = [0 for _ in range(self.k)]
        for i in range(self.k):
            state_sum = tuple([(0,0) for _ in range(self.coord_nr)])
            nr = 0.0
            for state,cluster in clusters.iteritems():
                if cluster == i:
                    nr += 1
                    state_sum = self.add_states(state_sum, state)
            # At least one representat for a cluster should exist.
            #assert(nr > 0)
            if nr > 0:
                # Now divide by the number of members in a cluster every coordinate.
                new_centroids[i] = map(lambda coord: tuple([c / nr for c in coord]),
                                       state_sum)
            else:
                new_centroids[i] = map(lambda coord: tuple([self.game.preprocess.infinity
                                                            for c in coord]),
                                       state_sum)
        return new_centroids

    def pretty_print_clusters(self, clusters):
        d = defaultdict(int)
        for _,cluster in clusters.iteritems():
            d[cluster] += 1
        print d

    def kmeans_clusters(self, instances, centroids):
        '''Create a hashtable of instance-index in centroids list.'''
        clusters = {}
        for instance in instances:
            min_dist = self.states_distance(instance, centroids[0])
            cluster_index = 0
            for i in range(1, len(centroids)):
                dist = self.states_distance(instance, centroids[i])
                if dist < min_dist:
                    min_dist = dist
                    cluster_index = i
            clusters[instance] = cluster_index
        return clusters

    def add_states(self, state1, state2):
        if not state1:
            return state2

        predator_coords1 = state1[:self.pred_nr]
        predator_coords2 = state2[:self.pred_nr]
        trap_coords1 = state1[self.pred_nr:]
        assert(len(trap_coords1) == self.trap_nr)
        trap_coords2 = state2[self.pred_nr:]
        assert(len(trap_coords2) == self.trap_nr)

        return self.__add_states(predator_coords1, predator_coords2) +\
               self.__add_states(trap_coords1, trap_coords2)

    def states_distance(self, state1, state2):
        predator_coords1 = state1[:self.pred_nr]
        predator_coords2 = state2[:self.pred_nr]
        trap_coords1 = state1[self.pred_nr:]
        assert(len(trap_coords1) == self.trap_nr)
        trap_coords2 = state2[self.pred_nr:]
        assert(len(trap_coords2) == self.trap_nr)

        return self.__states_distance(predator_coords1, predator_coords2) +\
               self.__states_distance(trap_coords1, trap_coords2)

    def __add_states(self, state1, state2):
        '''Adding two states together first requires to match
        two characteristics together (the best ones), and then
        add them (they're just coordinates, the characterisitcs).
        '''
        state1, state2 = list(state1[:]), list(state2[:])
        for i in range(len(state1)):
            coord1 = state1[i]
            _, coord2 = self.__find_best_state(coord1, state2)
            state2.remove(coord2)
            state1[i] = self.__add_coords(coord1, coord2)
        return state1

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
            min_d, min_point = self.__find_best_state(c1, state2)
            total_dist += min_d
            state2.remove(min_point)
        return total_dist

    def __find_best_state(self, state, states):
        '''Find the best state out of states array to match
        the given state.
        '''
        best_d = Helper.euclidian_distance(state, states[0])
        best_state = states[0]
        for state2 in states[1:]:
            d = Helper.euclidian_distance(state, state2)
            if best_d > d:
                best_d = d
                best_state = state2
        return best_d, best_state

    def __add_coords(self, coord1, coord2):
        assert(len(coord1) == len(coord2))
        return tuple([coord1[i] + coord2[i] for i in range(len(coord1))])
