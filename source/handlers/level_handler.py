from source.configuration import global_params
from source.factories.level_factory import level_factory
from source.factories.planet_factory import planet_factory
from source.factories.universe_factory import universe_factory
from source.gui.event_text import event_text
from source.handlers import file_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.screenshot import capture_screenshot
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.text.info_panel_text_generator import info_panel_text_generator


class LevelHandler:
    def __init__(self, app):
        self.app = app
        self.data = level_factory.load_level(0)

    def delete_level(self):
        # delete objects
        universe_factory.delete_universe()
        universe_factory.delete_artefacts()
        planet_factory.delete_planets()
        self.app.ship_factory.delete_ships()
        for i in sprite_groups.collectable_items.sprites():
            i.end_object()
        for i in sprite_groups.ufos.sprites():
            i.end_object()
        for i in sprite_groups.gif_handlers.sprites():
            i.end_object()

    def load_level(self, level):
        self.delete_level()
        self.app.player.reset()
        self.data = level_factory.load_level(level)
        if not self.data:
            self.data = level_factory.load_level(0)

        ships = self.data.get("ships")
        for key in ships.keys():
            self.app.ship_factory.create_ship(f"{ships[key]['name']}_30x30.png", int(
                ships[key]["world_x"]), int(
                ships[key]["world_y"]), global_params.app)

        planet_factory.create_planets_from_data(self.data)
        self.app.level_edit.set_data_to_editor(level)
        self.app.level_edit.set_selector_current_value()
        self.app.level_edit.width = self.data.get("globals").get("width")
        self.app.level_edit.height = self.data.get("globals").get("height")
        self.app.level_edit.create_universe()
        self.app.game_event_handler.level = global_params.app.level_handler.data.get("globals").get("level")
        self.app.game_event_handler.set_goal(global_params.app.level_handler.data.get("globals").get("goal"))

        self.app.resource_panel.mission_icon.info_text = info_panel_text_generator.create_info_panel_mission_text()
        global_params.edit_mode = False

    def save_level(self):
        print(self.data)
        level_factory.save_level(self.level, self.data)
        # save screenshot
        screen_x, screen_y = pan_zoom_handler.world_2_screen(0, 0)
        capture_screenshot(
            self.win,
            f"level_{self.level}.png",
            (screen_x, screen_y, self.width * pan_zoom_handler.zoom, self.height * pan_zoom_handler.zoom),
            (360, 360),
            event_text=event_text)

        file_handler.get_level_list()
        self.app.level_select.update_icons()

    def update(self):
        pass
        #print (f"level_handler.update:")

