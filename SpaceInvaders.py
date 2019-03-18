from pygame import *
from os.path import abspath, dirname

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + '/images/'

white = (255,255,255)

# names of created images
IMG_NAMES = ['filename']

DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 1000

init()   # initialize all imported pygame modules
gameDisplay = display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # Initialize a window for display
display.set_caption("Space Invaders")

# TODO: loading images into IMAGES
# TODO: create images
# TODO: create and implement main menu layout


# single enemy ship
class Enemy(sprite.Sprite):  # sprite - base class for visible game objects
    def __init__(self, row, column, image_filename, power):
        # Call the parent class (Sprite) constructor
        sprite.Sprite.__init__(self)
        # self.image = IMAGES['image_filename']
        self.row = row
        self.column = column
        self.health = Health()
        self.power = power


# Block or a group of enemies, it's responsible for changing position of each enemy and select their specification
class GroupOfEnemies(sprite.Group):
    def __init__(self, row, column):
        sprite.Group.__init__(self)
        # self.image = IMAGES['filename']
        self.row = row
        self.column = column


# Bullet - display and keep information about shot bullet
# direction in constructor depends on who attack
class Bullet(sprite.Sprite):
    def __init__(self, x_position, y_position, direction, speed, power):  # direction -
        sprite.Sprite.__init__(self)
        # self.image = IMAGES['filename']
        self.speed = speed
        self.destruction = power


class Ship(sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = IMAGES['filename']


# Health - displaying HP point and health management
class Health(sprite.Sprite):
    def __init_(self):
        sprite.Sprite.__init__(self)


# MainMenu - whole structure of main menu, including buttons
# class MainMenu:


# SpaceInvaders - main program class, responding to events and game loop
class SpaceInvaders:
    def __init__(self):
        self.screen = gameDisplay
    # def mainMenu:

    # main loop
    # def gameLoop:
    # while True:

    # main function
    def main(self):
        gameDisplay.fill(white)
        gameDisplay

# TODO: if need add more classes

# if __name__ == '__main__':
    # game = SpaceInvaders()
    # game.main()
