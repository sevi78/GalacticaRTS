from source.configuration import global_params

from source.factories.planet_factory import planet_factory
from source.factories.universe_factory import universe_factory
from source.gui.event_text import event_text
from source.handlers.file_handler import load_file, write_file
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.screenshot import capture_screenshot
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.text.info_panel_text_generator import info_panel_text_generator


class LevelHandler:
    def __init__(self, app):
        self.app = app
        self.win = app.win
        self.data = load_file(f"level_{0}.json", folder="levels")
        self.level = self.data.get("globals").get("level")
        self.width = self.data.get("globals").get("width")
        self.height = self.data.get("globals").get("height")

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

    def load_level(self, level, **kwargs):
        data = kwargs.get("data", {})
        if not data:
            # load level data
            self.level = level
            self.data = load_file(f"level_{level}.json", folder="levels")
            if not self.data:
                self.data = load_file(f"level_{0}.json", folder="levels")
        else:
            self.data = data

        # delete level
        self.delete_level()

        # reset player
        self.app.player.reset(self.data["player"])

        # create planets
        planet_factory.create_planets_from_data(self.data)

        # create ships
        ships = self.data.get("ships")
        for key in ships.keys():
            self.app.ship_factory.create_ship(f"{ships[key]['name']}_30x30.png", int(
                ships[key]["world_x"]), int(
                ships[key]["world_y"]), global_params.app, ships[key]["weapons"], data=ships[key])

        # setup level_edit
        self.app.level_edit.set_data_to_editor(level)
        self.app.level_edit.set_selector_current_value()
        self.app.level_edit.width = self.data.get("globals").get("width")
        self.app.level_edit.height = self.data.get("globals").get("height")

        # create universe
        self.app.level_edit.create_universe()

        # setup game_event_handler
        self.app.game_event_handler.level = global_params.app.level_handler.data.get("globals").get("level")
        self.app.game_event_handler.set_goal(global_params.app.level_handler.data.get("globals").get("goal"))

        # setup mission
        self.app.resource_panel.mission_icon.info_text = info_panel_text_generator.create_info_panel_mission_text()
        global_params.edit_mode = False

    def generate_level_dict__(self):
        # get all planets
        for planet in sprite_groups.planets.sprites():
            for key, value in self.data["celestial_objects"][str(planet.id)].items():
                if hasattr(planet, key):
                    self.data["celestial_objects"][str(planet.id)][key] = getattr(planet, key)

        # get ship config, used if ship is created dynamically
        ship_config = load_file("ship_settings.json")

        # get all ships
        for ship in sprite_groups.ships.sprites():
            # initialize data if ship is not in data
            if not str(ship.id) in self.data["ships"].keys():
                self.data["ships"][str(ship.id)] = {"name": "", "world_x": 0, "world_y": 0}

            # fill the data from the ship data
            for key, value in self.data["ships"][str(ship.id)].items():
                if hasattr(ship, key):
                    self.data["ships"][str(ship.id)][key] = getattr(ship, key)

            # fill rest of the values from ship config
            for var in ship_config[ship.name].keys():
                if hasattr(ship, var):
                    self.data["ships"][str(ship.id)][var] = getattr(ship, var)

            # get weapons from ship weapon_handler
            self.data["ships"][str(ship.id)]["weapons"] = ship.weapon_handler.weapons

            # get specials loaded in ship
            self.data["ships"][str(ship.id)]["specials"] = ship.specials

    def generate_level_dict(self):
        data = self.data
        # get player
        player = global_params.app.player
        data["player"]["stock"] = player.get_stock()
        data["player"]["population"] = player.population

        # get all planets
        for planet in sprite_groups.planets.sprites():
            for key, value in data["celestial_objects"][str(planet.id)].items():
                if hasattr(planet, key):
                    value_ = getattr(planet, key)
                    data["celestial_objects"][str(planet.id)][key] = value_

        # get ship config, used if ship is created dynamically
        ship_config = load_file("ship_settings.json")

        # get all ships
        for ship in sprite_groups.ships.sprites():
            # initialize data if ship is not in data
            if not str(ship.id) in data["ships"].keys():
                data["ships"][str(ship.id)] = {"name": "", "world_x": 0, "world_y": 0}

            # fill the data from the ship data
            for key, value in data["ships"][str(ship.id)].items():
                if hasattr(ship, key):
                    data["ships"][str(ship.id)][key] = getattr(ship, key)

            # fill rest of the values from ship config
            for var in ship_config[ship.name].keys():
                if hasattr(ship, var):
                    data["ships"][str(ship.id)][var] = getattr(ship, var)

            # get weapons from ship weapon_handler
            data["ships"][str(ship.id)]["weapons"] = ship.weapon_handler.weapons

            # get specials loaded in ship
            data["ships"][str(ship.id)]["specials"] = ship.specials

        return data

    # def generate_game_dict(self, data):
    #     data[""]
    def save_level(self):
        self.data = self.generate_level_dict()
        write_file(f"level_{self.level}.json", self.data, folder="levels")

        # save screenshot
        screen_x, screen_y = pan_zoom_handler.world_2_screen(0, 0)
        capture_screenshot(
            self.win,
            f"level_{self.level}.png",
            (screen_x, screen_y, self.width * pan_zoom_handler.zoom, self.height * pan_zoom_handler.zoom),
            (360, 360),
            event_text=event_text)

        # file_handler.get_level_list()
        self.app.level_select.update_icons()
