import math
import random

class BaseObject(object):
    def __init__(self, config, coord):
        self.config = config
        self.coord = coord
        # Common properties for objects.
        self.gameX = config.getint('game', 'x')
        self.gameY = config.getint('game', 'y')
        self.set_new_direction()
        self.dead = False

    def is_dead(self):
        '''Killing an object should have an effect of not drawing it any
        more.'''
        return self.dead

    def kill(self):
        self.dead = True

    def move(self):
        '''By default, it does not move :).'''
        pass

    def set_new_direction(self):
        self.direction = random.randrange(0,360)

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
        pass

    @staticmethod
    def objects_collide(o1, o2):
        return game.objects_collide(o1.coord, o1.collision_radius,
                                    o2.coord, o2.collision_radius)


class Pray(BaseObject):
    def move(self):
        '''Execute a move, but check for corners too.'''
        (x,y) = self.get_next_position()
        # In case we would leave the board.
        if x < 0 or x > self.gameX or y < 0 or y > self.gameY:
            self.set_new_direction()
            self.move()
        else:
            self.coord = (x,y)

    def get_next_position(self):
        (x,y) = self.coord
        rad = self.direction * math.pi / 180
        x += self.speed * math.cos(rad)
        y += self.speed * math.sin(rad)
        return (x,y)

    @property
    def collision_radius(self):
        return self.config.getint('game', 'pray_collision')
    @property
    def perception_radius(self):
        return self.config.getint('game', 'pray_perception')
    @property
    def speed(self):
        return self.config.getint('game', 'pray_speed')

class Predator(Pray):
    @property
    def collision_radius(self):
        return self.config.getint('game', 'pred_collision')
    @property
    def perception_radius(self):
        return self.config.getint('game', 'pred_perception')
    @property
    def speed(self):
        return self.config.getint('game', 'pred_speed')

class Trap(BaseObject):
    @property
    def collision_radius(self):
        return self.config.getint('game', 'trap_collision')
    @property
    def perception_radius(self):
        return 0
    @property
    def speed(self):
        return 0
