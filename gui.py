import pygame, math, sys
from pygame.locals import *

from objects import Pray, Predator, Trap

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
PINK=(255,0,128)
LIGHTBLUE=(0,255,255)
YELLOW=(255,255,0)
BLUE=(0,0,255)
GRAY=(128,128,128)

PERCEPT_COLOR=GRAY
COLLIDE_COLOR=RED
PRAY_COLOR=YELLOW
PRED_COLOR=BLUE
TRAP_COLOR=GRAY

class GUI:
    def __init__(self, game):
        resolution = (game.config.getint('game','x'),
                      game.config.getint('game','y'))
        self.screen = pygame.display.set_mode(resolution, DOUBLEBUF)
        self.game = game
        self.clock = pygame.time.Clock()
        self.running = True

    def draw(self):
        if self.running == False:
            return

        #self.clock.tick(30)

        # USER INPUT
        for event in pygame.event.get():
            # In case of quit
            if event.type == pygame.QUIT:
                self.running = False
                break

            if not hasattr(event, 'key'):
                continue
            down = event.type == KEYDOWN
            if event.key == K_ESCAPE:
                self.running = False
                break

        if self.running:
            self.screen.fill(BLACK)
            for instance in self.game.instances:
                self.draw_instance(instance)
            pygame.display.flip()
        else:
            pygame.quit()


    def draw_instance(self, instance):
        '''Draw a creature: two outer shells: perception, collision,
        (draw perception first as perception should be > collision)
        then the creature.'''
        coord = self.get_coord(instance.coord)
        if instance.perception_radius > 0:
            pygame.draw.circle(self.screen, PERCEPT_COLOR, coord,
                               instance.perception_radius, 1)
        pygame.draw.circle(self.screen, COLLIDE_COLOR, coord,
                           instance.collision_radius, 1)
        if isinstance(instance, Predator):
            color = PRED_COLOR
        elif isinstance(instance, Pray):
            color = PRAY_COLOR
        else:
            color = TRAP_COLOR
        pygame.draw.circle(self.screen, color, coord,
                           instance.collision_radius / 2)

    def get_coord(self, coord):
        '''Pygame knows only how to draw w/ integer coords.'''
        (a,b) = coord
        return (int(a),int(b))
