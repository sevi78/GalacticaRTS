import random
import time

import pygame

from source.configuration.game_config import config
from source.gui.event_text import event_text
from source.gui.lod import level_of_detail
from source.gui.widgets.progress_bar import ProgressBar
from source.handlers.color_handler import colors
from source.handlers.file_handler import load_file
from source.handlers.garbage_handler import garbage_handler
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.weapon_handler import WeaponHandler
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.gif_handler import GifHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_game_object import PanZoomGameObject
from source.text.info_panel_text_generator import info_panel_text_generator

# lifetime in seconds
LIFETIME = 60

pan_zoom_ufo_config = load_file("enemy_handler_config.json", "config")["enemy handler"]

SHRINK_FACTOR = 0.005


class PanZoomUfo(PanZoomGameObject):  # , InteractionHandler):
    __slots__ = PanZoomGameObject.__slots__ + (
        'random_target_interval', 'frame_color', '_disabled', '_hidden', 'move_to_target', 'rotate_to_target',
        'speed', 'orbit_speed', 'exploded', 'energy', 'energy_max', 'name', 'property', 'target', 'tooltip',
        'attack_distance_raw', 'attack_distance', 'progress_bar', 'gun_power', "_on_hover", "on_hover_release")

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        # InteractionHandler.__init__(self)
        self.id = kwargs.get("id", 0)
        self.lifetime = kwargs.get("lifetime", LIFETIME)
        self.shrink = 0.0
        self.creation_time = time.time()
        self.elapsed_time = 0.0
        self.info_text = kwargs.get("infotext", "")
        self.random_target_interval = pan_zoom_ufo_config["random_target_interval"]
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
        self.food = kwargs.get("food", 100)
        self.food_max = 200
        self.minerals = kwargs.get("minerals", 100)
        self.minerals_max = 200
        self.water = kwargs.get("water", 100)
        self.water_max = 200
        self.population = kwargs.get("population", 100)
        self.population_max = 200
        self.technology = kwargs.get("technology", 100)
        self.technology_max = 200

        self.resources = {
            "minerals": self.minerals,
            "food": self.food,
            "population": self.population,
            "water": self.water,
            "technology": self.technology
            }
        self.specials = []
        self.attitude = kwargs.get("attitude", random.randint(0, 100))
        self.attitude_text = "friendly" if self.attitude > 50 else "hostile"
        self.name = "ufo"
        self.property = "ufo"
        self.target = None
        self.set_target(random.choice([_ for _ in sprite_groups.planets.sprites() if _.type != "sun"]))
        self.tooltip = "this is a u.f.o,   might be dangerous!"
        self.attack_distance_raw = pan_zoom_ufo_config["attack_distance"]
        self.attack_distance = self.attack_distance_raw
        self.gun_power = 10
        self.emp_attacked = False
        self.gif = "electro_discharge.gif"
        self.gif_handler = GifHandler(self, self.gif, loop=True, relative_gif_size=1.2, offset_y=5, layer=self.layer + 1)

        # energy progress bar
        self.progress_bar = ProgressBar(
                win=self.win,
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
        self.weapon_handler = WeaponHandler(self, kwargs.get("current_weapon", "laser"))
        self.weapon_handler.gun_power = pan_zoom_ufo_config["gun_power"]

        # register
        sprite_groups.ufos.add(self)

    def setup(self):
        data = pan_zoom_ufo_config
        for name, dict in data.items():
            for key, value in dict.items():
                if key in self.__dict__ or key in self.__slots__:
                    setattr(self, key, value)

    def set_random_target(self, **kwargs):
        immediately = kwargs.get("immediately")
        planets = [_ for _ in sprite_groups.planets.sprites() if _.type != "sun"]
        if immediately:
            self.set_target(random.choice(planets))
            self.target_reached = False
            return

        r = random.randint(0, self.random_target_interval)
        if r == 1:
            self.set_target(random.choice(planets))
            self.target_reached = False

    def flickering(self):
        if self.emp_attacked:
            return

        if self.attitude > 50:
            return

        if not level_of_detail.inside_screen(self.get_screen_position()):
            return
        r = random.randint(-3, 4)
        r2 = random.randint(0, 6)
        startpos = self.rect.center
        endpos = self.target.rect.center
        colors = [pygame.color.THECOLORS["blue"], pygame.color.THECOLORS["purple"], pygame.color.THECOLORS["pink"]]

        if r == 3:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                    color=random.choice(colors), width=r2)
        if r == 2:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                    color=random.choice(colors), width=r * 2)

        self.damage()

    def damage(self):
        if not self.target:
            return

        if self.target.property == "ship":
            self.target.energy -= self.weapon_handler.gun_power
            if self.target.energy < 0:
                self.target.explode()
                self.set_random_target(immediately=True)

        if self.target.population - self.weapon_handler.gun_power / 100 > 0:
            self.target.under_attack = True
            self.target.population -= self.weapon_handler.gun_power / 100
            event_text.set_text(f"ufo attack !!!!, people are getting killed at {self.target.name}! population: {int(self.target.population)}", obj=self.target)

    def listen(self):
        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()
            config.app.tooltip_instance.reset_tooltip(self)

            if self.rect.collidepoint(x, y):
                if mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                    # self.win.blit(self.image_outline, self.rect)
                    self.win.blit(pygame.transform.scale(self.image_outline, self.rect.size), self.rect)
                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            config.tooltip_text = self.tooltip

                    if self.info_text:
                        if self.info_text != "":
                            # config.app.info_panel.text = self.info_text
                            self.info_text = info_panel_text_generator.create_info_panel_ufo_text(self)
                            config.app.info_panel.set_text(self.info_text)
                            config.app.info_panel.set_planet_image(self.image_raw, size=(
                                self.image_raw.get_width(), self.image_raw.get_height()), align="topright")

    def end_object(self, **kwargs):
        explode = kwargs.get("explode", True)
        if explode:
            self.explode(sound="explosion")

        WidgetHandler.remove_widget(self.progress_bar)
        self.progress_bar = None
        self.gif_handler.end_object()
        for i in sprite_groups.ships.sprites():
            garbage_handler.delete_all_references(self, i)
            # for key, value in i.__dict__.items():
            #     if self == i.__dict__[key]:
            #         i.__dict__[key] = None

        self.kill()

    def update(self):
        # print (f"ufo.update: explode_calls {self.explode_calls}")
        if not config.game_paused:
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

        # Check the elapsed time
        self.elapsed_time = time.time() - self.creation_time

        if self.elapsed_time > LIFETIME:
            self.disappear()
        else:
            self.appear()

        # set gif handler to make sure its only drawn if self emp attacked
        self.gif_handler._hidden = not self.emp_attacked

        # self.debug_object()
