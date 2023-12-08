import pygame
from settings import *
from classes import *
from menu import *

FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        # Initialize a new game
        self.level = Level(level_list, self.screen)
        self.menu = Menu(self.level)    

    def run(self):
        self.new()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.menu.current_screen == "main_menu":
                self.menu.main_menu(r"src\graphics\backgrounds\level_1\parque2.png")
            elif self.menu.current_screen == "play":
                self.menu.play()
            elif self.menu.current_screen == "options":
                self.menu.options()
            elif self.level.current_level == -1:
                self.menu.game_over()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
