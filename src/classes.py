import pygame
from os import walk
from settings import *
from menu import *
import time
import sys


# Auxiliary function
def import_folder(path):
    """
    Import images of a folder

    Parameters
    ----------
    path : str
        The path of the folder containing the images
    
    Returns
    -------
    list
        A list of surfaces (images)
    """

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
    """
    Base class for game entities.

    Attributes
    ----------
    rect : pygame.Rect
        The rectangular area of the entity.

    Methods
    -------
    __init__(self, pos)
        Initializes the entity
    
    update(self)
    """

    def __init__(self, pos):
        """
        Initializes the entity.

        Parameters
        ----------
        pos : tuple
            The initial position of the entity (x, y).
        """
        super().__init__()
        self.rect = pygame.Rect(pos[0], pos[1], 0, 0)

    def update(self):
        pass


class Tile(Entity):
    """
    Class representing a block (tile) in the game.

    Attributes
    ----------
    image : pygame.Surface
        The surface (image) of the block.

    rect : pygame.Rect
        The rectangular area of the block.

    Methods
    -------
    __init__(self, pos, size)
        Initializes the block.
    
    update(self, x_shift)
        Updates the position of the block along the x-axis.
    """

    def __init__(self, pos, size):
        """
        Initializes the block.

        Parameters
        ----------
        pos : tuple
            The initial position of the block (x, y).

        size : int
            The size of the block's sides.

        Returns
        -------
        None.
        """

        super().__init__(pos)
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        """
        Updates the position of the block along the x-axis.

        Parameters
        ----------
        x_shift : int
            The amount to be shifted along the x-axis.

        Returns
        -------
        None.
        """

        self.rect.x += x_shift


class Finish(Tile):
    """
    Class representing a finish block in the game.

    Attributes
    ----------
    image : pygame.Surface
        The surface (image) of the finish block.

    rect : pygame.Rect
        The rectangular area of the finish block.

    Methods
    -------
    __init__(self, pos, size)
        Initializes the finish block.
    
    update(self, x_shift)
        Updates the position of the finish block along the x-axis.
    """
        
    def __init__(self, pos, size):
        """
        Initializes the finish block.

        Parameters
        ----------
        pos : tuple
            The initial position of the finish block (x, y).

        size : int
            The size of the finish block's sides.

        Returns
        -------
        None.
        """

        super().__init__(pos, size)
        self.image.fill('green')
    
    def update(self, x_shift):
        """
        Updates the position of the finish block along the x-axis.

        Parameters
        ----------
        x_shift : int
            The amount to be shifted along the x-axis.

        Returns
        -------
        None.
        """
        self.rect.x += x_shift


