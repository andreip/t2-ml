import sys

from objects import BaseObject, Pray, Predator, Trap

class Preprocess:
    INFINITY = sys.maxint

    def __init__(self, config):
        # Keep a record of all the states a k
        self.states = set()
        self.config = config

    @property
    def states(self):
        return self.states

    def process_state(self, instances):
        self.states.add(self.get_state(instances))

    def get_state(self, instances):
        pray, _, _ = BaseObject.count_instances(instances)
        assert(pray != 0)

        # Make a list of all visible instances from pray's point of view.
        visible_predators = []
        visible_traps = []
        pray = None
        for i in instances:
            if isinstance(i, Pray):
                pray = i
                break

        for i in instances:
            # Check if it's visible from pray's position.
            if i != pray:
                if BaseObject.object_sees_object(pray, i):
                    if isinstance(i, Predator):
                        visible_predators.append(i)
                    elif isinstance(i, Trap):
                        visible_traps.append(i)

        pred_nr = self.config.getint('game', 'pred_nr')
        trap_nr = self.config.getint('game', 'trap_nr')
        # Sanity checks.
        assert(pred_nr >= len(visible_predators))
        assert(trap_nr >= len(visible_traps))

        predators = map(lambda o: self.get_relative_coord(pray.coord, o.coord),
                        visible_predators)
        traps = map(lambda o: self.get_relative_coord(pray.coord, o.coord),
                    visible_traps)
        while len(predators) < pred_nr:
            # Append a big number, way bigger than the map.
            predators.append((Preprocess.INFINITY, Preprocess.INFINITY))
        while len(traps) < trap_nr:
            # Append a big number, way bigger than the map.
            traps.append((Preprocess.INFINITY, Preprocess.INFINITY))
        return tuple(predators + traps)

    def get_relative_coord(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return (x2-x1, y2-y1)
