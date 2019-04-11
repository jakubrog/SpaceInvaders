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
YELLOW = (244,226,2)

# names of created images
IMG_NAMES = ['ship_1', 'bullet_1']

FPS = 15

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768

FONT = FONT_PATH + 'Minecraftia.ttf'

pygame.init()  # initialize all imported pygame modules
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # Initialize a window for display
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

IMAGES = {name: pygame.image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha()
          for name in IMG_NAMES}


# TODO: shrink images to reduce time of creating objects
# TODO: ENEMIES: shoots, movement,
# TODO: collisions

# single enemy ship
class Enemy(pygame.sprite.Sprite):  # sprite - base class for visible game objects
    def __init__(self, row, column):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # self.image = IMAGES['image_filename']
        self.row = row
        self.column = column


# Block or a group of enemies, it's responsible for changing position of each enemy and select their specification
class GroupOfEnemies(pygame.sprite.Group):
    def __init__(self, rows, columns):
        pygame.sprite.Group.__init__(self)
        # self.image = IMAGES['filename']
        


# Bullet - display and keep information about shot bullet
# direction in constructor depends on who attack
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, direction, speed, image_name):  # direction -
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES[image_name]
        self.image = self.image = pygame.transform.scale(self.image, (10, 7))
        self.rect = self.image.get_rect(topleft=(x_position, y_position))
        self.speed = speed
        self.direction = direction

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        if self.rect.y < 0 or self.rect.y > DISPLAY_HEIGHT:
            self.kill()


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES['ship_1']
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(topleft=(DISPLAY_WIDTH / 2 - 35, DISPLAY_HEIGHT - 80))
        self.speed = 5

    def update(self, keys):
        gameDisplay.blit(self.image, self.rect)
        if keys[pygame.K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < DISPLAY_WIDTH - 80:
            self.rect.x += self.speed

    def shoot(self, bullets):
        if len(bullets) < 2:  # max two bullets on screen at the same time
            left_bullet = Bullet(self.rect.x + 3, self.rect.y + 10, -1, 15, 'bullet_1')
            right_bullet = Bullet(self.rect.x + 57, self.rect.y + 10, -1, 15, 'bullet_1')
            # self.sounds['shoot'].play()
            bullets.add(left_bullet)
            bullets.add(right_bullet)
        return bullets


# Health - displaying HP point and health management
class Health(pygame.sprite.Sprite):
    def __init_(self):
        pygame.sprite.Sprite.__init__(self)


def settings_menu_show(background):
    font = pygame.font.Font(FONT, 35)
    help_font = pygame.font.Font(FONT, 17)
    about_font = pygame.font.Font(FONT, 25)

    music_label = font.render("Music", True, RED)
    music_select = font.render("< ON >", True, YELLOW)

    music_label = font.render("Sounds", True, GRAY)
    music_select = font.render("< ON >", True, GRAY)



    about = about_font.render("Created by Jakub Rog and Jan Makowiecki in 2019.", True, WHITE)
    help_label = help_font.render("[ESC] - get back", True, ORANGE)

    music = True

    while True:
        gameDisplay.blit(background, (0, 0))
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
                        music_select = font.render("< OFF >", True, YELLOW)
                    else:
                        music_select = font.render("< ON >", True, YELLOW)
                    music = not music

                elif event.key == pygame.K_q or event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                    gameDisplay.fill(BLACK)
                    return music

        pygame.display.update()
        clock.tick(FPS)

#not completed
class Shop:
    def _init_(self):
        self.background = pygame.image.load(IMAGE_PATH + "shop.png").convert()
        self.background = pygame.transform.scale(self.background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        gameDisplay.blit(self.background, (0, 0))
        self.font = pygame.font.Font(FONT, 25)
        self.index = 0
        self.label0 = self.font.render("HP", True, RED)
        self.label1 = self.font.render("DMG", True, WHITE)
        self.label2 = self.font.render("SPEED", True, WHITE)
        self.label3 = self.font.render("BULLETS", True, WHITE)
        self.label4 = self.font.render("Continue", True, ORANGE)

    def shop_upgrade_select(self, index):
        self.label0 = self.font.render("HP", True, WHITE)
        self.label1 = self.font.render("DMG", True, WHITE)
        self.label2 = self.font.render("SPEED", True, WHITE)
        self.label3 = self.font.render("BULLETS", True, WHITE)

        if index == 0:
            self.label0 = self.font.render("> HP", True, RED)
        elif index == 1:
            self.label1 = self.font.render("> DMG", True, RED)
        elif index == 2:
            self.label2 = self.font.render("> SPEED", True, RED)
        elif index == 3:
            self.label3 = self.font.render("> BULLETS", True, RED)
        elif index == 4:
            self.label4 = self.font.render("Continue", True, RED)

        gameDisplay.blit(self.background, (0, 0))
        gameDisplay.blit(self.label0, (100, 520))
        gameDisplay.blit(self.label1, (100, 570))
        gameDisplay.blit(self.label2, (100, 620))
        gameDisplay.blit(self.label3, (100, 670))

    def show(self, current_upgrades):
        index = 0
        self.shop_upgrade_select(index)
        curr_hp = current_upgrades[0]
        curr_dmg = current_upgrades[1]
        curr_speed = current_upgrades[2]
        curr_bullets = current_upgrades[3]


        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if index < 3:
                        index += 1
                        self.shop_upgrade_select(index)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if index > 0:
                        index -= 1
                        self.shop_upgrade_select(index)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # other menu choices
                    if index == 0:
                        curr_hp += 1

                    if index == 1:
                        curr_dmg += 1

                    if index == 2:
                        curr_speed += 1

                    if index == 3:
                        curr_bullets += 1

                    if index == 4:
                        gameDisplay.blit(self.background, (0, 0))
                        ship, level = (1, 1)
                        return curr_hp, curr_dmg, curr_speed, curr_bullets
                

            pygame.display.update()
            clock.tick(FPS)

# new feature 
def newgame_menu_show(background):
    def menu_select(index2):
        if index2 == 0:
            return RED, WHITE, WHITE, GRAY, GRAY
        if index2 == 1:
            return WHITE, RED, WHITE, YELLOW, GRAY
        if index2 == 2:
            return WHITE, WHITE, RED, GRAY, YELLOW

    font = pygame.font.Font(FONT, 25)
    back_font = pygame.font.Font(FONT, 17)
    index2 = 0
    
    music = True
    ship = 1
    diff = 1

    label20 = font.render("Start", True, RED)
    label21 = font.render("Ship", True, WHITE)
    label22 = font.render("Difficulty", True, WHITE)

    ship_select = font.render("< Ship1 >", True, GRAY)
    diff_select = font.render("< Easy >", True, GRAY)

    back_label = back_font.render("[ESC] - get back", True, ORANGE)


    while True:
        gameDisplay.blit(background, (0, 0))

        gameDisplay.blit(label20, (100, 520))
        gameDisplay.blit(label21, (100, 570))
        gameDisplay.blit(label22, (100, 620))

        gameDisplay.blit(ship_select, (400, 570))
        gameDisplay.blit(diff_select, (400, 620))
        gameDisplay.blit(back_label, (10, 730))

        sel = ()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if index2 < 2:
                    index2 += 1
                    del sel
                    sel = menu_select(index2)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if index2 > 0:
                    index2 -= 1
                    del sel
                    sel = menu_select(index2)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if index2 == 0:
                    gameDisplay.fill(YELLOW)
                
            #back
            if event.key == pygame.K_q or event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                gameDisplay.fill(BLACK)
                return music

        if sel:
            label20 = font.render("Start", True, sel[0])
            label21 = font.render("Ship", True, sel[1])
            label22 = font.render("Difficulty", True, sel[2])

            ship_select = font.render("< Ship1 >", True, sel[3])
            diff_select = font.render("< Easy >", True, sel[4])
        del sel

        pygame.display.update()
        clock.tick(FPS)

class MainMenu:
    def __init__(self):
        self.background = pygame.image.load(IMAGE_PATH + "menu.png").convert()
        self.background = pygame.transform.scale(self.background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        gameDisplay.blit(self.background, (0, 0))
        self.font = pygame.font.Font(FONT, 25)
        self.index = 0
        self.label0 = self.font.render("New Game", True, RED)
        self.label1 = self.font.render("Highscores", True, WHITE)
        self.label2 = self.font.render("Settings", True, WHITE)
        self.label3 = self.font.render("Quit", True, WHITE)

    def menu_option_select(self, index):
        self.label0 = self.font.render("New Game", True, WHITE)
        self.label1 = self.font.render("Highscores", True, WHITE)
        self.label2 = self.font.render("Settings", True, WHITE)
        self.label3 = self.font.render("Quit", True, WHITE)

        if index == 0:
            self.label0 = self.font.render("> New Game", True, RED)
        elif index == 1:
            self.label1 = self.font.render("> Highscores", True, RED)
        elif index == 2:
            self.label2 = self.font.render("> Settings", True, RED)
        elif index == 3:
            self.label3 = self.font.render("> Quit", True, RED)

        gameDisplay.blit(self.background, (0, 0))
        gameDisplay.blit(self.label0, (100, 520))
        gameDisplay.blit(self.label1, (100, 570))
        gameDisplay.blit(self.label2, (100, 620))
        gameDisplay.blit(self.label3, (100, 670))

    # show - shows menu with buttons, returns selected options where 0 is start game and 2 is settings
    def show(self):
        index = 0
        self.menu_option_select(index)
        music = True
        #level = 0
        #ship = 0

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
                         # after start there should be a function() -> tuple with ship and level
                        return ship, level, music
                    
                    if index == 1:
                        music = newgame_menu_show(self.background)
                        self.menu_option_select(index)

                    if index == 2:
                        music = settings_menu_show(self.background)
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
        self.ship = Ship()
        self.allSprites = pygame.sprite.Group(self.ship)  # every item which is on screen should be here
        self.map = pygame.image.load(IMAGE_PATH + 'map1.png')
        self.bullets = pygame.sprite.Group()  # every bullet is here and whole group is in allSpirites

        # self.map = pygame.transform.scale(self.map, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # main loop
    # def gameLoop:
    # while True:

    # main function
    def main(self):
        ship, diff_level, music = self.menu.show()
        while True:
            gameDisplay.blit(self.map, (0, 0))  # map load
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullets = self.ship.shoot(self.bullets)
                        self.allSprites.add(self.bullets)

            self.allSprites.update(keys)  # update every element

            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()