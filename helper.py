import ConfigParser
import math
import io

class Helper:
    @staticmethod
    def get_config(config_file='config.rc'):
        with open(config_file) as f:
            # Read values from config file
            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(io.BytesIO(f.read()))
        return config

    @staticmethod
    def objects_collide(pos1, rad1, pos2, rad2):
        '''Detects if two objects touch another.'''
        (x1, y1), (x2, y2) = pos1, pos2
        actual_dist = math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)
        no_collision_dist = rad1 + rad2
        return actual_dist < no_collision_dist

    @staticmethod
    def get_direction_towards(p1, p2):
        '''Get direction from p1 to p2 (in degrees).'''
        (xf,yf) = p2
        (x,y) = p1
        rad = math.atan2(yf-y, xf-x)
        return math.degrees(rad)

    @staticmethod
    def object_sees_object(coord1, coord2, radius):
        '''First object can see second object.'''
        return Helper.objects_collide(coord1, radius, coord2, 0)

    @staticmethod
    def euclidian_distance(p1, p2):
        '''Euclidian distance between two points.'''
        assert(len(p1) == len(p2))
        s = 0
        for i in range(len(p1)):
            s += (p1[i] - p2[i])**2
        return math.sqrt(s)

    @staticmethod
    def get_final_position(coord, angle, distance):
        '''Calculate where the coord would end up with the
        angle, if it were to move for distance.
        '''
        (x,y) = coord
        rad = math.radians(angle)
        x += distance * math.cos(rad)
        y += distance * math.sin(rad)
        return (x,y)

    @staticmethod
    def verbose_print(msg):
        config = Helper.get_config()
        if config.getint('game', 'verbose'):
            print msg
