import pygame

from source.configuration.game_config import config
from source.gui.event_text import event_text
from source.gui.widgets.building_widget import BuildingWidget

from source.handlers.file_handler import load_file
from source.multimedia_library.sounds import sounds


class BuildingFactoryJsonDictReader:
    def __init__(self):
        self.json_dict = self.load_json_dict()

    def load_json_dict(self):
        dict_ = load_file("buildings.json", "config")
        return dict_

    def get_building_dict_from_buildings_json(self, building: str) -> dict:
        building_dict = {}
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    building_dict[item] = value
        return building_dict

    def get_prices_from_buildings_json(self, building: str) -> dict:
        prices = {}
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    if item.startswith("price_"):
                        prices[item.split("price_")[1]] = value
        return prices

    def get_prices_from_weapons_dict(self, weapon: str, level: int):
        prices = {}
        for key, value in self.json_dict["weapons"][weapon]["upgrade cost"][f"level_{level}"].items():
            if key.startswith("price_"):
                prices[key.split("price_")[1]] = value

        return prices

    def get_production_from_buildings_json(self, building: str) -> dict:
        """
        this return a dict of the production of the building
        """
        production = {}
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    if item.startswith("production_"):
                        production[item.split("production_")[1]] = value
        return production

    def get_build_population_minimum_from_buildings_json(self, building) -> int:
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    if item == "build_population_minimum":
                        return value

    def get_build_population_minimum_list(self) -> list:
        build_population_minimum_list = []
        for category, building_names in self.json_dict.items():
            for building_name in building_names.keys():
                build_population_minimum_list.append(self.get_build_population_minimum_from_buildings_json(building_name))

        return sorted(set(build_population_minimum_list))

    def get_progress_time_from_buildings_json(self, building):
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    if item == "building_production_time":
                        return value * self.json_dict[category][building]["building_production_time_scale"]

    def get_category_by_building(self, building_name):
        for category in self.json_dict.values():
            for building in category.values():
                if building['name'] == building_name:
                    return building['category']
        return None

    def get_all_possible_categories(self) -> list:
        """ returns a list of all building categories:
        list: [str,str,str ....]"""
        return list(self.json_dict.keys())

    def get_a_list_of_building_names_with_build_population_minimum_bigger_than(self, minimum) -> list:
        list_ = []
        for i in self.get_resource_categories():
            for building_name, building_dict in self.json_dict[i].items():
                for key, value in building_dict.items():
                    if key == "build_population_minimum":
                        if value == minimum:
                            list_.append(building_name)
        return list_

    def get_a_list_of_building_names_from_category_with_build_population_minimum_bigger_than(self, minimum: int,
                                                                                             category: str) -> list:
        list_ = []
        for i in self.get_resource_categories():
            if i == category:
                for building_name, building_dict in self.json_dict[i].items():
                    for key, value in building_dict.items():
                        if key == "build_population_minimum":
                            if value == minimum:
                                list_.append(building_name)
        return list_

    def get_resource_categories(self) -> list[str]:
        not_resource = ['planetary_defence', 'ship', 'weapons']
        return [_ for _ in self.json_dict.keys() if not _ in not_resource]

    def get_technology_upgrade(self, building) -> dict:
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    if item == "technology_upgrade":
                        return value

    def get_defence_unit_names(self) -> list:
        return self.json_dict["planetary_defence"].keys()

    def get_weapons_names(self):
        return self.json_dict["weapons"].keys()

    def get_building_names(self, category) -> list:
        return list(self.json_dict[category].keys())

    # def insert_technology_upgrade(self):
    #     for category in self.json_dict.values():
    #         for building in category.values():
    #             building['technology_upgrade'] = {}

    def get_all_building_names(self) -> list:
        building_names = []
        for category, buildings in self.json_dict.items():
            for building in buildings.values():
                building_names.append(building['name'])
        return building_names

    def add_production(self, production, production1):
        d = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "population": 0
            }
        for key, value in production.items():
            if key in production1:
                d[key] = value + production1[key]

        return d

    def get_most_consuming_building(self, buildings, category):
        building_name = "mine"
        min_production = 0
        buildings = sum(buildings, [])
        for building in buildings:
            d = self.get_building_by_name(building)
            for key, value in d.items():
                if d["production_" + category] < min_production:
                    min_production = d["production_" + category]
                    building_name = building

        return building_name

    def get_building_by_name(self, building_name):
        for category, buildings in self.json_dict.items():
            for building in buildings.values():
                if building['name'] == building_name:
                    return building
        return None

    def get_all_resource_buildings(self) -> list:
        builings = []
        for key, value in self.json_dict.items():
            if key in self.get_resource_categories():
                if not key == "population":
                    if not key == "technology":
                        builings.extend(value.keys())

        return builings

    def get_fitting_building(self, planet, preferred_building_key):
        building_names = building_factory.get_building_names(preferred_building_key)

        if planet.population < 1000:
            return building_names[0]
        elif planet.population in range(1000, 10000):
            return building_names[1]
        elif planet.population in range(10000, 100000):
            return building_names[2]

        return building_names


