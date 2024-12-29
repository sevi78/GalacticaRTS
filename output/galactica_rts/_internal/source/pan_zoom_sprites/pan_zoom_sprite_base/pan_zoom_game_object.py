import copy
import math

from pygame import Vector2

from source.configuration.game_config import config
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.time_handler import time_handler
from source.interaction.interaction_handler import InteractionHandler
from source.multimedia_library.images import outline_image, rotate_image_to
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

        self.angle = 0
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
                # self.target_position = self.pan_zoom.screen_2_world(self.target.screen_x, self.target.screen_y)
                self.target_position = self.pan_zoom.screen_2_world(self.target.rect.centerx, self.target.rect.centery)
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

    def move_towards_target(self):
        self.moving = True
        direction = self.target_position - Vector2(self.world_x, self.world_y)
        distance = direction.length() * pan_zoom_handler.get_zoom()
        if distance < self.attack_distance:
            self.target_reached = True
            return
        if direction.length() != 0:
            direction.normalize()
        else:
            # print("move_towards_target error! direction vector length is zero.")
            return
        displacement = direction * self.speed * time_handler.game_speed
        time_steps = distance / self.speed / pan_zoom_handler.get_zoom()
        if time_steps != 0:
            self.world_x += displacement.x / time_steps
            self.world_y += displacement.y / time_steps
        # else:
        #     print("move_towards_target error! time_steps is zero.")

    def move_towards_target_with_gravity(self):
        self.moving = True
        direction = self.target_position - Vector2(self.world_x, self.world_y)
        distance = direction.length() * pan_zoom_handler.get_zoom()

        if distance < self.attack_distance:
            self.target_reached = True
            return

        # Calculate initial velocity components
        initial_velocity = self.speed
        angle_rad = math.radians(self.initial_rotation-self.rotate_correction_angle)
        vx = initial_velocity * math.cos(angle_rad)
        vy = +initial_velocity * math.sin(angle_rad)  # Negative because y increases downward

        # Simulate gravity (adjust this value to change the curve)
        gravity = 9.8 * 0.1  # Reduced gravity for game purposes

        # Calculate new position
        time_step = time_handler.game_speed
        self.world_x += vx * time_step
        self.world_y += vy * time_step + 0.5 * gravity * time_step ** 2  # Add gravity (positive y is downward)

        # Update velocity for next frame
        vy += gravity * time_step

        # Update missile rotation to face direction of travel
        new_angle = math.degrees(math.atan2(vy, vx))  # Remove negative sign from vy
        self.angle = (new_angle + 360) % 360  # Normalize angle to 0-360 range

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
        # pygame.draw.rect(self.win, self.frame_color, self.collide_rect, 1)
        # if config.game_paused:
        #     return
        self.update_pan_zoom_sprite()
        if config.game_paused:
            return

        self.set_attack_distance()

        if self.target:
            if self.rotate_to_target:
                self.angle = rotate_image_to(self, self.target.rect.center, self.rotate_correction_angle)

            if self.move_to_target:
                self.moving = True
                self.set_target_position()
                # if self.initial_rotation != 0:
                #     self.move_towards_target_with_gravity()
                # else:
                self.move_towards_target()

        if self.target_reached:
            if self.explode_if_target_reached:
                self.explode()
            if hasattr(self, "damage"):
                self.damage()

    def update(self):
        self.update_pan_zoom_game_object()
