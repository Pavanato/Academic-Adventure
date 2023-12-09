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
        self.book = 0
        self.cur_health = 100  
        self.max_health = 4
        self.ui_instance = UI(self.screen, 'src/graphics/collectibles/book_bar.png')


    def new(self):
        # Initialize a new game
        self.level = Level(level_list, self.screen, self.change_books, self.change_health)
        self.menu = Menu(self.level)
        
    def change_books(self, amount):
        self.book += amount
        self.ui_instance.show_books(self.book)
        
    def change_health(self, amount):
        self.cur_health += amount
    
    def run(self):
        self.new()
    
        while self.running:
            self.ui_instance.show_health(self.cur_health, self.max_health)
            self.ui_instance.show_books(self.book)
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


        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
