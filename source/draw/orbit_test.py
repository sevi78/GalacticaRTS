import pygame, math


class Crucifix(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, "white", (20, 20), 20)
        pygame.draw.line(self.image, "magenta", (20, 0), (20, 40), 5)
        pygame.draw.line(self.image, "magenta", (0, 20), (40, 20), 5)
        self.rect = self.image.get_rect(center=(400, 400))
        self.mask = pygame.mask.from_surface(self.image)
        self.px = 400
        self.a = 0

    def update(self):
        offset_x = math.sin(self.a) * 100
        self.a += 0.05
        self.rect.x = round(self.px + offset_x)


class EnemiesStrong(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, "red", (20, 20), 20)
        pygame.draw.polygon(self.original_image, "yellow", ((20, 0), (40, 20), (20, 40), (0, 20)))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.angle = 0

    def initLoc(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def update(self):
        center = pygame.math.Vector2(self.pos) + pygame.math.Vector2(0, -self.radius).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(round(center.x), round(center.y)))

    def turnLeft(self):
        self.angle = (self.angle + 4) % 360

    def updatePos(self, new_pos):
        self.pos = new_pos


pygame.init()
window = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
cross1 = Crucifix()
enemy_s = EnemiesStrong()
pos = cross1.rect.x, cross1.rect.y

enemy_s.initLoc(cross1.rect.center, 100)
all_sprites = pygame.sprite.Group(enemy_s)
all_sprites.add(cross1)

background = pygame.Surface(window.get_size())
ts, w, h, c1, c2 = 50, *background.get_size(), (32, 32, 32), (48, 48, 48)
tiles = [((x * ts, y * ts, ts, ts), c1 if (x + y) % 2 == 0 else c2) for x in range((w + ts - 1) // ts) for y in
         range((h + ts - 1) // ts)]
[pygame.draw.rect(background, color, rect) for rect, color in tiles]

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    enemy_s.turnLeft()
    enemy_s.updatePos(cross1.rect.center)
    all_sprites.update()

    window.blit(background, (0, 0))

    all_sprites.draw(window)
    pygame.display.flip()

pygame.quit()
exit()