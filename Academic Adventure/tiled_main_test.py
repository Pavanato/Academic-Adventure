import pygame, sys
import tiled_settings_test as ts
from tiled_level_test import Level

# Game_data
level_0 = {'background': 'levels/teste/back_2.csv'}

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((ts.screen_width, ts.screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)
