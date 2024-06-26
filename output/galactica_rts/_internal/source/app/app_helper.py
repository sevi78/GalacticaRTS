from source.handlers.economy_handler import economy_handler


class AppHelper:
    """ this class is only to make App more readable, must be inherited to 'App'
    Main functionalities:

    The AppHelper class is designed to make the App more readable and contains various methods to handle different
    functionalities such as quitting the game, setting the screen size, opening and closing the build menu,
    updating game objects, calculating global production, exploring all planets, cheating, drawing fog of war,
    and saving planets. It also contains fields such as population_limit, ctrl_pressed, and s_pressed.

    Methods:
    - quit_game: quits the game with quit icon or esc
    - set_screen_size: sets the screen site using 's'
    - set_planet_name: sets the planet name if explored, or ??? of not
    - open_build_menu: opens the build menu and disables all objects below
    - close_build_menu: closes the build menu and enables all objects below
    - set_selected_planet: sets the selected planet
    - update_icons: updates the icons
    - update_game_objects: updates the game objects
    - calculate_global_production: calculates the production of all planets and sets values to player
    - cheat_ship: cheats the ship energy
    - cheat: cheats the game
    - explore_all: explores all planets
    - cheat_resources_and_population: cheats the resources and population
    - draw_fog_of_war: draws the fog of war circle based on the fog of war radius of the obj
    - save_planets: stores the planet positions

    Fields:
    - population_limit: the population limit
    - ctrl_pressed: whether the ctrl key is pressed or not
    - s_pressed: whether the s key is pressed or not"""

    def __init__(self):
        self.population_limit = None
        self.ctrl_pressed = False
        self.s_pressed = False
        self.l_pressed = False

    def get_planet_name(self):
        """
        sets the planet name if explored,  or ??? of not
        :return: planetname
        """
        if self.selected_planet:
            if self.selected_planet.explored:
                planetname = self.selected_planet.name + ":"
            else:
                planetname = "???"
        else:
            planetname = "select planet"

        return planetname

    def calculate_global_production(self, player):
        economy_handler.calculate_global_production(player)


def select_next_item_in_list(my_list: list, current_item: any, value: int):
    """Selects the next item in a list based on the current item and a value.

       Args:
           my_list (list): The list to select from.
           current_item (str): The current item in the list.
           value (int): The value to add to the current index to get the next index.

       Returns:
           str: The next item in the list.

    Objective:
    The objective of the function is to select the next item in a given list based on the current item and a value that
    determines the number of steps to move forward in the list.

    Inputs:
    - my_list: a list of items
    - current_item: the current item in the list
    - value: an integer that determines the number of steps to move forward in the list

    Flow:
    1. Get the index of the current item in the list
    2. Calculate the index of the next item by adding the value to the current index and taking the modulus of the
       length of the list
    3. Return the item at the calculated index in the list

    Outputs:
    - The next item in the list based on the current item and the value

    Additional aspects:
    - If the value is negative, the function will move backwards in the list
    - If the current item is not in the list, the function will raise a ValueError exception
    """

    if not isinstance(value, int) or value == 0:
        raise ValueError('value must be a non-zero integer')

    if not my_list:
        return None

    if current_item in my_list:
        current_index = my_list.index(current_item)
    else:
        print(f"select_next_item_in_list(): current_item not in my_list: {my_list} current_item: {current_item}")
        current_index = 0

    next_index = (current_index + value) % len(my_list)
    return my_list[next_index]
