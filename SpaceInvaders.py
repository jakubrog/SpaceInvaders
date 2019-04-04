import pygame
import sys
from os.path import abspath, dirname

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + '/images/'
FONT_PATH = BASE_PATH + '/fonts/'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 156, 0)
GRAY = (105, 105, 105)

# names of created images
IMG_NAMES = ['filename']

FPS = 15

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768

FONT = FONT_PATH + 'Minecraftia.ttf'

pygame.init()  # initialize all imported pygame modules
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # Initialize a window for display
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

MUSIC_ON = True


# TODO: loading images into IMAGES
# TODO: create images


# single enemy ship
class Enemy(pygame.sprite.Sprite):  # sprite - base class for visible game objects
    def __init__(self, row, column, image_filename, power):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # self.image = IMAGES['image_filename']
        self.row = row
        self.column = column
        self.health = Health()
        self.power = power


# Block or a group of enemies, it's responsible for changing position of each enemy and select their specification
class GroupOfEnemies(pygame.sprite.Group):
    def __init__(self, row, column):
        pygame.sprite.Group.__init__(self)
        # self.image = IMAGES['filename']
        self.row = row
        self.column = column


# Bullet - display and keep information about shot bullet
# direction in constructor depends on who attack
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, direction, speed, power):  # direction -
        pygame.sprite.Sprite.__init__(self)
        # self.image = IMAGES['filename']
        self.speed = speed
        self.destruction = power


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = IMAGES['filename']


# Health - displaying HP point and health management
class Health(pygame.sprite.Sprite):
    def __init_(self):
        pygame.sprite.Sprite.__init__(self)


def settings_menu_show():
    font = pygame.font.Font(FONT, 35)
    help_font = pygame.font.Font(FONT, 17)
    about_font = pygame.font.Font(FONT, 25)

    music_label = font.render("Music", True, RED)
    help_label = help_font.render("[ESC] - get back", True, ORANGE)
    music_select = font.render("< ON >", True, GRAY)
    about = about_font.render("Created by Jakub Rog and Jan Makowiecki in 2019.", True, BLACK)
    music = True

    while True:
        gameDisplay.fill(WHITE)
        gameDisplay.blit(music_label, (50, 300))
        gameDisplay.blit(music_select, (500, 300))
        gameDisplay.blit(about, (105, 650))
        gameDisplay.blit(help_label, (10, 730))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN]:
                        if music:
                            music_select = font.render("< OFF >", True, GRAY)
                        else:
                            music_select = font.render("< ON >", True, GRAY)
                        music = not music

                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    gameDisplay.fill(WHITE)
                    return music

        pygame.display.update()
        clock.tick(FPS)


class MainMenu:
    def __init__(self):
        gameDisplay.fill(WHITE)
        self.font = pygame.font.Font(FONT, 25)
        self.index = 0
        self.label0 = self.font.render("New Game", True, RED)
        self.label1 = self.font.render("Highscores", True, BLACK)
        self.label2 = self.font.render("Settings", True, BLACK)
        self.label3 = self.font.render("Quit", True, BLACK)

    def menu_option_select(self, index):
        self.label0 = self.font.render("New Game", True, BLACK)
        self.label1 = self.font.render("Highscores", True, BLACK)
        self.label2 = self.font.render("Settings", True, BLACK)
        self.label3 = self.font.render("Quit", True, BLACK)

        if index == 0:
            self.label0 = self.font.render("> New Game", True, RED)
        elif index == 1:
            self.label1 = self.font.render("> Highscores", True, RED)
        elif index == 2:
            self.label2 = self.font.render("> Settings", True, RED)
        elif index == 3:
            self.label3 = self.font.render("> Quit", True, RED)

        gameDisplay.fill(WHITE)
        gameDisplay.blit(self.label0, (100, 520))
        gameDisplay.blit(self.label1, (100, 570))
        gameDisplay.blit(self.label2, (100, 620))
        gameDisplay.blit(self.label3, (100, 670))

    # show - shows menu with buttons, returns selected options where 0 is start game and 2 is settings
    def show(self):
        index = 0
        self.menu_option_select(index)
        music = True
        level = 0
        ship = 0

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if index < 3:
                        index += 1
                        self.menu_option_select(index)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if index > 0:
                        index -= 1
                        self.menu_option_select(index)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # other menu choices
                    if index == 0:
                        ship, level = (1, 1)# after start there should be a function() -> tuple with ship and level
                        return ship, level, music
                    if index == 1:
                        music = settings_menu_show()
                        self.menu_option_select(index)

                    # TODO: add showing highscores
                    if index == 3:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            clock.tick(FPS)


# SpaceInvaders - main program class, responding to events and game loop
class SpaceInvaders:
    def __init__(self):
        self.screen = gameDisplay
        self.menu = MainMenu()

    # main loop
    # def gameLoop:
    # while True:

    # main function
    def main(self):
        while True:
            self.menu.show()
            # menu


if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()
