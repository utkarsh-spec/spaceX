import pygame
pygame.init()

display = pygame.display.set_mode((500, 500))
pygame.display.set_caption("spaceX")
bg = pygame.image.load("back.png")
ship_image = [pygame.image.load("ship_sprites/tile000.png"), pygame.image.load("ship_sprites/tile001.png"),
              pygame.image.load("ship_sprites/tile002.png"), pygame.image.load("ship_sprites/tile003.png"),
              pygame.image.load("ship_sprites/tile004.png"), pygame.image.load("ship_sprites/tile005.png"),
              pygame.image.load("ship_sprites/tile006.png"), pygame.image.load("ship_sprites/tile007.png"),
              pygame.image.load("ship_sprites/tile008.png"), pygame.image.load("ship_sprites/tile009.png")]


class Player(object):
    def __init__(self, x, y, weidth, height):
        self.x = x
        self.y = y
        self.weidth = weidth
        self.height = height
        self.vel = 5
        self.count = 0
        self.move = True

    def draw(self, display):
        display.fill((0, 0, 0))
        display.blit(bg, (0, 0))
        # pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.weidth, self.height))
        if self.count + 1 >= 9:
            self.count = 0
        if self.move:
            display.blit(ship_image[self.count//3], (self.x, self.y))
            self.count += 1


class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 10

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)

ship = Player(225, 400, 16, 24)


def game_window():
    ship.draw(display)

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

    game_window()

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        ship.x -= ship.vel
    if key[pygame.K_RIGHT]:
        ship.x += ship.vel
    if key[pygame.K_UP]:
        ship.y -= ship.vel
    if key[pygame.K_DOWN]:
        ship.y += ship.vel

    if key[pygame.K_SPACE]:
        # bullets counts
        if len(bullets) < 100:
            bullets.append(Projectile(round(ship.x + ship.weidth//2), round(ship.y), 3, (255, 200, 0)))


pygame.quit()
