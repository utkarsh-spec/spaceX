import pygame
import random
pygame.init()

display = pygame.display.set_mode((500, 500))
pygame.display.set_caption("spaceX")
bg = pygame.image.load("back.png")
ship_image = [pygame.image.load("ship_sprites/tile000.png"), pygame.image.load("ship_sprites/tile001.png"),
              pygame.image.load("ship_sprites/tile002.png"), pygame.image.load("ship_sprites/tile003.png"),
              pygame.image.load("ship_sprites/tile004.png"), pygame.image.load("ship_sprites/tile005.png"),
              pygame.image.load("ship_sprites/tile006.png"), pygame.image.load("ship_sprites/tile007.png"),
              pygame.image.load("ship_sprites/tile008.png"), pygame.image.load("ship_sprites/tile009.png")]
astro_sprite = [pygame.image.load("astro/1.png"), pygame.image.load("astro/2.png"), pygame.image.load("astro/3.png"),
                pygame.image.load("astro/4.png"), pygame.image.load("astro/5.png"), pygame.image.load("astro/6.png"),
                pygame.image.load("astro/7.png"), pygame.image.load("astro/8.png"), pygame.image.load("astro/9.png"),
                pygame.image.load("astro/10.png"), pygame.image.load("astro/11.png"), pygame.image.load("astro/12.png")]

score = 0
fire_sound = pygame.mixer.Sound('ship_bullet.wav')
hit_sound = pygame.mixer.Sound('hit.wav')
pygame.mixer.music.load('bg.mp3')
pygame.mixer.music.play(-1)


class Player(object):
    def __init__(self, x, y, weidth, height):
        self.x = x
        self.y = y
        self.weidth = weidth
        self.height = height
        self.vel = 5
        self.count = 0
        self.move = True
        self.hitbox = (self.x, self.y, 16, 24)
        self.health = 100

    def draw(self, display):

        display.blit(bg, (0, 0))

        if self.count + 1 >= 30:
            self.count = 0
        if self.move:
            display.blit(ship_image[self.count//3], (self.x, self.y))
            self.count += 1

        self.hitbox = (self.x, self.y, 16, 24)
        # pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(display, (150, 0, 0), (20, 30, 100, 20))
        pygame.draw.rect(display, (0, 150, 0), (20, 30, 100 - (1 * (100 - self.health)), 20))

    def hit(self):
        font = pygame.font.SysFont('comicsans', 70)
        text = font.render('HEALTH LOSS', True, (255, 0, 0))
        display.blit(text, (80, 50))
        pygame.display.update()
        self.health -= 1
        if self.health < 0:
            self.health = 0

        # print('hit with object')


class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 5

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    def __init__(self, x, y, weidth, height):
        self.x = x
        self.y = y
        self.weidth = weidth
        self.height = height
        self.count = 0
        self.vel = 1
        self.hitbox = (self.x+30, self.y+30, 50, 50)
        self.health = 10
        self.visible = True

    def draw(self, display):
        self.move()
        if self.count + 1 >= 96:
            self.count = 0
        # if self.visible:
        display.blit(astro_sprite[self.count//8], (self.x, self.y))
        self.count += 1

        self.hitbox = (self.x+30, self.y+30, 80, 80)
        # pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)
        # for health box
        pygame.draw.rect(display, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(display, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

    def move(self):
        if self.health == 0:
            self.y = -100
            self.health = 10
            self.x = random.randint(0, 300)
            self.visible = True
        if self.y < 500:
            self.y += self.vel
            if self.y >= 500:
                self.y = -100
                self.x = random.randint(0, 300)

    def hit(self):
        hit_sound.play()
        bullets.pop(bullets.index(bullet))
        self.health -= 1
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            self.visible = False
        if not self.visible:
            global score
            score += 1


ship = Player(225, 400, 16, 24)
astra = Enemy(200, -100, 145, 145)


def game_window():
    ship.draw(display)
    astra.draw(display)
    # health bar
    font1 = pygame.font.SysFont('comicsans', 22)
    text1 = font1.render('HEALTH BAR', True, (0, 200, 255))
    display.blit(text1, (20, 10))
    # score
    font2 = pygame.font.SysFont('comicsans', 22)
    text2 = font2.render('SCORE: '+ str(score), True, (0, 200, 255))
    display.blit(text2, (400, 10))

    for bullet in bullets:
        bullet.draw(display)
    # update display
    pygame.display.update()


bullets = []
run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # game over
    if ship.health == 0:
        font = pygame.font.SysFont('comicsans', 100)
        text = font.render('GAME OVER', True, (255, 0, 0))
        display.blit(text, (30, 100))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()
            pygame.time.delay(10)

    # player hit with object
    if ship.hitbox[1] < astra.hitbox[1] + astra.hitbox[3] and ship.hitbox[1] + ship.hitbox[3] > astra.hitbox[1]:
        if ship.hitbox[0] + ship.hitbox[2] > astra.hitbox[0] and ship.hitbox[0] < astra.hitbox[0] + astra.hitbox[2]:
            ship.hit()

    game_window()

    for bullet in bullets:
        if 0 < bullet.y < 500:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

        # bullet hiting object
        if bullet.y - bullet.radius < astra.hitbox[1] + astra.hitbox[3] and bullet.y + bullet.radius > astra.hitbox[1]:
            if bullet.x - bullet.radius < astra.hitbox[0] + astra.hitbox[2] and bullet.x + bullet.radius > astra.hitbox[0]:
                astra.hit()

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and ship.x > 0:
        ship.x -= ship.vel
    if key[pygame.K_RIGHT] and ship.x < 485:
        ship.x += ship.vel
    if key[pygame.K_UP] and ship.y > 0:
        ship.y -= ship.vel
    if key[pygame.K_DOWN] and ship.y < 475:
        ship.y += ship.vel

    if key[pygame.K_SPACE]:
        # fire_sound.play()
        # bullets counts
        if len(bullets) < 5:
            bullets.append(Projectile(round(ship.x + ship.weidth//2), round(ship.y), 2, (255, 200, 0)))


pygame.quit()
