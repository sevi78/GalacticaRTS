import pygame
import math
#
from source.draw.arrow import draw_arrow
#
#
# class MovingArrow:
#     def __init__(self, start_pos, target_pos, color, arrow_size):
#         self.start_pos = start_pos
#         self.target_pos = target_pos
#         self.color = color
#         self.arrow_size = arrow_size
#
#     def update(self, speed):
#         dx, dy = self.target_pos[0] - self.start_pos[0], self.target_pos[1] - self.start_pos[1]
#         angle = math.atan2(dy, dx)
#         self.start_pos = (self.start_pos[0] + speed * math.cos(angle), self.start_pos[1] + speed * math.sin(angle))
#
#     def draw(self, screen):
#         draw_arrow(screen, self.start_pos, self.target_pos, self.color, self.arrow_size)
#
#
# # Example usage
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# moving_arrow = MovingArrow((400, 300), (200, 100), (255, 0, 0), 50)
#
# while True:
#     screen.fill((0, 0, 0))
#     moving_arrow.update(0.1)
#     moving_arrow.draw(screen)
#     pygame.display.flip()


# class MovingArrow:
#     def __init__(self, start_pos, target_pos, color, arrow_size):
#         self.start_pos = start_pos
#         self.target_pos = target_pos
#         self.color = color
#         self.arrow_size = arrow_size
#
#     def update(self, speed):
#         dx, dy = self.target_pos[0] - self.start_pos[0], self.target_pos[1] - self.start_pos[1]
#         distance = math.hypot(dx, dy)
#         if distance > 0:
#             angle = math.atan2(dy, dx)
#             self.start_pos = (self.start_pos[0] + speed * math.cos(angle), self.start_pos[1] + speed * math.sin(angle))
#         else:
#             return False
#         return True
#
#     def draw(self, screen):
#         draw_arrow(screen, self.start_pos, self.target_pos, self.color, self.arrow_size)
#
# # # Example usage
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
#
# arrows = [MovingArrow((400, 300), pygame.mouse.get_pos(), (255, 0, 0), 50) for _ in range(5)]
#
# while True:
#     screen.fill((0, 0, 0))
#     for arrow in arrows[:]:
#         if not arrow.update(0.1):
#             arrows.remove(arrow)
#         else:
#             arrow.draw(screen)
#     pygame.display.flip()


import pygame
import math
from source.draw.arrow import draw_arrow

class MovingArrow:
    def __init__(self, start_pos, target_pos, color, arrow_size):
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.color = color
        self.arrow_size = arrow_size

    def update(self, speed):
        self.target_pos = pygame.mouse.get_pos()  # Update target position to mouse position
        dx, dy = self.target_pos[0] - self.start_pos[0], self.target_pos[1] - self.start_pos[1]
        distance = math.hypot(dx, dy)
        if distance > 0:
            angle = math.atan2(dy, dx)
            self.start_pos = (self.start_pos[0] + speed * math.cos(angle), self.start_pos[1] + speed * math.sin(angle))
        else:
            return False
        return True

    def draw(self, screen):
        draw_arrow(screen, self.start_pos, self.target_pos, self.color, self.arrow_size)

pygame.init()

screen = pygame.display.set_mode((800, 600))

arrows = []
for _ in range(5):
    arrows.append(MovingArrow((400, 300), pygame.mouse.get_pos(), (255, 0, 0), 50))
      # Delay of 0.5 seconds

while True:
    screen.fill((0, 0, 0))
    for arrow in arrows[:]:
        if not arrow.update(0.1):
            arrows.remove(arrow)
        else:
            arrow.draw(screen)
        pygame.time.delay(200)
    pygame.display.flip()

