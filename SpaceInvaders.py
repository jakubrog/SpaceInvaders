import pygame
import sys
from os.path import abspath, dirname

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + '/images/'
FONT_PATH = BASE_PATH + '/fonts/'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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


# TODO: loading images into IMAGES
# TODO: create images
# TODO: create and implement main menu layout


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


class MainMenu:
    def __init__(self):
        gameDisplay.fill(WHITE)
        self.font = pygame.font.Font(FONT, 25)
        self.index = 0
        self.label0 = self.font.render("New Game", True, RED)
        self.label1 = self.font.render("Highscores", True, BLACK)
        self.label2 = self.font.render("Settings", True, BLACK)
        self.label3 = self.font.render("Quit", True, BLACK)

    def option_select(self, index):
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
        self.option_select(index)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if index < 3:
                        index += 1
                        self.option_select(index)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if index > 0:
                        index -= 1
                        self.option_select(index)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if index == 3:
                        pygame.quit()
                        sys.exit()
                    else:
                        return index

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
            action = self.menu.show()
        
            if action == 1:
                continue  # TODO: move to second screen
            if action == 2:
                continue  # TODO: move to highscores
            if action == 3:
                continue  # TODO: move to settings


if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()
