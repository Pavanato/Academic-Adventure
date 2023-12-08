import pygame
from settings import *

    
# TODO: Create screen, clock for the main menu. Check if these can be removed
screen = pygame.display.set_mode((screen_width, screen_height))
# TODO: Create the function Game() that has the clock as an entrie
clock = pygame.time.Clock()

# Auxiliary functions
def get_font(size):
    return pygame.font.Font(r"src\graphics\button\font.ttf", size)

class Button:
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

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.check_for_input(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Menu:
    def __init__(self, level_instance):
        self.current_screen = "main_menu"
        self.level = level_instance

    def play(self):
        while self.current_screen == "play":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(pygame.image.load(r"src\graphics\backgrounds\level_1\parque2.png"), (0, 0))
            self.level.run()

            pygame.display.update()
            clock.tick(60)

    def options(self):
        while self.current_screen == "options":
            options_mouse_pos = pygame.mouse.get_pos()

            screen.fill("white")

            options_text = get_font(45).render("This is the OPTIONS screen.", True, "Black")
            options_rect = options_text.get_rect(center=(640, 260))
            screen.blit(options_text, options_rect)

            options_back = Button(image=None, pos=(640, 460),
                                  text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            options_back.change_color(options_mouse_pos)
            options_back.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if options_back.check_for_input(options_mouse_pos):
                        self.current_screen = "main_menu"

            pygame.display.update()

    def main_menu(self, background_image_path):
        background = pygame.image.load(background_image_path)

        while self.current_screen == "main_menu":
            screen.blit(background, (0, 0)) 

            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(30).render("Academic Adventure: From ABC to PhD", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))

            play_button = Button(image=pygame.image.load("src/graphics/button/Play Rect.png"), pos=(640, 250),
                                 text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=pygame.image.load("src/graphics/button/Options Rect.png"), pos=(640, 400),
                                    text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load("src/graphics/button/Quit Rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            screen.blit(menu_text, menu_rect)

            for button in [play_button, options_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        self.current_screen = "play"
                        self.play()
                    if options_button.check_for_input(menu_mouse_pos):
                        self.current_screen = "options"
                        self.options()
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def game_over(self):
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
