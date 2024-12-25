import random

from source.auto_economy.score_calculator import ScoreCalculator
from source.configuration.game_config import config
from source.economy.economy_handler import economy_handler
from source.factories.building_factory import building_factory
from source.gui.event_text import event_text
from source.gui.widgets.moving_image import add_moving_image
from source.handlers.time_handler import time_handler
from source.math.math_handler import get_sum_up_to_n
from source.multimedia_library.sounds import sounds


class EconomyAgent:
    """
    The PanZoomPlanetEconomy class models the economy of a planet in a game. It manages resources, population,
    buildings, and production. The class includes methods to update resources, calculate production,
    and manage population growth and limits.

        Example Usage
        kwargs = {
            "buildings": ["town", "city"],
            "population": 5000,
            "alien_population": 200,
            "alien_attitude": 50,
            "building_slot_amount": 5,
            "specials": ["energy", "food"],
            "possible_resources": ["water", "energy", "food"]
        }
        planet_economy = PanZoomPlanetEconomy(kwargs)
        planet_economy.update_planet_resources(["water", "energy"])
        planet_economy.calculate_production()
        planet_economy.add_population()


        Main functionalities
        Manages and updates planet resources.
        Calculates production of various resources.
        Handles population growth and limits.
        Manages buildings and their upgrades.

        Methods
        __init__(self, kwargs): Initializes the class with given parameters.
        update_planet_resources(self, checkbox_values): Updates possible resources based on input.
        calculate_production(self): Calculates the production of resources.
        calculate_population(self): Calculates population growth.
        set_population_limit(self): Sets the population limit based on buildings.
        set_technology_upgrades(self, building): Applies technology upgrades from buildings.
        add_population(self): Adjusts population based on food production and limits.

        Fields
        population_special,
        technology_special,
        minerals_special,
        food_special,
        energy_special,
        water_special:Special attributes for various resources.
        population_grow_factor: Factor for population growth.
        resources: Dictionary holding current resources.
        buildings, buildings_max: List of buildings and maximum allowed buildings.
        population, population_limit, population_grow: Current population, its limit, and growth rate.
        alien_population, alien_attitude: Alien population and their attitude.
        building_slot_amount, building_slot_upgrades, building_slot_upgrade_prices,
        building_slot_upgrade_energy_consumption, building_slot_max_amount: Building slot management attributes.
        building_cue: Cue for building construction.
        specials, specials_dict: Special attributes and their values.
        possible_resources: List of possible resources.
        production: Dictionary holding production values for resources.
        production_water, production_energy, production_food, production_minerals, production_population,
        production_technology: Individual production values for resources.
        population_buildings, population_buildings_values: Types of population buildings and their capacities.
        building_buttons_energy, building_buttons_water, building_buttons_food, building_buttons_minerals:
        Lists of building buttons for each resource.
        building_buttons, building_buttons_list: Dictionary and list of all building buttons.
    """

    def __init__(self, planet, **kwargs):
        self.planet = planet

        # self.player = config.app.players[self.planet.owner] if self.planet.owner in config.app.players else None
        self.population_special = None
        self.technology_special = None
        self.minerals_special = None
        self.food_special = None
        self.energy_special = None
        self.water_special = None
        self.population_grow_factor = 0.1
        self.resources = {"energy": 0, "food": 0, "minerals": 0, "water": 0}

        self.buildings = kwargs.get("buildings", [])
        self.buildings_max = kwargs.get("buildings_max", 10)
        self.population = kwargs.get("population", 0)
        self.population_limit = 0.0
        self.population_grow = 0.0
        self.alien_population = kwargs.get("alien_population", 0)
        self.alien_attitude = kwargs.get("alien_attitude", random.randint(0, 100))

        self.building_slot_amount = kwargs.get("building_slot_amount", 3)
        self.building_slot_upgrades = 0
        self.building_slot_upgrade_prices = {0: 500, 1: 750, 2: 1250, 3: 2500, 4: 5000, 5: 25000, 6: 100000}
        self.building_slot_upgrade_energy_consumption = {0: 0, 1: 2, 2: 3, 3: 5, 4: 10, 5: 15, 6: 25}
        self.building_slot_max_amount = self.building_slot_amount + len(self.building_slot_upgrade_prices)

        self.building_cue = 0
        self.specials = kwargs.get("specials", [])
        self.specials_dict = {
            "energy": {"operator": "", "value": 0},
            "food": {"operator": "", "value": 0},
            "minerals": {"operator": "", "value": 0},
            "water": {"operator": "", "value": 0},
            "population": {"operator": "", "value": 0},
            "technology": {"operator": "", "value": 0},
            "population_grow_factor": {"operator": "", "value": 0}
            }
        self.possible_resources = kwargs.get("possible_resources")

        self.production = kwargs.get("production", {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "population": 0.0,
            "technology": 0
            })

        # population buildings
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        # production score
        self.lowest_production_score_keys = []
        self.building_production_scores_sums = {key: 100 for key in building_factory.get_all_building_names()}
        self.score_calculator = ScoreCalculator(self)

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        self._population = value
        if self._population < 1:
            self._population = 0

    def update_planet_resources(self, checkbox_values):
        # get new values
        resources = ["water", "energy", "food", "minerals", "technology", "population"]
        self.possible_resources = [i for i in checkbox_values if i in resources]

    def calculate_production(self):
        self.production = economy_handler.calculate_planet_production(self)
        self.production["energy"] -= get_sum_up_to_n(
                self.building_slot_upgrade_energy_consumption,
                self.building_slot_upgrades + 1)

        self.calculate_population()

        self.update_displays()

    def calculate_prodcuction_score(self):
        pass

    def update_displays(self):
        if hasattr(self.planet, "set_thumpsup_status"):
            self.planet.set_thumpsup_status()
            self.planet.set_smiley_status()
            self.planet.set_technology_level_status()
            self.planet.set_overview_images()

    def calculate_population(self):
        """ calculates population"""
        # if self.production["food"] > 0:
        self.population_grow = self.population_grow_factor * self.production["food"]  # * time_handler.game_speed

        if self.population < 0:
            self.population = 0

        # danger!!! might destroy everything
        self.production["population"] = self.population_grow  # * time_handler.game_speed

    def set_population_limit(self):
        """
        sets the population limit for the planet, based on city buildings:
        "town":1000,  "city":10000, "metropole":100000
        """
        self.population_limit = sum([self.population_buildings_values[i] for i in self.buildings if
                                     i in self.population_buildings])

    def set_technology_upgrades(self, building):
        upgrade = building_factory.get_technology_upgrade(building)
        for key, value in upgrade.items():
            setattr(self, key, getattr(self, key) + value)

    def add_population(self):
        if self.population_limit > self.population and self.production["food"] > 0:
            self.population += self.production["population"] * time_handler.game_speed

    def load_cargo(self, ship):
        if ship.target.collected:
            return
        ship.collect_text = ""
        waste_text = ""

        # show what is loaded
        x, y = ship.get_screen_x(), ship.get_screen_y()
        for key, value in ship.target.resources.items():
            if value > 0:
                max_key = key + "_max"
                current_value = getattr(ship, key)
                max_value = getattr(ship, max_key)

                # Load as much resources as possible
                load_amount = min(value, max_value - current_value)
                setattr(ship, key, current_value + load_amount)

                # Update collect_text
                ship.collect_text += str(load_amount) + " of " + key + " "

                # Update waste_text
                if load_amount < value:
                    waste_text += str(value - load_amount) + " of " + key + ", "

                add_moving_image(
                        surface=ship.win,
                        x=x,
                        y=y,
                        width=30,
                        height=30,
                        key=key,
                        operand="",
                        value=value,
                        velocity=(random.uniform(-0.8, 0.8), random.uniform(-1.0, -1.9)),
                        lifetime=3,
                        parent=ship.rect,
                        target=None)

        special_text = " Specials: "
        if len(ship.target.specials) != 0:
            for i in ship.target.specials:
                ship.specials.append(i)
                special_text += f"{i}"
                key_s, operand_s, value_s = i.split(" ")

                add_moving_image(
                        surface=ship.win,
                        x=x,
                        y=y,
                        width=50,
                        height=50,
                        key=key_s,
                        operand=operand_s,
                        value=value_s,
                        velocity=(0, random.uniform(-0.3, -0.6)),
                        lifetime=5,
                        parent=ship.rect,
                        target=None)

        ship.target.specials = []

        if waste_text:
            ship.collect_text += f". because the ship's loading capacity was exceeded, the following resources were wasted: {waste_text[:-2]}!"

        ship.set_resources()
        ship.set_info_text()
        sounds.play_sound(sounds.collect_success)

        event_text.set_text(f"You are a Lucky Guy! you just found some resources: {special_text}, " + ship.collect_text, obj=ship, sender=ship.owner)
        ship.target.collected = True


    def unload_cargo(self, ship): # original
        x, y = ship.get_screen_x(), ship.get_screen_y()
        text = ""
        for key, value in ship.resources.items():
            if value > 0:
                text += key + ": " + str(value) + ", "
                if not key == "energy":
                    # setattr(self.parent.players[self.owner], key, getattr(self.parent.players[self.owner], key) + value)
                    ship.parent.players[ship.owner].stock[key] = ship.parent.players[ship.owner].stock[key] + value
                    ship.resources[key] = 0
                    setattr(ship, key, 0)
                    if hasattr(config.app.resource_panel, key + "_icon"):
                        target_icon_rect = getattr(config.app.resource_panel, key + "_icon").rect.center
                        if ship.owner == config.app.game_client.id:
                            add_moving_image(
                                    surface=ship.win,
                                    x=x,
                                    y=y,
                                    width=30,
                                    height=30,
                                    key=key,
                                    operand="",
                                    value=value,
                                    velocity=(random.uniform(-10.8, 10.8), random.uniform(-1.0, -1.9)),
                                    lifetime=4,
                                    parent=ship.target.rect,
                                    target=target_icon_rect
                                    )

        special_text = ""
        for i in ship.specials:
            ship.target.economy_agent.specials.append(i)
            special_text += f"found special: {i.split(' ')[0]} {i.split(' ')[1]} {i.split(' ')[2]}"
            key_s, operand_s, value_s = i.split(" ")

            if ship.owner == config.app.game_client.id:
                add_moving_image(
                        surface=ship.win,
                        x=x,
                        y=y,
                        width=50,
                        height=50,
                        key=key_s,
                        operand=operand_s,
                        value=value_s,
                        velocity=(0, random.uniform(-0.3, -0.6)),
                        lifetime=5,
                        parent=ship.rect,
                        target=ship.target.rect.center)

        ship.specials = []

        if not text:
            return

        # set event text
        event_text.set_text("unloading ship: " + text[:-2], obj=ship, sender=ship.owner)

        # play sound
        sounds.play_sound(sounds.unload_ship)


    def unload_cargo_(self, ship):
        x, y = ship.rect.center
        text = ""
        for key, value in ship.economy_agent.resources.items():
            if value > 0:
                text += key + ": " + str(value) + ", "
                if not key == "energy":
                    # setattr(self.parent.players[self.owner], key, getattr(self.parent.players[self.owner], key) + value)
                    ship.parent.players[ship.owner].stock[key] = ship.parent.players[ship.owner].stock[key] + value
                    ship.resources[key] = 0
                    setattr(ship, key, 0)
                    if hasattr(config.app.resource_panel, key + "_icon"):
                        target_icon_rect = getattr(config.app.resource_panel, key + "_icon").rect.center
                        if ship.owner == config.app.game_client.id:
                            add_moving_image(
                                    surface=ship.win,
                                    x=x,
                                    y=y,
                                    width=30,
                                    height=30,
                                    key=key,
                                    operand="",
                                    value=value,
                                    velocity=(random.uniform(-10.8, 10.8), random.uniform(-1.0, -1.9)),
                                    lifetime=4,
                                    parent=ship.target.rect,
                                    target=target_icon_rect
                                    )

        special_text = ""
        for i in ship.economy_agent.specials:
            ship.target.economy_agent.specials.append(i)
            special_text += f"found special: {i.split(' ')[0]} {i.split(' ')[1]} {i.split(' ')[2]}"
            key_s, operand_s, value_s = i.split(" ")

            if ship.owner == config.app.game_client.id:
                add_moving_image(
                        surface=ship.win,
                        x=x,
                        y=y,
                        width=50,
                        height=50,
                        key=key_s,
                        operand=operand_s,
                        value=value_s,
                        velocity=(0, random.uniform(-0.3, -0.6)),
                        lifetime=5,
                        parent=ship.rect,
                        target=ship.target.rect.center)

        ship.specials = []

        if not text:
            return

        # set event text
        event_text.set_text("unloading ship: " + text[:-2], obj=ship, sender=ship.owner)

        # play sound
        sounds.play_sound(sounds.unload_ship)

    def update(self):

        self.lowest_production_score_keys = self.score_calculator.calculate_lowest_production_score_keys(self)

        # print (self.lowest_production_score_keys)
