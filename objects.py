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
        self.killed = False

    def is_dead(self):
        return self.killed

    def kill(self):
        self.killed = True

    def move(self):
        '''By default, it does not move :).'''
        pass

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
        (x,y) = self.coord
        rad = self.direction * math.pi / 180
        x += self.speed * math.cos(rad)
        y += self.speed * math.sin(rad)
        return (x,y)

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
        import game
        return game.objects_collide(o1.coord, o1.collision_radius,
                                    o2.coord, o2.collision_radius)


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
