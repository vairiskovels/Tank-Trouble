# Loads all modules
import sys
import pygame, math, random, time
from pygame.locals import *

# Initializes pygame and music settings
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# ======================= Variables =======================

gray = (168, 168, 168)
dark_gray = (77, 77, 77)
white = (255, 255, 255)
red = (255, 89, 60)
green = (17, 176, 0)
blue = (66, 135, 245)
yellow = (255, 255, 0)

font = pygame.font.Font("bin/font/Montserrat.ttf", 20) # loads font used in the game

bounce = pygame.mixer.Sound("bin/audio/bounce.wav") # loads necessary sounds
bounce.set_volume(0.5)

shoot = pygame.mixer.Sound("bin/audio/shoot.wav")
shoot.set_volume(0.5)

tone = pygame.mixer.Sound("bin/audio/tone.wav")

fps = 120 # fps of the game

# ======================= Classes =======================

class Game: # main game class

    def __init__(self):
        # sets values of game screen
        self.run = True
        self.screen_width = 1060
        self.screen_height = 798
        self.image = pygame.image.load("bin/sprites/background/background1.png")
        self.image = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # sets values of player and enemy score
        self.player_scoreboard = 0
        self.enemy_scoreboard = 0

        # all_sprites is used to update and draw all sprites together.
        self.all_sprites = pygame.sprite.Group()

        # for collision detection with enemies.
        self.bullet_group = pygame.sprite.Group()

        # sets groups for player and enemy; all characters are stored here
        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        # for collision detection with walls.
        self.wall_list = pygame.sprite.Group()

        # sets player character
        self.tank = Tank()
        self.all_sprites.add(self.tank) # adds to all_sprite group
        self.player_group.add(self.tank) # adds to player_group

        # sets enemy character
        self.enemy = Enemy()
        self.all_sprites.add(self.enemy) # adds to all_sprite group
        self.enemy_group.add(self.enemy) # adds to player_group

        # projectile shoots when enter bar is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.bullet_group.add(bullet)
            self.all_sprites.add(bullet)

        # -------------- Walls --------------

        # all wall coordinates and sizes
        wallx = [0, 0, 1044, 0, 0, 260, 146, 130, 146, 146, 130, 146, 390, 522, 390, 260, 390, 406, 522, 522, 522, 652,
                 652, 782, 914, 782, 782, 914, 914, 914, 652, 652, 782, ]
        wally = [0, 0, 0, 782, 260, 0, 130, 130, 522, 390, 652, 652, 0, 0, 130, 260, 260, 390, 260, 260, 522, 130, 130,
                 0, 0, 260, 390, 390, 522, 652, 522, 652, 522, ]
        wallWidth = [16, 1060, 16, 1060, 130, 16, 130, 16, 130, 130, 16, 130, 16, 16, 148, 146, 16, 132, 16, 130, 16,
                     278, 16, 16, 16, 278, 148, 16, 148, 148, 146, 146, 16, ]
        wallHeight = [798, 16, 798, 16, 16, 130, 16, 408, 16, 16, 146, 16, 146, 146, 16, 16, 408, 16, 146, 16, 260, 16,
                      296, 146, 146, 16, 16, 148, 16, 16, 16, 16, 276]

        # adds walls to wall_list group
        for i in range(len(wallx)):
            self.wall = Wall(wallx[i], wally[i], wallWidth[i], wallHeight[i])
            self.wall_list.add(self.wall)
            self.all_sprites.add(self.wall)

    def handle_events(self):

        # responsible for colliding with walls
        tank_pos = pygame.math.Vector2(self.tank.pos)
        self.tank.handle_events()
        if pygame.sprite.spritecollide(self.tank, self.wall_list, False):
            self.tank.pos = tank_pos
            self.tank.rect.center = round(tank_pos[0]), round(tank_pos[1])

        enemy_pos = pygame.math.Vector2(self.enemy.pos)
        self.enemy.handle_events()
        if pygame.sprite.spritecollide(self.enemy, self.wall_list, False):
            self.enemy.pos = enemy_pos
            self.enemy.rect.center = round(enemy_pos[0]), round(enemy_pos[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE: # if space button is pressed then player 1 is shooting and shooting sound is playing
                    bullet = Bullet(self.tank)
                    self.bullet_group.add(bullet)
                    self.all_sprites.add(bullet)
                    shoot.play()
                if event.key == pygame.K_RETURN: # if return/enter button is pressed then player 2/enemy is shooting and shooting sound is playing
                    bullet = Bullet(self.enemy)
                    self.bullet_group.add(bullet)
                    self.all_sprites.add(bullet)
                    shoot.play()

    def update(self):
        # Calls `update` methods of all contained sprites.
        self.all_sprites.update()

    def draw_score(self):
        font = pygame.font.SysFont("bin/font/Montserrat.ttf", 35)
        score = font.render("SCORE", 1, dark_gray)
        playerScores = font.render(str(self.player_scoreboard) + " : " + str(self.enemy_scoreboard), 1, dark_gray)
        self.screen.blit(score, (self.screen_width/2 - score.get_width()/2, 830))
        self.screen.blit(playerScores, (self.screen_width/2 - playerScores.get_width()/2, 860))

    def player_health(self): # draws player 1 health on the screen
        font = pygame.font.SysFont("bin/font/Montserrat.ttf", 25)
        self.health = font.render("HP: " + str(int(self.tank.hp / 2)), 1, green)

        self.healthBarOut = (20, 20, 120, 25)
        pygame.draw.rect(self.screen, (0, 0, 0), self.healthBarOut, 2)
        self.screen.blit(self.health, (55, 25))

    def enemy_health(self): # draws player 2 health on the screen
        font = pygame.font.SysFont("bin/font/Montserrat.ttf", 25)
        self.health = font.render("HP: " + str(int(self.enemy.hp / 2)), 1, red)

        self.healthBarOut = (920, 20, 120, 25)
        pygame.draw.rect(self.screen, (0, 0, 0), self.healthBarOut, 2)
        self.screen.blit(self.health, (955, 25))

    def draw(self): # draws all sprites on the screen
        self.screen.blit(self.image, (0, 0))
        self.all_sprites.draw(self.screen)  # Draw the contained sprites.
        self.draw_score()
        self.player_health()
        self.enemy_health()
        pygame.display.update()


class Tank(pygame.sprite.Sprite): # player 1 class

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bin/sprites/player/player_tank1.png") # sets player 1 sprite
        self.org_image = self.image.copy()

        self.spawnx = [70, 336, 460]  # spawning x coord
        self.spawny = [600, 72, 330]  # spawning y coord
        self.i = random.randint(0, len(self.spawnx) - 1)

        # A nicer way to set the start pos with `get_rect`.
        self.rect = self.image.get_rect(center=(self.spawnx[self.i], self.spawny[self.i]))

        self.vel = 3.5

        if self.i == 0: # spawning angles
            self.angle = 270
        elif self.i == 1:
            self.angle = 180
        elif self.i == 2:
            self.angle = 0

        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)

        self.hp = 6


    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.angle += 3
        if keys[pygame.K_d]:
            self.angle -= 3
        if keys[
            pygame.K_w] and self.rect.left - 5 > 0 and self.rect.top - 5 > 0 and self.rect.right + 5 < 1060 and self.rect.bottom + 5 < 798:
            self.move(-self.vel)
        if keys[
            pygame.K_s] and self.rect.left - 5 > 0 and self.rect.top - 5 > 0 and self.rect.right + 5 < 1060 and self.rect.bottom + 5 < 798:
            self.move(self.vel)

        self.direction = pygame.Vector2(1, 0).rotate(-self.angle) # responsible for player 1 rotation
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        return self.rect

    def move(self, vel):
        direction = pygame.Vector2(0, vel).rotate(-self.angle) # responsible for player 1 rotation
        self.pos += direction
        self.rect.center = round(self.pos[0]), round(self.pos[1])


class Enemy(pygame.sprite.Sprite): # player 2 class

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bin/sprites/enemy/enemy_tank1.png") # sets player 2 sprite
        self.org_image = self.image.copy()

        self.spawnx = [600, 850, 860]  # spawning x coord
        self.spawny = [70, 200, 700]  # spawning y coord
        self.i = random.randint(0, len(self.spawnx) - 1)

        # A nicer way to set the start pos with `get_rect`.
        self.rect = self.image.get_rect(center=(self.spawnx[self.i], self.spawny[self.i]))

        self.vel = 3
        self.hp = 6

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
        keys = pygame.key.get_pressed() # bot controls
        if keys[pygame.K_LEFT]:
            self.angle += 3
        if keys[pygame.K_RIGHT]:
            self.angle -= 3
        if keys[pygame.K_UP]:
            self.move(-3)
        if keys[pygame.K_DOWN]:
            self.move(3)

        # -------------- Palayer 2 movement --------------

        self.direction = pygame.Vector2(1, 0).rotate(-self.angle) # responsible for player 1 rotation
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, vel):
        direction = pygame.Vector2(0, vel).rotate(-self.angle) # responsible for player 1 rotation
        self.pos += direction
        self.rect.center = round(self.pos[0]), round(self.pos[1])


