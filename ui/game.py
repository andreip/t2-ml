import pygame, math, sys
from pygame.locals import *

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
        '''Draw objects like pray, predators, traps on the map.'''
        # Draw pray
        pray_percept_radius = self.config.getint('game','pray_perception')
        pray_collide_radius = self.config.getint('game','pray_collision')
        pray_coord = self.config.get('game', 'pray_coord')
        self.draw_creature(self.get_coord(pray_coord),
                          [PERCEPT_COLOR, COLLIDE_COLOR, PRAY_COLOR],
                          [pray_percept_radius, pray_collide_radius,
                           pray_collide_radius / 2])
        # Draw predators
        pred_percept_radius = self.config.getint('game','pred_perception')
        pred_collide_radius = self.config.getint('game','pred_collision')
        for i in range(self.config.getint('game','pred_nr')):
            pred_coord = self.config.get('game','pred_coords')[i]
            self.draw_creature(self.get_coord(pred_coord),
                              [PERCEPT_COLOR, COLLIDE_COLOR, PRED_COLOR],
                              [pred_percept_radius, pred_collide_radius,
                               pred_collide_radius / 2])
        # Draw traps
        trap_collide_radius = self.config.getint('game','trap_collision')
        for i in range(self.config.getint('game','trap_nr')):
            trap_coord = self.config.get('game','trap_coords')[i]
            self.draw_trap(self.get_coord(trap_coord),
                          [COLLIDE_COLOR, TRAP_COLOR],
                          [trap_collide_radius, trap_collide_radius / 2])

    def draw_creature(self, coords, colors, dimensions):
        '''Draw a creature: two outer shells: perception, collision,
        (draw perception first as perception should be > collision)
        then the creature.'''
        pygame.draw.circle(self.screen, colors[0], coords, dimensions[0], 1)
        pygame.draw.circle(self.screen, colors[1], coords, dimensions[1], 1)
        pygame.draw.circle(self.screen, colors[2], coords, dimensions[2])

    def draw_trap(self, coords, colors, dimensions):
        '''Draw a trap: one outer shell: collision, then the trap.'''
        pygame.draw.circle(self.screen, colors[0], coords, dimensions[0], 1)
        pygame.draw.circle(self.screen, colors[1], coords, dimensions[1])

    def get_coord(self, coord):
        '''Pygame knows only how to draw w/ integer coords.'''
        (a,b) = coord
        return (int(a),int(b))