class BuildingFactory(BuildingFactoryJsonDictReader):
    def __init__(self):
        BuildingFactoryJsonDictReader.__init__(self)

    def build(self, building, receiver, **kwargs):  # new version based on buildings.json
        """
        this builds the buildings on the planet: first check for prices ect, then build a building_widget
        that overgives the values to the planet if ready
        :param building: string
        """
        # print(f"BuildingFactory.build: building: {building}, receiver: {receiver},receiver.owner:{receiver.owner}, kwargs: {kwargs}")
        if not building in self.get_all_building_names():
            return

        prices = kwargs.get("prices", None)
        if not prices:
            prices = self.get_prices_from_buildings_json(building)

        # only build if selected planet is set
        if not receiver: return

        # check for minimum population
        build_population_minimum = self.get_build_population_minimum_from_buildings_json(building)
        if build_population_minimum > receiver.population:
            event_text.text = "you must reach a population of minimum " + str(build_population_minimum) + " people to build a " + building + "!"

            sounds.play_sound("bleep", channel=7)
            return

        # build building widget, first pay the bill
        # pay the bill
        if receiver.building_cue >= receiver.building_slot_amount:
            event_text.text = "you have reached the maximum(" + str(receiver.building_slot_amount) + ") of buildings that can be build at the same time on " + receiver.name + "!"
            sounds.play_sound("bleep", channel=7)
            return

        defence_units = self.get_defence_unit_names()
        civil_buildings = [i for i in receiver.buildings if not i in defence_units]

        if len(civil_buildings) + receiver.building_cue >= receiver.buildings_max:
            if not building in defence_units:
                event_text.text = "you have reached the maximum(" + str(receiver.buildings_max) + ") of buildings that can be build on " + receiver.name + "!"
                sounds.play_sound("bleep", channel=7)
                return

        check = self.build_payment(building, prices, config.app.players[receiver.owner])

        # predefine variables used to build building widget to make shure it is only created once
        widget_key = None
        widget_value = None
        widget_name = None

        # check for prices
        for key, value in prices.items():
            if check:
                widget_key = key
                widget_value = value
                widget_name = building
            else:
                return

        # create building_widget ( progressbar)
        if widget_key:
            self.create_building_widget(receiver, widget_key, widget_name, widget_value)

    def create_building_widget(self, receiver, widget_key, widget_name, widget_value):
        widget_width = config.app.building_panel.get_screen_width()
        widget_height = 35
        spacing = 5

        # get the position and size
        win = pygame.display.get_surface()
        height = win.get_height()
        y = height - spacing - widget_height - widget_height * len(config.app.building_widget_list)
        sounds.play_sound(sounds.bleep2, channel=7)

        is_building = True
        if widget_name in self.json_dict["weapons"].keys():
            is_building = False

        building_widget = BuildingWidget(win=config.app.win,
            x=config.app.building_panel.screen_x,
            y=y,
            width=widget_width,
            height=widget_height,
            name=widget_name,
            fontsize=14,
            progress_time=5,
            key=widget_key,
            value=widget_value,
            receiver=receiver,
            tooltip="building widget",
            layer=4,
            building_production_time=self.get_progress_time_from_buildings_json(widget_name),
            is_building=is_building
            )

        # add building widget to building cue to make shure it can be build only if building_cue is < building_slots_amount
        receiver.building_cue += 1

        # print(f"create_building_widget:receiver:{receiver}, receiver.owner:{receiver.owner},widget_name:{widget_name}, widget_key:{widget_key}, widget_value:{widget_value}  ")

    def check_if_enough_resources_to_build(self, building: str, prices, player) -> bool:
        check = True
        text = f"not enough resources to build a {building}! you are missing: "

        # check for prices
        for key, value in prices.items():
            if not getattr(player, key) - value >= 0:
                text += f"{getattr(player, key) - value} {key}, "
                check = False

        if not check:
            text = text[:-2] + "!"
            event_text.text = text

        return check

    def build_payment(self, building: str, prices, player) -> bool:  # new version based on buildings.json
        """
        pays the bills if something is build ;)
        :param building: str
        """
        # only build if has selected planet
        if not config.app.selected_planet: return

        # check for prices, if enough to build
        check = self.check_if_enough_resources_to_build(building, prices, player)
        if check:
            for key, value in prices.items():
                setattr(player, key, getattr(player, key) - value)

        return check

    def destroy_building(self, building, planet):
        # print(f"destroy_building on planet {planet}: {building}")
        if building in planet.buildings:
            planet.buildings.remove(building)

        planet.calculate_production()
        planet.calculate_population()
        planet.set_population_limit()

        config.app.calculate_global_production(config.app.players[planet.owner])

        event_text.text = f"you destroyed one {building}! You will not get anything back from it! ... what a waste ..."
        sounds.play_sound(sounds.destroy_building)


building_factory = BuildingFactory()


def main():
    # building_factory.insert_technology_upgrade()
    # write_file("buildings.json", building_factory.json_dict)

    # print(building_factory.get_all_building_names())
    # print (building_factory.get_most_consuming_building(building_factory.get_all_building_names(), "energy"))
    # print(building_factory.get_most_consuming_building(building_factory.get_all_building_names(), "food"))
    # print (building_factory.get_resource_categories())
    # print (building_factory.get_all_resource_buildings())
    building_factory = BuildingFactory()
    print(building_factory.get_fitting_building(None, "energy"))


if __name__ == "__main__":
    main()
