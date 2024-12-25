"""
concept:

every player should always build the best fitting building. this means the building, that reduces the differences between
production, resources of the goal.

possible variables are:

from player:

- population
- population_limit
- production
- resources
- buildings
- buildings_max ( all possible building_sots)

from planet: ( planet.economy_agent)

- population
- population_limit
- production
- buildings
- buildings_max
- population_grow_factor
- building_slot_amount
- possible_resources

from goal:
- production_energy
- production_food
- production_minerals
- production_water
- production_technology
- production_population
- resource_energy
- resource_food
- resource_minerals
- resource_water
- resource_population

from building_dict:
example:
{
    "spring": {
      "name": "spring",
      "category": "water",
      "production_energy": 0,
      "production_food": -1,
      "production_minerals": 0,
      "production_water": 3,
      "production_technology": 0,
      "production_population": 0,
      "price_energy": 5,
      "price_food": 5,
      "price_minerals": 5,
      "price_water": 0,
      "price_technology": 0,
      "price_population": 0,
      "build_population_minimum": 0,
      "building_production_time_scale": 5,
      "building_production_time": 5,
      "population_buildings_value": 0,
      "technology_upgrade": {}
    }
- category
- production_energy
- production_food
- production_minerals
- production_water
- production_technology
- production_population
- price_energy
- price_food
- price_minerals
- price_water
- price_technology
- price_population
- build_population_minimum


to find the best building, we need to calculate a weighted graph:

1. calculate the difference between the goals.production and the buildings.production values.
    means:  if goal["production_energy"] is 1 and player.production["energy"] is -2, then the difference is 3
            if goal["production_energy"] is 10 and player.production["energy"] is 12, then the difference is 2
            if goal["production_energy"] is 1 and player.production["energy"] is 10, then the difference is 9

    the bigger the difference, the more likely it is to build this building, because its more far away from the goal

2. calculate the difference between the goals.resources and the player.resources(player.get_stock()) values.
    means:
            if goal["resource_energy"] is 1000 and player.get_stock()["energy"] is 100, then the difference is 900
            if goal["resource_energy"] is 1000 and player.get_stock()["energy"] is -100, then the difference is 1100
            if goal["resource_energy"] is 1000 and player.get_stock()["energy"] is 10000, then the difference is 9000

    the bigger the difference, the more likely it is to build this building, because its more far away from the goal

resources = ["energy","food","minerals","water","technology","population"]

3. calculate the difference between the goals.resources and the building["price_" + resource] values.
    means:
            if goal["resource_energy"] is 1000 and building["price_energy"] is 5, then the difference is 1005
            if goal["resource_energy"] is 1000 and building["price_energy"] is 0, then the difference is 1000
            if goal["resource_energy"] is 1000 and building["price_energy"] is 1, then the difference is 1001

    the smaller the difference, the more likely it is to build this building, because its more far away from the goal

4 implement also some other cases:
    if player.population is >= player.population_limit:
        the values of all buildings from categories["population"] must be adjusted to ensure the probability of these buildings increases

    if "technology" planet.economy_agent.possible_buildings:
        also the probability of building "university" must be increased because it increases the player.buildings_max

        the smaller the difference of player.buildings to player.buildings_max, the more likely technology buildings must be built:


        if there is any "space harbor" in planet.economy_agent.buildings, then the the probability should be drastically reduced:
            every player need only one of these, basically

        if no "particle accelerator" in planet.economy_agent.buildings:
            if "technology" planet.economy_agent.possible_buildings

    else:
        all technology and planetary_defence and ship must be decreased, because we cannot build these on a planet with no possible
        technology buildings.

    in common, if not category of the building in planet.economy_agent.possible_buildings, then its probability should decrease drastically,
    because we cannot build these on a planet with no possible buildings of this category.







"""
from source.economy.EconomyAgent import EconomyAgent

goal = {
  "production_energy": 1,
  "production_food": 1,
  "production_minerals": 1,
  "production_water": 1,
  "production_technology": 1,
  "production_population": 1,
  "resource_energy": 1000,
  "resource_food": 1000,
  "resource_minerals": 1000,
  "resource_water": 1000,
  "resource_technology": 1000,
  "resource_population": 1000,
  "calculation_production": 1,
  "calculation_resource": 1,
  "calculation_population": 1,
  "calculation_ship": 1}

production = {
  "energy": 0,
  "food": 0,
  "minerals": 0,
  "water": 0,
  "technology": 0,
  "population": 0
    }
resources = {
  "energy": 100,
  "food": 100,
  "minerals": 100,
  "water": 100,
  "technology": 100,
  "population": 0}

spring = {
      "name": "spring",
      "category": "water",
      "production_energy": 0,
      "production_food": -1,
      "production_minerals": 0,
      "production_water": 3,
      "production_technology": 0,
      "production_population": 0,
      "price_energy": 5,
      "price_food": 5,
      "price_minerals": 5,
      "price_water": 0,
      "price_technology": 0,
      "price_population": 0,
      "build_population_minimum": 0,
      "building_production_time_scale": 5,
      "building_production_time": 5,
      "population_buildings_value": 0,
      "technology_upgrade": {}
    }


class Player:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        for key, value in self.stock.items():
            setattr(self, key, value)

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "population": 0
            }

        self.population_limit = 0
        self.buildings = ["farm", "solar panel", "town"]
        self.stock = {
            "energy": 1000,
            "food": 1000,
            "minerals": 1000,
            "water": 1000,
            "technology": 1000,
            "population": 1000
            }

        self.economy_agents = [EconomyAgent(self), EconomyAgent(self), EconomyAgent(self)]
        self.ships = []


    def get_stock(self) -> dict:
        return self.stock

    def get_all_buildings(self) -> list:
        buildings = []
        for i in self.economy_agents:
            buildings += i.buildings
        return buildings

    def get_all_building_slots(self) -> int:
        """
        returns the sum of all buildings_slots of all planets of the player:
        - the maximum of buildings can be built
        """
        slots = sum([i.buildings_max for i in self.economy_agents])
        return slots

    def set_population_limit(self) -> None:
        population_buildings = ["town", "city", "metropole"]
        population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        self.population_limit = sum([population_buildings_values[i] for i in self.buildings if
                                     i in population_buildings])

    def get_population_limit(self):
        self.set_population_limit()
        return self.population_limit


    def set_global_population(self) -> None:
        self.stock["population"] = int(sum([i.population for i in self.economy_agents]))






def calculate_buidling_production_to_goal_production_value(building_dict:dict, goal:dict) -> dict:
    """ this returns the differnece of the buildings values to the goal values:
        - negative values means that the goal id over topped
        - positive value means that the goal is not reached
    """
    production_dict = {}
    for key, value in building_dict.items():
        # calculate the difference between the goal and the buildings production values
        new_value = 0
        if key.startswith("production"):
            goal_value = goal[key]
            new_value = goal_value - value

            production_dict[key] = new_value

    return production_dict
def calculate_building_prize_to_goal_resource_value(building_dict:dict, goal:dict, resource_dict:dict) -> dict:
    differ_dict = {}
    for key, value in building_dict.items():
        # calculate the difference between the goal and the buildings prizes values
        new_value = 0
        if key.startswith("price"):
            resource_key = key.split("price_")[1]
            goal_key = "resource_" + resource_key

            goal_value = goal[goal_key]
            new_value = goal_value + value - resource_dict[resource_key]
            differ_dict[resource_key] = new_value


    return differ_dict



print (calculate_buidling_production_to_goal_production_value(spring, goal))
print (calculate_building_prize_to_goal_resource_value(spring, goal, resources))




