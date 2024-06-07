import math
from collections import Counter

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.file_handler import load_file
from source.text.text_formatter import format_number


class InfoPanelTextGenerator:
    def __init__(self):
        self.json_dict = load_file("buildings.json", "config")
        self.info_text = ("Ships:\n\nright click to move to a planet, or reload the ship."
                          "\n\nmouse wheel click to navigate"
                          "\n\ndouble click on ship to open upgrade menu"
                          "\n\npress SPACE to pause game."
                          "\n\n\n\nproduce enough food to make you population grow! ")

        self.ship_settings = load_file("ship_settings.json", "config")

    def get_building(self, building):
        dict_ = {}
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    dict_[item] = value
        return dict_

    def create_info_panel_price_text(self, building):
        dict_ = self.get_building(building)
        price_text = f"{building}:\n\nprices:\n\n"
        for key, value in dict_.items():
            if key.startswith("price_"):
                resource_key = key.split('price_')[1]
                if value > 0:
                    price_text += f"{resource_key}: {value}\n"
        return price_text

    def create_info_panel_building_text(self, building):
        ignorables = ["name", "category", "building_production_time_scale", "population"]
        price_text = self.create_info_panel_price_text(building)
        production_text = ""
        other_text = ""
        dict_ = self.get_building(building)
        time_scale = dict_["building_production_time_scale"]
        for key, value in dict_.items():
            if key.startswith("production_"):
                production_key = key.split('production_')[1]
                if production_key not in ignorables:
                    production_text += f"{production_key}: {value}\n"
            elif key == "build_population_minimum":
                if value > 0:
                    other_text += f"\nminimum population needed to build: {value}\n"
            elif key == "population_buildings_value":
                if value > 0:
                    other_text += f"\nincreases population maximum on the planet by: {value}\n"
            elif key == "building_production_time":
                other_text += f"\ntime needed to build: {value * time_scale}s\n"
            elif key not in ignorables:
                if not key.startswith("price_"):
                    other_text += f"{key}: {value}\n"
        text = f"{price_text}\nproduction:\n\n{production_text}{other_text}"
        return text

    def create_special_info_panel_string(self, planet):
        text = ""
        for key, value in planet.specials_dict.items():
            operator = value["operator"]
            special_key = key
            special_value = value["value"]
            if special_key in planet.resources:
                if operator == "*":
                    operator = "x"
                text += f"{special_key} is produced {special_value}x faster!\n"
            elif operator == "+":
                text += f"{special_value} {special_key} units are produced for free!\n"
            elif special_key == "population_grow_factor":
                if operator == "*":
                    operator = "x"
                text += f"The population will grow {special_value}x faster!\n"
            elif operator == "+":
                text += f"The population grow rate is increased by {special_value}!\n"
        return text

    def create_info_panel_planet_text(self, planet):
        text = f"Welcome to {planet.name}!\n\n"
        if planet.owner == -1:
            text += f"You are the first to arrive on this {planet.type}. It's a blank slate waiting for you to make your mark.\n"
        else:
            text += f"This planet belongs to the mighty {config.app.players[planet.owner].name}, ruler of the {config.app.players[planet.owner].species}."
        text += f"You can build up to {planet.buildings_max} buildings on this planet.\n"
        if planet.specials:
            text += f"This planet has some special properties:\n\n {self.create_special_info_panel_string(planet)}.\n"
        else:
            text += "There are no special buildings available on this planet.\n"
        text += "Possible resources on this planet include:\n\n"
        for resource in planet.possible_resources:
            text += f"- {resource}\n"
        if planet.orbit_object:
            distance = math.dist((planet.world_x, planet.world_y), (
                planet.orbit_object.world_x, planet.orbit_object.world_y))
            text += f"\nThe planet orbits around its sun at a distance of {format_number(distance * 1000, 1)} km with a speed of {format_number(planet.orbit_speed * 1000, 1)}km/s.\n"
        return text

    def create_info_panel_ship_text_from_json_dict(self, ship_name: str) -> str:
        price_text = self.create_info_panel_price_text(ship_name)

        other_text = ""
        ship_text = ""
        dict_ = self.get_building(ship_name)
        time_scale = dict_["building_production_time_scale"]

        for key, value in dict_.items():
            if key == "build_population_minimum":
                if value > 0:
                    other_text += f"\nminimum population needed to build: {value}\n"

            elif key == "building_production_time":
                other_text += f"\ntime needed to build: {value * time_scale}s\n"

        ship_text += f"energy: {self.ship_settings[ship_name]['energy']}\n"
        ship_text += f"energy use : {self.ship_settings[ship_name]['energy_use']}\n"
        ship_text += f"energy reload rate: {self.ship_settings[ship_name]['energy_reload_rate']}\n"
        ship_text += f"\nmaximum load capacity:\n\n"

        resources = building_factory.get_resource_categories()
        for i in resources:
            key = f"{i}_max"
            if key in self.ship_settings[ship_name]:
                ship_text += f"{i}: {self.ship_settings[ship_name][key]}\n"

        crew_text = f"crew: {self.ship_settings[ship_name]['crew']}\n\n"

        text = f"{price_text}\n\n{other_text}\n\n{ship_text}\n\n{crew_text}"
        text += f"speed: {self.ship_settings[ship_name]['speed']}\n\n"

        return text

    def create_info_panel_ship_text(self, ship: object) -> str:
        if ship.__class__.__name__ == "PanZoomRescueDrone":
            return self.create_info_panel_rescue_drone_text(ship)

        text = f"{ship.name}:\n\n"
        text += f"owner: {config.app.players[ship.owner].name}\n"
        text += f"experience: {int(ship.experience)}\n"
        text += f"rank: {ship.rank}\n"
        text += f"speed: {ship.speed}\n\n"
        text += "resources loaded:\n\n"
        text += f"water: {format_number(ship.water, 1)}/{format_number(ship.water_max, 1)}\n"
        text += f"energy: {format_number(ship.energy, 1)}/{format_number(ship.energy_max, 1)}\n"
        text += f"food: {format_number(ship.food, 1)}/{format_number(ship.food_max, 1)}\n"
        text += f"minerals: {format_number(ship.minerals, 1)}/{format_number(ship.minerals_max, 1)}\n"
        text += f"technology: {format_number(ship.technology, 1)}/{format_number(ship.technology_max, 1)}\n\n"
        if ship.specials:
            text += "specials:\n"
            for i in ship.specials:
                text += f" {i}\n"
        text += "\n"
        if ship.weapon_handler.weapons:
            try:
                text += "weapons:\n\n"
                for key in ship.weapon_handler.weapons.keys():
                    text += f" {key} level {ship.weapon_handler.weapons[key]['level']}\n"
            except TypeError as e:
                print(f"create_info_panel_ship_text error: {e}, key: {key}, weapons: {ship.weapon_handler.weapons}")
        if ship.is_spacestation:
            text += f"\nspacestation energy production: {format_number(ship.spacestation.production_energy, 3)} \n"

        if ship.debug:
            text += "\n\ndebug:\n"
            text += f"id: {ship.id}\n"
            text += f"name: {ship.name}\n"
            text += f"selected: {str(ship.selected)}\n"
            if ship.energy_reloader:
                text += f"reloader: {str(ship.energy_reloader.name)}\n"
            else:
                text += "reloader: None\n"
            text += f"move_stop: {str(ship.move_stop)}\n"
            text += f"moving: {str(ship.moving)}\n"
            text += f"position, x,y: {ship.world_x}/{ship.world_y}\n"

            if ship.target:
                text += f"\ntarget: {str(ship.target.name)}\n"
            else:
                text += "target: None\n"

            if ship.orbit_object:
                text += f"orbit_object: {ship.orbit_object.name}\n"
                text += f"orbit_object_id: {ship.orbit_object_id}\n"
                text += f"orbit_object_name: {ship.orbit_object_name}\n"
            else:
                text += "orbit_object: None\n"
                text += f"orbit_object_id: {ship.orbit_object_id}\n"
                text += f"orbit_object_name: {ship.orbit_object_name}\n"
            if ship.orbit_angle:
                text += f"orbit_angle: {ship.orbit_angle}\n"
            else:
                text += "orbit_angle: None\n"

            text += f"orbit_radius: {ship.orbit_radius}\n"
            if ship.target:
                dist = math.dist(ship.world_position, ship.target.world_position)
                text += f"reload_max_distance: {ship.reload_max_distance}/{dist}\n"
                text += f"attack_distance: {ship.attack_distance}/{dist}\n"
                text += f"target_object_reset_distance: {ship.target_object_reset_distance}/{dist}\n"
                text += f"desired_orbit_radius: {ship.desired_orbit_radius}/{dist}\n"

            else:
                text += f"reload_max_distance: {ship.reload_max_distance}\n"
                text += f"attack_distance: {ship.attack_distance}\n"
                text += f"target_object_reset_distance: {ship.target_object_reset_distance}\n"
                text += f"desired_orbit_radius: {ship.desired_orbit_radius}\n"

            if ship.enemy:
                text += f"enemy: {ship.enemy}\n"
                text += f"distance: {math.dist(ship.world_position, ship.enemy.world_position)}\n"
            else:
                text += "enemy: None\n"
            text += f"target_reached: {ship.target_reached}\n"

            text += f"path: {ship.pathfinding_manager.path}"
        return text

    def create_info_panel_collectable_item_text(self, resources, specials):
        text = "Alien Artefact:\n\n"
        for key, value in resources.items():
            text += f"{key}: {value}\n"
        special_text = "\nSpecials:\n\n"
        for i in specials:
            special_text += f"{i}\n"
        text += special_text
        return text

    def create_info_panel_ufo_text(self, ufo):
        infotext = ""
        text = f"{ufo.name}:\n\n"
        text += f"lifetime: {str(ufo.lifetime)}/{str(format_number(ufo.elapsed_time, 1))}\n\n"
        text += f"speed: {str(ufo.speed)}\n\n"
        text += "resources loaded:\n\n"
        text += f"water: {str(ufo.water)}/{str(ufo.water_max)}\n"
        text += f"energy: {str(int(ufo.energy))}/{str(int(ufo.energy_max))}\n"
        text += f"food: {str(ufo.food)}/{str(ufo.food_max)}\n"
        text += f"minerals: {str(ufo.minerals)}/{str(ufo.minerals_max)}\n"
        text += f"technology: {str(ufo.technology)}/{str(ufo.technology_max)}\n\n"
        if ufo.specials:
            text += "specials:\n"
            for i in ufo.specials:
                text += f" {i}\n"
        text += f"\nattitude: {ufo.attitude_text} ({ufo.attitude})\n"
        infotext += text
        return infotext

    def create_info_panel_planetary_defence_text(self, item):
        text = f"{item}:\n"
        text += "\nprices:\n\n"
        for key, value in building_factory.get_prices_from_buildings_json(item).items():
            text += f"{key}: {value}\n"
        return text

    def create_create_info_panel_level_text(self, level: int, data: dict) -> str:
        goal = "goal:\n\n"
        try:
            goal += f"{data['globals']['goal']}\n"
        except KeyError:
            goal += "no goal defined!!\n"
        width, height = (
            format_number(data["globals"]["width"] * 1000, 1), format_number(data["globals"]["height"] * 1000, 1))
        num_planets = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "planet")
        num_moons = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "moon")
        num_suns = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "sun")
        resources = set()
        for obj in data["celestial_objects"].values():
            resources.update(obj["possible_resources"])
        all_resources = []
        for obj in data["celestial_objects"].values():
            all_resources.extend(obj["possible_resources"])
        ordered_resources = dict(sorted(Counter(all_resources).items(), key=lambda item: item[1], reverse=True))
        ordered_resources_list = list(ordered_resources.items())
        alien_population_count = sum(
                obj["alien_population"] for obj in data["celestial_objects"].values() if
                obj["type"] in ["planet", "moon"])
        area_text = f"{width} x {height} km"
        if num_suns > 1:
            suntext = f"There are {num_suns} suns in this area of {area_text} of the universe "
        else:
            suntext = f"There is a single sun in this area of {area_text} of the universe "
        if num_planets > 1:
            planettext = f"with {num_planets} planets"
        else:
            planettext = f"with a single planet"
        if num_moons > 1:
            moontext = f" and {num_moons} moons."
        else:
            moontext = f" and a single moon."
        if alien_population_count > 0:
            alien_text = f"An estimated {format_number(alien_population_count, 1)} extraterrestrials live there. "
        else:
            alien_text = "(un)fortunately there are no aliens here."
        if len(ordered_resources_list) > 0:
            if ordered_resources_list[0][0] == "population":
                resource_text = "A good place to grow population."
            else:
                resource_text = f"plenty of {ordered_resources_list[0][0]} can be found here !"
        else:
            resource_text = "No resources can be found here !"
        infotext = f"level {level}:\n\n\n\n\n\n"
        infotext += f"{goal}"
        infotext += "stats:"
        res_string = ""
        for i in resources:
            res_string += f"{i}\n"
        infotext += (f"\n\narea: {area_text}\nsuns: {num_suns}\nplanets: {num_planets}\nmoons: {num_moons}\n"
                     f"alien population: {format_number(alien_population_count, 1)}\n\nresources:\n\n{res_string}\n\n")
        infotext += (f"{suntext}{planettext}{moontext}\n"
                     f"{resource_text}\n{alien_text}")
        return str(infotext)

    def create_info_panel_mission_text(self):
        level = config.app.level_handler.data.get("globals").get("level")
        goal = config.app.level_handler.data.get("globals").get("goal")
        infotext = f"your mission in level {level}:\n\n\n\n\n\n"
        infotext += "goals:\n\n"
        for key, value in goal.items():
            infotext += f" {key}: {value}"
            if config.app.game_event_handler.goal_success[key]:
                infotext += ' \u2713'
        infotext += "\n\n"
        return infotext

    def create_info_panel_player_text(self, player_index: int) -> str:
        player = config.app.players[player_index]
        trader = player.trade_assistant
        text = player.name

        text += f"\n\noffer_percentage: {trader.offer_percentage}\n"
        text += f"request_percentage: {trader.request_percentage}\n\n"

        return text

    def create_info_panel_rescue_drone_text(self, ship):
        text = f"{ship.name}:\n\n"
        text += f"owner: {config.app.players[ship.owner].name}\n"
        text += f"the rescue drone rescues ships that are lost in space by sending energy! send the drone to a ship that has run out of energy. the ship will get:\n\n"
        text += f"energy: {format_number(ship.energy, 1)}\n\n from the drone\n"
        return text


info_panel_text_generator = InfoPanelTextGenerator()
