import math
import random

from helper import Helper

class BaseObject(object):
    def __init__(self, config, coord, game):
        self.config = config
        self.coord = coord
        self.game = game
        # Common properties for objects.
        self.gameX = config.getint('game', 'x')
        self.gameY = config.getint('game', 'y')
        self.set_new_direction()
        self.killed = False

    def trunc(self, f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        return ('%.*f' % (n + 1, f))[:-1]

    def __str__(self):
        coord = map(lambda c: float(self.trunc(c, 2)), self.coord)
        return '(' + str(coord) + ',' + self.get_type_letter() + ')'
    __repr__ = __str__

    def is_dead(self):
        return self.killed

    def kill(self):
        self.killed = True

    def set_new_direction(self):
        self.direction = random.randrange(0,360)

    def move(self):
        '''Execute a move based on the direction and
        the speed, don't keep count of any radius collision
        with the space.

        In case we would exit the space, change the direction
        until we don't.
        '''
        (x,y) = self.get_next_position()
        # In case we would leave the board.
        eps = 0
        if (x + eps < 0 or x + eps > self.gameX or
            y + eps < 0 or y + eps > self.gameY):
            self.set_new_direction()
            self.move()
        else:
            self.coord = (x,y)

    def get_next_position(self):
        '''Use speed and direction to calculate next position.'''
        return Helper.get_final_position(self.coord, self.direction, self.speed)

    @property
    def collision_radius(self):
        raise NotImplementedError
    @property
    def perception_radius(self):
        raise NotImplementedError
    @property
    def speed(self):
        raise NotImplementedError

    @staticmethod
    def resolve_collisions(objects):
        '''Checks if objects collide and resolves all collisions:
        * if a trap and an object get in contact, both consume
        * if ONE attacker and a prey get in contact, attacker dies
        * if MORE THAN ONE attacker and a prey get in contact, pray dies
        * if attackers get in contact, nothing happens, just change their direction
        '''
        nr_predators_collide_with_pray = 0
        predator_collide_with_pray = None
        pray = None
        for i in range(len(objects)-1):
            for j in range(i+1, len(objects)):
                if BaseObject.objects_collide(objects[i], objects[j]):
                    pray, pred, trap =\
                        BaseObject.count_instances([objects[i], objects[j]])
                    if trap == 1:
                        objects[i].kill()
                        objects[j].kill()
                    elif pred == 2:
                        objects[i].set_new_direction()
                        objects[j].set_new_direction()
                    elif pray == 1 and pred == 1:
                        nr_predators_collide_with_pray += 1
                        if isinstance(objects[i], Predator):
                            predator_collide_with_pray = objects[i]
                        else:
                            predator_collide_with_pray = objects[j]

        # Kill pray
        if nr_predators_collide_with_pray > 1:
            for o in objects:
                if isinstance(o, Pray):
                    o.kill()
        # It was a single predator that collided with the pray, so kill it.
        elif nr_predators_collide_with_pray == 1:
            predator_collide_with_pray.kill()

        # Return a list of objects only with those that survived collisions.
        return filter(lambda o: not o.is_dead(), objects)

    @staticmethod
    def count_instances(objects):
        pray, pred, trap = 0, 0, 0
        for o in objects:
            if isinstance(o, Pray):
                pray += 1
            elif isinstance(o, Predator):
                pred += 1
            elif isinstance(o, Trap):
                trap += 1
        assert pray <= 1
        return pray, pred, trap

    @staticmethod
    def objects_collide(o1, o2):
        return Helper.objects_collide(o1.coord, o1.collision_radius,
                                      o2.coord, o2.collision_radius)

    @staticmethod
    def object_sees_object(o1, o2):
        '''First object can see second object.'''
        return Helper.object_sees_object(o1.coord, o2.coord, o1.perception_radius)

class Pray(BaseObject):
    @property
    def collision_radius(self):
        return self.config.getint('game', 'pray_collision')
    @property
    def perception_radius(self):
        return self.config.getint('game', 'pray_perception')
    @property
    def speed(self):
        return self.config.getint('game', 'pray_speed')

    def get_type_letter(self):
        return 'P'

    def move(self):
        '''Pray should avoid colliding with traps if it sees them.'''
        for instance in self.game.instances:
            if isinstance(instance, Trap):
                # In case the pray sees a trap, try and avoid it.
                if BaseObject.object_sees_object(self, instance):
                    distance = Helper.euclidian_distance(self.coord, instance.coord)
                    future_point = Helper.get_final_position(self.coord,
                        self.direction, distance)
                    if Helper.objects_collide(future_point,
                                              self.collision_radius,
                                              instance.coord,
                                              instance.collision_radius):
                        self.set_new_direction()
        super(Pray, self).move()

class Predator(BaseObject):
    @property
    def collision_radius(self):
        return self.config.getint('game', 'pred_collision')
    @property
    def perception_radius(self):
        return self.config.getint('game', 'pred_perception')
    @property
    def speed(self):
        return self.config.getint('game', 'pred_speed')

    def get_type_letter(self):
        return 'p'

    def move(self):
        '''Predator is pretty dumb: if it sees a pray, it follows it to
        autodestruction.
        '''
        # Can always do indexing on filtered instances, as it should be a pray
        # always, else the game should have finished (bug?).
        pray = filter(lambda x: isinstance(x, Pray), self.game.instances)[0]
        # In case it sees the pray, change direction to follow it.
        if BaseObject.object_sees_object(self, pray):
            self.direction = Helper.get_direction_towards(self.coord, pray.coord)
        super(Predator, self).move()

class Trap(BaseObject):
    def move(self):
        '''Traps don't move :).'''
        pass

    @property
    def collision_radius(self):
        return self.config.getint('game', 'trap_collision')
    @property
    def perception_radius(self):
        return 0
    @property
    def speed(self):
        return 0

    def get_type_letter(self):
        return 'T'
