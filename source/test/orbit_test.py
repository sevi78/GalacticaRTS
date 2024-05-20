# import math
# import pygame
# import time
#
# # Initialize Pygame
# pygame.init()
# screen = pygame.display.set_mode((600, 600))
# clock = pygame.time.Clock()
#
#
# class PlanetOrbiter:
#     def __init__(self, cx, cy, r):
#         self.cx = cx
#         self.cy = cy
#         self.r = r
#         self.points = self.calculate_circle_points()
#
#     def calculate_circle_points(self):
#         """
#         Calculate the (x, y) coordinates of points on the circumference of a circle.
#
#         Returns:
#             list: A list of (x, y) coordinates for points on the circumference
#         """
#         points = []
#         for angle in range(0, 361, 1):  # Iterate over angles from 0 to 360 degrees
#             rad = angle * math.pi / 180  # Convert angle to radians
#             x = self.cx + self.r * math.cos(rad)  # Calculate x coordinate
#             y = self.cy + self.r * math.sin(rad)  # Calculate y coordinate
#             points.append((int(x), int(y)))  # Add point to the list (convert to int for Pygame)
#         return points
#
#
# class Draw:
#     @staticmethod
#     def draw_circle(points, color, thickness):
#         """
#         Draw a circle on the Pygame window using a list of points.
#
#         Args:
#             points (list): A list of (x, y) coordinates for points on the circumference
#             color (tuple): RGB color value for the circle
#             thickness (int): Line thickness for the circle
#         """
#         pygame.draw.polygon(screen, color, points, thickness)
#         pygame.display.flip()
#
#     @staticmethod
#     def draw_moving_circle(points, radius, index):
#         """
#         Draw a circle at the specified point on the circumference.
#
#         Args:
#             points (list): A list of (x, y) coordinates for points on the circumference
#             radius (int): Radius of the moving circle
#             index (float): Index of the point in the points list (can be a float)
#         """
#         point_index = int(index)
#         next_point_index = (point_index + 1) % len(points)
#         fraction = index - point_index
#
#         x1, y1 = points[point_index]
#         x2, y2 = points[next_point_index]
#
#         x = x1 + (x2 - x1) * fraction
#         y = y1 + (y2 - y1) * fraction
#
#         pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), radius)
#         pygame.display.flip()
#
#
# class OrbitHandler:
#     def __init__(self, planet_orbiter):
#         self.planet_orbiter = planet_orbiter
#         self.index = 0.0
#         self.speed = 0.01 # Pixels per second
#         self.last_time = pygame.time.get_ticks()
#
#     def run(self):
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return
#
#             screen.fill((0, 0, 0))  # Clear the screen
#             Draw.draw_moving_circle(self.planet_orbiter.points, 10, self.index)
#
#             self.update_position()
#
#             clock.tick(60)  # Limit the frame rate to 60 FPS
#
#     def update_position(self):
#         current_time = pygame.time.get_ticks()
#         dt = (current_time - self.last_time) / 1000  # Convert to seconds
#         self.last_time = current_time
#
#         # Calculate the distance to move based on speed and elapsed time
#         distance = self.speed * dt
#
#         # Update the index based on the distance
#         self.index = (
#                                  self.index + distance / self.planet_orbiter.r * len(self.planet_orbiter.points)) % len(self.planet_orbiter.points)
#
#
# def main():
#     # Center and radius of the circle
#     cx, cy = 300, 300
#     r = 100
#
#     # Create instances
#     planet_orbiter = PlanetOrbiter(cx, cy, r)
#     orbit_handler = OrbitHandler(planet_orbiter)
#
#     # Run the simulation
#     orbit_handler.run()
#
#
# if __name__ == "__main__":
#     main()


import math
import pygame
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()


class PlanetOrbiter:
    def __init__(self, cx, cy, r, parent=None, obj_type="sun", color=(255, 0, 0)):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.parent = parent
        self.obj_type = obj_type
        self.color = color
        self.points = self.calculate_circle_points()
        self.index = 0.0
        self.speed = 100 if obj_type == "sun" else 200 if obj_type == "planet" else 300  # Pixels per second
        self.last_time = pygame.time.get_ticks()
        self.children = []

    def calculate_circle_points(self):
        """
        Calculate the (x, y) coordinates of points on the circumference of a circle.

        Returns:
            list: A list of (x, y) coordinates for points on the circumference
        """
        points = []
        for angle in range(0, 361, 1):  # Iterate over angles from 0 to 360 degrees
            rad = angle * math.pi / 180  # Convert angle to radians
            x = self.cx + self.r * math.cos(rad)  # Calculate x coordinate
            y = self.cy + self.r * math.sin(rad)  # Calculate y coordinate
            points.append((int(x), int(y)))  # Add point to the list (convert to int for Pygame)
        return points

    def draw(self):
        """
        Draw the object on the Pygame window.
        """
        if self.obj_type == "sun":
            pygame.draw.circle(screen, self.color, (self.cx, self.cy), self.r)
        else:
            Draw.draw_moving_circle(self.points, self.r // 2, self.index, self.color)

        for child in self.children:
            child.draw()

    def update_position(self):
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_time) / 1000  # Convert to seconds
        self.last_time = current_time

        # Calculate the distance to move based on speed and elapsed time
        distance = self.speed * dt

        # Update the index based on the distance
        if self.parent:
            self.index = (self.index + distance / self.parent.r * len(self.parent.points)) % len(self.parent.points)
        else:
            self.index = 0.0

        for child in self.children:
            child.update_position()


class Draw:
    @staticmethod
    def draw_moving_circle(points, radius, index, color):
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

        pygame.draw.circle(screen, color, (int(x), int(y)), radius)
        pygame.display.flip()


def main():
    # Create suns
    sun1 = PlanetOrbiter(400, 400, 50, None, "sun", (255, 255, 0))
    sun2 = PlanetOrbiter(200, 200, 30, None, "sun", (255, 165, 0))
    sun3 = PlanetOrbiter(600, 600, 40, None, "sun", (255, 215, 0))

    # Create planets orbiting around suns
    planet1 = PlanetOrbiter(400, 400, 150, sun1, "planet", (0, 255, 0))
    planet2 = PlanetOrbiter(200, 200, 100, sun2, "planet", (0, 255, 255))
    planet3 = PlanetOrbiter(600, 600, 120, sun3, "planet", (255, 0, 255))

    # Create moons orbiting around planets
    moon1 = PlanetOrbiter(400, 400, 30, planet1, "moon", (128, 128, 128))
    moon2 = PlanetOrbiter(200, 200, 20, planet2, "moon", (192, 192, 192))
    moon3 = PlanetOrbiter(600, 600, 25, planet3, "moon", (128, 128, 128))

    # Add planets to suns
    sun1.children.append(planet1)
    sun2.children.append(planet2)
    sun3.children.append(planet3)

    # Add moons to planets
    planet1.children.append(moon1)
    planet2.children.append(moon2)
    planet3.children.append(moon3)

    # Run the simulation
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))  # Clear the screen

        sun1.draw()
        sun2.draw()
        sun3.draw()

        sun1.update_position()
        sun2.update_position()
        sun3.update_position()

        clock.tick(60)  # Limit the frame rate to 60 FPS


if __name__ == "__main__":
    main()
