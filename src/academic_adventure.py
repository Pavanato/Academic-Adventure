"""
academic_adventure.py

This module contains the main game logic for the Academic Adventure game. It uses the pygame 
library to create a game window, handle events, and render the game state to the screen.
"""

# importing libraries
import pygame

from classes import *
from menu import *
from settings import *

class Game:
    def __init__(self) -> None:
        # Initialize pygame and create window
        pygame.init()
        pygame.mixer.init()

        #audio
        self.bg_music = pygame.mixer.Sound('src/audio/bg_music.wav')
        self.bg_music.set_volume(0.3)
        self.bg_music.play(loops = -1)

        # Create the screen and clock
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.x = 0

        # Game loop control
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

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # 'ESC' key to pause the game
                            self.menu.current_screen = "pause"
                            self.menu.pause()

            if self.menu.current_screen == "main_menu":
                self.menu.main_menu(r"src\graphics\backgrounds\level_1\parque2.png")
            elif self.menu.current_screen == "play":
                self.level.run()
                pygame.display.flip()
                clock.tick(60)
            elif self.menu.current_screen == "credits":
                self.menu.credits()
            elif self.level.game_over:
                self.menu.game_over()
    
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
