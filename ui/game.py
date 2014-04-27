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

class Draw:
    def __init__(self, game):
        resolution = (game.get_config().getint('game','x'),
                      game.get_config().getint('game','y'))
        self.screen = pygame.display.set_mode(resolution, DOUBLEBUF)
        self.game = game
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
            for instance in self.game.get_instances():
                self.draw_instance(instance)
            self.game.play()
            pygame.display.flip()

            game_ended = self.game.game_ended()
            if game_ended:
                print 'game ended: ' + game_ended
                # So screen stays longer.
                pygame.time.delay(3000)
                break

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
