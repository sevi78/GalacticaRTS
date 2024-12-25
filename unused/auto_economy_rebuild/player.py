# from source.auto_economy_rebuild.economy_agent import EconomyAgent
from source.economy.EconomyAgent import EconomyAgent


class Player:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
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
        self.buildings = []
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