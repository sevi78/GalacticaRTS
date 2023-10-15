import math
from pygame import Vector2

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.utils.positioning import rot_center

GAME_OBJECT_SPEED = 2.0
screen = global_params.win
explosions = sprite_groups.explosions


class PanZoomGameObject(PanZoomSprite):
    __slots__ = PanZoomSprite.__slots__ + ('moving', 'rotation_smoothing', 'explode_if_target_reached',
                                           'explosion_relative_gif_size', 'exploded',
                                           'attack_distance_raw', 'attack_distance', 'target', 'rotate_to_target',
                                           'rotate_correction_angle',
                                           'prev_angle', 'move_to_target', 'target_position', 'target_reached', 'speed')

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)

        self.moving = False
        self.rotation_smoothing = 15
        self.explode_if_target_reached = kwargs.get("explode_if_target_reached", False)
        self.explosion_relative_gif_size = kwargs.get("explosion_relative_gif_size", 1.0)
        self.exploded = False
        self.attack_distance_raw = 5.0
        self.attack_distance = self.attack_distance_raw
        self.target = None
        self.rotate_to_target = kwargs.get("rotate_to_target", True)
        self.rotate_correction_angle = 0
        self.prev_angle = None
        self.move_to_target = kwargs.get("move_to_target", False)
        self.target_position = Vector2(0, 0)
        self.target_reached = False

        # speed
        self.speed = GAME_OBJECT_SPEED



    def set_attack_distance(self):
        self.attack_distance = self.attack_distance_raw * self.pan_zoom.zoom

    def set_target(self, obj):
        self.target = obj

    def set_target_position(self):
        if hasattr(self.target, "property"):
            if self.target.property == "planet":
                self.target_position = self.pan_zoom.screen_2_world(self.target.screen_x, self.target.screen_y)
                return

            if self.target.property == "ship":
                self.target_position = self.target.rect.center

            if self.target.property == "ufo":
                self.target_position = self.target.rect.center

                # self.target_position = Vector2((self.target.world_x, self.target.world_y))

        # elif hasattr(self.target, "world_x"):
        #     self.target_position = Vector2((self.target.world_x, self.target.world_y))
        #
        if hasattr(self.target, "align_image"):
            if self.target.align_image == "center":
                self.target_position = Vector2((self.target.world_x, self.target.world_y))

            elif self.target.align_image == "topleft":
                self.target_position = Vector2((
                    self.target.world_x + self.target.world_width / 2,
                    self.target.world_y + self.target.world_height / 2))

            elif self.target.align_image == "bottomleft":
                self.target_position = Vector2((
                    self.target.world_x + self.target.world_width / 2,
                    self.target.world_y - self.target.world_height / 2))

            elif self.target.align_image == "topright":
                self.target_position = Vector2((
                    self.target.world_x - self.target.world_width / 2,
                    self.target.world_y + self.target.world_height / 2))

            elif self.target.align_image == "bottomright":
                self.target_position = Vector2((
                    self.target.world_x - self.target.world_width / 2,
                    self.target.world_y - self.target.world_height / 2))

    def rotate_image_to_target(self, **kwargs):
        # 0 - image is looking to the right
        # 90 - image is looking up
        # 180 - image is looking to the left
        # 270 - image is looking down
        target = kwargs.get("target", self.target)
        rotate_correction_angle = kwargs.get("rotate_correction_angle", self.rotate_correction_angle)

        if target:
            rel_x, rel_y = target.rect.centerx - self.rect.x, target.rect.centery - self.rect.y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - rotate_correction_angle
        else:
            if self.prev_angle:
                angle = self.prev_angle + 1
            else:
                angle = 0

        # Smoothing algorithm
        if self.prev_angle:
            diff = angle - self.prev_angle
            if abs(diff) > self.rotation_smoothing:
                angle = self.prev_angle + 5 * (diff / abs(diff))

        self.prev_angle = angle
        new_image, new_rect = rot_center(self.image, angle, self.rect.x, self.rect.y)
        self.image = new_image
        self.rect = new_rect

    def move_towards_target(self):
        self.moving = True
        direction = self.target_position - Vector2(self.world_x, self.world_y)

        # Calculate the distance between the current position and the target position
        distance = direction.length() * self.get_zoom()

        # pygame.draw.circle(global_params.win, pygame.color.THECOLORS["purple"], self.rect.center, distance, 1)
        # pygame.draw.circle(global_params.win, pygame.color.THECOLORS["orange"], self.rect.center, self.attack_distance, 1)

        # Check if the distance is zero (bullet is already at the target position)
        if distance < self.attack_distance:
            self.target_reached = True
            return

        # Normalize the direction vector
        direction.normalize()

        # Calculate the displacement vector for each time step
        displacement = direction * self.speed * global_params.time_factor

        # Calculate the number of time steps needed to reach the target position
        time_steps = int(distance / self.speed) / self.get_zoom()

        # Move the obj towards the target position with a constant speed
        try:
            self.world_x += displacement.x / time_steps
            self.world_y += displacement.y / time_steps
        except ZeroDivisionError:
            pass
            # print("move_towards_target.ZeroDivisionError")

    def explode(self, **kwargs):
        sound = kwargs.get("sound", None)
        x, y = self.world_x, self.world_y
        if not self.exploded:
            explosion = PanZoomSprite(screen, x, y, 40, 40, self.pan_zoom, "explosion.gif",
                loop_gif=False, kill_after_gif_loop=True, align_image="center",
                relative_gif_size=self.explosion_relative_gif_size, layer=10, sound=sound)
            explosions.add(explosion)
            self.exploded = True
        if hasattr(self, "__delete__"):
            self.__delete__(self)
        self.kill()

    def update_pan_zoom_game_object(self):
        if global_params.game_paused:
            return
        self.update_pan_zoom_sprite()
        self.set_attack_distance()

        if self.target:
            if self.rotate_to_target:
                self.rotate_image_to_target()

            if self.move_to_target:
                self.moving = True
                self.set_target_position()
                self.move_towards_target()

        if self.target_reached:
            if self.explode_if_target_reached:
                self.explode()
            if hasattr(self, "damage"):
                self.damage()

    def update(self):
        self.update_pan_zoom_game_object()
