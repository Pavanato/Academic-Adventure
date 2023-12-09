import pygame
import sys

from settings import *

    
# TODO: Create screen, clock for the main menu. Check if these can be removed
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# TODO: Create the function Game() that has the clock as an entrie
clock = pygame.time.Clock()

# Auxiliary function
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

    def main_menu(self, background_image_path):
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
        while self.current_screen == "credits":
            credits_mouse_pos = pygame.mouse.get_pos()

            screen.fill("white")

            credits_text = get_font(45).render("This is the credits screen.", True, "Black")
            credits_rect = credits_text.get_rect(center=(640, 260))
            screen.blit(credits_text, credits_rect)

            credits_back = Button(image=None, pos=(640, 460),
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
