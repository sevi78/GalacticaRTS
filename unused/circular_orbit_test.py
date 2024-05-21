import pygame
import math


def move_coords(angle, radius, center):
    theta = math.radians(angle)
    return center[0] + radius * math.cos(theta), center[1] + radius * math.sin(theta)


def main():
    pygame.display.set_caption("Oribit")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    center = 400, 200
    angle = 0
    rect = pygame.Rect(*center, 20, 20)
    speed = 50
    next_tick = 500

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 30))
        ticks = pygame.time.get_ticks()
        if ticks > next_tick:
            next_tick += speed
            angle += 1
            x,y = center
            x += 1
            center = move_coords(angle, 2, (x,y))
            rect.topleft = center
            pygame.draw.circle(screen, pygame.color.THECOLORS.get("red"), center, math.dist(center,rect.center ))


        screen.fill((0, 150, 0), rect)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()