class Player(Entity):
    """
    Attributes
    ----------
    frame_index : float
        Index used for animation frames.

    animation_speed : float
        Speed of the animation.

    image : pygame.Surface
        Current image of the player.

    direction : pygame.math.Vector2
        Vector representing the player's movement direction.

    speed : int
        Speed of the player's movement.

    _gravity : float
        Acceleration which the player moves downward.

    jump_speed : int
        Vertical speed during a jump.

    status : str
        Current status of the player (e.g., 'idle_direita', 'fall', 'walking_right').

    on_ground : bool
        True if the player is on the ground.

    on_ceiling : bool
        True if the player is on the ceiling.

    on_left : bool
        True if the player is touching a surface on the left.

    on_right : bool
        True if the player is touching a surface on the right.

    Methods
    -------
    __init__(pos)
        Initializes the player instance.

    import_character_assets()
        Imports character animations.

    update()
        Updates the player's state.

    handle_input()
        Handles player input.

    handle_status()
        Handles player status based on direction.

    apply_gravity()
        Applies gravity to the player's vertical movement.

    jump()
        Initiates a jump.

    animate()
        Animates the player based on the current status.
    """

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
        self._gravity = 0.8
        self.jump_speed = -16

        self.status = 'idle_direita'
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        #audio
        self.__jump_sound = pygame.mixer.Sound('src/audio/jump_sound.wav')
        self.__jump_sound.set_volume(0.8)

    def import_character_assets(self):
        """
        Imports character animations.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
                
        character_path = 'src/graphics/character/'
        
        self.animations = {'idle_direita':[],'idle_esquerda':[], 'fall':[], 'walking_right':[], 'menino_andando_esquerda':[], 'run':[], 'jump':[]}

        for animation in self.animations.keys():
            full_path = character_path +  animation
            self.animations[animation] = import_folder(full_path)

    def update(self):
        """
        Updates the player's state.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        
        self.handle_input()
        self.handle_status()
        self.animate()

    def handle_input(self):
        """
        Handles player input.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

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
        """
        Handles player status based on direction.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x > 0:
                self.status = 'walking_right'
            elif self.direction.x < 0:
                self.status = 'menino_andando_esquerda'
            else:
                if self.status == 'walking_right':
                    self.status = 'idle_direita'
                elif self.status == 'menino_andando_esquerda':
                    self.status = 'idle_esquerda'

    def apply_gravity(self):
        """
        Applies gravity to the player's vertical movement.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

        self.direction.y += self._gravity
        self.rect.y += self.direction.y

    def jump(self):
        """
        Initiates a jump.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

        self.direction.y = self.jump_speed
        self.__jump_sound.play()

    def animate(self):
        """
        Animates the player based on the current status.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

        animation = self.animations[self.status]

        # Check if animation list is empty
        if not animation:
            return

        self.frame_index += self.animation_speed

        # Ensure frame_index is within the range of animation list
        self.frame_index %= len(animation)

        self.image = animation[int(self.frame_index)]


class NPC(Entity):
    """
    Represents a non-player character (NPC) in the game.

    Attributes
    ----------
    image : pygame.Surface
        Surface representing the NPC (blue rectangle).

    rect : pygame.Rect
        Rectangular area of the NPC.

    list_of_questions : list
        List of dictionaries containing questions and answers.

    question_index : int
        Index indicating the current question from the list.

    was_answered : bool
        True if the NPC's question was answered.

    Methods
    -------
    update(x_shift)
        Updates the position of the NPC along the x-axis.

    question(list_of_questions, question_index)
        Displays a question and handles player input for answering it.
    """

    def __init__(self, pos, list_of_questions, question_index):
        """
        Initializes the NPC instance.

        Parameters
        ----------
        pos : tuple
            Initial position of the NPC (x, y).

        list_of_questions : list
            List of dictionaries containing questions and answers.

        question_index : int
            Index indicating the current question from the list.

        Returns
        -------
        None.
        """
        
        super().__init__(pos)
        self.image = pygame.Surface((16, 16))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.list_of_questions = list_of_questions
        self.question_index = question_index
        self.was_answered = False

    def update(self, x_shift):
        """
        Updates the position of the NPC along the x-axis.

        Parameters
        ----------
        x_shift : int
            The amount to be shifted along the x-axis.

        Returns
        -------
        None.
        """
        self.rect.x += x_shift

    def question(self, list_of_questions, question_index):
        """
        Displays a question and handles player input for answering it.

        Parameters
        ----------
        list_of_questions : list
            List of dictionaries containing questions and answers.

        question_index : int
            Index indicating the current question from the list.

        Returns
        -------
        int
            1 if the answer is correct, 0 otherwise.
        """
        
        # Extract the question text and the answers
        question = list_of_questions[question_index]

        question_text, answers = question['text'], question['answers']
        correct_answer_index = answers[-1]  # Get the index of the correct answer

        # Create buttons for the answers (excluding the last element which is the correct answer index)
        answer_buttons = [Button(image=None, pos=(640, 360 + i * 100), text_input=answer, font=get_font(38), base_color="Black", hovering_color="Blue") for i, answer in enumerate(answers[:-1])]

        while True:
            mouse_pos = pygame.mouse.get_pos()

            thickness = 5

            question_len = len(question_text)
            pygame.draw.rect(screen, "black", pygame.Rect(640 - 18 * question_len - thickness, 150 - thickness, 36 * question_len + 2 * thickness, 100 + 2 * thickness))
            pygame.draw.rect(screen, "white", pygame.Rect(640 - 18 * question_len, 150, 36 * question_len, 100))

            answers_len = answers[0:3]
            answers_len = len(max(answers_len))
            pygame.draw.rect(screen, "black", pygame.Rect(640 - 40 * answers_len - thickness, 310 - thickness, 80* answers_len + 2 * thickness, 300 + 2 * thickness))
            pygame.draw.rect(screen, "white", pygame.Rect(640 - 40 * answers_len, 310, 80 * answers_len, 300))


            # Split the question into lines
            lines = question_text.split('\n')

            # Display each line separately
            for i, line in enumerate(lines):
                line_surface = get_font(30).render(line, True, "Black")
                line_rect = line_surface.get_rect(center=(640, 200 + i * 30))  # Adjust the y-coordinate for each line
                screen.blit(line_surface, line_rect)

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
                                # Display a message indicating that the answer is correct
                                screen.fill("black")                                
                                answer_event = get_font(30).render("CORRECT ANSWER", True, "Green")
                                answer_rect= answer_event.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                                screen.blit(answer_event, answer_rect)
                                pygame.display.flip()
                                time.sleep(2.5)           
                                return 1
                            else:
                                # Display a message indicating that the answer is incorrect
                                screen.fill("black")                                
                                answer_event = get_font(30).render("INCORRECT ANSWER", True, "Red")
                                answer_rect= answer_event.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                                screen.blit(answer_event, answer_rect)
                                pygame.display.flip()
                                time.sleep(2.5)
                                return 0
                            
                            
            pygame.display.update()        
        

class Collectible(Entity):
    """
    Represents a collectible item in the game.

    Attributes
    ----------
    image : pygame.Surface
        Surface representing the collectible.

    rect : pygame.Rect
        Rectangular area of the collectible.

    value : int
        Value associated with the collectible.

    Methods
    -------
    __change_books(amount)
        Changes the number of books collected and updates the UI.

    __change_health(amount)
        Changes the player's health by the specified amount.

    update(x_shift)
        Updates the position of the collectible along the x-axis.
    """

    def __init__(self, pos, value):
        """
        Initializes the Collectible instance.

        Parameters
        ----------
        pos : tuple
            Initial position of the collectible (x, y).

        value : int
            Value associated with the collectible.

        Returns
        -------
        None.

        """
        
        super().__init__(pos)
        image = pygame.image.load("src/graphics/collectibles/book.png").convert_alpha()
        rect_image = image.get_rect()
        self.image = pygame.Surface((rect_image.width, rect_image.height), pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.value = value

    def __change_books(self, amount):
        """
        Changes the number of books collected and updates the UI.

        Parameters
        ----------
        amount : int
            The change in the number of books collected.

        Returns
        -------
        None.

        """

        self.book += amount
        self.ui_instance.show_books(self.book)

    def __change_health(self, amount):
        """
        Changes the player's health by the specified amount.

        Parameters
        ----------
        amount : int
            The change in the player's health.

        Returns
        -------
        None.

        """
        self.cur_health += amount

    def update(self, x_shift):
        """
        Updates the position of the collectible along the x-axis.

        Parameters
        ----------
        x_shift : int
            The amount to be shifted along the x-axis.

        Returns
        -------
        None.

        """

        self.rect.x += x_shift


class UI:
    """
    Represents the user interface in the game.

    Attributes
    ----------
    display_surface : pygame.Surface
        The display surface for rendering the UI.

    book_bar : pygame.Surface
        The image representing the book bar.

    book_bar_topleft : tuple
        The top-left coordinates of the book bar.

    bar_max_width : int
        The maximum width of the book bar.

    bar_height : int
        The height of the book bar.

    book : pygame.Surface
        The image representing a book.

    book_rect : pygame.Rect
        The rectangular area of the book image.

    font : pygame.font.Font
        The font used for rendering text on the UI.

    Methods
    -------
    show_health(current, full)
        Displays the health bar on the UI based on the current and full health values.

    show_books(amount)
        Displays the collected books and their amount on the UI.
    """
    
    def __init__(self, surface, book_bar_image_path):
        """
        Initializes the UI instance.

        Parameters
        ----------
        surface : pygame.Surface
            The display surface for rendering the UI.

        book_bar_image_path : str
            The file path for the image representing the book bar.

        Returns
        -------
        None.
        """
        
        # setup 
        self.display_surface = surface 

        # health 
        self.book_bar = pygame.image.load(book_bar_image_path).convert_alpha()
        self.book_bar_topleft = (35, 45)
        self.bar_max_width = 4
        self.bar_height = 4

        # books
        self.book = pygame.image.load('src/graphics/collectibles/book.png').convert_alpha()
        self.book_rect = self.book.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font(None, 36)

    def show_health(self, current, full):
        """
        Displays the health bar on the UI based on the current and full health values.

        Parameters
        ----------
        current : int
            The current health value.

        full : int
            The full health value.

        Returns
        -------
        None.
        """

        self.display_surface.blit(self.book_bar, (20, 10))
        current_book_ratio = current / full
        current_bar_width = self.bar_max_width * current_book_ratio
        health_bar_rect = pygame.Rect(self.book_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_books(self, amount):
        """
        Displays the collected books and their amount on the UI.

        Parameters
        ----------
        amount : int
            The number of collected books.

        Returns
        -------
        None.
        """
        self.display_surface.blit(self.book, self.book_rect)
        book_amount_surf = self.font.render(str(amount), False, '#33323d')
        book_amount_rect = book_amount_surf.get_rect(midleft=(self.book_rect.right + 4, self.book_rect.centery))
        self.display_surface.blit(book_amount_surf, book_amount_rect)


class Level:
    """
    Represents a level in the game.

    Attributes
    ----------
    display_surface : pygame.Surface
        The display surface for rendering the level.

    levels : list
        List containing level layouts.

    current_level : int
        Index of the current level.

    world_shift : int
        Horizontal shift of the world.

    current_x : int
        Current x-coordinate.

    background_image : pygame.Surface
        The background image of the level.

    bg_x : int
        Background x-coordinate.

    game_over : bool
        Flag indicating whether the game is over.

    collectibles_collected : int
        Number of collectibles (books) collected.

    book_bar : pygame.Surface
        Image representing the book bar.

    ui : UI
        The user interface for the level.

    Methods
    -------
    initialize_level(layout)
        Initializes the level based on the given layout.

    next_level()
        Moves to the next level.

    scroll_x()
        Handles horizontal scrolling based on player position.

    horizontal_movement_collision()
        Handles collisions during horizontal movement.

    vertical_movement_collision()
        Handles collisions during vertical movement.

    check_npc_collision()
        Checks for collisions between the player and NPCs.

    check_collectible_collisions()
        Checks for collisions between the player and collectibles.

    change_collectible(value)
        Changes the number of collected collectibles.

    is_completed()
        Checks if the level is completed.

    run()
        Runs the main logic for the level.
    """

    def __init__(self, level_list, bg_list,surface):
        """
        Initializes the Level instance.

        Parameters
        ----------
        level_list : list
            List containing level layouts.

        surface : pygame.Surface
            The display surface for rendering the level.

        Returns
        -------
        None.
        """

        self.display_surface = surface
        self.initialize_level(level_list[0])
        self.background_image = pygame.image.load(bg_list[0])
        self.levels = level_list
        self.current_level = 0
        self.world_shift = 0
        self.current_x = 0
        self.bg_x = 0
        self.game_over = False
        self.score = 0

        #collectibles
        self.collectibles_collected = 0 
        self.book_bar = pygame.image.load('src/graphics/collectibles/book_bar.png').convert_alpha()
        self.ui = UI(self.display_surface, 'src/graphics/collectibles/book_bar.png')  # Add the UI to the level

    def initialize_level(self, layout):
        """
        Initializes the level based on the given layout.

        Parameters
        ----------
        layout : list
            Layout representing the level.

        Returns
        -------
        None.
        """

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.npcs = pygame.sprite.Group()
        self.finish = pygame.sprite.GroupSingle()
        self.collectible = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if cell == 'X':
                    tile = Tile((x, y), TILE_SIZE)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if cell == 'N':
                    npc_sprite = NPC((x, y), list_of_questions, 0)
                    self.npcs.add(npc_sprite)
                if cell == 'F':
                    finish_sprite = Finish((x, y), TILE_SIZE)
                    self.finish.add(finish_sprite)
                if cell == 'C':
                    collectible_sprite = Collectible((x,y), value = 1)
                    self.collectible.add(collectible_sprite)

    def next_level(self):
        """
        Moves to the next level.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        
        # Check if the current level is the last one
        if self.current_level == len(self.levels) - 1:
            self.game_over = True
            return
        
        # Move to the next level
        self.current_level += 1
        self.player.empty()
        self.bg_x = 0
        self.background_image = pygame.image.load(bg_list[self.current_level])
        self.initialize_level(self.levels[self.current_level])

    def restart(self):
        """
        Restarts the game.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        self.current_x = 0
        self.game_over = False
        self.score = 0
        self.collectibles_collected = 0 
        self.bg_x = 0
        self.current_level = 0
        self.player.empty()
        self.background_image = pygame.image.load(bg_list[self.current_level])
        self.initialize_level(self.levels[self.current_level])

    def scroll_x(self):
        """
        Handles horizontal scrolling based on player position.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < SCREEN_WIDTH / 3 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 3) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        """
        Handles collisions during horizontal movement.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

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
        """
        Handles collisions during vertical movement.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

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
    
    def check_npc_collision(self):
        """
        Checks for collisions between the player and NPCs.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

        # Check for collisions between the player and each NPC
        for index, npc in enumerate(self.npcs.sprites()):
            if not npc.was_answered and pygame.sprite.collide_rect(self.player.sprite, npc):
                # If a collision is detected, display a text box
                self.score += npc.question(list_of_questions, index)

    
    def check_collectible_collisions(self):
        """
        Checks for collisions between the player and collectibles.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """

        collided_collectible = pygame.sprite.spritecollide(self.player.sprite, self.collectible, True)
       		
        for collectible in collided_collectible:
            self.change_collectible(collectible.value)

    def change_collectible(self, value):
        """
        Changes the number of collected collectibles.

        Parameters
        ----------
        value : int
            The change in the number of collectibles.

        Returns
        -------
        None.

        """

        self.collectibles_collected += value

    def show_score(self):
        """
        Displays the score on the screen.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        score_surface = get_font(30).render(f"Grade: {self.score}/10", True, "Black")
        score_rect = score_surface.get_rect(center=(1080, 50))
        screen.blit(score_surface, score_rect)

    def is_completed(self):
        """
        Checks if the level is completed.

        Parameters
        ----------
        None.

        Returns
        -------
        bool
            True if the level is completed, False otherwise.
        """

        # Level is completed when the player collides with the finish line
        return pygame.sprite.collide_rect(self.player.sprite, self.finish.sprite)

    def run(self):
        """
        Runs the main logic for the level.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """

        self.bg_x += self.world_shift

        screen.blit(self.background_image, (self.bg_x, 0))

        self.tiles.update(self.world_shift)
        # self.tiles.draw(self.display_surface)

        self.finish.update(self.world_shift)
        self.finish.draw(self.display_surface)
        
        self.scroll_x()

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        # self.enemies.update(self.world_shift)
        # self.enemies.draw(self.display_surface)

        self.npcs.update(self.world_shift)
        # for npc in self.npcs.sprites():
        #     self.npc_horizontal_movement_collision(npc)
        self.npcs.draw(self.display_surface)
        self.check_npc_collision()

        self.collectible.update(self.world_shift)
        self.collectible.draw(self.display_surface)
        self.check_collectible_collisions()
        
        self.ui.show_health(self.collectibles_collected, 10)  # Exemplo: 10 é o valor máximo de livros a serem coletados
        self.ui.show_books(self.collectibles_collected)

        self.show_score()
        
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

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game_level = Level(level_data, screen)


    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")

    menu = Menu(game_level)

    menu.main_menu(background_image_path=r"graphics\button\Background.png")
