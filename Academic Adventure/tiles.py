import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        # Creates a new surface for the tile with the specified size
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        # Gets the rectangle area of the tile and position it at specified coordinates
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, x_shift):
        # Upadates the position of the tile to simulate scrolling
        self.rect.x += x_shift
        