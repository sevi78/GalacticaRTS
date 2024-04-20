import copy
import math

from pygame import Vector2

from source.configuration.game_config import config
from source.handlers.image_handler import outline_image
from source.handlers.position_handler import rot_center
from source.interaction.interaction_handler import InteractionHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite

GAME_OBJECT_SPEED = 2.0
screen = config.win


class PanZoomGameObject(PanZoomSprite, InteractionHandler):
    __slots__ = PanZoomSprite.__slots__ + ('moving', 'rotation_smoothing', 'explode_if_target_reached',
                                           'explosion_relative_gif_size', 'exploded',
                                           'attack_distance_raw', 'attack_distance', 'target', 'rotate_to_target',
                                           'rotate_correction_angle',
                                           'prev_angle', 'move_to_target', 'target_position', 'target_reached', 'speed')

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        InteractionHandler.__init__(self)

        self.initial_rotation = kwargs.get("initial_rotation", 0)
        self.moving = False
        self.rotation_smoothing = kwargs.get("rotation_smoothing", 10)
        self.explode_if_target_reached = kwargs.get("explode_if_target_reached", False)
        self.explosion_relative_gif_size = kwargs.get("explosion_relative_gif_size", 1.0)
        self.explosion_name = kwargs.get("explosion_name", "explosion.gif")
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

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        if hasattr(self, "on_hover"):
            if self.on_hover:
                self.image_outline = outline_image(copy.copy(self.image), self.frame_color, self.outline_threshold, self.outline_thickness)

    def set_attack_distance(self):
        self.attack_distance = self.attack_distance_raw * self.pan_zoom.zoom

    def set_target(self, obj):
        if self.target:
            if obj != self.target:
                if hasattr(self.target, "under_attack"):
                    if self.target.under_attack:
                        self.target.under_attack = False

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
        """
        # 0 - image is looking to the right
        # 90 - image is looking up
        # 180 - image is looking to the left
        # 270 - image is looking down
        """

        target = kwargs.get("target", self.target)
        rotate_correction_angle = kwargs.get("rotate_correction_angle", self.rotate_correction_angle)

        if target:
            rel_x, rel_y = target.rect.centerx - self.rect.x, target.rect.centery - self.rect.y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - rotate_correction_angle
        else:
            if self.prev_angle:
                angle = self.prev_angle + 1
            else:
                angle = self.initial_rotation

        # Smoothing algorithm
        if self.prev_angle:
            diff = angle - self.prev_angle
            if abs(diff) > self.rotation_smoothing:
                angle = self.prev_angle + 5 * (diff / abs(diff))

        self.prev_angle = angle
        new_image, new_rect = rot_center(self.image, angle, self.rect.x, self.rect.y, align="shipalign")
        self.image = new_image
        self.rect = new_rect

    def move_towards_target__(self):
        self.moving = True
        direction = self.target_position - Vector2(self.world_x, self.world_y)

        # Calculate the distance between the current position and the target position
        distance = direction.length() * self.get_zoom()

        # Check if the distance is zero (bullet is already at the target position)
        if distance < self.attack_distance:
            self.target_reached = True
            return

        # Normalize the direction vector
        try:
            direction.normalize()
        except Exception as e:
            print(f"move_towards_target error! (direction.normalize()):{e}")

        # Calculate the displacement vector for each time step
        displacement = direction * self.speed * config.game_speed

        # Calculate the number of time steps needed to reach the target position
        time_steps = int(distance / self.speed) / self.get_zoom()

        # Move the obj towards the target position with a constant speed
        try:
            self.world_x += displacement.x / time_steps
            self.world_y += displacement.y / time_steps
        except ZeroDivisionError as e:
            print(f"move_towards_target error! (self.world_x += displacement.x / time_steps...):{e}")

    def move_towards_target(self):
        self.moving = True
        direction = self.target_position - Vector2(self.world_x, self.world_y)
        distance = direction.length() * self.get_zoom()
        if distance < self.attack_distance:
            self.target_reached = True
            return
        if direction.length() != 0:
            direction.normalize()
        else:
            print("move_towards_target error! direction vector length is zero.")
            return
        displacement = direction * self.speed * config.game_speed
        time_steps = int(distance / self.speed) / self.get_zoom()
        if time_steps != 0:
            self.world_x += displacement.x / time_steps
            self.world_y += displacement.y / time_steps
        else:
            print("move_towards_target error! time_steps is zero.")

    def explode(self, **kwargs):
        # self.explode_calls += 1
        sound = kwargs.get("sound", None)
        size = kwargs.get("size", (40, 40))

        x, y = self.world_x, self.world_y
        if not self.exploded:
            explosion = PanZoomSprite(
                screen, x, y, size[0], size[1], self.pan_zoom, self.explosion_name,
                loop_gif=False, kill_after_gif_loop=True, align_image="center",
                relative_gif_size=self.explosion_relative_gif_size,
                layer=10, sound=sound, group="explosions", name="explosion")

            self.exploded = True

        if hasattr(self, "__delete__"):
            self.__delete__(self)
        self.kill()

    def update_pan_zoom_game_object(self):
        # if config.game_paused:
        #     return
        self.update_pan_zoom_sprite()
        if config.game_paused:
            return

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
