from pprint import pprint

from source.configuration.config import planetary_defence_prices, ship_prices
from source.database.saveload import write_file, load_file

""" this is a temporary mess to get all spaghetized values, prices ect into a single buildings.json file.
todo: need to replace all dependencies from prices ect into buildings.json to make it more eays to work with
"""


class Building:
    def __init__(self, name, parent, category):
        self.parent = parent
        self.name = name

        # category
        self.category = category
        # production
        self.production_energy = 0
        self.production_food = 0
        self.production_minerals = 0
        self.production_water = 0
        self.production_technology = 0
        self.production_city = 0

        # prices
        self.price_energy = 0
        self.price_food = 0
        self.price_minerals = 0
        self.price_water = 0
        self.price_technology = 0
        self.price_city = 0

        # others
        self.build_population_minimum = 0
        self.building_production_time_scale = 5
        self.building_production_time = 0
        self.population_buildings_value = 0

        # register
        self.parent.add(self.name, self)

    def get_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if not key == "parent":
                d[key] = value
        return d


class Buildings:
    def __init__(self):
        self.buildings = {}

        self.resources = ["water", "energy", "food", "minerals", "technology", "city"]
        self.water_buildings = ["spring", "water treatment", "terra former"]
        self.energy_buildings = ["solar panel", "wind mill", "power plant"]
        self.food_buildings = ["farm", "ranch", "agriculture complex"]
        self.mineral_buildings = ["mine", "open pit", "mineral complex"]
        self.technology_buildings = ["university", "space harbor", "particle accelerator"]
        self.city_buildings = ["town", "city", "metropole"]
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        self.create_buildings()
        self.fill_buildings()
        # self.json_dict = self.load_json_dict()#self.create_json_dict()

    def create_buildings(self):
        # for building_name, dict in production.items():
        #     building = Building(building_name, self, category=?)
        self.create_buildings_from_production()

        for building_name, dict in planetary_defence_prices.items():
            building = Building(building_name, self, "planetary_defence")

        for building_name, dict in ship_prices.items():
            building = Building(building_name, self, "ship")

    def create_buildings_from_production(self):
        for building_name, dict in production.items():
            if building_name in self.water_buildings:
                building = Building(building_name, self, category="water")
            elif building_name in self.energy_buildings:
                building = Building(building_name, self, category="energy")
            elif building_name in self.food_buildings:
                building = Building(building_name, self, category="food")
            elif building_name in self.mineral_buildings:
                building = Building(building_name, self, category="mineral")
            elif building_name in self.technology_buildings:
                building = Building(building_name, self, category="technology")
            elif building_name in self.city_buildings:
                building = Building(building_name, self, category="city")
            elif building_name in self.population_buildings:
                building = Building(building_name, self, category="population")
            else:
                building = Building(building_name, self, category="unknown")

    def fill_buildings(self):
        """ gather all information and write to a building instance"""
        for building_name, building in self.buildings.items():
            # production
            if building_name in production:
                building.production_energy = production[building_name]["energy"]
                building.production_food = production[building_name]["food"]
                building.production_minerals = production[building_name]["minerals"]
                building.production_water = production[building_name]["water"]
                building.production_technology = production[building_name]["technology"]
                building.production_city = production[building_name]["city"]
            else:
                building.production_energy = 0
                building.production_food = 0
                building.production_minerals = 0
                building.production_water = 0
                building.production_technology = 0
                building.production_city = 0

            # prices
            if building_name in prices:
                building.price_energy = prices[building_name]["energy"]
                building.price_food = prices[building_name]["food"]
                building.price_minerals = prices[building_name]["minerals"]
                building.price_water = prices[building_name]["water"]
                building.price_technology = 0

            elif building_name in planetary_defence_prices:
                building.price_energy = planetary_defence_prices[building_name]["energy"]
                building.price_food = planetary_defence_prices[building_name]["food"]
                building.price_minerals = planetary_defence_prices[building_name]["minerals"]
                building.price_water = planetary_defence_prices[building_name]["water"]
                building.price_technology = planetary_defence_prices[building_name]["technology"]

            elif building_name in ship_prices:
                building.price_energy = ship_prices[building_name]["energy"]
                building.price_food = ship_prices[building_name]["food"]
                building.price_minerals = ship_prices[building_name]["minerals"]
                building.price_water = ship_prices[building_name]["water"]
                building.price_technology = ship_prices[building_name]["technology"]

            # others
            if building_name in build_population_minimum:
                building.build_population_minimum = build_population_minimum[building_name]
                building.building_production_time_scale = building_production_time_scale
                building.building_production_time = building_production_time[building_name]
            else:
                building.build_population_minimum = 0
                building.building_production_time_scale = 0
                building.building_production_time = 0

            # population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}
            if building_name in self.population_buildings_values.keys():
                building.population_buildings_value = self.population_buildings_values[building_name]
            else:
                building.population_buildings_value = 0

    def add(self, key, value):
        self.buildings[key] = value

    def get_building(self, key):
        return self.buildings[key]

    def save_buildings_to_json(self):
        json_dict = self.create_json_dict()

        pprint(json_dict)
        write_file("buildings.json", json_dict)

    def load_json_dict(self):
        json_dict = load_file("buildings.json")
        return json_dict

    def create_json_dict(self):
        json_dict = {}
        for key, value in self.buildings.items():
            category = value.category
            if category not in json_dict:
                json_dict[category] = {}
            json_dict[category][key] = value.get_dict()
        return json_dict

        # def set_building_button_tooltip(self, i):
        #     """
        #     creates tooltops for the buttons
        #     :param i:
        #     """
        #     return_list = []
        #     price_list = []
        #     production_list = []
        #     population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}
        #
        #     # prices
        #     text = ""
        #     for building in self.parent.buildings[i.name]:
        #         if building[0] == "a":
        #             text = "to build an " + building + " you need: "
        #         else:
        #             text = "to build a " + building + " you need: "
        #
        #         for key, value in source.configuration.config.prices[building].items():
        #             if value > 0:
        #                 text += key + ": " + str(value) + ", "
        #         text = text[:-2]
        #
        #         price_list.append(text)
        #
        #     # production
        #     text = ""
        #     for building in self.parent.buildings[i.name]:
        #         # population
        #         if building in self.population_buildings:
        #             text = ". a " + building + " increases the planets population limit by " + str(
        #                 population_buildings_values[building]) + "  "
        #
        #         # production
        #         elif building[0] == "a":
        #             text = " . an " + building + " will produce: "
        #         else:
        #             text = " . a " + building + " will produce: "
        #
        #         for key, value in source.configuration.config.production[building].items():
        #             if value > 0:
        #                 text += key + ": " + str(value) + ", "
        #             #
        #             # elif value < 0:
        #             #     text += "but it will also cost you " + key + ": " +  str(value) + " everytime it produces something!, "
        #
        #         if building == "university":
        #             text += f"it will increase the maximum buildings on the planet by {technology_upgrades[building]['buildings_max']}, "
        #
        #         if building == "space harbor":
        #             text += f"this will allow you to build space ships!, "
        #
        #         text = text[:-2]
        #
        #         production_list.append(text)
        #
        #     for i in range(len(price_list)):
        #         return_list.append(price_list[i] + production_list[i])
        #
        #     return return_list


# buildings = Buildings()

# tooltip_generator = ToolTipGenerator()
# print("tooltip_generator", tooltip_generator.create_building_tooltip("farm"))
# info_panel_text_generator = InfoPanelTextGenerator()
# print (info_panel_text_generator.create_info_panel_building_text("mine"))


def main():
    pass
    # buildings.save_buildings_to_json()
    # json_dict = buildings.create_json_dict()
    # buildings.create_tooltips()
    pass


if __name__ == "__main__":
    pass
    # main()
