
from source.database.saveload import load_file
from source.factories.building_factory import building_factory



class InfoPanelTextGenerator:
    def __init__(self):
        self.json_dict = load_file("buildings.json")
        self.info_text = "PanZoomShip: rightclick to move to a planet, or reload the ship.\n\nctrl and mouse click to navigate\n\n" \
                         "numbers 1-9 to make layers visible or not\n\nb to open build menu\n\npress E for planet edit\n\n" \
                         "press SPACE to pause game\n\npress Z for Zen-Modus"

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

    def create_info_panel_planet_text(self, obj):
        #text_keys = ["name", "possible_resources", "specials", "buildings_max", "alien_population", "orbit_speed",
        #             "orbit_distance", "type"]
        #orbit_object = [i for i in sprite_groups.planets if i.id == obj.orbit_object_id]
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
            text += f"There are special buildings available: {obj.specials}.\n"
        else:
            text += "There are no special buildings available on this planet.\n"

        text += "Possible resources on this planet include:\n\n"
        for resource in obj.possible_resources:
            text += f"- {resource}\n"

        text += f"\nThe planet's orbits around its sun at a distance of {obj.orbit_distance} with a speed of {obj.orbit_speed}.\n"

        return text

    def create_info_panel_ship_text(self, ship):
        text = ship + ":" + "\n"
        text += "\n" + "prices:" + "\n\n"

        for key, value in building_factory.get_prices_from_buildings_json(ship).items():
            text += key + ": " + str(value) + "\n"

        return text

    def create_info_panel_planetary_defence_text(self, item):
        text = item + ":" + "\n"
        text += "\n" + "prices:" + "\n\n"

        for key, value in building_factory.get_prices_from_buildings_json(item).items():
            text += key + ": " + str(value) + "\n"

        return text

    def get_info_text(self):
        return self.info_text


info_panel_text_generator = InfoPanelTextGenerator()
