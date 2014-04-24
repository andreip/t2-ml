import pygame, math, sys
from pygame.locals import *

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
PINK=(255,0,128)
LIGHTBLUE=(0,255,255)
YELLOW=(255,255,0)
BLUE=(0,0,255)

PERCEPT_COLOR=LIGHTBLUE
COLLIDE_COLOR=PINK
PRAY_COLOR=YELLOW
PRED_COLOR=BLUE

class Draw:
    def __init__(self, config):
        self.config = config
        resolution = (config.getint('game','x'),
                      config.getint('game','y'))
        self.screen = pygame.display.set_mode(resolution, DOUBLEBUF)
        self.run()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(30)

            # USER INPUT
            for event in pygame.event.get():
                # In case of quit
                if event.type == pygame.QUIT:
                    running = False
                    break

                if not hasattr(event, 'key'):
                    continue
                down = event.type == KEYDOWN
                if event.key == K_ESCAPE:
                    running = False
                    break
            self.screen.fill(BLACK)
            self.draw_once()
            pygame.display.flip()

        pygame.quit()

    def draw_once(self):
        pray_percept_radius = self.config.getint('game','pray_perception')
        pray_collide_radius = self.config.getint('game','pray_collision')
        pray_coord = self.config.get('game', 'pray_coord')
        self.draw_object(self.get_coord(pray_coord),
                         [PERCEPT_COLOR, COLLIDE_COLOR, PRAY_COLOR],
                         [pray_percept_radius, pray_collide_radius,
                          pray_collide_radius / 2])
        pred_percept_radius = self.config.getint('game','pred_perception')
        pred_collide_radius = self.config.getint('game','pred_collision')
        for i in range(self.config.getint('game','pred_nr')):
            pred_coord = self.config.get('game','pred_coords')[i]
            self.draw_object(self.get_coord(pred_coord),
                             [PERCEPT_COLOR, COLLIDE_COLOR, PRED_COLOR],
                             [pred_percept_radius, pred_collide_radius,
                              pred_collide_radius / 2])

    def draw_object(self, coords, colors, dimensions):
        '''Draw two outer shells, then the object.'''
        pygame.draw.circle(self.screen, colors[0], coords, dimensions[0], 1)
        pygame.draw.circle(self.screen, colors[1], coords, dimensions[1], 1)
        pygame.draw.circle(self.screen, colors[2], coords, dimensions[2])

    def get_coord(self, coord):
        '''Pygame knows only how to draw w/ integer coords.'''
        (a,b) = coord
        return (int(a),int(b))
