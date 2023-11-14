import pygame
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        #self.import_enemy_assets()
        #self.frame_index = 0
        #self.animation_speed = 0.15
        self.image = pygame.Surface((32, 64))
        self.image.fill('red')
        #self.image = self.animations['run'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

    def import_enemy_assets(self):
            enemy_path = 'graphics/enemy/run/'
            self.animations = {'run':[]}

            for animation in self.animations.keys():
                full_path = enemy_path + animation
                self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
    
    def update(self, x_shift):
        #self.animate()
        self.rect.x += x_shift

"""
class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
"""