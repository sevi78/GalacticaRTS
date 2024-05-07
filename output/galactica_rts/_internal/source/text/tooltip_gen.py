from collections import Counter

from source.handlers.file_handler import load_file
from source.text.text_formatter import format_number


class ToolTipGenerator:
    def __init__(self):
        self.json_dict = load_file("buildings.json", "config")

    def get_building(self, building):
        dict_ = {}
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    dict_[item] = value
        return dict_

    def create_building_tooltip(self, building):
        price_text = f"to build a {building}, you will need "
        production_text = ""
        for key, value in self.get_building(building).items():
            if key.startswith("price_"):
                resource_key = key.split('price_')[1]
                if value > 0:
                    price_text += f"{resource_key}: {value}, "

            if key.startswith("production_"):
                production_key = key.split('production_')[1]
                if production_key == "minerals":
                    production_key = "mineral"

                if value > 0:
                    if production_text == "":
                        production_text = f"it will produce: "
                    production_text += f" {production_key}:  {value}, "
        text = price_text[:-2] + ". " + production_text[:-2]

        return text

    def create_ufo_tooltip(self, ufo):
        tooltip = ""
        text = ""
        # print (f"create_ufo_tooltip")

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
        # text += "scanner range: " + str(self.fog_of_war_radius) + "\n"
        # text += "crew: " + str(self.crew) + "\n"

        tooltip += text
        return tooltip

    def create_level_tooltip(self, level, data):
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
                obj["alien_population"] for obj in data["celestial_objects"].values() if
                obj["type"] in ["planet", "moon"])

        # Create the tooltip strings
        area_text = f"{width} x{height} km"
        if num_suns > 1:
            suntext = f"There are {num_suns} suns in this area of {area_text} of the universe"
        else:
            suntext = f"There is a single sun in this area of {area_text} of the universe"

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

        resource_text = ""
        if len(ordered_resources_list) > 0:
            if ordered_resources_list[0][0] == "population":
                resource_text = f"A good place to grow population."
            else:
                resource_text = f"plenty of {ordered_resources_list[0][0]} can be found here !"

        else:
            resource_text = f"No resources can be found here !"

        # create the final tooltip
        tooltip = (f"level {level}: {suntext} {planettext} {moontext} Possible resources: {', '.join(resources)}."
                   f" {resource_text} {alien_text} ")

        return tooltip


tooltip_generator = ToolTipGenerator()
