import pygame
from os import walk
from settings import *

# TODO averiguar a necessidade de importar sys
import sys

# TODO Criando screen, clock, BG para o main menu. Averiguar se há como retirar
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
BG = pygame.image.load("graphics/button/Background.png")

# TODO função que toma a fonte para o main menu. Averiguar um melhor lugar onde deve ser colocada em outro lugar.
def get_font(size):
    return pygame.font.Font("graphics/button/font.ttf", size)

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
        

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Imports character assets and initializes player attributes
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.10
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # Player movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # Player status attributes
        self.status = 'idle'
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False


    def import_character_assets(self):
        character_path = 'graphics/character/'
        
        self.animations = {'idle':[], 'fall':[], 'menino_andando_direita':[], 'menino_andando_esquerda':[], 'run':[], 'jump':[]}

        for animation in self.animations.keys():
            full_path = character_path +  animation
            self.animations[animation] = import_folder(full_path)


    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]


    def get_input(self):
        keys = pygame.key.get_pressed()

        # Adding motion controls
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        # Adding jump controls (space, up or w)
        if self.on_ground and keys[pygame.K_SPACE]:
            self.jump()
        elif self.on_ground and keys[pygame.K_UP]:
            self.jump()
        elif self.on_ground and keys[pygame.K_w]:
            self.jump()


    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x > 0:
                self.status = 'menino_andando_direita'
            elif self.direction.x < 0:
                self.status = 'menino_andando_esquerda'
            else:
                self.status = 'idle'


    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    def jump(self):
        self.direction.y = self.jump_speed


    def update(self):
        # Updates player attributes based on input, status and animation
        self.get_input()
        self.get_status()
        self.animate()


class Level:
    def __init__(self, level_data, surface):
        # Level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0


    def setup_level(self, layout):
        # Initialization of data structures for tiles and player
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        
        # Loop through level data (layout)
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                # TODO: 64 is the tile size for now, make sure to change it in the future
                tile_size = 64
                x = col_index * tile_size  # Calculates x position based on tile size
                y = row_index * tile_size  # Calculates y position based on tile size

                if cell == 'X':
                    # Creates a tile object
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    # Creates a player
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # TODO: 1200 is the screen widht for now, make sure to change it in the future
        screen_width = 1200
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
        
        # Clears player's left or right contact when not touching the obstacle anymore
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

            # Updates the player, handle horizontal and vertical movement collisions
            self.player.update()
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.player.draw(self.display_surface)


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


# Button made for game's MAIN MENU 
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
                        
class Menu():
    def __init__(self, level_instance):
        self.current_screen = "main_menu"
        self.level = level_instance  # Adicionando o objeto Level à classe Menu

    def play(self):
        while self.current_screen == "play":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill('black')
            self.level.run()

            pygame.display.update()
            clock.tick(60)

    def options(self):
        while self.current_screen == "options":
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            screen.fill("white")

            OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(640, 460),
                                 text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.current_screen = "main_menu"

            pygame.display.update()

    def main_menu(self):
        while self.current_screen == "main_menu":
            screen.fill('black')
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("graphics/button/Play Rect.png"), pos=(640, 250),
                                text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("graphics/button/Options Rect.png"), pos=(640, 400),
                                    text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("graphics/button/Quit Rect.png"), pos=(640, 550),
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.current_screen = "play"
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.current_screen = "options"
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()




################################



# import pygame
# from os import walk
# from settings import tile_size, screen_width

# def import_folder(path):
#     surface_list = []

#     for _, __, img_files in walk(path):
#         for image in img_files:
#             full_path = path + '/' + image
#             image_surf = pygame.image.load(full_path).convert_alpha()
#             surface_list.append(image_surf)

#     return surface_list

# class Entity(pygame.sprite.Sprite):
#     def __init__(self, pos):
#         super().__init__()
#         self.frame_index = 0
#         self.animation_speed = 0.10
#         self.image = None  # Entities should set their own image
#         self.rect = self.image.get_rect(topleft=pos)
#         self.direction = pygame.math.Vector2(0, 0)
#         self.speed = 0
#         self.gravity = 0
#         self.jump_speed = 0
#         self.status = 'idle'
#         self.on_ground = False
#         self.on_ceiling = False
#         self.on_left = False
#         self.on_right = False

#     def import_assets(self, character_path, animations):
#         self.animations = {'idle': [], 'fall': [], 'menino_andando_direita': [],
#                            'menino_andando_esquerda': [], 'run': [], 'jump': []}

#         for animation in animations:
#             full_path = character_path + animation
#             self.animations[animation] = import_folder(full_path)

#     def animate(self):
#         animation = self.animations[self.status]
#         self.frame_index += self.animation_speed
#         if self.frame_index >= len(animation):
#             self.frame_index = 0
#         self.image = animation[int(self.frame_index)]

#     def apply_gravity(self):
#         self.direction.y += self.gravity
#         self.rect.y += self.direction.y

#     def jump(self):
#         self.direction.y = self.jump_speed

