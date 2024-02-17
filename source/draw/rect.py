import pygame


def draw_transparent_rounded_rect(surface, color, rect, radius, alpha):
    # Create a Surface with the correct dimensions and with per-pixel alpha enabled
    rect_surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    # Draw a transparent rounded rectangle on the created Surface
    pygame.draw.rect(rect_surface, color + (alpha,), (0, 0, rect[2], rect[3]), border_radius=radius)
    # Blit the transparent rounded rectangle onto the target surface at the correct position
    surface.blit(rect_surface, rect[:2])

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((640, 480))
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         screen.fill((0, 0, 0))
#         pygame.draw.rect(screen, (255, 155, 255), (50, 100, 200, 100))
#         draw_transparent_rounded_rect(screen, (100, 100, 100), (100, 100, 200, 100), 20, 128)
#         pygame.display.flip()
#     pygame.quit()
#
# if __name__ == "__main__":
#     main()

# def main__():
#     pygame.init()
#     screen = pygame.display.set_mode((640, 480))
#
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         screen.fill((0,0,0))
#         draw_transparent_rounded_rect(screen, (100, 100, 100), (100, 100, 200, 100), 20, 128)
#         pygame.display.flip()
#
#     pygame.quit()
#
# if __name__ == "__main__":
#     main()
