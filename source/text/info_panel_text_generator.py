from collections import Counter

from source.database.file_handler import load_file
from source.factories.building_factory import building_factory
from source.utils.positioning import distance_between_points
from source.text.text_formatter import format_number


class InfoPanelTextGenerator:
    def __init__(self):
        self.json_dict = load_file("buildings.json")
        self.info_text = "Ships: right click to move to a planet, or reload the ship.\n\nctrl and mouse click to navigate\n\n" \
                         "press SPACE to pause game.\n\n\n\nproduce enough food to make you population grow! "

    def get_building(self, building):
        dict_ = {}
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    dict_[item] = value
        return dict_

    def create_info_panel_building_text(self, building):
        ignorables = ["name", "category", "building_production_time_scale", "city"]
        price_text = f"{building}:\n\nprices:\n\n"
        production_text = ""
        other_text = ""
        dict_ = self.get_building(building)
        time_scale = dict_["building_production_time_scale"]

        for key, value in dict_.items():
            if key.startswith("price_"):
                resource_key = key.split('price_')[1]
                if value > 0:
                    price_text += f"{resource_key}: {value}\n"

            elif key.startswith("production_"):
                production_key = key.split('production_')[1]
                if production_key == "minerals":
                    production_key = "mineral"
                if not production_key in ignorables:
                    production_text += f"{production_key}: {value}\n"

            elif key == "build_population_minimum":
                if value > 0:
                    other_text += f"\nminimum population needed to build: {value}\n"

            elif key == "population_buildings_value":
                if value > 0:
                    other_text += f"\nincreases population maximum on the planet by: {value}\n"

            elif key == "building_production_time":
                other_text += f"\ntime needed to build: {value * time_scale}s\n"

            elif not key in ignorables:
                other_text += f"{key}: {value}\n"

        text = price_text + "\nproduction:\n\n" + production_text + other_text
        return text

    def create_special_info_panel_string(self, planet):
        text = ""

        for key, value in planet.specials_dict.items():
            operator = value["operator"]
            special_key = key
            special_value = value["value"]

            # text += f"{special_key}:{special_value}\n"

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
                    text += f"The population grow rate is increased by{special_value}!\n"

        # text += "\n\n"
        # for special in planet.specials:
        #     special_key, operator, special_value = special.split()
        #     special_value = float(special_value)
        #     if special_key in planet.resources:
        #         if operator == "*":
        #             operator = "x"
        #             text += f"{special_key} is produced {special_value}x faster!\n"
        #
        #         elif operator == "+":
        #             text += f"{special_value} {special_key} units are produced for free!\n"
        #
        #     elif special_key == "population_grow_factor":
        #         if operator == "*":
        #             operator = "x"
        #             text += f"The population will grow {special_value}x faster!\n"
        #
        #         elif operator == "+":
        #             text += f"The population grow rate is increased by{special_value}!\n"
        return text

    def create_info_panel_planet_text(self, obj):
        # text_keys = ["name", "possible_resources", "specials", "buildings_max", "alien_population", "orbit_speed",
        #             "orbit_distance", "type"]
        # orbit_object = [i for i in sprite_groups.planets if i.id == obj.orbit_object_id]
        # for i in text_keys:
        #
        #     print (f"{i}:{getattr(obj, i)}")
        # #print ("data:", data)
        # return
        #
        # info = {}
        # for key, value in data["celestial_objects"][str(obj.id)].items():
        #     if key in text_keys:
        #         if "[" in str(value):
        #             value = eval(value)
        #         info[key] = value
        #
        # name = info['name']
        # alien_population = info['alien_population']
        # buildings_max = info['buildings_max']
        # specials = info['specials']
        # possible_resources = info['possible_resources']
        # orbit_speed = info['orbit_speed']
        # orbit_distance = str(round(info['orbit_distance'] / 1000, 1)) + " million kilometers"
        # type = info['type']
        #
        # text = f"Welcome to {name}!\n\n"
        # if alien_population == 0:
        #     text += f"You are the first to arrive on this {type}. It's a blank slate waiting for you to make your mark.\n"
        # else:
        #     text += f"You are not alone on this {type}. There are {alien_population} aliens living here already.\n"
        #
        # text += f"You can build up to {buildings_max} buildings on this planet.\n"
        # if specials:
        #     text += f"There are special buildings available: {specials}.\n"
        # else:
        #     text += "There are no special buildings available on this planet.\n"
        #
        # text += "Possible resources on this planet include:\n\n"
        # for resource in possible_resources:
        #     text += f"- {resource}\n"
        #
        # text += f"\nThe planet's orbits around its sun at a distance of {orbit_distance} with a speed of {orbit_speed}.\n"
        #
        # return text

        text = f"Welcome to {obj.name}!\n\n"
        if obj.alien_population == 0:
            text += f"You are the first to arrive on this {obj.type}. It's a blank slate waiting for you to make your mark.\n"
        else:
            text += f"You are not alone on this {obj.type}. There are {obj.alien_population} aliens living here already.\n"

        text += f"You can build up to {obj.buildings_max} buildings on this planet.\n"
        if obj.specials:

            text += f"This planet has some special properties:\n\n {self.create_special_info_panel_string(obj)}.\n"
        else:
            text += "There are no special buildings available on this planet.\n"

        text += "Possible resources on this planet include:\n\n"
        for resource in obj.possible_resources:
            text += f"- {resource}\n"
        distance = distance_between_points(obj.world_x, obj.world_y, obj.orbit_object.world_x, obj.orbit_object.world_y)
        text += (f"\nThe planet's orbits around its sun at a distance of {format_number(distance * 1000, 1)}"
                 f" km with a speed of {format_number(obj.orbit_speed * 1000, 1)}km/s.\n")

        return text

    def create_info_panel_ship_text(self, ship):
        settings_dict = load_file("ship_settings.json")[ship]
        text = ship + ":" + "\n"
        text += "\n" + "prices:" + "\n\n"

        for key, value in building_factory.get_prices_from_buildings_json(ship).items():
            text += key + ": " + str(value) + "\n"

        text += f"load capacity:\n\n"
        text += f"water: {settings_dict['water_max']}\n"
        text += f"energy: {settings_dict['energy_max']}\n"
        text += f"food: {settings_dict['food_max']}\n"
        text += f"minerals: {settings_dict['minerals_max']}\n"
        text += f"technology: {settings_dict['technology_max']}\n"

        # special_text = "\nSpecials:\n\n"
        # for i in ship.specials:
        #     special_text += f"{i}\n"

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
        text = ""
        #print(f"create_ufo_tooltip")

        text += ufo.name + ":\n\n"

        text += "speed: " + str(ufo.speed) + "\n\n"
        text += "resources loaded: " + "\n\n"
        text += "    water: " + str(ufo.water) + "/" + str(ufo.water_max) + "\n"
        text += "    energy: " + str(int(ufo.energy)) + "/" + str(int(ufo.energy_max)) + "\n"
        text += "    food: " + str(ufo.food) + "/" + str(ufo.food_max) + "\n"
        text += "    minerals: " + str(ufo.minerals) + "/" + str(ufo.minerals_max) + "\n"
        text += "    technology: " + str(ufo.technology) + "/" + str(ufo.technology_max) + "\n\n"

        if ufo.specials:
            text += f"    specials:\n"

            for i in ufo.specials:
                text += f"    {i}\n"

        text += f"\nattitude: {ufo.attitude_text} ({ufo.attitude})\n"
        # text += "scanner range: " + str(self.fog_of_war_radius) + "\n"
        # text += "crew: " + str(self.crew) + "\n"

        infotext += text
        return infotext


    def create_info_panel_planetary_defence_text(self, item):
        text = item + ":" + "\n"
        text += "\n" + "prices:" + "\n\n"

        for key, value in building_factory.get_prices_from_buildings_json(item).items():
            text += key + ": " + str(value) + "\n"

        return text

    def create_create_info_panel_level_text(self, level: int, data: dict) -> str:
        # get goal
        goal = "goal:\n\n"
        try:
            goal += f"{data['globals']['goal']}\n"
        except KeyError:
            goal += "no goal defined!!\n"
        # get the size of the level
        width, height = (format_number(data["globals"]["width"] * 1000, 1),
                         format_number(data["globals"]["height"] * 1000, 1))

        # Count the number of planets, sun, moons
        num_planets = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "planet")
        num_moons = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "moon")
        num_suns = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "sun")

        # Get the possible resources
        resources = set()
        for obj in data["celestial_objects"].values():
            resources.update(obj["possible_resources"])

        # Count all resources in all planets
        all_resources = []
        for obj in data["celestial_objects"].values():
            all_resources.extend(obj["possible_resources"])

        # Order the resources from most to least
        ordered_resources = dict(sorted(Counter(all_resources).items(), key=lambda item: item[1], reverse=True))

        # Convert the ordered_resources dictionary to a list of tuples and then access the first item
        ordered_resources_list = list(ordered_resources.items())

        # Count the alien_population of all planets and moons
        alien_population_count = sum(
            obj["alien_population"] for obj in data["celestial_objects"].values() if obj["type"] in ["planet", "moon"])

        # Create the tooltip strings
        area_text = f"{width} x{height} km"
        if num_suns > 1:
            suntext = f"There are {num_suns} suns in this area of {area_text} of the universe "
        else:
            suntext = f"There is a single sun in this area of {area_text} of the universe "

        if num_planets > 1:
            planettext = f"with {num_planets} planets"
        else:
            planettext = f"with a single planet"

        if num_moons > 1:
            moontext = f"and {num_moons} moons."
        else:
            moontext = f"and a single moon."

        if alien_population_count > 0:
            alien_text = f"An estimated {format_number(alien_population_count, 1)} extraterrestrials live there. "
        else:
            alien_text = "(un)fortunately there are no aliens here."

        if len(ordered_resources_list) > 0:
            if ordered_resources_list[0][0] == "city":
                resource_text = f"A good place to grow population."
            else:
                resource_text = f"plenty of {ordered_resources_list[0][0]} can be found here !"
        else:
            resource_text = f"No resources can be found here !"

        # create the final tooltip
        infotext = f"level {level}:\n\n\n\n\n\n"
        infotext += f"{goal}"
        infotext += "stats:"
        # infotext += "\u0332".join("stats:")

        res_string = ""
        for i in resources:
            res_string += i + "\n"

        infotext += (f"\n\narea: {area_text}\nsuns: {num_suns}\nplanets: {num_planets}\nmoons: {num_moons}\n"
                     f"alien population: {format_number(alien_population_count, 3)}\n\nresources:\n\n{res_string}\n\n")

        infotext += (f"{suntext}{planettext}{moontext}\n"
                     f"{resource_text}\n{alien_text}")

        return infotext

    def get_info_text(self):
        return self.info_text


info_panel_text_generator = InfoPanelTextGenerator()
