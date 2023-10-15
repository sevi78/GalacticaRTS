import math

import pygame
from pygame_widgets.util import drawText

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.utils import global_params


def smooth_position(prev_x, prev_y, x, y, smooth):
    new_x, new_y = None, None

    if abs(prev_x - x) > smooth:
        new_x = prev_x + smooth if x > prev_x else prev_x - smooth
    else:
        new_x = x

    if abs(prev_y - y) > smooth:
        new_y = prev_y + smooth if y > prev_y else prev_y - smooth
    else:
        new_y = y

    return new_x, new_y


def rot_center(image, angle, x, y):
    """
    rotates the image around its center
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def get_world_distance(pos_a, pos_b):
    """
    returns the world distance betweeen two positions
    :param pos_a:
    :param pos_b:
    :return: distance
    """
    if global_params.app:
        x, y = pan_zoom_handler.screen_2_world(pos_a[0], pos_a[1])
        x1, y1 = pan_zoom_handler.screen_2_world(pos_b[0], pos_b[1])
    else:
        x, y = pos_a[1], pos_a[0]
        x1, y1 = pos_b[0], pos_b[1]

    distance = math.dist((x, y), (x1, y1))

    return distance


def get_distance(pos_a, pos_b):
    if not pos_a:
        return 0

    x = pos_a[0]
    y = pos_a[1]
    x1 = pos_b[0]
    y1 = pos_b[1]
    distance = math.dist((x, y), (x1, y1))

    return distance


def get_distance_to(self, obj):
    if not obj:
        return 0

    x = self.get_screen_x()
    y = self.get_screen_y()
    x1 = obj.get_screen_x()
    y1 = obj.get_screen_y()
    distance = math.dist((x, y), (x1, y1))

    return distance


def limit_positions(obj, screen_size):
    """
    this hides the obj if it is outside the screen
    """
    # win = pygame.display.get_surface()
    border = 0
    # win_width = win.get_width()
    # win_height = win.get_height()
    x, y = obj.get_position()

    def hide_obj_outside_view():
        if x <= border or x >= screen_size[0] - border or y <= border or y >= screen_size[1] - border:
            obj.hide()
        else:
            obj.show()

    if hasattr(obj, "property"):
        if not obj.property == "ship" or obj.property == "planet":
            hide_obj_outside_view()
    else:
        hide_obj_outside_view()


def hide_obj_outside_view_(obj, win_height, win_width, x, y, zero):
    if x <= zero or x >= win_width:
        obj.hide()
    elif y <= zero or y >= win_height:
        obj.hide()
    else:
        obj.show()


def hide_obj_outside_view__(obj, win_height, win_width, x, y, border):
    if x <= border or x >= win_width - border or y <= border or y >= win_height - border:
        obj.hide()
    else:
        obj.show()


def debug_positions(x, y, color, text, size, **kwargs):
    if not global_params.debug:
        return
    # color = kwargs.get("color", "red")
    # x,y = kwargs.get("x"), kwargs.get("y")
    # size = kwargs.get("size")
    text = text + str(int(x)) + ", " + str(int(y))
    text_spacing = 15

    pygame.draw.circle(global_params.app.win, color, (x, y), size, 1)
    font = pygame.font.SysFont(global_params.font_name, 18)
    drawText(global_params.app.win, text, color, (x, y, 400, 30), font, "left")


def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def prevent_object_overlap(objects, min_dist):
    smoothing = 100
    for obj1 in objects:
        for obj2 in objects:
            if obj1 != obj2:
                distance = distance_between_points(obj1.world_x, obj1.world_y, obj2.world_x, obj2.world_y)
                if distance < min_dist:

                    # Calculate the direction vector
                    dx = obj1.world_x - obj2.world_x
                    dy = obj1.world_y - obj2.world_y

                    # Normalize the direction vector
                    try:
                        length = math.sqrt(dx * dx + dy * dy)
                    except ZeroDivisionError:
                        length = 1

                    try:
                        dx /= length
                        dy /= length
                    except ZeroDivisionError:
                        dx = 1
                        dy = 1

                    # Move the ships apart
                    adjustment = (min_dist - distance) / 2 / smoothing
                    obj1.world_x += dx * adjustment
                    obj1.world_y += dy * adjustment
                    obj2.world_x -= dx * adjustment
                    obj2.world_y -= dy * adjustment


def follow_target(self):
    if self.target:  # and not self.orbit_object:
        if hasattr(self.target, "screen_x"):
            tx, ty = self.target.screen_x, self.target.screen_y

        if self.target.property == "ufo":
            tx, ty = self.target.rect.centerx, self.target.rect.centery

        dx = (self.screen_x - tx)
        dy = (self.screen_y - ty)

        if hasattr(self, "set_speed"):
            speed = self.set_speed()
        else:
            speed = self.speed

        self.world_x -= dx / int(global_params.fps) / float(self.get_zoom()) * float(speed) * float(global_params.time_factor)
        self.world_y -= dy / int(global_params.fps) / float(self.get_zoom()) * float(speed) * float(global_params.time_factor)


def follow_object__(self, obj):
    tx, ty = obj.rect.centerx, obj.rect.centery

    dx = (self.rect.centerx - tx)
    dy = (self.rect.centery - ty)

    if hasattr(self, "set_speed"):
        speed = self.set_speed()
    else:
        speed = self.speed

    self.world_x += dx / int(global_params.fps) / float(self.get_zoom()) * float(speed) * float(global_params.time_factor)
    self.world_y += dy / int(global_params.fps) / float(self.get_zoom()) * float(speed) * float(global_params.time_factor)


def follow_object__(self, obj):
    tx, ty = obj.rect.centerx, obj.rect.centery

    dx = (self.rect.centerx - tx)
    dy = (self.rect.centery - ty)

    # Check the sign of dx and dy to make sure that the object is moving towards obj
    dx = abs(dx) * (-1 if dx < 0 else 1)
    dy = abs(dy) * (-1 if dy < 0 else 1)

    # Get the speed of the object
    speed = self.speed if not hasattr(self, "set_speed") else self.set_speed()

    # Set the new world coordinates based on the object's position and speed
    # self.world_x += dx / pygame.time.get_ticks() / self.get_zoom() * speed * global_params.time_factor
    # self.world_y += dy / pygame.time.get_ticks() / self.get_zoom() * speed * global_params.time_factor

    self.world_x += dx / pygame.time.get_ticks() * speed * global_params.time_factor
    self.world_y += dy / pygame.time.get_ticks() * speed * global_params.time_factor


def follow_object__(self, obj):
    tx, ty = obj.world_x, obj.world_y

    dx = tx - self.world_x
    dy = ty - self.world_y

    distance = math.sqrt(dx * dx + dy * dy)

    if distance > 0:
        dx /= distance
        dy /= distance

        self.world_x += dx * self.speed
        self.world_y += dy * self.speed
    print("follow object")


def follow_object__almost(self, obj):
    tx, ty = obj.world_x, obj.world_y

    dx = tx - self.world_x
    dy = ty - self.world_y

    distance = math.sqrt(dx * dx + dy * dy)

    if distance > 0:
        dx /= distance
        dy /= distance

        # Get the speed of the obj
        obj_speed = obj.speed if hasattr(obj, "speed") else self.speed

        # Set the new world coordinates based on the object's position and speed
        self.world_x += dx * obj_speed
        self.world_y += dy * obj_speed


def orbit__(obj, orbit_obj, orbit_speed, direction):
    pos_diff = pygame.math.Vector2(orbit_obj.world_x, orbit_obj.world_y) - pygame.math.Vector2(obj.world_x, obj.world_y)
    obj.orbit_radius = pos_diff.length()
    if not obj.orbit_angle:
        obj.orbit_angle = pos_diff.angle_to(pygame.math.Vector2(0, 1))
    obj.orbit_angle += orbit_speed
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(obj.angle * direction)  # Rotate by the negative angle
    obj.world_x, obj.world_y = (orbit_obj.world_x + pos.x, orbit_obj.world_y + pos.y)


def orbit(obj, orbit_obj, orbit_speed, direction):
    pos_diff = pygame.math.Vector2(orbit_obj.world_x, orbit_obj.world_y) - pygame.math.Vector2(obj.world_x, obj.world_y)
    obj.orbit_radius = pos_diff.length()
    if not obj.orbit_angle:
        obj.orbit_angle = pos_diff.angle_to(pygame.math.Vector2(0, 1))

    obj.orbit_angle += orbit_speed * global_params.time_factor
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(obj.orbit_angle * direction)  # Rotate by the negative angle
    obj.world_x, obj.world_y = (orbit_obj.world_x + pos.x, orbit_obj.world_y + pos.y)
