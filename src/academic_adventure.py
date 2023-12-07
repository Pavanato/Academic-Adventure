import pygame
from settings import *
from classes import *


screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

pygame.init()

menu = Menu(level)
menu.main_menu(background_image_path="src/graphics/button/Background.png")