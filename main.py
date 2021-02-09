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
astro_sprite = [pygame.image.load("astro/1.png"), pygame.image.load("astro/2.png"),
                pygame.image.load("astro/3.png"), pygame.image.load("astro/4.png"),
                pygame.image.load("astro/5.png"), pygame.image.load("astro/6.png"),
                pygame.image.load("astro/7.png"), pygame.image.load("astro/8.png"),
                pygame.image.load("astro/9.png"), pygame.image.load("astro/10.png"), pygame.image.load("astro/11.png"),
                pygame.image.load("astro/12.png")]


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

    def draw(self, display):

        display.blit(bg, (0, 0))

        if self.count + 1 >= 30:
            self.count = 0
        if self.move:
            display.blit(ship_image[self.count//3], (self.x, self.y))
            self.count += 1

        self.hitbox = (self.x, self.y, 16, 24)
        # pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        print('hit with object')


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

    def draw(self, display):
        self.move()
        if self.count + 1 >= 96:
            self.count = 0
        display.blit(astro_sprite[self.count//8], (self.x, self.y))
        self.count += 1

        self.hitbox = (self.x+30, self.y+30, 80, 80)
        # pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.y < 500:
            self.y += self.vel
            if self.y >= 500:
                self.y = -100
                self.x = random.randint(0, 300)

    def hit(self):
        bullets.pop(bullets.index(bullet))
        print('hit')


ship = Player(225, 400, 16, 24)
astra = Enemy(200, -100, 145, 145)


def game_window():
    ship.draw(display)
    astra.draw(display)
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

    # player hit with object
    if ship.hitbox[1] < astra.hitbox[1] + astra.hitbox[3] and ship.hitbox[1] + ship.hitbox[3] > astra.hitbox[1]:
        if ship.hitbox[0] + ship.hitbox[2] > astra.hitbox[0] and ship.hitbox[0] < astra.hitbox[0] + astra.hitbox[2]:
            ship.hit()

    game_window()

    for bullet in bullets:
        if 0 < bullet.x < 500:
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
        # bullets counts
        if len(bullets) < 100:
            bullets.append(Projectile(round(ship.x + ship.weidth//2), round(ship.y), 2, (255, 200, 0)))


pygame.quit()
