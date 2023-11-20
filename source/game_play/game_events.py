import random
import sys

import pygame
from source.factories.building_factory import building_factory
from source.utils import global_params

resources = ["water", "food", "energy", "technology", "minerals"]


class Deal:
    """
    Main functionalities:
    The Deal class represents a deal between the player and another entity in the game. It has the ability to create a random offer and request, and also to create a friendly offer based on the resources of the player. The make_deal method adds the offer to the player's resources and subtracts the request from them.

    Methods:
    - __init__: initializes the class with an offer, request, and optional friendly parameter. It also calls the create_friendly_offer method.
    - make_deal: adds the offer to the player's resources and subtracts the request from them.
    - create_friendly_offer: creates an offer and request based on the resources of the player. It calculates the lowest value resource and sets it to 25, then adds a random value between 25 and 250 to create the offer. It also selects the highest value resource and subtracts a random value between 25 and 250 to create the request.

    Fields:
    - offer: a dictionary representing the resources offered in the deal.
    - request: a dictionary representing the resources requested in the deal.
    - friendly: an optional boolean parameter indicating whether the deal is friendly or not.

    how to use:
    Deal(offer={random.choice(resources):random.randint(0,1000)}, request={random.choice(resources):random.randint(0,1000)}
    """

    def __init__(self, offer, request, **kwargs):
        self.offer = offer
        self.request = request
        self.friendly = kwargs.get("friendly", None)

        self.create_friendly_offer()

    def make_deal(self):
        player = global_params.app.player
        # add offer
        for key, value in self.offer.items():
            setattr(player, key, getattr(player, key) + value)

        # subtract request
        for key, value in self.request.items():
            setattr(player, key, getattr(player, key) - value)

    def create_friendly_offer(self):
        """
        this should create an offer based on the resources of the player, always what you need
        """
        player = None  # define player variable
        if global_params.app:
            player = global_params.app.player

            # extract "city" from dict
            d_raw = player.get_stock()
            d = {key: max(0, value) for key, value in d_raw.items() if key != "city"}

            # check if any value in the stock is less than 0
            if any(value < 0 for value in d.values()):
                # replace negative values with 0
                d = {key: max(0, value) for key, value in d.items()}

            # get key with lowest value
            lowest_value_key = min(d, key=d.get)

            # calculate minimum value needed to set lowest value to 25
            min_value = max(25 - d[lowest_value_key], 0)

            # calculate offer value
            offer_value = d[lowest_value_key] + min_value + random.randint(25, 250)
            self.offer = {lowest_value_key: offer_value}

            # calculate request value
            request_key = max(d, key=d.get)
            request_value = getattr(player, request_key)
            request_value -= random.randint(25, 250)
            self.request = {request_key: request_value}


class GameEvent:
    """Main functionalities:
    The GameEvent class is responsible for creating and managing game events. It stores information about the event, such as its name, title, body, and end text, as well as any functions associated with it. The class also generates the body of the event based on a randomly selected planet and a deal offered by its alien population.

    Methods:
    - __init__(self, name, title, body, end_text, functions, **kwargs): initializes a new GameEvent object with the given parameters and adds it to the game_events dictionary.
    - set_body(self): generates the body of the event based on a randomly selected planet and a deal offered by its alien population.

    Fields:
    - name: the name of the event.
    - title: the title of the event.
    - body: the body of the event.
    - end_text: the text displayed when the event ends.
    - functions: any functions associated with the event.
    - deal: the deal offered by the alien population of a randomly selected planet.
    - event_id: the unique identifier of the event."""
    game_events = {}

    def __init__(self, name, title, body, end_text, functions, **kwargs):
        self.name = name
        self.title = title
        self.body = body
        self.end_text = end_text
        self.functions = functions
        self.deal = kwargs.get("deal", None)
        self.event_id = len(GameEvent.game_events.keys())

        GameEvent.game_events[self.name] = self

    def set_body(self):
        # check for valid references, otherwise return
        if not global_params.app:
            return

        # check for deal, otherwise don't change the body
        if not self.deal:
            return

        # get a random planet from the explored planets
        explored_planets = global_params.app.explored_planets
        explored_planets_with_aliens = []

        # check if has some explored planets
        if len(explored_planets) > 0:
            explored_planets_with_aliens = [i for i in explored_planets if i.alien_population != 0]

        # check for planets with alien population, choose a random one
        if len(explored_planets_with_aliens) > 0:
            planet = random.choice(explored_planets_with_aliens)
        else:
            planet = None

        # generate text to display
        request_text = ""
        offer_text = ""

        for key, value in self.deal.request.items():
            request_text += str(value) + " " + key
        for key, value in self.deal.offer.items():
            offer_text += str(value) + " " + key

        # set body
        if planet:
            self.body = f"the alien population of the planet {planet.name} offers you a deal: they want {request_text} for {offer_text}."
        else:
            self.body = f"some aliens offer you a deal: they want {request_text} for {offer_text}"

    def end_game(self):
        pygame.quit()
        quit()
        sys.exit()

    def restart_game(self):
        print("restart game")
        global_params.app.restart_game()


# define GameEvents
start = GameEvent(
    name="start",
    title="Welcome !!!",
    body="... after 75000 years of darkness, you finally reached the the solar system " \
         "of ExoPrime I.\nYou are the last survivors from PlanetEarth.Mankind is " \
         "counting on you, so don't mess it up!!!\nYour goal is to get at least 500 people " \
         "surviving ! ",
    end_text="GOOD LUCK !",
    functions=None,
    )

goal1 = GameEvent(
    name="goal1",
    title="Congratulation!",
    body="your population has reached 500 people.  ",
    end_text="",
    functions=None
    )

goal2 = GameEvent(
    name="goal2",
    title="Congratulation!",
    body="your population has reached 1000 people.\nYou are now able to build second level buildings like:\n\n" +
         str(building_factory.get_a_list_of_building_names_with_build_population_minimum_bigger_than(1000)).split("[")[
             1].split("]")[0],
    end_text="go for it!",
    functions=None
    )

goal3 = GameEvent(
    name="goal3",
    title="Congratulation!",
    body="your population has reached 10000 people.\nYou are now able to build third level buildings like:\n\n" +
         str(building_factory.get_a_list_of_building_names_with_build_population_minimum_bigger_than(10000)).split("[")[
             1].split("]")[0],
    end_text="go for it!",
    functions=None
    )

alien_deal_random = GameEvent(
    name="alien_deal_random",
    title="Deal Offer",
    body="the alien population of the planet (not set) offers you a deal: they want 200 food for 33 technology.",
    end_text="do you accept the offer?",
    deal=Deal(offer={random.choice(resources): random.randint(0, 1000)}, request={random.choice(resources): random.randint(0, 1000)}),
    functions={"yes": None, "no": None},
    )

friendly_trader = GameEvent(
    name="friendly_trader",
    title="Deal Offer",
    body="the alien population of the planet (not set) offers you a deal: they want 200 food for 33 technology.",
    end_text="do you accept the offer?",
    deal=Deal(offer={random.choice(resources): random.randint(0, 1000)}, request={random.choice(resources): random.randint(0, 1000)}, friendly=True),
    functions={"yes": None, "no": None},
    friendly=True
    )

end = GameEvent(
    name="end",
    title="GAME OVER !!!",
    body="... Bad Luck !!! ... ",
    end_text="make it better next time!  RESTART?!",
    functions={"yes": "self.game_event.restart_game()", "no": "self.game_event.end_game()"},
    )