#     def update(self):
#         self.animate()

# class Tile(pygame.sprite.Sprite):
#     def __init__(self, pos, size):
#         super().__init__()
#         # Creates a new surface for the tile with the specified size
#         self.image = pygame.Surface((size, size))
#         self.image.fill('grey')
#         # Gets the rectangle area of the tile and position it at specified coordinates
#         self.rect = self.image.get_rect(topleft = pos)
        
#     def update(self, x_shift):
#         # Upadates the position of the tile to simulate scrolling
#         self.rect.x += x_shift

# class Player(Entity):
#     def __init__(self, pos):
#         super().__init__(pos)
#         self.import_assets('graphics/character/', ['idle', 'fall', 'menino_andando_direita', 'menino_andando_esquerda', 'run', 'jump'])

#     def get_input(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#             self.direction.x = 1
#         elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
#             self.direction.x = -1
#         else:
#             self.direction.x = 0

#         if self.on_ground and (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
#             self.jump()

#     def get_status(self):
#         if self.direction.y < 0:
#             self.status = 'jump'
#         elif self.direction.y > 1:
#             self.status = 'fall'
#         else:
#             if self.direction.x > 0:
#                 self.status = 'menino_andando_direita'
#             elif self.direction.x < 0:
#                 self.status = 'menino_andando_esquerda'
#             else:
#                 self.status = 'idle'

#     def update(self):
#         self.get_input()
#         self.get_status()
#         super().update()
#     def __init__(self, pos):
#         super().__init__(pos)
#         self.import_assets('graphics/character/', ['idle', 'fall', 'menino_andando_direita', 'menino_andando_esquerda', 'run', 'jump'])

#     def get_input(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#             self.direction.x = 1
#         elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
#             self.direction.x = -1
#         else:
#             self.direction.x = 0

#         if self.on_ground and (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
#             self.jump()

#     def get_status(self):
#         if self.direction.y < 0:
#             self.status = 'jump'
#         elif self.direction.y > 1:
#             self.status = 'fall'
#         else:
#             if self.direction.x > 0:
#                 self.status = 'menino_andando_direita'
#             elif self.direction.x < 0:
#                 self.status = 'menino_andando_esquerda'
#             else:
#                 self.status = 'idle'

#     def update(self):
#         self.get_input()
#         self.get_status()
#         super().update()

# class Level:
#     def __init__(self, level_data, surface):
#         self.display_surface = surface
#         self.setup_level(level_data)
#         self.world_shift = 0
#         self.current_x = 0

#     def setup_level(self, layout):
#         self.tiles = pygame.sprite.Group()
#         self.player = pygame.sprite.GroupSingle()

#         for row_index, row in enumerate(layout):
#             for col_index, cell in enumerate(row):
#                 tile_size = 64
#                 x = col_index * tile_size
#                 y = row_index * tile_size

#                 if cell == 'X':
#                     tile = Tile((x, y), tile_size)
#                     self.tiles.add(tile)
#                 if cell == 'P':
#                     player_sprite = Player((x, y))
#                     self.player.add(player_sprite)

#     def scroll_x(self):
#         player = self.player.sprite
#         player_x = player.rect.centerx
#         direction_x = player.direction.x
#         screen_width = 1200

#         if player_x < screen_width / 4 and direction_x < 0:
#             self.world_shift = 8
#             player.speed = 0
#         elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
#             self.world_shift = -8
#             player.speed = 0
#         else:
#             self.world_shift = 0
#             player.speed = 8

#     def horizontal_movement_collision(self):
#         player = self.player.sprite
#         player.rect.x += player.direction.x * player.speed

#         for sprite in self.tiles.sprites():
#             if sprite.rect.colliderect(player.rect):
#                 if player.direction.x < 0:
#                     player.rect.left = sprite.rect.right
#                     player.on_left = True
#                     self.current_x = player.rect.left
#                 elif player.direction.x > 0:
#                     player.rect.right = sprite.rect.left
#                     player.on_right = True
#                     self.current_x = player.rect.right

#         if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
#             player.on_left = False
#         if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
#             player.on_right = False

#     def vertical_movement_collision(self):
#         player = self.player.sprite
#         player.apply_gravity()

#         for sprite in self.tiles.sprites():
#             if sprite.rect.colliderect(player.rect):
#                 if player.direction.y > 0:
#                     player.rect.bottom = sprite.rect.top
#                     player.direction.y = 0
#                     player.on_ground = True
#                 elif player.direction.y < 0:
#                     player.rect.top = sprite.rect.bottom
#                     player.direction.y = 0
#                     player.on_ceiling = True

#         if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
#             player.on_ground = False
#         if player.on_ceiling and player.direction.y > 0:
#             player.on_ceiling = False

#     def run(self):
#         self.tiles.update(self.world_shift)
#         self.tiles.draw(self.display_surface)
#         self.scroll_x()
#         self.player.update()
#         self.horizontal_movement_collision()
#         self.vertical_movement_collision()
#         self.player.draw(self.display_surface)