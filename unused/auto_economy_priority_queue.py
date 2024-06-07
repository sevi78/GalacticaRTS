from source.configuration.game_config import config


class AutoEconomyHandlerPriorityQueue:
    def __init__(self):
        self.planet = None
        self.global_task_priorities = {
            "delete_buildings": 0,
            "maximize_population_grow": 0,
            "handle_infinite_loops": 0,
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
        return str(self.get_highest_priority_keys(self.planet_task_priorities[self.planet.id])) if self.planet else "None"
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
        player = config.app.players[planet.owner]
        self.planet_task_priorities[planet.id] = {
            "delete_buildings": 0,
            "maximize_population_grow": 0,
            "handle_infinite_loops": 0,
            "destroy_most_consuming_building": 0,
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
            "add_deal": 0,
            }

        # if planet has no buildings, set "build"
        if not planet.buildings:
            self.planet_task_priorities[planet.id]["build"] += 1

        # if planet has buildings but max is not reached set "build"
        else:
            if len(planet.buildings) < planet.buildings_max:
                self.planet_task_priorities[planet.id]["build"] += 1
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
            if len([_ for _ in player.get_all_buildings() if _ == "space harbor"]) < 1:
                self.planet_task_priorities[self.planet.id]["build_space_harbour"] += self.priority_values["build_space_harbour"]

            if not "particle_accelerator" in planet.buildings:
                self.planet_task_priorities[self.planet.id]["build_particle_accelerator"] += self.priority_values["build_particle_accelerator"]

            elif not "planetary_defence" in planet.possible_resources:
                self.planet_task_priorities[self.planet.id]["build_planetary_defence"] += self.priority_values["build_planetary_defence"]

        print (f"set_planet_task_priorities: {self.planet_task_priorities}")


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
    def get_highest_priority_keys(self, dict_:dict)->list:
        highest_value = max(dict_.values())
        highest_keys = []
        for key, value in dict_.items():
            if value == highest_value:
                highest_keys.append(key)
        return highest_keys