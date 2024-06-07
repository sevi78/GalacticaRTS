from source.configuration.game_config import config
from source.factories.building_factory import building_factory

PARTICLE_ACCELERATOR_BUILD_THRESHOLD = 10000
PARTICLE_ACCELERATOR_AMOUNT = 1
SPACE_HARBOR_AMOUNT = 1
PLANETARY_DEFENCE_AMOUNT = 1
MIN_TECH_PRODUCTION_THRESHOLD = 0


class AutoEconomyHandlerPriorityQueue:
    def __init__(self):
        self.planet = None
        self.player = None
        self.auto_economy_handler = None
        self.global_task_priorities = {
            "delete_buildings": 0,
            "maximize_population_grow": 0,
            "handle_infinte_loops": 0,
            "destroy_most_consuming_building": 0,
            "deal_with_the_bank": 0,
            "optimize_planets": 0,
            "build": 0,
            "build_food_buildings": 0,
            "build_space_harbour": 0,
            "build_ship": 0,
            "build_ship_weapons": 0,
            "build_particle_accelerator": 0,
            "build_planetary_defence": 0,
            "build_population_buildings": 0,
            "build_fitting_building": 0,
            "build_university": 0,
            "add_deal": 0
            }
        self.planet_task_priorities = {}
        self.planet_resource_priorities = {}

    def __repr__(self):
        return str(self.get_highest_priority_keys(
                self.planet_task_priorities[self.planet.id])) if self.planet else "None"

    def set_priorities(self, planets):
        """
        this sets the task priorities for the planets andon global level:

        1. check if there are any planets
            if any planets:
                set planet prioritites:
                - check for possible buildings and set the prioritites based on the possible resources


        2. check the production and stock to set priorities
        3. check for population and set to set priorities
        4. check for tech buildings
        5. check for ships
        6. check for planetary defence
        7. check for infinite loops

        """
        for planet in planets:
            self.set_planet_task_priorities(planet)
            # self.set_planet_resource_priorities(planet)

        # self.set_priorities()

    def set_planet_task_priorities(self, planet):
        """
        sets the task priority for every planet
        """
        self.planet = planet
        self.player = config.app.players[planet.owner]
        self.auto_economy_handler = self.player.auto_economy_handler

        production = {key: value for key, value in self.player.production.items() if key != "population"}
        resource_stock = self.player.remove_population_key_from_stock(self.player.get_resource_stock())
        negative_stock = any(value < 0 for value in resource_stock.values())
        negative_production = any(value < 0 for value in production.values())
        negative_stock_resources = []

        # get all negative resources from stock
        for key, value in resource_stock.items():
            if value < 0:
                negative_stock_resources.append(key)

        self.planet_task_priorities[planet.id] = {
            "delete_buildings": 0,
            "maximize_population_grow": 0,
            "handle_infinte_loops": 0,
            "destroy_most_consuming_building": 0,
            "optimize_planets": 0,
            "build_food_buildings": 0,
            "build_space_harbour": 0,
            "build_ship": 0,
            "build_ship_weapons": 0,
            "build_particle_accelerator": 0,
            "build_planetary_defence": 0,
            "build_population_buildings": 0,
            "build_fitting_building": 0,
            "build_university": 0,
            "add_deal": 0,
            "deal_with_the_bank": 0

            }

        # handle zero production
        zero_productions = self.auto_economy_handler.get_zero_productions()
        if len(zero_productions) > 0:
            for building in self.planet.buildings:
                category = building_factory.get_category_by_building(building)
                if category in zero_productions:
                    self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] += self.priority_values["destroy_most_consuming_building"]
                    self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] += self.priority_values["deal_with_the_bank"]
                    # self.planet_task_priorities[self.planet.id]["optimize_planets"] += self.priority_values["optimize_planets"]

        # handle negative stock
        if negative_stock:
            self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] += self.priority_values["destroy_most_consuming_building"]
            self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] += self.priority_values["deal_with_the_bank"]
            # self.planet_task_priorities[self.planet.id]["optimize_planets"] += self.priority_values["optimize_planets"]

        # handle negative production
        if negative_production:
            self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] += self.priority_values["destroy_most_consuming_building"]
            self.planet_task_priorities[self.planet.id]["optimize_planets"] += self.priority_values["optimize_planets"]

        # if both , deal with bank
        if negative_production and negative_stock:
            if resource_stock["technology"] > 0:
                self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] += self.priority_values["deal_with_the_bank"]
            else:
                self.planet_task_priorities[planet.id]["deal_with_the_bank"] -= 10
            # self.planet_task_priorities[self.planet.id]["optimize_planets"] += self.priority_values["optimize_planets"]

        # if planet has no buildings, set "build"
        if not planet.buildings:
            self.planet_task_priorities[planet.id]["build_fitting_building"] += 1
            self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] -= self.priority_values["destroy_most_consuming_building"]

        # if planet has buildings but max is not reached set "build"
        else:
            if len(planet.buildings) < planet.buildings_max:
                self.planet_task_priorities[planet.id]["build_fitting_building"] += 1

            # otherwise prior optimize
            else:
                self.planet_task_priorities[self.planet.id]["optimize_planets"] += self.priority_values["optimize_planets"]
                # and to build a university ( first delete one)
                self.planet_task_priorities[planet.id]["delete_buildings"] += 1
                self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] += self.priority_values["destroy_most_consuming_building"]
                self.planet_task_priorities[planet.id]["build_university"] += 1

        # if has population and food, prior food and population
        if "population" in planet.possible_resources and "food" in planet.possible_resources:
            if planet.population >= planet.population_limit:
                if self.player.population >= self.player.population_limit:
                    self.planet_task_priorities[planet.id]["build_population_buildings"] += 1

            if planet.production["food"] < 1:
                self.planet_task_priorities[self.planet.id]["build_food_buildings"] += self.priority_values["build_food_buildings"]
            elif planet.production["food"] < 3:
                self.planet_task_priorities[self.planet.id]["maximize_population_grow"] -= self.priority_values["maximize_population_grow"]
            else:
                # if it is possible to build tech buildings
                if "technology" in planet.possible_resources:
                    if not "particle_accelerator" in planet.buildings:
                        self.planet_task_priorities[self.planet.id]["build_particle_accelerator"] += self.priority_values["build_particle_accelerator"]
                    elif not "planetary_defence" in planet.possible_resources:
                        self.planet_task_priorities[self.planet.id]["build_planetary_defence"] += self.priority_values["build_planetary_defence"]

        # if it is possible to build tech buildings
        if "technology" in planet.possible_resources:
            # check for population greater than 10000
            if self.planet.population > PARTICLE_ACCELERATOR_BUILD_THRESHOLD:

                # only prior these building if player has a positive production
                if not any(value < MIN_TECH_PRODUCTION_THRESHOLD for value in production.values()) or min(
                        value for value in production.values()) > 10000:

                    # space harbor
                    if self.player.get_all_buildings().count("space harbor") < SPACE_HARBOR_AMOUNT:
                        self.planet_task_priorities[self.planet.id]["build_space_harbour"] += self.priority_values["build_space_harbour"]

                    # particle accelerator
                    if not "particle accelerator" in self.planet.buildings:
                        self.planet_task_priorities[self.planet.id]["build_particle_accelerator"] += self.priority_values["build_particle_accelerator"]

                    elif not "planetary_defence" in self.planet.buildings:
                        self.planet_task_priorities[self.planet.id]["build_planetary_defence"] += self.priority_values["build_planetary_defence"]

        # build ships
        if "space harbor" in self.planet.buildings:
            self.planet_task_priorities[planet.id]["build_ship"] += 5
        # print(f"set_planet_task_priorities: {self.planet_task_priorities}")

    def set_planet_resource_priorities(self, planet):
        """
        sets the planets resource priorities
        """
        self.planet_resource_priorities[planet.id] = {
            "water": 0,
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "technology": 0,
            "population": 0,
            "planetary_defence": 0,
            "space harbor": 0,
            "particle accelerator": 0,
            "university": 0
            }

    def get_highest_priority_keys(self, dict_: dict) -> list:
        highest_value = max(dict_.values())
        highest_keys = []
        for key, value in dict_.items():
            if value == highest_value:
                highest_keys.append(key)
        return highest_keys
