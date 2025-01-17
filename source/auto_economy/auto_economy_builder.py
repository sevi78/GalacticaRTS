import random

from source.configuration.game_config import config
from source.factories.building_factory import building_factory

DELETE_BUILDING_THRESHOLD = 500
SHIP_MAXIMUM = 15
SPACESHIP_MAXIMUM = 5
SPACEHUNTER_MAXIMUM = 5
CARGO_LOADER_MAXIMUM = 3
SPACESTATION_MAXIMUM = 2

import logging
import os
from datetime import datetime

# Create the "logging" directory if it doesn't exist
log_dir = os.path.join(os.getcwd(), "logging")
os.makedirs(log_dir, exist_ok=True)

# Get the current date and time
now = datetime.now()

# Create a log file name with the current date and time
# log_filename = f"auto_economy_builder_{now.strftime('%Y%m%d_%H%M%S')}.log"
log_filename = f"auto_economy_builder.log"

# Create the full path to the log file in the "logging" directory
log_file = os.path.join(log_dir, log_filename)

# Configure logging to create a new log file for each run
logging.basicConfig(filename=log_file, filemode="w", level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoEconomyBuilder:

    def build_population_buildings__(self):
        """
        Check if the planet has the necessary resources to produce food and build population buildings for growth.
        If the player's population is not greater than or equal to the population limit, return.
        If the planet has "food" and "population" in its possible resources, set the population limit of the planet and
        proceed to build population buildings.
        Build the first population building, a town, if it does not already exist.
        Upgrade population buildings based on population thresholds:
            - If population is >= 1000, upgrade to a city if not already present.
            - If population is between 1000 and 10000, upgrade to a city and then to a metropole.
            - If population is between 10000 and 100000, upgrade to a metropole.
            - If population is over 100000, build additional metropoles.
        """
        # check if planet has the productions: food and population that it need to:
        # produce food
        # build population buildings needed to grow
        if not self.planet:
            return

        if not self.player.population >= self.player.population_limit:
            return

        if "food" in self.planet.possible_resources and "population" in self.planet.possible_resources:
            # get population and population limit of the planet
            self.planet.set_population_limit()
            population = int(self.planet.population)

            # build the first population building
            # build a first town
            if not "town" in self.planet.economy_agent.buildings:
                building_factory.build("town", self.planet)
                building_factory.build("farm", self.planet)
                building_factory.build("farm", self.planet)

            # check if population is > 1000 to ensure it needs population building upgrades
            if population >= 1000:
                # check if population is over the population limit
                if population >= self.planet.population_limit:
                    # check if population is between 1000 and 10000
                    if population in range(1000, 10000):
                        # upgrade population building
                        if not "city" in self.planet.economy_agent.buildings:
                            if "town" in self.planet.economy_agent.buildings:
                                # delete town
                                building_factory.destroy_building("town", self.planet)
                            building_factory.build("city", self.planet)

                            # upgrade farm
                            if "farm" in self.planet.economy_agent.buildings:
                                building_factory.destroy_building("farm", self.planet)
                            building_factory.build("ranch", self.planet)

                    # check if population is between 10000 and 100000
                    if population in range(10000, 100000):
                        # upgrade population building
                        if not "metropole" in self.planet.economy_agent.buildings:
                            if "city" in self.planet.economy_agent.buildings:
                                # delete city
                                building_factory.destroy_building("city", self.planet)
                            building_factory.build("metropole", self.planet)

                            if "ranch" in self.planet.economy_agent.buildings:
                                building_factory.destroy_building("ranch", self.planet)
                            building_factory.build("metropole", self.planet)

                    # build more metropoles
                    if population in range(100000, 1000000):
                        building_factory.build("metropole", self.planet)
                        building_factory.destroy_building("agriculture complex", self.planet)

    def build_energy_buildings__(self):
        building = building_factory.get_fitting_building(self.planet.population, "energy")
        building_factory.build(building, self.planet)

    def build_water_buildings__(self):
        building = building_factory.get_fitting_building(self.planet.population, "water")
        building_factory.build(building, self.planet)

    def build_food_buildings(self):
        building = building_factory.get_fitting_building(self.planet.population, "food")
        building_factory.build(building, self.planet)

    def build_minerals_buildings(self):
        building = building_factory.get_fitting_building(self.planet.population, "minerals")
        building_factory.build(building, self.planet)

    def build_building_by_category__(self, planet, category):
        """
        builds buildings to planet based on category
        checks for fitting building based on population of the planet
        """
        building = building_factory.get_fitting_building(planet.population, category)
        building_factory.build(building, planet)

    def build_space_harbour__(self):
        """ builds a space harbour if not found on any planet and:

            10000 population on the planet
            all production values positive
        """
        building_factory.build("space harbor", self.planet)

    def build_ship(self):
        """
        builds ships if possible and send rescue drones
        """
        space_harbour_planet = [i for i in self.planets if "space harbor" in i.economy_agent.buildings]

        if space_harbour_planet:
            ships = self.player.get_all_ships()
            if not len(ships) > SHIP_MAXIMUM:
                spaceships = len([i for i in ships if i.name == "spaceship"])
                spacehunters = len([i for i in ships if i.name == "spacehunter"])
                cargoloaders = len([i for i in ships if i.name == "cargoloader"])
                spacestations = len([i for i in ships if i.name == "spacestation"])
                rescue_drones = len([i for i in ships if i.name == "rescue drone"])

                # get lost ships
                lost_ships = [ship for ship in ships if ship.state_engine.state == "move_stop"]
                if lost_ships:
                    # if any rescue drone available, send rescue drone
                    if rescue_drones > 0:
                        [i for i in ships if i.name == "rescue drone"][0].set_target(target=lost_ships[0])
                    # if not, build rescue drone
                    else:
                        building_factory.build("rescue drone", space_harbour_planet[0])

                # build spaceships
                if spaceships < SPACESHIP_MAXIMUM:
                    building_factory.build("spaceship", space_harbour_planet[0])
                elif spacehunters < SPACEHUNTER_MAXIMUM:
                    building_factory.build("spacehunter", space_harbour_planet[0])
                elif cargoloaders < CARGO_LOADER_MAXIMUM:
                    building_factory.build("cargoloader", space_harbour_planet[0])
                elif spacestations < SPACESTATION_MAXIMUM:
                    building_factory.build("spacestation", space_harbour_planet[0])

    # def build_ship_weapons_(self):  # orig
    #     ships = self.player.get_all_ships()
    #     weaponised_ships = [i for i in ships if i.name in ["spaceship", "spacehunter", "cargoloader"]]
    #     weapons = building_factory.get_building_names("weapons")
    #     if weaponised_ships:
    #         ship = random.choice(weaponised_ships)
    #         if not ship.weapon_handler.weapons:
    #             config.app.weapon_select.obj = ship
    #             weapon = random.choice(weapons)
    #             config.app.weapon_select.select_weapon(weapon)
    #             config.app.weapon_select.upgrade()

    def build_ship_weapons_(self):
        ships = self.player.get_all_ships()
        weaponised_ships = [i for i in ships if i.name in ["spaceship", "spacehunter", "cargoloader"]]
        weapons = building_factory.get_building_names("weapons")
        if weaponised_ships:
            ship = random.choice(weaponised_ships)
            weapon = random.choice(weapons)

            # if ship has no weapons
            if not ship.weapon_handler.weapons:
                # build the weapon
                prices = building_factory.get_prices_from_weapons_dict(
                        ship.weapon_handler.current_weapon["name"], ship.weapon_handler.current_weapon["level"])
                building_factory.build(ship.weapon_handler.current_weapon["name"], ship, prices=prices)
                print(f"build_ship_weapons:buy {weapon} on ship: {ship.id}")

            # if has weapons already, upgrade
            else:
                all_building_widgets = config.app.building_widget_list
                # print(f"all_building_widgets: {all_building_widgets}")
                # print(f"all_building_widgets.names: {[_.name for _ in all_building_widgets]}")
                # print(f"all_building_widgets.keys:{[_.key for _ in all_building_widgets]}")

                already_in_cue = len([_.name for _ in all_building_widgets if _.name == weapon])

                if ship.weapon_handler.current_weapon[
                    "level"] + already_in_cue < ship.weapon_handler.max_weapons_upgrade_level:
                    prices = building_factory.get_prices_from_weapons_dict(
                            ship.weapon_handler.current_weapon["name"], ship.weapon_handler.current_weapon["level"])
                    building_factory.build(ship.weapon_handler.current_weapon["name"], ship, prices=prices)
                    # print(f"build_ship_weapons:upgrade {weapon} on ship: {ship.id}")


    def build_ship_weapons__(self):
        ships = self.player.get_all_ships()
        weaponised_ships = [i for i in ships if i.name in ["spaceship", "spacehunter", "cargoloader"]]
        weapons = building_factory.get_building_names("weapons")
        if weaponised_ships:
            ship = random.choice(weaponised_ships)
            weapon = random.choice(weapons)

    def build_ship_weapons(self):
        ships = self.player.get_all_ships()
        weaponised_ships = [i for i in ships if i.name in ["spaceship", "spacehunter", "cargoloader"]]
        weapons = building_factory.get_building_names("weapons")

        if weaponised_ships:
            ship = random.choice(weaponised_ships)
            weapon = random.choice(weapons)

            ship.weapon_handler.update_weapon_state(weapon)
            if not ship.weapon_handler.weapons:
                # Build the first weapon
                ship.weapon_handler.upgrade_weapon()
                print(f"build_ship_weapons: buy {weapon} on ship: {ship.id}")
            else:
                # Upgrade existing weapon
                if ship.weapon_handler.upgrade_weapon():
                    print(f"build_ship_weapons: upgrade {ship.weapon_handler.current_weapon['name']} on ship: {ship.id}")







    def build_particle_accelerator__(self):
        """ builds a particle accelerator if:

            10000 population on the planet
            all production values positive

        """
        if not "particle accelerator" in self.planet.economy_agent.buildings:
            result = building_factory.build("particle accelerator", self.planet)
            # logger.info(f"building 'particle accelerator' on {self.planet} by {self.player.name}: result: {result}")

    def build_planetary_defence(self):
        """ builds a planetary defence if:

            a particle accelerator is buildt on the planet
            10000 population on the planet
            all production values positive

        """
        production = {key: value for key, value in self.player.production.items() if key != "population"}
        # check if it has a particle accelerator
        if "particle accelerator" in self.planet.economy_agent.buildings:
            if not any(value < 0 for value in production.values()):
                defence_buildings = building_factory.get_building_names("planetary_defence")
                defence_found = False

                for i in defence_buildings:
                    if i in self.planet.buildings:
                        defence_found = True

                if not defence_found:
                    building = random.choice(defence_buildings)
                    result = building_factory.build(building, self.planet)
                    logger.info(f"build_planetary_defence: building {building} on {self.planet} by {self.player.name}: result: {result}")

    def build_university(self):
        building_factory.build("university", self.planet)

    def build_immediately(self) -> None:
        """
        Builds a building immediately if certain conditions are met.

        This function checks if there are any building widgets in the `building_widget_list` and if so, it randomly
        selects a building widget.
        If the selected building widget's `immediately_build_cost` is less than the player's technology and the owner
        of the building widget's receiver is the same as the player's owner,
        the building widget is built immediately and a message is printed indicating the player's technology.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        if len(self.building_widget_list) > 0:
            r = random.randint(0, int(len(self.building_widget_list) / 3))
            for i in self.building_widget_list:
                if self.building_widget_list.index(i) == r:
                    if i.immediately_build_cost < self.player.stock[
                        "technology"] and i.receiver.owner == self.player.owner:
                        i.build_immediately()
                        # print(f"building immediately !: {self.player.technology}")

    def build_fitting_building(self):
        self.set_fit_building()
        if self.fit_building:
            self.building = self.fit_building
            building_factory.build(self.building, self.planet)
