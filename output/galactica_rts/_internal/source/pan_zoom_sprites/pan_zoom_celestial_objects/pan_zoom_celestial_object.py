import random

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.handlers.time_handler import time_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite


class PanZoomCelestialObject(PanZoomSprite):
    # __slots__ = WidgetBase.__slots__
    # __slots__ += (
    #     'speed', 'direction', 'rotation', 'rotation_direction', 'rotation_speed', 'layer', 'type', 'world_x', 'world_y',
    #     'world_width', 'height', 'image', 'image_raw', 'rect', 'rotateable', 'colors', 'start_pulse', 'pulse_time',
    #     'pulsating_star_size', 'pulsating_star_color', 'color_index', 'gif', 'gif_handler', 'parent', 'ui_parent',
    #     'zoomable')
    possible_directions = [-1, 1]

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        # WidgetBase.__init__(self, win, x, y, width, height, is_sub_widget, **kwargs)
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.speed = random.uniform(0.1, 1.5)
        self.direction = (random.uniform(-self.speed, self.speed), random.uniform(-self.speed, self.speed))
        self.rotation = 0
        self.rotation_direction = random.choice(PanZoomCelestialObject.possible_directions)
        self.rotation_speed = random.uniform(0.1, 1.0)
        self.type = kwargs.get("type", "star")
        self.rotateable = ["galaxy", "nebulae", "asteroid", "comet"]

        # colors
        # Generate a list of random colors
        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(10)]

        # start pulse
        self.start_pulse = random.random()
        self.pulse_time = random.uniform(0.5, 3.0)
        self.pulsating_star_size = random.randint(1, 3)
        self.pulsating_star_color = (random.randint(110, 255), random.randint(110, 255), random.randint(110, 255))

        # Initialize the color index
        self.color_index = 0
        self.zoomable = True

    def move(self, direction):
        if direction:
            self.world_x += direction[0] * time_handler.game_speed
            self.world_y += direction[1] * time_handler.game_speed
        else:
            self.world_x -= self.speed * time_handler.game_speed
            self.world_y += self.speed * time_handler.game_speed / 2

        if self.world_x > config.scene_width * config.quadrant_amount:
            self.world_x = 0
        if self.world_x < 0:
            self.world_x = config.scene_width * config.quadrant_amount

        if self.world_y > config.scene_height * config.quadrant_amount:
            self.world_y = 0
        if self.world_y < 0:
            self.world_y = config.scene_height * config.quadrant_amount

        self.set_world_position((self.world_x, self.world_y))

    def update(self):
        self.update_pan_zoom_sprite()
        if not level_of_detail.inside_screen(self.rect.center):
            return

        self.draw()

    def draw(self):
        if self._hidden:
            return
        if not self.image_name == "no_image.png":
            self.win.blit(self.image, self.rect)
