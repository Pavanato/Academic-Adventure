import pygame
import sys

from settings import *

    
# TODO: Create screen, clock for the main menu. Check if these can be removed
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# TODO: Create the function Game() that has the clock as an entrie
clock = pygame.time.Clock()

# Auxiliary function
def get_font(size):
    """
    Get a Pygame font object with a specified size.

    Parameters
    ----------
    size : int
        The font size.

    Returns
    -------
    pygame.font.Font
        A Pygame font object.

    """
    return pygame.font.Font(r"src\graphics\button\font.ttf", size)


class Button:
    """
    Represents a clickable button in the game.

    Attributes
    ----------
    image : pygame.Surface
        The image representing the button.

    x_pos : int
        The x-coordinate of the button's center.

    y_pos : int
        The y-coordinate of the button's center.

    font : pygame.font.Font
        The font used for rendering text on the button.

    base_color : str
        The base color of the button's text.

    hovering_color : str
        The color of the button's text when hovering.

    text_input : str
        The text displayed on the button.

    text : pygame.Surface
        The rendered text surface.

    rect : pygame.Rect
        The rectangular area of the button.

    text_rect : pygame.Rect
        The rectangular area of the rendered text.

    Methods
    -------
    update(screen)
        Updates and renders the button on the given screen.

    check_for_input(position)
        Checks if a given position is within the button's area.

    change_color(position)
        Changes the color of the button's text based on the mouse position.

    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Initializes the Button instance.

        Parameters
        ----------
        image : pygame.Surface
            The image representing the button.

        pos : tuple
            The x, y coordinates of the button's center.

        text_input : str
            The text displayed on the button.

        font : pygame.font.Font
            The font used for rendering text on the button.

        base_color : str
            The base color of the button's text.

        hovering_color : str
            The color of the button's text when hovering.

        Returns
        -------
        None.

        """ 
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
        """
        Updates and renders the button on the given screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen where the button will be rendered.

        Returns
        -------
        None.

        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """
        Checks if a given position is within the button's area.

        Parameters
        ----------
        position : tuple
            The x, y coordinates of the position to check.

        Returns
        -------
        bool
            True if the position is within the button's area, False otherwise.

        """
        return self.rect.collidepoint(position)

    def change_color(self, position):
        """
        Changes the color of the button's text based on the mouse position.

        Parameters
        ----------
        position : tuple
            The x, y coordinates of the mouse position.

        Returns
        -------
        None.

        """
        if self.check_for_input(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Menu:
    """
    Represents the menu system in the game.

    Attributes
    ----------
    current_screen : str
        The current active screen.

    level : Level
        The instance of the game level associated with the menu.

    Methods
    -------
    main_menu(background_image_path)
        Displays the main menu screen with buttons for play, credits, and quit.

    credits()
        Displays the credits screen with information about the game developers.

    pause()
        Displays the pause screen with options to resume, go to the main menu, or quit the game.

    game_over()
        Displays the game over screen with the option to return to the main menu.

    """
    def __init__(self, level_instance):
        """
        Initializes the Menu instance.

        Parameters
        ----------
        level_instance : Level
            The instance of the game level associated with the menu.

        Returns
        -------
        None.

        """
        self.current_screen = "main_menu"
        self.level = level_instance

    def main_menu(self, background_image_path):
        """
        Displays the main menu screen with buttons for play, credits, and quit.

        Parameters
        ----------
        background_image_path : str
            The file path for the background image of the main menu.

        Returns
        -------
        None.

        """
        background = pygame.image.load(background_image_path)

        while self.current_screen == "main_menu":
            screen.blit(background, (0, 0)) 

            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(30).render("Academic Adventure: From ABC to PhD", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))

            play_button = Button(image=pygame.image.load("src/graphics/button/Play Rect.png"), pos=(640, 250),
                                 text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            credits_button = Button(image=pygame.image.load("src/graphics/button/Credits Rect.png"), pos=(640, 400),
                                    text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load("src/graphics/button/Quit Rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            screen.blit(menu_text, menu_rect)

            for button in [play_button, credits_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        self.current_screen = "play"
                    if credits_button.check_for_input(menu_mouse_pos):
                        self.current_screen = "credits"
                        self.credits()
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def credits(self):
        """
        Displays the credits screen with information about the game developers.

        Returns
        -------
        None.

        """
        credits_image_pavanato = pygame.image.load("src/graphics/photos_credits/pavanato_photo.png").convert_alpha()
        credits_image_pavanato = pygame.transform.scale(credits_image_pavanato, (150, 150))

        credits_image_roberta = pygame.image.load("src/graphics/photos_credits/roberta_photo.jfif").convert_alpha()
        credits_image_roberta = pygame.transform.scale(credits_image_roberta, (150, 150))

        credits_image_beatriz = pygame.image.load("src/graphics/photos_credits/beatriz_photo.jfif").convert_alpha()
        credits_image_beatriz = pygame.transform.scale(credits_image_beatriz, (150, 150))

        credits_image_eduardo = pygame.image.load("src/graphics/photos_credits/eduardo_photo.jfif").convert_alpha()
        credits_image_eduardo = pygame.transform.scale(credits_image_eduardo, (150, 150))

        while self.current_screen == "credits":
            credits_mouse_pos = pygame.mouse.get_pos()

            screen.fill("white")

            screen.blit(credits_image_pavanato, (200, 120))
            screen.blit(credits_image_roberta, (880, 120))
            screen.blit(credits_image_beatriz, (200, 360))
            screen.blit(credits_image_eduardo, (880, 360))

            credits_text = get_font(45).render("Game made by:", True, "Black")
            credits_rect = credits_text.get_rect(center=(640, 50))

            pavanato_text = get_font(20).render("Gabriel Pavanato", True, "Black")
            pavanato_rect = pavanato_text.get_rect(center=(280, 300))

            roberta_text = get_font(20).render("Roberta Müller Nuñes", True, "Black")
            roberta_rect = roberta_text.get_rect(center=(980, 300))

            beatriz_text_1 = get_font(20).render("Beatriz Lúcia", True, "Black")
            beatriz_rect_1 = beatriz_text_1.get_rect(center=(280, 530))
            beatriz_text_2 = get_font(20).render("Teixeira de Souza", True, "Black")
            beatriz_rect_2 = beatriz_text_2.get_rect(center=(280, 560))

            eduardo_text = get_font(20).render("Eduardo Nunes Alves", True, "Black")
            eduardo_rect = eduardo_text.get_rect(center=(970, 530))

            screen.blit(credits_text, credits_rect)
            screen.blit(pavanato_text, pavanato_rect)
            screen.blit(roberta_text, roberta_rect)
            screen.blit(beatriz_text_1, beatriz_rect_1)
            screen.blit(beatriz_text_2, beatriz_rect_2)
            screen.blit(eduardo_text, eduardo_rect)

            credits_back = Button(image=None, pos=(640, 650),
                                  text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            credits_back.change_color(credits_mouse_pos)
            credits_back.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if credits_back.check_for_input(credits_mouse_pos):
                        self.current_screen = "main_menu"

            pygame.display.update()

    def pause(self):
        """
        Displays the pause screen with options to resume, go to the main menu, or quit the game.

        Returns
        -------
        None.

        """
        while self.current_screen == "pause":
            pause_mouse_pos = pygame.mouse.get_pos()

            screen.fill("white")

            pause_text = get_font(45).render("PAUSE", True, "Black")
            pause_rect = pause_text.get_rect(center=(640, 260))
            screen.blit(pause_text, pause_rect)

            resume_button = Button(image=None, pos=(640, 360),
                                text_input="RESUME", font=get_font(75), base_color="Black", hovering_color="Green")
            menu_button = Button(image=None, pos=(640, 460),
                                text_input="MENU", font=get_font(75), base_color="Black", hovering_color="Green")
            quit_button = Button(image=None, pos=(640, 560),
                                text_input="QUIT", font=get_font(75), base_color="Black", hovering_color="Green")

            for button in [resume_button, menu_button, quit_button]:
                button.change_color(pause_mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.check_for_input(pause_mouse_pos):
                        self.current_screen = "play"
                    if menu_button.check_for_input(pause_mouse_pos):
                        self.current_screen = "main_menu"
                    if quit_button.check_for_input(pause_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def game_over(self):
        """
        Displays the game over screen with the option to return to the main menu.

        Returns
        -------
        None.
        
        """
        self.level.display_surface.fill((0, 0, 0))  # fill the screen with black

        font = pygame.font.Font(None, 72)  # create a font object
        text = font.render("Game Over", True, (255, 255, 255))  # create a text surface
        rect = text.get_rect(center=(640, 360))  # get the rectangle of the text surface
        self.level.display_surface.blit(text, rect)  # blit the text surface to the screen

        pygame.display.flip()  # update the display

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.current_screen = "main_menu"  # return to the main menu
                    return
