import time

from source.game_play.game_events import GameEvent
from source.handlers.file_handler import load_file
from source.text.info_panel_text_generator import info_panel_text_generator


# def create_random_event(self):
#     if self.event_time > self.random_event_time:
#         self.random_event_time += random.randint(self.min_intervall, self.intervall) * config.game_speed
#         event = GameEvent(
#             name="alien_deal_random",
#             title="Deal Offer",
#             body="the alien population of the planet (not set) offers you a deal: they want 200 food for 33 technology.",
#             end_text="do you accept the offer?",
#             deal=Deal(offer={random.choice(resources): random.randint(0, 1000)}, request={random.choice(resources): random.randint(0, 1000)}),
#             functions={"yes": None, "no": None},
#             condition=None
#             )
#         event.offer = {random.choice(resources): random.randint(0, 1000)}
#         event.request = {random.choice(resources): random.randint(0, 1000)}
#         GameEvent.game_events[event.name] = event.name
#         self.set_game_event(event)


class GameEventHandler:
    def __init__(self, data, app):
        # intitialize variables
        self.level = 0
        self.data = data
        self.app = app
        self.game_event_interval = 0
        self.update_interval = data.get("update_interval")
        self.start_time = time.time()
        self.event_time = 0
        self.goal = {}
        self.goal_success = {}

        self.event_cue = []
        self.obsolete_events = {}
        self.game_events = {}
        self.resources = ["water", "food", "energy", "technology", "minerals", "population"]

        # add game events
        self.game_events["start"] = GameEvent(
                name="start",
                title="Welcome !!!",
                body="... after 75000 years of darkness, you finally reached the the solar system " \
                     "of ExoPrime I.\nYou are the last survivors from PlanetEarth.Mankind is " \
                     "counting on you, so don't mess it up!!!\nYour goal is to get at least 500 people " \
                     "surviving ! ",
                end_text="GOOD LUCK !",
                functions=None,
                condition=None,
                id_=len(self.game_events.keys())
                )

        self.game_events["end"] = GameEvent(
                name="end",
                title="GAME OVER !!!",
                body="... Bad Luck !!! ... ",
                end_text="make it better next time!  RESTART?!",
                functions={"yes": "restart_game", "no": "end_game"},
                condition=None,
                id_=len(self.game_events.keys())
                )

        self.event_cue.append(self.game_events["start"])

        # setup variables
        self.setup()

    def setup(self):
        data = load_file("game_event_handler.json", "config")
        for key, value in data.items():
            if key in self.__dict__:
                setattr(self, key, value)

    def set_goal(self, goal):
        self.goal = goal
        self.set_goal_success()

    def set_goal_success(self):
        self.goal_success = {}
        for key, value in self.goal.items():
            self.goal_success[key] = False

    def end_game(self):
        # check for condition to end the game
        # create random event (alien deals)
        # self.create_random_event()

        # print (f"self.parent.player.{self.goal},  {eval(f'self.parent.player.{self.goal}')}")
        # check if level goal is reached

        # end game event
        # self.end_game(self.parent.player)
        # self.end_game()
        player = self.app.player
        """ this checks for conditions to end the game"""
        for key, value in player.get_stock().items():
            if value < 0:
                if not key == "energy":
                    print(f"end_game: {key} is lower than 0")
                    if not "end" in self.obsolete_events:
                        self.app.event_panel.set_game_event(self.game_events["end"])

    def restart_game(self):
        if self.app.level_handler.current_game.startswith("level_"):
            self.app.level_handler.load_level(self.app.level_handler.current_game, "levels")
        else:
            self.app.level_handler.load_level(self.app.level_handler.current_game, "games")

    def update(self):
        # check the cue and activate first event, then delete it
        if len(self.event_cue) > 0:
            next_event = self.event_cue[0]
            if not next_event in self.obsolete_events.keys():
                self.app.event_panel.set_game_event(next_event)
                self.obsolete_events[next_event.name] = next_event
                self.event_cue.pop(0)

        # check for update interval
        if not time.time() - self.start_time > self.update_interval:
            return

        # set event_time
        self.event_time = time.time() - self.start_time

        # activate timed event
        if self.event_time > self.game_event_interval:
            self.start_time = time.time()
            self.activate_timed_events()

        self.evaluate_goal()

        # end game event
        self.end_game()
        # print (self.game_events)

    def evaluate_goal(self):
        """ goal must  be a dict:
            keys can be resources or buildings, or any other ideas ??

            if key is a resource, value must be int
            if key is a building , value must be int
        """
        # reset the goal success to make sure values are correct after level load
        self.set_goal_success()

        # set body text
        body = "you have reached the goal:"

        # check for goal
        for key, value in self.goal.items():
            # evaluate the goals: check if certain resource is > value
            if key in self.resources:
                player_value = eval(f"self.app.player.{key}")
                if player_value > value:
                    self.goal_success[key] = True
                    body += f"your {key} is greater than {value} "
                else:
                    self.goal_success[key] = False

            # check if has the building amount > value
            if key in self.app.player.get_all_buildings():
                if self.app.player.get_all_buildings().count(key) >= value:
                    self.goal_success[key] = True
                    body += f"and you have build a {value}"
                else:
                    self.goal_success[key] = False
            # else:
            #     self.goal_success[key] = False

        # debug only
        body += f"event_cue: {self.event_cue}, obsolete_events: {self.obsolete_events}, goal_success: {self.goal_success}"

        # set mission text
        self.app.settings_panel.mission_icon.info_text = info_panel_text_generator.create_info_panel_mission_text()

        # create event if succeeded
        all_values_are_true = all(value for value in self.goal_success.values())
        if all_values_are_true:
            # print(self.data)
            if not f"goal{self.level}" in self.obsolete_events.keys():
                self.game_events[f"goal{self.level}"] = GameEvent(
                        name=f"goal{self.level}",
                        title="Congratulation!",
                        body=f"{body}. Well Done! move to next level !",
                        end_text="",
                        functions={"yes": "load_next_level", "no": "update_level_success"},
                        condition="",
                        id_=len(self.game_events.keys())
                        )
                self.event_cue.append(self.game_events[f"goal{self.level}"])
                self.app.event_panel.set_game_event(self.game_events[f"goal{self.level}"])

    def update_level_success(self):
        self.app.level_handler.save_level_succcess_to_file(f"level_{self.level}.json", "levels", True)
        self.app.level_handler.update_level_successes()
        self.app.level_select.update_icons()

    def load_next_level(self):
        self.app.level_handler.save_level_succcess_to_file(f"level_{self.level}.json", "levels", True)
        self.level += 1
        self.app.level_handler.load_level(f"level_{self.level}.json", "levels")
        self.app.level_handler.update_level_successes()
        self.app.level_select.update_icons()

    def activate_timed_events(self):
        pass
        # print (f"activating timed event:")
