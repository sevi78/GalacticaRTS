import pygame

pygame.init()


class curvemove:
    def __init__(self, x, y, height, width, color):
        self.pos = pygame.math.Vector2(x, y)
        self.color = color
        self.rect = pygame.Rect(x, y, height, width)
        self.speed = pygame.math.Vector2(5.0, 0)
        self.gravity = 0.5
        self.friction = 0.99

    def draw(self):
        self.rect.center = (self.pos.x, self.pos.y)
        pygame.draw.circle(window, self.color, (self.pos.x, self.pos.y), self.rect.width // 2)

    def update(self, target_pos):
        dir_vec = pygame.math.Vector2(target_pos) - self.rect.center
        v_len_sq = dir_vec.length_squared()
        if v_len_sq > 0:
            dir_vec.scale_to_length(self.gravity)
            self.speed = (self.speed + dir_vec) * self.friction
            self.pos += self.speed



window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("test map")
clock = pygame.time.Clock()
white = 255, 255, 255
red = 205, 0, 10
curve_move1 = curvemove(250, 400, 20, 20, white)
touched = curvemove(250, 200, 20, 20, red)
fps = 60
move = False


def redraw():
    window.fill((0, 0, 0))
    curve_move1.draw()
    touched.draw()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                move = True
            if event.key == pygame.K_r:
                move = False
                curve_move1 = curvemove(250, 400, 20, 20, white)

    if (curve_move1.pos - touched.pos).length() < 10:
        move = False
    if move:
        curve_move1.update(touched.rect.center)
    redraw()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
exit()