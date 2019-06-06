import pygame
import sys
from os.path import abspath, dirname
from random import choice

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + '/images/'
FONT_PATH = BASE_PATH + '/fonts/'
MUSIC_PATH = BASE_PATH + '/Sounds/'

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 156, 0)
GRAY = (105, 105, 105)
YELLOW = (244, 226, 2)
GREEN = (0, 255, 0)

# game details
FPS = 60
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768

# other details
UPGRADE_COUNT = 5
ENEMY_DEFAULT_POSITION = 50  # initial value for a new game
ENEMY_MOVE_DOWN = 10  # how much lower in next round
SHOOT_FREQ = 1000

# stats
# MAX_BULLETS = 2 # on the screen at the same time (also BASE_BULLETS)
BASE_HEALTH = 100
BASE_SPEED = 8
BASE_ARMOR = 1
MAX_BULLETS = 4

pygame.init()  # initialize all imported pygame modules
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                      pygame.RESIZABLE)  # Initialize a window for display
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
pygame.mixer.music.load(MUSIC_PATH + "music.mp3")
icon = pygame.image.load(IMAGE_PATH + 'icon.png')
pygame.display.set_icon(icon)

global_hslist = []
DIFFICULTIES = ['Easy', 'Medium', 'Hard']
SHIP_NAMES = ['Ship1', 'Ship2', 'Ship3']

FONT = FONT_PATH + 'Goodtimes.ttf'  # basic font

# names of created IMAGES
IMG_NAMES = ['ship_1', 'bullet_1', 'enemy1_1', 'enemy2_1', 'enemy3_1', ]
MAPS_NAMES = ['map3', 'map2', 'map1', 'map0']

IMAGES = {name: pygame.image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha()
          for name in IMG_NAMES}

MAPS = {name: pygame.image.load(IMAGE_PATH + '/maps/' + '{}.png'.format(name)).convert_alpha() for name in MAPS_NAMES}


# --------------------Sprites-------------------


