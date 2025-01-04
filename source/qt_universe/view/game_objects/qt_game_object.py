import math

from source.qt_universe.view.game_objects.qt_points import Point


# from source.pan_zoom_quadtree.model.points import Point


def calculate_mass(width, height, density=5000, scaling_factor=1e-10):
    # Assume the planet is a sphere with diameter equal to the average of width and height
    diameter = (width + height) / 2
    radius = diameter / 2

    # Calculate volume (4/3 * pi * r^3)
    volume = (4 / 3) * math.pi * (radius ** 3)

    # Calculate mass
    mass = volume * density

    # Scale the mass to be within a reasonable range for the simulation
    return mass * scaling_factor


class GameObject(Point):
    def __init__(self, x, y, width, height, image_name, color, type, orbit_angle=0, orbit_speed=0.01):
        super().__init__(x, y, width, height)
        self.color = color
        self.image_name = image_name
        self.type = type
        self.orbit_object = None

        # self.rect_raw = pygame.rect.Rect(x, y, width, height)
        # self.rect = pygame.rect.Rect(0, 0, 0, 0)
        self.selected = False

        # self.mass = calculate_mass(self.width, self.height)

        self.vx = 0
        self.vy = 0
        self.lod = 0

        self.orbit_angle = orbit_angle
        self.orbit_speed = orbit_speed  # Adjust this value to change orbital speed
