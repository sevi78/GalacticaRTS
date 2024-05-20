import math

import pygame.display

from source.handlers.pan_zoom_handler import pan_zoom_handler


def calculate_circle_points__(cx, cy, r, resolution = 360):
    """
    Calculate the (x, y) coordinates of points on the circumference of a circle.

    Returns:
        list: A list of (x, y) coordinates for points on the circumference
    """
    points = []
    for angle in range(0, resolution + 1, 1):  # Iterate over angles from 0 to 360 degrees
        rad = angle * math.pi / 180  # Convert angle to radians
        x = cx + r * math.cos(rad)  # Calculate x coordinate
        y = cy + r * math.sin(rad)  # Calculate y coordinate
        points.append((int(x), int(y)))  # Add point to the list (convert to int for Pygame)
    return points

import math

def calculate_circle_points(cx, cy, r, resolution=360):
    """
    Calculate the (x, y) coordinates of points on the circumference of a circle.

    Args:
        cx (int): The x-coordinate of the circle center.
        cy (int): The y-coordinate of the circle center.
        r (int): The radius of the circle.
        resolution (int, optional): The number of points to calculate on the circumference. Defaults to 360.

    Returns:
        list: A list of (x, y) coordinates for points on the circumference.
    """
    points = []
    for angle in range(resolution):
        rad = angle * 2 * math.pi / resolution  # Calculate the angle in radians
        x = cx + r * math.cos(rad)  # Calculate x coordinate
        y = cy + r * math.sin(rad)  # Calculate y coordinate
        points.append((int(x), int(y)))  # Add point to the list (convert to int for Pygame)

    return points

def draw_circle(surface, points, color, thickness):
    """
    Draw a circle on the Pygame window using a list of points.

    Args:
        points (list): A list of (x, y) coordinates for points on the circumference
        color (tuple): RGB color value for the circle
        thickness (int): Line thickness for the circle
    """
    pygame.draw.polygon(surface, color, points, thickness)
    # pygame.display.flip()


def draw_moving_circle__(surface, points, radius, index, color):
    """
    Draw a circle at the specified point on the circumference.

    Args:
        points (list): A list of (x, y) coordinates for points on the circumference
        radius (int): Radius of the moving circle
        index (float): Index of the point in the points list (can be a float)
        color (tuple): RGB color value for the circle
    """
    point_index = int(index)
    next_point_index = (point_index + 1) % len(points)
    fraction = index - point_index

    x1, y1 = points[point_index]
    x2, y2 = points[next_point_index]

    x = x1 + (x2 - x1) * fraction
    y = y1 + (y2 - y1) * fraction

    pygame.draw.circle(surface, color, (int(x), int(y)), radius)


def draw_moving_circle(surface, points, radius, index, color, obj):
    """
    Draw a circle at the specified point on the circumference.

    Args:
        points (list): A list of (x, y) coordinates for points on the circumference
        radius (int): Radius of the moving circle
        index (float): Index of the point in the points list (can be a float)
        color (tuple): RGB color value for the circle
    """
    point_index = int(index)
    next_point_index = (point_index + 1) % len(points)
    fraction = index - point_index

    x1, y1 = points[point_index]
    x2, y2 = points[next_point_index]

    x = x1 + (x2 - x1) * fraction
    y = y1 + (y2 - y1) * fraction


    # center = pan_zoom_handler.world_2_screen(int(x), int(y))
    center = (int(x), int(y))
    pygame.draw.circle(surface, color, center, radius)

# def main():
#     # Initialize Pygame
#     pygame.init()
#     screen = pygame.display.set_mode((800, 800))
#     clock = pygame.time.Clock()
#
#     all_points = []
#     points = calculate_circle_points(100,100,50, resolution= 10)
#     all_points.append(points)
#
#     points = calculate_circle_points(200, 200, 150, resolution=5)
#     all_points.append(points)
#
#     points = calculate_circle_points(200, 200, 150, resolution=1005)
#     all_points.append(points)
#
#     running = True
#     while running:
#         for i in all_points:
#             draw_circle(screen, i, pygame.color.THECOLORS.get("red"), 1)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#
#
#
# if __name__ == "__main__":
#     main()
