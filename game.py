import sys
import pygame, math, random, time
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# ======================= Variables =======================

gray = (168, 168, 168)
dark_gray = (77, 77, 77)
white = (255, 255, 255)
red = (255, 89, 60)
green = (17, 176, 0)
blue = (66, 135, 245)

font = pygame.font.Font("bin/font/Montserrat.ttf", 20)

bounce = pygame.mixer.Sound("bin/audio/bounce.wav")
bounce.set_volume(0.5)

shoot = pygame.mixer.Sound("bin/audio/shoot.wav")
shoot.set_volume(0.5)

tone = pygame.mixer.Sound("bin/audio/tone.wav")

fps = 120


# =========================================================

class Game:

    def __init__(self):
        self.run = True
        self.screen_width = 1060
        self.screen_height = 798
        self.image = pygame.image.load("bin/sprites/background/background1.png")
        self.image = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.player_scoreboard = 0
        self.enemy_scoreboard = 0

        # all_sprites is used to update and draw all sprites together.
        self.all_sprites = pygame.sprite.Group()

        # for collision detection with enemies.
        self.bullet_group = pygame.sprite.Group()

        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        # for collision detection with walls.
        self.wall_list = pygame.sprite.Group()

        self.tank = Tank()
        self.all_sprites.add(self.tank)
        self.player_group.add(self.tank)

        self.enemy = Enemy()
        self.all_sprites.add(self.enemy)
        self.enemy_group.add(self.enemy)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.bullet_group.add(bullet)
            self.all_sprites.add(bullet)

        # -------------- Walls --------------

        wallx = [0, 0, 1044, 0, 0, 260, 146, 130, 146, 146, 130, 146, 390, 522, 390, 260, 390, 406, 522, 522, 522, 652,
                 652, 782, 914, 782, 782, 914, 914, 914, 652, 652, 782, ]
        wally = [0, 0, 0, 782, 260, 0, 130, 130, 522, 390, 652, 652, 0, 0, 130, 260, 260, 390, 260, 260, 522, 130, 130,
                 0, 0, 260, 390, 390, 522, 652, 522, 652, 522, ]
        wallWidth = [16, 1060, 16, 1060, 130, 16, 130, 16, 130, 130, 16, 130, 16, 16, 148, 146, 16, 132, 16, 130, 16,
                     278, 16, 16, 16, 278, 148, 16, 148, 148, 146, 146, 16, ]
        wallHeight = [798, 16, 798, 16, 16, 130, 16, 408, 16, 16, 146, 16, 146, 146, 16, 16, 408, 16, 146, 16, 260, 16,
                      296, 146, 146, 16, 16, 148, 16, 16, 16, 16, 276]

        for i in range(len(wallx)):
            self.wall = Wall(wallx[i], wally[i], wallWidth[i], wallHeight[i])
            self.wall_list.add(self.wall)
            self.all_sprites.add(self.wall)

    def handle_events(self):

        self.enemy.handle_events()

        # responsible for colliding with walls
        tank_pos = pygame.math.Vector2(self.tank.pos)
        self.tank.handle_events()
        if pygame.sprite.spritecollide(self.tank, self.wall_list, False):
            self.tank.pos = tank_pos
            self.tank.rect.center = round(tank_pos[0]), round(tank_pos[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.tank)
                    self.bullet_group.add(bullet)
                    self.all_sprites.add(bullet)
                    shoot.play()
                if event.key == pygame.K_RETURN:
                    bullet = Bullet(self.enemy)
                    self.bullet_group.add(bullet)
                    self.all_sprites.add(bullet)
                    shoot.play()

    def update(self):
        # Calls `update` methods of all contained sprites.
        self.all_sprites.update()

    def player_score(self):
        font = pygame.font.SysFont("bin/font/Montserrat.ttf", 35)
        tank_score = font.render("PLAYER: " + str(self.player_scoreboard), 1, green)
        tank_score_image = pygame.image.load("bin/sprites/player/player_tank1.png")
        tank_score_image = pygame.transform.scale(tank_score_image, (24, 28))
        self.screen.blit(tank_score, (375, 750))
        self.screen.blit(tank_score_image, (350, 745))

    def enemy_score(self):
        font = pygame.font.SysFont("bin/font/Montserrat.ttf", 35)
        enemy_score = font.render("ENEMY: " + str(self.enemy_scoreboard), 1, red)
        enemy_score_image = pygame.image.load("bin/sprites/enemy/enemy_tank1.png")
        enemy_score_image = pygame.transform.scale(enemy_score_image, (24, 28))
        self.screen.blit(enemy_score, (580, 750))
        self.screen.blit(enemy_score_image, (555, 745))

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        self.all_sprites.draw(self.screen)  # Draw the contained sprites.
        self.player_score()
        self.enemy_score()
        pygame.display.update()


class Tank(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bin/sprites/player/player_tank1.png")
        self.org_image = self.image.copy()

        # A nicer way to set the start pos with `get_rect`.
        self.rect = self.image.get_rect(center=(70, 600))

        self.vel = 3.5

        self.angle = 270  # starts looking right
        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)

        self.hp = 1

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 3
        if keys[pygame.K_RIGHT]:
            self.angle -= 3
        if keys[
            pygame.K_UP] and self.rect.left - 5 > 0 and self.rect.top - 5 > 0 and self.rect.right + 5 < 1060 and self.rect.bottom + 5 < 798:
            self.move(-self.vel)
        if keys[
            pygame.K_DOWN] and self.rect.left - 5 > 0 and self.rect.top - 5 > 0 and self.rect.right + 5 < 1060 and self.rect.bottom + 5 < 798:
            self.move(self.vel)

        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        return self.rect

    def move(self, vel):
        direction = pygame.Vector2(0, vel).rotate(-self.angle)
        self.pos += direction
        self.rect.center = round(self.pos[0]), round(self.pos[1])


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bin/sprites/enemy/enemy_tank1.png")
        self.org_image = self.image.copy()

        self.spawnx = [600, 850, 860]  # spawning x coord
        self.spawny = [70, 200, 700]  # spawning y coord
        self.i = random.randint(0, len(self.spawnx) - 1)

        # A nicer way to set the start pos with `get_rect`.
        self.rect = self.image.get_rect(center=(self.spawnx[self.i], self.spawny[self.i]))

        self.vel = 3
        self.hp = 1

        if self.i == 0:
            self.angle = 180
        elif self.i == 1:
            self.angle = 90
        elif self.i == 2:
            self.angle = 0

        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)
        # self.rect = self.pos

    def handle_events(self):
        '''keys = pygame.key.get_pressed() # Uncomment this for bot control
        if keys[pygame.K_a]:
            self.angle += 3
        if keys[pygame.K_d]:
            self.angle -= 3
        if keys[pygame.K_w]:
            self.move(-3)
        if keys[pygame.K_s]:
            self.move(3)'''

        # -------------- Bot Movement --------------

        if self.i == 0:
            if self.rect.bottom < 230 and self.rect.left > 170:
                self.move(-3)
            if self.rect.bottom == 230 and self.rect.left != 170:
                self.angle -= 90

        if self.i == 1:
            if self.rect.left > 700 and self.rect.bottom < 500:
                self.move(-3)
            if self.rect.left <= 700:
                self.angle += 90

        if self.i == 2:
            if self.rect.top > 450 and self.rect.left > 500:
                self.move(-3)
            if self.rect.top == 450:
                self.angle += 90

        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, vel):
        direction = pygame.Vector2(0, vel).rotate(-self.angle)
        self.pos += direction
        self.rect.center = round(self.pos[0]), round(self.pos[1])


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()

        # Make a wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(dark_gray)  # change wall color

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Bullet(pygame.sprite.Sprite):

    def __init__(self, tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bin/sprites/bullet/bullet.png")
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.rect.centerx + 0  # How much pixels from tank turret on x axis
        self.rect.centery = tank.rect.centery - 0  # How much pixels from tank turret on y axis
        self.angle = tank.angle
        self.pos = pygame.Vector2(self.rect.center)
        self.direction = pygame.Vector2(0, -10).rotate(-self.angle)
        self.hp = 4  # how many times bounces

    def update(self):

        self.pos += self.direction
        self.rect.center = round(self.pos[0]), round(self.pos[1])

        for wall in game.wall_list:
            if self.rect.colliderect(wall.rect):  # if collided
                if self.rect.centerx < wall.rect.left:
                    self.direction.x *= -1
                    self.rect.right = wall.rect.left
                    self.hp -= 1
                    if self.hp == 0:
                        return self.kill()
                    bounce.play()

                if self.rect.centerx > wall.rect.right:
                    self.direction.x *= -1
                    self.rect.left = wall.rect.right
                    self.hp -= 1
                    if self.hp == 0:
                        return self.kill()
                    bounce.play()

                if self.rect.centery < wall.rect.top:
                    self.direction.y *= -1
                    self.rect.bottom = wall.rect.top
                    self.hp -= 1
                    if self.hp == 0:
                        return self.kill()
                    bounce.play()

                if self.rect.centery > wall.rect.bottom:
                    self.direction.y *= -1
                    self.rect.top = wall.rect.bottom
                    self.hp -= 1
                    if self.hp == 0:
                        return self.kill()
                    bounce.play()

        enemy_list = game.enemy_group
        for enemy in enemy_list:
            if self.rect.colliderect(enemy.rect):
                self.hp -= 1
                if self.hp <= 0:
                    return self.kill()
                enemy.hp -= 1
                if enemy.hp <= 0:
                    game.enemy = Enemy()  # adds new enemy after last one is dead
                    game.all_sprites.add(game.enemy)
                    game.enemy_group.add(game.enemy)
                    game.player_scoreboard += 1
                    tone.play()
                    # bounce.play()
                    return enemy.kill(), self.kill()

        player_list = game.player_group
        for tank in player_list:
            if self.rect.colliderect(tank.rect) and self.hp < 4:
                self.hp -= 1
                if self.hp <= 0:
                    return self.kill()
                tank.hp -= 1
                if tank.hp <= 0:
                    game.tank = Tank()  # adds new player after last one is dead
                    game.all_sprites.add(game.tank)
                    game.player_group.add(game.tank)
                    game.enemy_scoreboard += 1
                    tone.play()
                    # bounce.play()
                    return tank.kill(), self.kill()


game = Game()
font = pygame.font.SysFont("bin/font/Montserrat.ttf", 40)
text = font.render("PLAY", 1, white)
font = pygame.font.SysFont("bin/font/Montserrat.ttf", 50)
title = font.render("TANK TROUBLE", 1, dark_gray)

click = False


def main_menu():
    global click
    clock = pygame.time.Clock()
    # game = Game()

    while True:
        pygame.display.set_caption('Tank Trouble')
        game.screen.fill((white))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(377, 370, 300, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                main()
        pygame.draw.rect(game.screen, gray, button_1)
        game.screen.blit(text, (490, 383))
        game.screen.blit(title, (395, 320))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RETURN:
                    main()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(fps)


def main():
    pygame.display.set_caption('Tank Trouble')
    clock = pygame.time.Clock()
    # game = Game()

    while game.run:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(fps)


if __name__ == '__main__':
    main_menu()
    pygame.quit()
    sys.exit()
