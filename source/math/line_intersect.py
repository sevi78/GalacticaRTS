import math

import pygame


def sign(x):
    return -1 if x < 0 else 1


def point_on_line_segment(p, l1, l2):
    # Check if point p is on the line segment defined by l1 and l2
    x, y = p
    x1, y1 = l1
    x2, y2 = l2

    # Check if the point is within the bounding box of the line segment
    if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        # Check if the point lies on the line using the line equation
        if abs((y2 - y1) * (x - x1) - (x2 - x1) * (y - y1)) < 1e-9:
            return True
    return False


def interectLineCircle(l1, l2, cpt, r):
    x1 = l1[0] - cpt[0]
    y1 = l1[1] - cpt[1]
    x2 = l2[0] - cpt[0]
    y2 = l2[1] - cpt[1]
    dx = x2 - x1
    dy = y2 - y1
    dr = math.sqrt(dx * dx + dy * dy)
    D = x1 * y2 - x2 * y1
    discriminant = r * r * dr * dr - D * D

    if discriminant < 0:
        return []

    intersection_points = []

    if discriminant == 0:
        point = ((D * dy) / (dr * dr) + cpt[0], (-D * dx) / (dr * dr) + cpt[1])
        if point_on_line_segment(point, l1, l2):
            intersection_points.append(point)
    else:
        xa = (D * dy + sign(dy) * dx * math.sqrt(discriminant)) / (dr * dr)
        xb = (D * dy - sign(dy) * dx * math.sqrt(discriminant)) / (dr * dr)
        ya = (-D * dx + abs(dy) * math.sqrt(discriminant)) / (dr * dr)
        yb = (-D * dx - abs(dy) * math.sqrt(discriminant)) / (dr * dr)

        point_a = (xa + cpt[0], ya + cpt[1])
        point_b = (xb + cpt[0], yb + cpt[1])

        if point_on_line_segment(point_a, l1, l2):
            intersection_points.append(point_a)
        if point_on_line_segment(point_b, l1, l2):
            intersection_points.append(point_b)

    return intersection_points


def draw_intersection(window, cpt, isect, l1, l2, r):
    pygame.draw.line(window, "white", l1, l2, 3)
    pygame.draw.circle(window, "white", cpt, r, 3)
    for p in isect:
        pygame.draw.circle(window, "red", p, 5)


def main():
    window = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    l1 = [50, 0]
    l2 = [450, 300]
    r = 50

    run = True
    while run:
        clock.tick(250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill("black")

        cpt = pygame.mouse.get_pos()
        isect = interectLineCircle(l1, l2, cpt, r)

        print(isect)

        draw_intersection(window, cpt, isect, l1, l2, r)
        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