class Wall(pygame.sprite.Sprite): # wall class

    def __init__(self, x, y, width, height):
        super().__init__()

        # Make a wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(dark_gray)  # change wall color

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Bullet(pygame.sprite.Sprite): # bullet class

    def __init__(self, tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bin/sprites/bullet/bullet.png") # loads bullet sprite
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.rect.centerx + 0  # How much pixels from tank turret on x axis
        self.rect.centery = tank.rect.centery - 0  # How much pixels from tank turret on y axis
        self.angle = tank.angle
        self.pos = pygame.Vector2(self.rect.center)
        self.direction = pygame.Vector2(0, -10).rotate(-self.angle)
        self.hp = 4  # how many times bounces player 1 ball
        self.en_hp = 4 # how many times bounces player 2 ball
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.hp -= 1
        if keys[pygame.K_SPACE]:
            self.en_hp -= 1



    def update(self):

        self.pos += self.direction
        self.rect.center = round(self.pos[0]), round(self.pos[1])

        for wall in game.wall_list: # responsible for ball collision with the walls
            if self.rect.colliderect(wall.rect):  # if collided
                if self.rect.centerx < wall.rect.left:
                    self.direction.x *= -1
                    self.rect.right = wall.rect.left
                    self.hp -= 1
                    self.en_hp -= 1
                    if self.hp == 0 or self.en_hp == 0:
                        return self.kill()
                    bounce.play()

                if self.rect.centerx > wall.rect.right:
                    self.direction.x *= -1
                    self.rect.left = wall.rect.right
                    self.hp -= 1
                    self.en_hp -= 1
                    if self.hp == 0 or self.en_hp == 0:
                        return self.kill()
                    bounce.play()

                if self.rect.centery < wall.rect.top:
                    self.direction.y *= -1
                    self.rect.bottom = wall.rect.top
                    self.hp -= 1
                    self.en_hp -= 1
                    if self.hp == 0 or self.en_hp == 0:
                        return self.kill()
                    bounce.play()

                if self.rect.centery > wall.rect.bottom:
                    self.direction.y *= -1
                    self.rect.top = wall.rect.bottom
                    self.hp -= 1
                    self.en_hp -= 1
                    if self.hp == 0 or self.en_hp == 0:
                        return self.kill()
                    bounce.play()

        enemy_list = game.enemy_group
        for enemy in enemy_list: # responsible for ball collision with player 2
            if self.rect.colliderect(enemy.rect) and self.en_hp < 4:
                self.en_hp -= 1
                if self.en_hp <= 0:
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
        for tank in player_list: # responsible for ball collision with player 1
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

click = False

# ======================================= Main game loop =======================================
def main_menu():
    global click
    clock = pygame.time.Clock()
    game.run = True

    font = pygame.font.SysFont("bin/font/Montserrat.ttf", 40)
    play = font.render("PLAY", 1, white)
    controls_text = font.render("CONTROLS", 1, white)
    settings_text = font.render("SETTINGS", 1, white)
    font = pygame.font.SysFont("bin/font/Montserrat.ttf", 50)
    title = font.render("TANK TROUBLE", 1, dark_gray)

    while True: # responsible for showing main menu
        pygame.display.set_caption('Tank Trouble')
        game.screen.fill((white))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(game.screen_width/2 - 150, 370, 300, 50)
        button_2 = pygame.Rect(game.screen_width/2 - 150, 430, 300, 50)
        button_3 = pygame.Rect(game.screen_width / 2 - 150, 490, 300, 50)

        pygame.draw.rect(game.screen, gray, button_1)
        pygame.draw.rect(game.screen, gray, button_2)
        pygame.draw.rect(game.screen, gray, button_3)

        if button_1.collidepoint((mx, my)):
            pygame.draw.rect(game.screen, green, button_1)
            if click:
                main()
        if button_2.collidepoint((mx, my)):
            pygame.draw.rect(game.screen, green, button_2)
            if click:
                controls()
        if button_3.collidepoint((mx, my)):
            pygame.draw.rect(game.screen, green, button_3)
            if click:
                settings()

        game.screen.blit(play, (game.screen_width / 2 - play.get_width() / 2, 383))
        game.screen.blit(controls_text, (game.screen_width / 2 - controls_text.get_width() / 2, 443))
        game.screen.blit(settings_text, (game.screen_width / 2 - settings_text.get_width() / 2, 503))
        game.screen.blit(title, (game.screen_width / 2 - title.get_width() / 2, 320))

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

def controls(): # controls tab on main screen
    global click
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("bin/font/Montserrat.ttf", 50)
    title = font.render("CONTROLS", 1, dark_gray)
    line = pygame.Rect(game.screen_width/2, game.screen_height/2 - 202, 5, 404)
    player1_image = pygame.image.load("bin/sprites/player/player_tank1.png")
    player1_image = pygame.transform.scale(player1_image, (54, 64))
    player2_image = pygame.image.load("bin/sprites/enemy/enemy_tank1.png")
    player2_image = pygame.transform.scale(player2_image, (54, 64))
    player1_control_1 = font.render("WASD", 1, dark_gray)
    player1_control_2 = font.render("SPACE", 1, dark_gray)
    player2_control_1 = font.render("ARROW KEYS", 1, dark_gray)
    player2_control_2 = font.render("ENTER", 1, dark_gray)

    while True: # responsible for showing controls tab
        pygame.display.set_caption('Tank Trouble')
        game.screen.fill((white))

        mx, my = pygame.mouse.get_pos()

        game.screen.blit(title, (game.screen_width/2 - title.get_width()/2 , 50))
        pygame.draw.rect(game.screen, dark_gray, line)
        game.screen.blit(player1_image, (242, 250))
        game.screen.blit(player2_image, (770, 250))
        game.screen.blit(player1_control_1, (game.screen_width/4 - player1_control_1.get_width()/2, 400))
        game.screen.blit(player1_control_2, (game.screen_width / 4 - player1_control_2.get_width() / 2, 440))
        game.screen.blit(player2_control_1, (game.screen_width / 4 * 3 - player2_control_1.get_width() / 2, 400))
        game.screen.blit(player2_control_2, (game.screen_width / 4  * 3 - player2_control_2.get_width() / 2, 440))


        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True



        pygame.display.update()
        clock.tick(fps)

def settings():
    global click
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("bin/font/Montserrat.ttf", 50)
    title = font.render("SETTINGS", 1, dark_gray)
    light_mode = pygame.image.load("bin/sprites/background/background1.png")
    light_mode = pygame.transform.scale(light_mode, (360, 256))
    dark_mode = pygame.image.load("bin/sprites/background/background3.png")
    dark_mode = pygame.transform.scale(dark_mode, (360, 256))
    font = pygame.font.SysFont("bin/font/Montserrat.ttf", 35)
    light_mode_text = font.render("LIGHT MODE", 1, dark_gray)
    dark_mode_text = font.render("DARK MODE", 1, dark_gray)
    light_button = pygame.Rect(game.screen_width/4 - light_mode.get_width()/2 + 30, 250, 360, 256)
    dark_button = pygame.Rect(game.screen_width/4 * 3 - dark_mode.get_width()/2 - 30, 250, 360, 256)

    while True: # responsible for showing settings tab
        pygame.display.set_caption('Tank Trouble')
        game.screen.fill((white))

        mx, my = pygame.mouse.get_pos()

        game.screen.blit(title, (game.screen_width / 2 - title.get_width() / 2, 50))
        game.screen.blit(light_mode, (game.screen_width/4 - light_mode.get_width()/2 + 30, 250))
        game.screen.blit(dark_mode, (game.screen_width/4 * 3 - dark_mode.get_width()/2 - 30, 250))
        game.screen.blit(light_mode_text, (game.screen_width / 4 - light_mode_text.get_width() / 2 + 30, 520))
        game.screen.blit(dark_mode_text, (game.screen_width / 4 * 3 - dark_mode_text.get_width() / 2 - 30, 520))

        if light_button.collidepoint((mx, my)):
            if click:
                game.image = pygame.image.load("bin/sprites/background/background1.png")
                game.image = pygame.transform.scale(game.image, (game.screen_width, 798))

                enemy_list = game.enemy_group
                for enemy in enemy_list:
                    game.enemy.image = pygame.image.load("bin/sprites/enemy/enemy_tank1.png")
                    game.enemy.org_image = game.enemy.image.copy()

                player_list = game.player_group
                for tank in player_list:
                    game.tank.image = pygame.image.load("bin/sprites/player/player_tank1.png")
                    game.tank.org_image = game.tank.image.copy()

                main_menu()

        elif dark_button.collidepoint((mx, my)):
            if click:
                game.image = pygame.image.load("bin/sprites/background/background2.png")
                game.image = pygame.transform.scale(game.image, (game.screen_width, 798))

                enemy_list = game.enemy_group
                for enemy in enemy_list:
                    enemy.image = pygame.image.load("bin/sprites/enemy/enemy_tank2.png")
                    enemy.org_image = enemy.image.copy()

                player_list = game.player_group
                for tank in player_list:
                    tank.image = pygame.image.load("bin/sprites/player/player_tank2.png")
                    tank.org_image = tank.image.copy()

                main_menu()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(fps)

def main():
    pygame.display.set_caption('Tank Trouble')
    clock = pygame.time.Clock()

    while game.run: # responsible for main game loop
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(fps)


if __name__ == '__main__':
    main_menu()
    pygame.quit()
    sys.exit()
