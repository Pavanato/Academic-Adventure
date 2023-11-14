import pygame
from tiled_settings_test import *
from tiled_tile_test import Tile, StaticTile

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = -1

        background_layout = import_csv_layout(level_data['background'])
        self.background_sprites = self.create_tile_group(background_layout, 'background')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'background':
                        background_tile_list = import_cut_graphic('images/twitter_background/full_school.jpg')
                        tile_surface = background_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

        return sprite_group

    def run(self):
        self.background_sprites.draw(self.display_surface)
        self.background_sprites.update(self.world_shift)

from csv import reader

def import_csv_layout(path):
    with open(path) as map:
        background_map = []
        level = reader(map, delimiter = ',')
        for row in level:
            background_map.append(list(row))
        return background_map
    
def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)

    return cut_tiles