import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING, ARROW_SIZE
from source.handlers.file_handler import write_file, load_file
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image

P_FONT_SIZE = 12


class AutoEconomyQueueEdit(EditorBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)

        # args
        self.planet_name = None
        self.planet_task_priorities = None
        self.highest_priority_key = None
        self.player = None
        self.planet = None
        self.p_font = pygame.font.SysFont(config.font_name, P_FONT_SIZE)

        #  widgets
        self.widgets = []

        # create widgets
        self.create_close_button()
        self.priority_values = load_file("economy_queue_settings.json", "config")
        self.create_selectors_from_dict(
                x=self.world_x - ARROW_SIZE / 2 + self.world_width / 2,
                y=130,
                dict_=self.priority_values.items(), arrow_size=ARROW_SIZE / 2)
        self.set_selector_current_value()
        self.max_height = 900
        self.create_save_button(lambda: self.save_settings(), "save settings", name="save_button")

        # hide initially
        self.hide()

    def set_planet(self):
        planet = sprite_groups.get_hit_object(lists=["planets"])
        if planet != None:
            self.planet = planet
            self.planet_name = self.planet.name
            owner = self.planet.owner
            if owner != -1:
                self.player = config.app.players[owner]

        if self.player:
            self.highest_priority_key = self.player.auto_economy_handler.priority_queue.highest_priority_key
            if self.planet.id in self.player.auto_economy_handler.priority_queue.planet_task_priorities.keys():
                self.planet_task_priorities = self.player.auto_economy_handler.priority_queue.planet_task_priorities[
                    self.planet.id]


        if self.planet:
            config.app.player_edit.player_buildings_overview.set_buildings(self.planet.buildings, self.planet_name)

    def draw_resource_images(self, x, y, size):
        if not self.planet:
            return
        for i in self.planet.possible_resources:
            image = pygame.transform.scale(get_image(f"{i}_25x25.png"), (size, size))
            self.win.blit(image, (x, y))
            x += size * 1.5

    def draw_priority_overview(self):
        x = self.rect.x + ARROW_SIZE
        y = self.world_y + self.rect.bottom / 2
        space_y = P_FONT_SIZE * 1.5
        image_size = 20

        # draw images
        self.draw_resource_images(x, y, image_size)
        y += image_size + space_y

        # planet name
        text_key_title = f"highest_priority_key of {self.planet_name}: "
        self.draw_text(
                x=x,
                y=y,
                width=self.get_screen_width(),
                height=15,
                text=text_key_title,
                font=self.p_font)
        y += space_y

        # draw highest_priority_key
        text_key = f"{self.highest_priority_key}"
        self.draw_text(
                x=x,
                y=y + P_FONT_SIZE,
                width=self.get_screen_width(),
                height=15,
                text=text_key,
                font=self.p_font)
        y += space_y

        # draw priorities
        if self.planet_task_priorities:
            sum_ = self.player.auto_economy_handler.priority_queue.player_task_priorities
            for key, value in self.planet_task_priorities.items():
                text_ = f"{key}: {value}/{sum_[key]}"
                self.draw_text(
                        x=x,
                        y=y + P_FONT_SIZE,
                        width=self.get_screen_width(),
                        height=15,
                        text=text_,
                        font=self.p_font)
                y += space_y

    def set_selector_current_value(self):
        """updates the selectors values"""
        for i in self.selectors:
            i.set_current_value(self.priority_values[i.key])

    def save_settings(self):
        data = {}
        for i in self.selectors:
            data[i.key] = i.current_value
        write_file("economy_queue_settings.json", "config", data)

    def selector_callback(self, key, value, selector):
        self.priority_values[key] = value
        # print("selector_callback:", self.priority_values)
        for key, value in config.app.players.items():
            config.app.players[key].auto_economy_handler.priority_queue.priority_values = self.priority_values

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)
            self.set_planet()

    def draw(self):
        if not self._hidden and not self._disabled:
            config.app.player_edit.player_buildings_overview._hidden = self._hidden
            self.draw_frame(alpha=255)
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 15, f"{self.planet_name}:")
            self.draw_priority_overview()
