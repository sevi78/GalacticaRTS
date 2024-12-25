"""
https://stackoverflow.com/questions/66984521/getting-rotated-rect-of-rotated-image-in-pygame/66984713#66984713
"""

import pygame

from source.draw.cross import draw_cross_in_circle

pygame.init()
window = pygame.display.set_mode((1400, 1000))
font = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

orig_image = font.render("rotated rectangle", True, (255, 0, 0))
angle = 30


def draw_rect_angle(surf, rect, pivot, angle):
    pts = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft, rect.center]
    pts = [(pygame.math.Vector2(p) - pivot).rotate(-angle) + pivot for p in pts]
    pygame.draw.lines(surf, (255, 255, 0), True, pts, 3)


def create_rotated_rect_points(rect, pivot, angle):
    pts = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft, rect.center]
    rotated_pts = [(pygame.math.Vector2(p) - pivot).rotate(-angle) + pivot for p in pts]

    return {
        "topleft": rotated_pts[0],
        "topright": rotated_pts[1],
        "bottomright": rotated_pts[2],
        "bottomleft": rotated_pts[3],
        "center": rotated_pts[4],
        "midtop": (rotated_pts[0] + rotated_pts[1]) / 2,
        "midright": (rotated_pts[1] + rotated_pts[2]) / 2,
        "midbottom": (rotated_pts[2] + rotated_pts[3]) / 2,
        "midleft": (rotated_pts[3] + rotated_pts[0]) / 2,
        "top": rotated_pts[0].y,
        "right": rotated_pts[1].x,
        "bottom": rotated_pts[2].y,
        "left": rotated_pts[0].x,
        "width": (rotated_pts[1] - rotated_pts[0]).length(),
        "height": (rotated_pts[3] - rotated_pts[0]).length()
        }


def rotate_image_around_pivot(image, pivot, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_offset = pygame.math.Vector2(image.get_rect().center) - pivot
    rotated_offset = rotated_offset.rotate(-angle)
    rotated_rect = rotated_image.get_rect(center=pivot + rotated_offset)
    return rotated_image, rotated_rect


run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    angle += 1
    window.fill(0)
    window_center = window.get_rect().center

    # Calculate the position for the original rectangle
    orig_rect = orig_image.get_rect(center=window_center)
    pivot = orig_rect.midleft
    draw_cross_in_circle(window, (0, 233, 255), pivot, 15)

    # Rotate the image around its pivot point
    rotated_image, rotated_rect = rotate_image_around_pivot(orig_image, pivot, angle)



    # Draw the rectangle outline
    draw_rect_angle(window, orig_rect, pivot, angle)

    rot_rect_points =create_rotated_rect_points(orig_rect, pivot, angle)
    # pygame.draw.lines(window, (255, 0, 0), True, rot_rect_points, 3)

    # Draw the rotated image
    window.blit(rotated_image, rot_rect_points.center)

    pygame.display.flip()

pygame.quit()
exit()
