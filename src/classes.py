import pygame
from os import walk
from settings import *
from menu import *
import math
import time
import sys

VOLUME = 1.0


# TODO: Create screen, clock for the main menu. Check if these can be removed
screen = pygame.display.set_mode((screen_width, screen_height))
# TODO: Create the function Game() that has the clock as an entrie
clock = pygame.time.Clock()

# Auxiliary function
def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            try:
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
            except pygame.error as e:
                print(f"Error loading image: {full_path} - {e}")

    return surface_list

# Classes
class Entity(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.rect = pygame.Rect(pos[0], pos[1], 0, 0)

    def update(self):
        pass


class Tile(Entity):
    def __init__(self, pos, size):
        super().__init__(pos)
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class Finish(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('green')

    
    def update(self, x_shift):
        self.rect.x += x_shift


class Player(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        pygame.mixer.init()


        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.10
        self.image = self.animations['idle_direita'][self.frame_index]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.status = 'idle_direita'
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        #audio
        self.jump_sound = pygame.mixer.Sound('src/audio/jump_sound.wav')
        self.jump_sound.set_volume(0.8 * VOLUME)

    def import_character_assets(self):
        character_path = 'src/graphics/character/'
        
        self.animations = {'idle_direita':[],'idle_esquerda':[], 'fall':[], 'walking_right':[], 'menino_andando_esquerda':[], 'run':[], 'jump':[]}

        for animation in self.animations.keys():
            full_path = character_path +  animation
            self.animations[animation] = import_folder(full_path)

    def update(self):
        self.handle_input()
        self.handle_status()
        self.animate()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if self.on_ground and (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
            self.jump()
            
    def handle_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x > 0:
                self.status = 'walking_right'
            elif self.direction.x < 0:
                self.status =  pygame.transform.flip('walking_right', True, False)
            else:
                if self.status == 'walking_right':
                    self.status = 'idle_direita'
                elif self.status == 'menino_andando_esquerda':
                    self.status = 'idle_esquerda'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def animate(self):
        animation = self.animations[self.status]

        # Check if animation list is empty
        if not animation:
            return

        self.frame_index += self.animation_speed

        # Ensure frame_index is within the range of animation list
        self.frame_index %= len(animation)

        self.image = animation[int(self.frame_index)]


class NPC(Entity):
    def __init__(self, pos, list_of_questions, question_index):
        super().__init__(pos)
        self.image = pygame.Surface((50, 50))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.speed = 2
        self.original_direction = self.speed
        self.list_of_questions = list_of_questions
        self.question_index = question_index
        self.was_answered = False

    def update(self, x_shift):
        self.rect.x += x_shift


    def question(self, list_of_questions, question_index):
        # Extract the question text and the answers
        question = list_of_questions[question_index]

        question_text, answers = question['text'], question['answers']
        correct_answer_index = answers[-1]  # Get the index of the correct answer

        # Create buttons for the answers (excluding the last element which is the correct answer index)
        answer_buttons = [Button(image=None, pos=(640, 360 + i * 100), text_input=answer, font=get_font(50), base_color="Black", hovering_color="Green") for i, answer in enumerate(answers[:-1])]

        while True:
            mouse_pos = pygame.mouse.get_pos()

            screen.fill("white")

            # Display the question
            question_surface = get_font(35).render(question_text, True, "Black")
            question_rect = question_surface.get_rect(center=(640, 260))
            screen.blit(question_surface, question_rect)

            # Update and draw the answer buttons
            for button in answer_buttons:
                button.change_color(mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(answer_buttons):
                        if button.check_for_input(mouse_pos):
                            self.was_answered = True
                            
                            # Check if the selected answer is correct
                            if i == correct_answer_index:

                                print("Correct answer!")
                                return
                            else:
                                print("Estude mais.")
                                return
                            
                            
            pygame.display.update()        
        

class Enemy(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.Surface((50, 50))  # Set the size of the enemy
        self.image.fill('red')  # Set the color of the enemy
        self.rect = self.image.get_rect(topleft=pos)
        self.start_time = time.time()  # Record the time when the enemy is created
        self.speed = 5  # The speed at which the enemy moves

    def update(self, x_shift):
        # Calculate the elapsed time since the enemy was created
        elapsed_time = time.time() - self.start_time

        # Calculate the direction of movement based on the elapsed time
        direction = math.sin(elapsed_time * math.pi)

        # Move the enemy
        self.rect.x += self.speed * direction + x_shift


class Level:
    def __init__(self, level_list, surface):
        self.display_surface = surface
        self.initialize_level(level_list[0])
        self.levels = level_list
        self.current_level = 0
        self.world_shift = 0
        self.current_x = 0
        self.background_image = pygame.image.load(r"src\graphics\backgrounds\level_1\parque2.png")

        #audio
        self.level_bg_music = pygame.mixer.Sound('src/audio/bg_music.wav')
        self.level_bg_music.set_volume(0.3 * VOLUME)
        self.level_bg_music.play(loops = -1)

    def initialize_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.finish = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                tile_size = 64
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if cell == 'E':
                    enemy_sprite = Enemy((x, y))
                    self.enemies.add(enemy_sprite)
                if cell == 'N':
                    npc_sprite = NPC((x, y), list_of_questions, 0)
                    self.npcs.add(npc_sprite)
                if cell == 'F':
                    finish_sprite = Finish((x, y), tile_size)
                    self.finish.add(finish_sprite)

    def next_level(self):
        # Move to the next level
        self.current_level += 1
        if self.current_level >= len(self.levels):  # if we've gone past the last level, go back to the first one
            self.current_level = -1
        self.initialize_level(self.levels[self.current_level])

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        screen_width = 1280
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

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    # def npc_horizontal_movement_collision(self, npc):
    #     npc.rect.x += npc.speed

    #     for sprite in self.tiles.sprites():
    #         if sprite.rect.colliderect(npc.rect):
    #             if npc.speed < 0:
    #                 npc.rect.left = sprite.rect.right
    #                 npc.speed = -npc.speed  # Reverse direction
    #             elif npc.speed > 0:
    #                 npc.rect.right = sprite.rect.left
    #                 npc.speed = -npc.speed  # Reverse direction
    
    def check_npc_collision(self):
        # Check for collisions between the player and each NPC
        for index, npc in enumerate(self.npcs.sprites()):
            if not npc.was_answered and pygame.sprite.collide_rect(self.player.sprite, npc):
                # If a collision is detected, display a text box
                npc.question(list_of_questions, index)


    def is_completed(self):
        # Level is completed when the player collides with the finish line
        return pygame.sprite.collide_rect(self.player.sprite, self.finish.sprite)

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        self.finish.update(self.world_shift)
        self.finish.draw(self.display_surface)
        
        self.scroll_x()

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        self.enemies.update(self.world_shift)
        self.enemies.draw(self.display_surface)

        self.npcs.update(self.world_shift)
        # for npc in self.npcs.sprites():
        #     self.npc_horizontal_movement_collision(npc)
        self.npcs.draw(self.display_surface)
        self.check_npc_collision()
        pygame.display.flip()

        if self.is_completed():
            self.next_level()


# Main
if __name__ == "__main__":

    # Initialize pygame
    pygame.init()

    # Initialize the font module separately
    pygame.font.init()

    # Now you can use pygame's font module
    font = pygame.font.Font("graphics/button/font.ttf", 30)

    # Example usage of the classes
    level_data = [
        "XXXXXXXXXXXXXXXXXXXX",
        "X                  X",
        "X         P        X",
        "X                  X",
        "X      X           X",
        "X                  X",
        "X          E       X",
        "X     XE           X",
        "X                  X",
        "X           E      X",
        "XXXXXXXXXXXXXXXXXXXX",
    ]

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game_level = Level(level_data, screen)


    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")

    menu = Menu(game_level)

    menu.main_menu(background_image_path=r"graphics\button\Background.png")



    #Q: any recomendation in this code?
#R: Yes, you can use a dictionary to store the buttons and their functions, like this:
#   buttons = {"Play": play, "Options": options, "Quit": quit}
#   Then you can iterate over the buttons and check if the mouse is over the button
#   for button in buttons:
#       if button.check_for_input(mouse_pos):
#           buttons[button]() # Call the function associated with the button
#   This way you can add new buttons without having to change the code that checks for input
#   and you can also add new functions without having to change the code that checks for input