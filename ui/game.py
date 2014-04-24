import pygame, math, sys
from pygame.locals import *

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255, 0, 0)
PINK=(255,0,128)
LIGHTBLUE=(0,255,255)

SCALE=5

PERCEPT_COLOR=LIGHTBLUE
COLLIDE_COLOR=PINK
PRAY_COLOR=WHITE
PRED_COLOR=RED

class Draw:
    def __init__(self, config):
        self.config = config
        resolution = (config.getint('game','x')*SCALE,
                      config.getint('game','y')*SCALE)
        self.screen = pygame.display.set_mode(resolution, DOUBLEBUF)
        print config.get('game','pray_coord')
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
            # Draw perception, collision, shape
            pygame.draw.circle(self.screen, PERCEPT_COLOR,
                               self.get_pray_coord(),
                               SCALE * pray_percept_radius, 1)
            pray_collide_radius = self.config.getint('game','pray_collision')
            pygame.draw.circle(self.screen, COLLIDE_COLOR,
                               self.get_pray_coord(),
                               SCALE * pray_collide_radius, 1)
            pygame.draw.circle(self.screen, PRAY_COLOR, self.get_pray_coord(), SCALE)

    def get_pray_coord(self):
        (a,b) = self.config.get('game', 'pray_coord')
        return (int(a),int(b))
