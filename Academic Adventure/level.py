import pygame
from tiles import Tile
from settings import tile_size, screen_width
from entity import Player
#from enemy import Enemy

class Level:
    def __init__(self, level_data, surface):

        # Level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

    def setup_level(self, layout):
        # Initialization of data structures for tiles, player and enemy
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        #self.enemy = pygame.sprite.GroupSingle()
        
        # Loop through level data (layout)
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size  # Calculate x position based on tile size
                y = row_index * tile_size  # Calculate y position based on tile size

                if cell == 'X':
                    # Creates a tile object
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    # Creates a player
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                #if cell == 'E':
                    # Creates an enemy
                    #enemy_sprite = Enemy((x, y))
                    #self.enemy.add(enemy_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        # If the player isn't touching the obstacle anymore
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y >1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
            # Level tiles
            self.tiles.update(self.world_shift)
            self.tiles.draw(self.display_surface)
            self.scroll_x()

            # Player
            self.player.update()
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.player.draw(self.display_surface)

            # Enemy
            #self.enemy.update(self.world_shift)
            #self.player.draw(self.display_surface)