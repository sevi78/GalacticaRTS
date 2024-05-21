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


def calc_orbit_position(points, index):
    point_index = int(index)
    next_point_index = (point_index + 1) % len(points)
    fraction = index - point_index

    x1, y1 = points[point_index]
    x2, y2 = points[next_point_index]

    x = x1 + (x2 - x1) * fraction
    y = y1 + (y2 - y1) * fraction

    # center = pan_zoom_handler.world_2_screen(int(x), int(y))
    center = (int(x), int(y))

    return center


def get_nearest_orbit_index(points, pos):
    """
    Returns the index of the nearest position_tuple to pos in the list points.

    Args:
        points (list): A list of position_tuples (x, y) representing orbit points.
        pos (tuple): A position_tuple (x, y) representing the reference point.

    Returns:
        int: The index of the nearest position_tuple to pos in the list points.
    """
    min_distance = float('inf')
    nearest_index = None

    for i, point in enumerate(points):
        distance = math.sqrt((point[0] - pos[0]) ** 2 + (point[1] - pos[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            nearest_index = i

    return nearest_index

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