# main character
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global BASE_SPEED
        self.image = IMAGES['ship_1']
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(topleft=(DISPLAY_WIDTH / 2 - 35, DISPLAY_HEIGHT - 80))
        self.speed = BASE_SPEED
        self.health = Health()

    def update(self, keys, *args):
        gameDisplay.blit(self.image, self.rect)
        if keys[pygame.K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < DISPLAY_WIDTH - 80:
            self.rect.x += self.speed
        self.health.update()

    def shoot(self, bullets):
        if len(bullets) < MAX_BULLETS:  # max two bullets on screen at the same time
            left_bullet = Bullet(self.rect.x + 3, self.rect.y + 10, -1, 15, 'bullet_1')
            right_bullet = Bullet(self.rect.x + 57, self.rect.y + 10, -1, 15, 'bullet_1')
            # self.sounds['shoot'].play()
            bullets.add(left_bullet)
            bullets.add(right_bullet)
        return bullets

    def hit(self, power):
        global BASE_ARMOR
        dmg = power + 1
        dmg *= 10
        dmg -= 2 * BASE_ARMOR
        self.health.hp -= dmg


# single enemy ship
class Enemy(pygame.sprite.Sprite):  # sprite - base class for visible game objects
    def __init__(self, row, column):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # self.image = IMAGES['image_filename']
        self.row = row
        self.column = column
        self.index = 0
        self.images = []
        self.load_images()
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    # setting proper image to ship
    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def load_images(self):
        images = {0: ['1_1', '1_1'],
                  1: ['2_1', '2_1'],
                  2: ['2_1', '2_1'],
                  3: ['3_1', '3_1'],
                  4: ['3_1', '3_1'],
                  }

        img1, img2 = (IMAGES['enemy{}'.format(img_num)] for img_num in images[self.row % 4])

        self.images.append(pygame.transform.scale(img1, (70, 60)))
        self.images.append(pygame.transform.scale(img2, (70, 60)))

    def update(self, *args):
        game.screen.blit(self.image, self.rect)


# Block or a group of enemies, it's responsible for changing position of each enemy and select their specification
class GroupOfEnemies(pygame.sprite.Group):
    def __init__(self, rows, columns, speed):
        pygame.sprite.Group.__init__(self)
        self.enemies = [[None] * columns for _ in range(rows)]

        self.columns = columns
        self.rows = rows

        if speed > 5:
            self.x_speed = 40
            self.y_speed = 5
        else:
            self.x_speed = 20 + (speed - 2) * 2
            self.y_speed = 3

        self.leftMoves = 30
        self.rightMoves = 30  # how much is moving to one of sides
        self.moveNumber = 15
        self.leftAddMove = 0
        self.rightAddMove = 0

        self.moveTime = 1500 / (speed + 1)
        self.direction = 1  # if direction is 1 then enemy is going to right
        self.timer = pygame.time.get_ticks()

        self._aliveColumns = list(range(columns))
        self._leftAliveColumn = 0
        self._rightAliveColumn = columns - 1

    def update(self, current_time):
        if current_time - self.timer > self.moveTime:
            x_max, x_min, y_max = self.get_max_and_min()
            self.direction = choice([-1, 1])
            if self.direction == 1 and x_max + self.x_speed < DISPLAY_WIDTH:
                self.direction = 1
            elif x_min - self.x_speed > 0:
                self.direction = -1
            else:
                self.direction *= (-1)

            for enemy in self:
                enemy.rect.y += self.y_speed
                enemy.rect.x += self.direction * self.x_speed
                enemy.toggle_image()

            self.timer = pygame.time.get_ticks()

    #  finding edges enemies (to make more movement)
    def get_max_and_min(self):
        x_max = 0
        x_min = DISPLAY_WIDTH
        y_max = 0
        for enemy in self:
            if enemy.rect.x > x_max:
                x_max = enemy.rect.x
            elif enemy.rect.x < x_min:
                x_min = enemy.rect.x
            if enemy.rect.y > y_max:
                y_max = enemy.rect.y
        return x_max + 70, x_min, y_max

    def add_internal(self, *sprites):
        super(GroupOfEnemies, self).add_internal(*sprites)
        for s in sprites:
            self.enemies[s.row][s.column] = s

    def remove_internal(self, *sprites):
        super(GroupOfEnemies, self).remove_internal(*sprites)
        for s in sprites:
            self.kill(s)
        self.update_speed()

    def is_column_dead(self, column):
        return not any(self.enemies[row][column] for row in range(self.rows))

    def random_bottom(self):
        col = choice(self._aliveColumns)
        col_enemies = (self.enemies[row - 1][col]
                       for row in range(self.rows, 0, -1))
        return next((en for en in col_enemies if en is not None), None)

    def update_speed(self):
        if len(self) == 1:
            self.moveTime = 200
        elif len(self) <= 10:
            self.moveTime = 400

    def kill(self, enemy):
        self.enemies[enemy.row][enemy.column] = None
        is_column_dead = self.is_column_dead(enemy.column)
        if is_column_dead:
            self._aliveColumns.remove(enemy.column)

        if enemy.column == self._rightAliveColumn:
            while self._rightAliveColumn > 0 and is_column_dead:
                self._rightAliveColumn -= 1
                self.rightAddMove += 5
                is_column_dead = self.is_column_dead(self._rightAliveColumn)

        elif enemy.column == self._leftAliveColumn:
            while self._leftAliveColumn < self.columns and is_column_dead:
                self._leftAliveColumn += 1
                self.leftAddMove += 5
                is_column_dead = self.is_column_dead(self._leftAliveColumn)


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


# Health - displaying HP point and health management
class Health(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global BASE_HEALTH
        self.hp = BASE_HEALTH

    def update(self):
        font = pygame.font.Font(FONT, 20)
        health_label = font.render("Hp:  " + str(self.hp), True, RED)
        gameDisplay.blit(health_label, (DISPLAY_WIDTH - 120, 10))

    def is_alive(self):
        return self.hp > 0


# ---------------------- Menu functions----------------------


# not completed
class Shop:
    upgrades = (1, 1, 1, 1)
    count = UPGRADE_COUNT

    def __init__(self):
        self.background = pygame.image.load(IMAGE_PATH + "shop.png").convert()
        self.background = pygame.transform.scale(self.background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        gameDisplay.blit(self.background, (0, 0))

        self.font = pygame.font.Font(FONT, 25)
        self.index = 0
        self.label0 = self.font.render("HP", True, RED)
        self.label1 = self.font.render("ARMOR", True, WHITE)
        self.label2 = self.font.render("SPEED", True, WHITE)
        self.label3 = self.font.render("BULLETS", True, WHITE)
        self.label4 = self.font.render("Continue", True, ORANGE)

        self.stat0 = self.font.render(str(self.upgrades[0]), True, YELLOW)
        self.stat1 = self.font.render(str(self.upgrades[1]), True, WHITE)
        self.stat2 = self.font.render(str(self.upgrades[2]), True, WHITE)
        self.stat3 = self.font.render(str(self.upgrades[3]), True, WHITE)

        self.count_label = pygame.font.Font(FONT, 70).render(str(self.count), True, WHITE)

    def shop_upgrade_select(self, index):
        self.label0 = self.font.render("HP", True, WHITE)
        self.label1 = self.font.render("ARMOR", True, WHITE)
        self.label2 = self.font.render("SPEED", True, WHITE)
        self.label3 = self.font.render("BULLETS", True, WHITE)
        self.label4 = self.font.render("Continue", True, ORANGE)

        self.stat0 = self.font.render(str(self.upgrades[0]), True, WHITE)
        self.stat1 = self.font.render(str(self.upgrades[1]), True, WHITE)
        self.stat2 = self.font.render(str(self.upgrades[2]), True, WHITE)
        self.stat3 = self.font.render(str(self.upgrades[3]), True, WHITE)

        self.count_label = pygame.font.Font(FONT, 70).render(str(self.count), True, WHITE)

        if index == 0:
            self.label0 = self.font.render("> HP", True, RED)
            self.stat0 = self.font.render(str(self.upgrades[0]) + " +", True, YELLOW)
        elif index == 1:
            self.label1 = self.font.render("> ARMOR", True, RED)
            self.stat1 = self.font.render(str(self.upgrades[1]) + " +", True, YELLOW)
        elif index == 2:
            self.label2 = self.font.render("> SPEED", True, RED)
            self.stat2 = self.font.render(str(self.upgrades[2]) + " +", True, YELLOW)
        elif index == 3:
            self.label3 = self.font.render("> BULLETS", True, RED)
            self.stat3 = self.font.render(str(self.upgrades[3]) + " +", True, YELLOW)
        elif index == 4:
            self.label4 = self.font.render("Continue", True, RED)

        gameDisplay.blit(self.background, (0, 0))

        gameDisplay.blit(self.label0, (100, 420))
        gameDisplay.blit(self.label1, (100, 470))
        gameDisplay.blit(self.label2, (100, 520))
        gameDisplay.blit(self.label3, (100, 570))
        gameDisplay.blit(self.label4, (150, 620))

        gameDisplay.blit(self.stat0, (300, 420))
        gameDisplay.blit(self.stat1, (300, 470))
        gameDisplay.blit(self.stat2, (300, 520))
        gameDisplay.blit(self.stat3, (300, 570))

        gameDisplay.blit(self.count_label, (600, 500))

    def add_stat(self, stat):
        curr_hp = self.upgrades[0]
        curr_armor = self.upgrades[1]
        curr_speed = self.upgrades[2]
        curr_bullets = self.upgrades[3]

        if stat == 0:
            curr_hp += 1
        elif stat == 1:
            curr_armor += 1
        elif stat == 2:
            curr_speed += 1
        elif stat == 3:
            curr_bullets += 1

        self.upgrades = curr_hp, curr_armor, curr_speed, curr_bullets

    # TODO: move upgrades somewhere else
    def get_upgrade(self, up_type):
        if up_type == 0:
            return self.upgrades[0]
        elif up_type == 1:
            return self.upgrades[1]
        elif up_type == 2:
            return self.upgrades[2]
        elif up_type == 3:
            return self.upgrades[3]

    def reset(self):
        self.upgrades = (1, 1, 1, 1)

    def apply_upgrades(self):
        global BASE_HEALTH
        global BASE_ARMOR
        global BASE_SPEED
        global MAX_BULLETS

        BASE_HEALTH = 90 + 10 * self.get_upgrade(0)
        BASE_ARMOR = -2 + 2 * self.get_upgrade(1)
        BASE_SPEED = 8 + 3 * self.get_upgrade(2)
        MAX_BULLETS = 2 * self.get_upgrade(3)


    def show(self):
        index = 0
        self.count = UPGRADE_COUNT
        self.shop_upgrade_select(index)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if index < 4:
                        index += 1
                        self.shop_upgrade_select(index)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if index > 0:
                        index -= 1
                        self.shop_upgrade_select(index)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # other menu choices
                    if index in {0, 1, 2, 3} and self.count > 0:
                        self.add_stat(index)
                        self.count -= 1
                        self.shop_upgrade_select(index)

                    if index == 4:
                        gameDisplay.blit(self.background, (0, 0))
                        self.apply_upgrades()
                        # ship, level = (1, 1)
                        return  # curr_hp, curr_dmg, curr_speed, curr_bullets

            pygame.display.update()
            clock.tick(FPS)


# highscores
class Highscore:
    def __init__(self):
        file = open("highscores.txt", "r")
        self.hslist = []

        f = file.readlines()
        self.file_data = []
        for i in range(10):
            self.file_data.append(f[i])

        self.convert_from_file()
        file.close()

    # dodanie wyniku do listy
    def add(self, name, score):
        if score > self.hslist[9][1]:
            self.hslist.append((name, score))
            self.sort_hslist()
            self.hslist = self.hslist[0:-1]

    # przerobienie danych z pliku na listę wyników
    def convert_from_file(self):
        for i in range(10):
            tmp = self.file_data[i]
            if tmp[-1] == '\n':
                tmp = tmp[0:-1]
            s = tmp.split()
            name_segments = s[0:-1]
            name = " ".join(name_segments)
            score = int(s[-1])
            self.hslist.append((name, score))

        self.sort_hslist()

    # sortowanie po wynikach
    def sort_hslist(self):
        def take_sec(tup):
            return tup[1]

        self.hslist.sort(key=take_sec, reverse=True)

    # dostęp do listy dla wyświetlania wyników
    def set_hslist(self):
        global global_hslist
        global_hslist = self.hslist

    # zapis do pliku
    def save_to_file(self):
        file = open("highscores.txt", "w")
        for i in range(10):
            tmp = self.hslist[i]
            file.write(" ".join((tmp[0], str(tmp[1]), '\n')))
        file.close()


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

    # [row, ship, diff]
    index2 = [0, 0, 0]

    label20 = font.render("Start", True, RED)
    label21 = font.render("Ship", True, WHITE)
    label22 = font.render("Difficulty", True, WHITE)

    ship_select = font.render(SHIP_NAMES[index2[1]], True, GRAY)
    diff_select = font.render(DIFFICULTIES[index2[2]], True, GRAY)

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
                if index2[0] < 2:
                    index2[0] += 1
                    del sel
                    sel = menu_select(index2[0])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if index2[0] > 0:
                    index2[0] -= 1
                    del sel
                    sel = menu_select(index2[0])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if index2[0] == 1 and index2[1] > 0:
                    index2[1] -= 1
                if index2[0] == 2 and index2[2] > 0:
                    index2[2] -= 1
                del sel
                sel = menu_select(index2[0])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if index2[0] == 1 and index2[1] < 2:
                    index2[1] += 1
                if index2[0] == 2 and index2[2] < 2:
                    index2[2] += 1
                del sel
                sel = menu_select(index2[0])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if index2[0] == 0:
                    return index2[1] + 1, index2[2] + 1
            # back
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                gameDisplay.fill(BLACK)
                return -1, -1

        if sel:
            label20 = font.render("Start", True, sel[0])
            label21 = font.render("Ship", True, sel[1])
            label22 = font.render("Difficulty", True, sel[2])

            ship_select = font.render(SHIP_NAMES[index2[1]], True, sel[3])
            diff_select = font.render(DIFFICULTIES[index2[2]], True, sel[4])
        del sel

        pygame.display.update()
        clock.tick(FPS)


class MainMenu:
    def __init__(self):
        self.background = pygame.image.load(IMAGE_PATH + "menu.png").convert()
        self.background = pygame.transform.scale(self.background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        gameDisplay.blit(self.background, (0, 0))
        self.font = pygame.font.Font(FONT, 25)
        self.index = 1
        self.label0 = self.font.render("New Game", True, RED)
        self.label1 = self.font.render("Highscores", True, WHITE)
        self.label2 = self.font.render("Settings", True, WHITE)
        self.label3 = self.font.render("Quit", True, WHITE)
        self.music = True
        pygame.mixer.music.play(-1)

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
                        ship, diff = newgame_menu_show(self.background)
                        if diff != (-1):
                            return diff
                        self.menu_option_select(index)

                        # highscores
                    if index == 1:
                        self.highscore_show()
                        self.menu_option_select(index)

                    if index == 2:
                        self.settings_menu_show()
                        self.menu_option_select(index)

                    if index == 3:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            clock.tick(FPS)

    # showing highscores
    def highscore_show(self):
        global global_hslist
        font = pygame.font.Font(FONT, 25)
        back_font = pygame.font.Font(FONT, 17)
        name_labels = []
        score_labels = []

        for i in range(10):
            name_labels.append(font.render(global_hslist[i][0], True, WHITE))
            score_labels.append(font.render(str(global_hslist[i][1]), True, WHITE))
        back_label = back_font.render("[ESC] - get back", True, ORANGE)

        while True:
            gameDisplay.blit(self.background, (0, 0))
            for i in range(10):
                gameDisplay.blit(name_labels[i], (100, 300 + 35 * i))
                gameDisplay.blit(score_labels[i], (600, 300 + 35 * i))
            gameDisplay.blit(back_label, (10, 730))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                    gameDisplay.fill(BLACK)
                    return

            pygame.display.update()
            clock.tick(FPS)

    def settings_menu_show(self):
        font = pygame.font.Font(FONT, 35)
        help_font = pygame.font.Font(FONT, 17)
        about_font = pygame.font.Font(FONT, 25)

        music_label = font.render("Music", True, RED)
        if self.music:
            music_select = font.render("< ON >", True, YELLOW)
        else:
            music_select = font.render("< OFF >", True, YELLOW)

        about = about_font.render("Created by Jakub Rog and Jan Makowiecki in 2019.", True, WHITE)
        help_label = help_font.render("[ESC] - get back", True, ORANGE)

        while True:
            gameDisplay.blit(self.background, (0, 0))
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
                        if self.music:
                            music_select = font.render("< OFF >", True, YELLOW)
                        else:
                            music_select = font.render("< ON >", True, YELLOW)
                        self.music = not self.music

                    elif event.key == pygame.K_q or event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                        gameDisplay.fill(BLACK)
                        if self.music:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                        return

            pygame.display.update()
            clock.tick(FPS)

    def get_music_setting(self):
        return self.music


# -------------------------Game-------------------------
# SpaceInvaders - main program class, responding to events and game loop
class SpaceInvaders:
    def __init__(self):
        global global_hslist
        self.screen = gameDisplay
        self.highscores = Highscore()
        self.highscores.set_hslist()
        self.menu = MainMenu()
        self.shop = Shop()

        # init objects
        self.ship = Ship()
        self.shipGroup = pygame.sprite.Group(self.ship)
        self.bullets = pygame.sprite.Group()
        self.enemiesRows = 4
        self.enemiesCols = 9
        self.current_lvl = 0
        self.enemies = self.make_enemies()
        self.enemyBullets = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group(self.shipGroup, self.enemies)

        # helpers
        self.enemyPosition = ENEMY_DEFAULT_POSITION  # starting enemies position, increasing each round
        self.gameOver = False
        self.nextRound = False
        self.score = 0
        self.bottom = 300
        self.timer = pygame.time.get_ticks()
        self.enemies_shoot_timer = pygame.time.get_ticks()

        # texts
        self.font = pygame.font.Font(FONT, 85)
        self.scoreFont = pygame.font.Font(FONT, 20)
        self.gameOverText = self.font.render("Game Over", True, RED)

        self.nextRoundText = self.font.render('Next Round', True, WHITE)
        self.scoreText = self.font.render("Score:" + str(self.score), True, GREEN)

    def make_enemies(self):
        enemies = GroupOfEnemies(self.enemiesRows, self.enemiesCols, self.current_lvl)
        for row in range(self.enemiesRows):
            for column in range(self.enemiesCols):
                enemy = Enemy(row, column)
                enemy.rect.x = 80 + (column * 100)

                # setting minimum height of starting position
                lvl_factor = ENEMY_MOVE_DOWN * self.current_lvl
                if lvl_factor > 70:
                    lvl_factor = 70

                enemy.rect.y = ENEMY_DEFAULT_POSITION + (row * 120) + lvl_factor
                enemies.add(enemy)
        return enemies

    def select_map(self):
        index = 0
        maps_no = len(MAPS)

        select_label = pygame.font.Font(FONT, 80).render("SELECT MAP", True, ORANGE)
        right_arrow_label = pygame.font.Font(FONT, 80).render(">", True, GRAY)
        left_arrow_label = pygame.font.Font(FONT, 80).render("<", True, GRAY)
        map_label = pygame.font.Font(FONT, 60)
        pygame.font.Font(FONT, 40).render("SELECT MAP" + str(self.score), True, ORANGE)

        while True:
            map = pygame.transform.scale(MAPS['map' + str(index)], (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            gameDisplay.blit(map, (0, 0))
            gameDisplay.blit(map_label.render('Map ' + str(index + 1), True, RED),
                             (DISPLAY_WIDTH / 2 - 110, DISPLAY_HEIGHT / 2 - 40))

            gameDisplay.blit(select_label, (200, 70))
            gameDisplay.blit(left_arrow_label, (DISPLAY_WIDTH / 2 - 240, DISPLAY_HEIGHT / 2 - 50))
            gameDisplay.blit(right_arrow_label, (DISPLAY_WIDTH / 2 + 190, DISPLAY_HEIGHT / 2 - 50))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT] and index > 0:
                        index -= 1
                    if event.key in [pygame.K_RIGHT] and index < maps_no - 1:
                        index += 1
                    if event.key in [pygame.K_RETURN]:
                        return pygame.transform.scale(MAPS['map' + str(index)], (DISPLAY_WIDTH, DISPLAY_HEIGHT))

            clock.tick(FPS)

    def make_enemies_shoot(self):
        freq = SHOOT_FREQ / (self.current_lvl + 1)
        if freq < 200:
            freq = 200
        if (self.timer - self.enemies_shoot_timer) > freq and self.enemies:
            enemy = self.enemies.random_bottom()
            self.enemyBullets.add(Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 15, 'bullet_1'))
            self.allSprites.add(self.enemyBullets)
            self.enemies_shoot_timer = pygame.time.get_ticks()

    def calculate_score(self, row):
        self.score += + 10 * (self.enemiesRows - row)

    def check_collisions(self):
        pygame.sprite.groupcollide(self.bullets, self.enemyBullets, True, True)

        for enemy in pygame.sprite.groupcollide(self.enemies, self.bullets, True, True).keys():
            self.calculate_score(enemy.row)
            if not self.enemies.sprites():
                self.nextRound = True
                return

        if pygame.sprite.groupcollide(self.shipGroup, self.enemyBullets, True, True).keys():
            self.ship.hit(self.current_lvl)
            self.shipGroup.add(self.ship)
            self.allSprites.add(self.shipGroup)

            if not self.ship.health.is_alive():
                self.gameOver = True

        if pygame.sprite.groupcollide(self.shipGroup, self.enemies, True, True).keys():
            self.gameOver = True

    def reset(self):
        global BASE_HEALTH, BASE_SPEED, BASE_ARMOR, MAX_BULLETS
        BASE_HEALTH = 100
        BASE_SPEED = 8
        BASE_ARMOR = 1
        MAX_BULLETS = 4

        self.ship = Ship()
        self.shipGroup = pygame.sprite.Group(self.ship)
        self.bullets = pygame.sprite.Group()
        self.enemies = self.make_enemies()
        self.enemyBullets = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group(self.shipGroup, self.enemies)

    def main(self):
        self.current_lvl = self.menu.show()
        map = self.select_map()

        # upgrades = (1,1,1,1)
        while True:
            # game over
            if self.gameOver:
                self.gameOver = False

                s = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
                s.fill((255, 255, 255, 80))
                gameDisplay.blit(s, (0, 0))

                gameDisplay.blit(self.gameOverText, (DISPLAY_WIDTH / 4 - 75, DISPLAY_HEIGHT / 4))
                score_label = pygame.font.Font(FONT, 40).render("Your Score: " + str(self.score), True, ORANGE)
                gameDisplay.blit(score_label, (DISPLAY_WIDTH / 4 + 55, DISPLAY_HEIGHT / 4 + 150))

                pygame.display.update()

                # score input
                input_box = pygame.Rect((DISPLAY_WIDTH / 4 + 50, DISPLAY_HEIGHT / 4 + 220), (470, 50))

                name = ''
                name_length = len(name)
                name_label = pygame.font.Font(FONT, 40).render(name, True, WHITE)
                submitted = False
                pygame.draw.rect(self.screen, GREEN, input_box)

                while not submitted:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                submitted = True

                            elif event.key == pygame.K_BACKSPACE:
                                name = name[:-1]
                                name_length = len(name)

                            else:
                                if name_length < 12:
                                    name += event.unicode
                                    name_length = len(name)

                    name_label = pygame.font.Font(FONT, 40).render(name, True, WHITE)
                    pygame.draw.rect(self.screen, GREEN, input_box)
                    gameDisplay.blit(name_label, (DISPLAY_WIDTH / 4 + 55, DISPLAY_HEIGHT / 4 + 220))
                    pygame.display.update()

                self.highscores.add(name, self.score)
                self.highscores.save_to_file()

                name = ''
                name_length = len(name)

                self.score = 0
                self.current_lvl = 0
                self.reset()
                self.shop.reset()

                pygame.time.wait(1000)
                self.current_lvl = self.menu.show()

            if self.nextRound:
                gameDisplay.blit(self.nextRoundText, (DISPLAY_WIDTH / 4 - 100, DISPLAY_HEIGHT / 4))
                pygame.display.update()
                pygame.time.wait(2000)
                self.current_lvl += 1
                self.reset()
                self.nextRound = False
                self.shop.show()

            gameDisplay.blit(map, (0, 0))  # map load
            self.scoreText = self.scoreFont.render("Score:  " + str(self.score), True, GREEN)
            gameDisplay.blit(self.scoreText, (10, 10))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullets = self.ship.shoot(self.bullets)
                        self.allSprites.add(self.bullets)

            self.check_collisions()
            self.allSprites.update(keys, pygame.time.get_ticks())
            self.enemies.update(pygame.time.get_ticks())
            self.timer = pygame.time.get_ticks()
            self.make_enemies_shoot()
            pygame.display.update()
            clock.tick(FPS)


if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()
