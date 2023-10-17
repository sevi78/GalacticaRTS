import random

import pygame

from source.gui.lod import inside_screen
from source.gui.widgets.progress_bar import ProgressBar
from source.gui.widgets.widget_base_components.interaction_handler import InteractionHandler
from source.gui.widgets.widget_handler import WidgetHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_game_object import PanZoomGameObject
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups

from source.utils import global_params
from source.utils.colors import colors
from source.utils.mouse import Mouse, MouseState
from source.database.saveload import load_file

# pan_zoom_ufo_config = load_file("pan_zoom_ufo_config.json")
pan_zoom_ufo_config = load_file("enemy_handler_config.json")["enemy handler"]


class PanZoomUfo(PanZoomGameObject, InteractionHandler):
    __slots__ = PanZoomGameObject.__slots__ + (
        'random_target_intervall', 'frame_color', '_disabled', '_hidden', 'move_to_target', 'rotate_to_target',
        'speed', 'orbit_speed', 'exploded', 'energy', 'energy_max', 'name', 'property', 'target', 'tooltip',
        'attack_distance_raw', 'attack_distance', 'progress_bar', 'gun_power', "_on_hover", "on_hover_release")

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        InteractionHandler.__init__(self)
        self.random_target_intervall = pan_zoom_ufo_config["random_target_intervall"]
        self.frame_color = colors.frame_color
        self._disabled = False
        self._hidden = False
        self.move_to_target = True
        self.rotate_to_target = False
        self.speed = pan_zoom_ufo_config["speed"]
        self.orbit_speed = pan_zoom_ufo_config["orbit_speed"]
        self.exploded = False

        self.energy = pan_zoom_ufo_config["energy"]
        self.energy_max = self.energy
        self.name = "ufo"
        self.property = "ufo"
        self.target = None

        # self.set_random_target()

        # self.set_target(random.choice(global_params.planets))
        # self.set_target(sprite_groups.planets.sprites()[0])
        self.set_target(sprite_groups.planets.sprites()[0])
        self.tooltip = "this is a u.f.o,   might be dangerous!"
        self.property = "ufo"
        self.attack_distance_raw = pan_zoom_ufo_config["attack_distance"]
        self.attack_distance = self.attack_distance_raw

        # energy progress bar
        self.progress_bar = ProgressBar(win=self.win,
            x=self.screen_x,
            y=self.screen_y + self.screen_height + self.screen_height / 5,
            width=self.screen_width,
            height=5,
            progress=lambda: 1 / self.energy_max * self.energy,
            curved=True,
            completedColour=self.frame_color,
            layer=self.layer,
            parent=self
            )

        # gun
        self.gun_power = pan_zoom_ufo_config["gun_power"]

        # register
        sprite_groups.ufos.add(self)
        #print(sprite_groups.ufos)

    def setup(self):
        data = load_file("enemy_handler_config.json")
        for name, dict in data.items():

            for key, value in dict.items():
                if key in self.__dict__ or key in self.__slots__:
                    setattr(self, key, value)

    def set_random_target(self, **kwargs):
        immediately = kwargs.get("immediately")
        if immediately:
            self.set_target(random.choice(sprite_groups.planets.sprites()))
            self.target_reached = False
            return

        r = random.randint(0, self.random_target_intervall)
        if r == 1:
            self.set_target(random.choice(sprite_groups.planets.sprites()))
            self.target_reached = False

    def flickering(self):
        if not inside_screen(self.get_screen_position()):
            return

        r = random.randint(-3, 4)
        r2 = random.randint(0, 9)

        startpos = self.rect.center
        endpos = self.target.rect.center

        if r == 3:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["red"], width=r2)

        if r == 2:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["blue"], width=r * 2)

        self.damage()

    def damage(self):

        if not self.target:
            return

        if self.target.property == "ship":
            self.target.energy -= self.gun_power
            if self.target.energy < 0:
                self.target.explode()
                self.set_random_target(immediately=True)

        if self.target.population > 0:
            self.target.population -= self.gun_power / 100
            global_params.app.event_text = f"ufo attack !!!!, people are getting killed ! {int(self.target.population)}"

    def listen(self):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()
            global_params.app.tooltip_instance.reset_tooltip(self)

            if self.rect.collidepoint(x, y):
                if mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:

                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            global_params.tooltip_text = self.tooltip

    def end_object(self):
        self.explode(sound="explosion")
        WidgetHandler.remove_widget(self.progress_bar)
        self.progress_bar = None
        self.kill()

    def update(self):
        if not global_params.game_paused:
            self.update_pan_zoom_game_object()
            self.set_attack_distance()
            self.set_random_target()

            if self.energy <= 0:
                self.end_object()

            if self.target_reached:
                self.flickering()

        self.listen()

        if hasattr(self, "progress_bar"):
            if self.progress_bar:
                self.progress_bar.set_progressbar_position()

        # self.debug_object()
