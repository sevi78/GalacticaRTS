import random

import pygame
from pygame_widgets.mouse import Mouse, MouseState

from source.editors.editor_base.editor_base import EditorBase
from source.factories.planet_factory import planet_factory
from source.game_play.game_events import GameEvent, Deal, resources
from source.gui.widgets.buttons.button import Button
from source.interfaces.interface import InterfaceData
from source.utils import global_params
from source.utils.colors import colors
from source.multimedia_library.images import images, pictures_path, get_image
from source.multimedia_library.sounds import sounds
from source.database.saveload import load_file
from source.utils.text_wrap import TextWrap


class EventPanel(TextWrap, EditorBase, InterfaceData):
    """Main functionalities:
    The EventPanel class is responsible for creating and managing game events in the GUI. It displays event information,
    such as the title, body, and end text, as well as any functions associated with it. The class also generates
    the body of the event based on a randomly selected planet and a deal offered by its alien population.
    It allows the player to accept or decline the deal, and handles the consequences of their decision.

    Methods:
    - accept(): handles the player accepting the deal offered by the alien population.
    - decline(): handles the player declining the deal offered by the alien population.
    - set_text(): sets the text for the event panel based on the current game event.
    - center_pos(width, height): calculates the center position of the event panel based on its width and height.
    - wrap_text(text, pos, font, color): wraps the text of the event body to fit within the event panel.
    - draw(): draws the event panel on the screen.
    - listen(events): listens for events, such as mouse clicks or key presses, and handles them accordingly.
    - set_game_event(event): sets the current game event to the given event.
    - close_event(): closes the current game event.
    - create_random_event(): creates a random game event based on a randomly selected planet and a deal offered by its
      alien population.
    - debug_events(function): prints debug information about the current game events.

    Fields:
    - win: the Pygame window.
    - x: the x-coordinate of the event panel.
    - y: the y-coordinate of the event panel.
    - width: the width of the event panel.
    - height: the height of the event panel.
    - layer: the layer of the event panel.
    - parent: the parent widget of the event panel.
    - frame_color: the color of the event panel's frame.
    - bg_color: the background color of the event panel.
    - font: the font used for the event panel's text.
    - title_font: the font used for the event panel's title.
    - center: a boolean indicating whether the event panel should be centered on the screen.
    - surface: the Pygame surface of the event panel.
    - surface_rect: the rectangle of the event panel's surface.
    - image: the image used for the event panel.
    - image_scaled: the scaled image used for the event panel.
    - game_event: the current game event.
    - game_events: a dictionary of all game events.
    - event_time: the time since the last game event.
    - min_intervall: the minimum time between random game events.
    - intervall: the maximum time between random game events.
    - random_event_time: the time until the next random game event.
    - text_surfaces: a dictionary of all text surfaces for the event panel.
    - border: the border size of the event panel.
    - size: the size of the event panel.
    - word_height_sum: the sum of the heights of all words in the event panel's body.
    - title: the title of the current game event.
    - title_surface_rect: the rectangle of the title surface.
    - title_surface: the surface of the title.
    - body: the body of the current game event.
    - end_text: the end text of the current game event.
    - end_text_surface_rect: the rectangle of the end text surface.
    - end_text_surface: the surface of the end text.
    - functions: the functions associated with the current game event.
    - event_cue: a list of game events to be displayed.
    - obsolete_events: a list of game events that have already been displayed.
    - yes_button: the button used to accept the deal offered by the alien population.
    - no_button: the button used to decline the deal offered by the alien population."""

    def __init__(self, win, x, y, width, height, interface_variables, **kwargs):
        TextWrap.__init__(self)
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        self.interface_variables = interface_variables

        self.name = "event panel"
        self.layer = kwargs.get("layer", 9)
        self.win = win
        self.parent = kwargs.get("parent")
        self.frame_color = colors.frame_color
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.font_size = 32
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.title_font = pygame.font.SysFont(global_params.font_name, 50)
        self.center = kwargs.get("center", True)

        # surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect[0] = x
        self.surface_rect[1] = y
        self.image = images[pictures_path]["textures"]["event_panel.png"]
        self.image_scaled = pygame.transform.scale(self.image, (width, height))

        # events
        self.game_event = None
        self.game_events = GameEvent.game_events
        self.event_time = 0
        self.min_intervall = 3500
        self.intervall = 10000
        self.random_event_time = self.intervall * global_params.time_factor

        # text
        self.size = (width + self.get_screen_x() - self.get_screen_width() / 6,
                     height + self.get_screen_height())  # used for text wrapper, makes no sense but works

        self.title = None
        self.title_surface_rect = None
        self.title_surface = None

        self.body = None
        self.end_text = None
        self.end_text_surface_rect = None
        self.end_text_surface = None

        self.functions = []
        self.event_cue = []
        self.obsolete_events = []

        # Buttons
        self.yes_button = Button(self.win, self.get_screen_x() + self.get_screen_width() / 2 - 30,
                                           self.world_y + self.get_screen_height(), 60, 60, isSubWidget=False,
            image=pygame.transform.scale(get_image("yes_icon.png"), (60, 60)),
            transparent=True, parent=self, onClick=lambda: self.accept())

        self.no_button = Button(self.win, self.get_screen_x() + self.get_screen_width() / 2 + 30,
                                          self.world_y + self.get_screen_height(), 60, 60, isSubWidget=False,
            image=pygame.transform.scale(get_image("no_icon.png"), (60, 60)),
            transparent=True, parent=self, onClick=lambda: self.decline())

        # set start event event
        self.set_game_event(self.game_events["start"])

        # interface
        self.interface_variable_names = []

        for dict_name, dict in interface_variables.items():
            for key, value in dict.items():
                setattr(self, key, value)
                setattr(self, key + "_max", value)
                if not key.endswith("_max"):
                    self.interface_variable_names.append(key)

        InterfaceData.__init__(self, self.interface_variable_names)
        self.setup()

    def setup(self):
        data = load_file("event_panel.json")
        for name, dict in data.items():
            if name == self.name:
                for key, value in dict.items():
                    if key in self.__dict__:
                        setattr(self, key, value)

    def accept(self):
        if not self._hidden:
            if self.game_event.functions:
                if self.game_event.deal:
                    self.game_event.deal.make_deal()

                else:
                    exec(self.game_event.functions["yes"])

            self.close_event()
            self.hide()
            global_params.game_paused = False

    def decline(self):
        if self.game_event.functions:
            if self.game_event.functions["no"]:
                exec(self.game_event.functions["no"])

        if not self._hidden:
            self.hide()
            self.close_event()
            global_params.game_paused = False

    def set_text(self):
        self.title = self.game_event.title
        self.body = self.game_event.body
        self.end_text = self.game_event.end_text
        self.functions = self.game_event.functions

        if not self.functions:
            self.yes_button.hide()
            self.no_button.hide()
        else:
            self.yes_button.show()
            self.no_button.show()

        self.show()

        global_params.game_paused = True
        self.obsolete_events.append(self.game_event.name)

    def center_pos(self, width, height):
        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()

        x = win_width / 2 - width / 2
        y = win_height / 2 - height / 2
        pos = (x, y)

        return pos

    def set_game_event(self, event):
        if not event in self.event_cue:
            self.event_cue.append(event)

        self.game_event = self.event_cue[0]
        if self.game_event.deal:
            self.game_event.deal.create_friendly_offer()
        self.game_event.set_body()
        self.set_text()

    def close_event(self):
        try:
            self.event_cue.pop(0)
        except IndexError as e:
            print("event_panel.close_event: error:", e)

        self.obsolete_events.append(self.game_event)

        # dirty hack to make shure the planets get loaded correctly
        if len(self.obsolete_events) == 2:
            #planet_factory.load_planets()
            print("""event_panel.close_event: dirty hack to make shure the planets get loaded correctly:
                     if len(self.obsolete_events) == 2:
                            self.parent.load_planets()""")

    def create_random_event(self):
        if self.event_time > self.random_event_time:
            self.random_event_time += random.randint(self.min_intervall, self.intervall) * global_params.game_speed
            event = GameEvent(
                name="alien_deal_random",
                title="Deal Offer",
                body="the alien population of the planet (not set) offers you a deal: they want 200 food for 33 technology.",
                end_text="do you accept the offer?",
                deal=Deal(offer={random.choice(resources): random.randint(0, 1000)}, request={random.choice(resources): random.randint(0, 1000)}),
                functions={"yes": None, "no": None},
                )
            event.offer = {random.choice(resources): random.randint(0, 1000)}
            event.request = {random.choice(resources): random.randint(0, 1000)}
            GameEvent.game_events[event.name] = event.name
            self.set_game_event(event)

    def debug_events(self):

        print("self.game_events", self.game_events)
        print("self.event_cue", self.event_cue)
        print("self.obsolete_events", self.obsolete_events)

    def update(self):
        """
        calls the game events based on time or conditions
        """
        if not global_params.enable_game_events:
            return
        # print (self.event_time, self.min_intervall, self.intervall, self.random_event_time)
        self.event_time += 1 * global_params.game_speed
        self.create_random_event()

        player = self.parent.player
        if player.population >= 500:
            if not "goal1" in self.obsolete_events:
                self.set_game_event(self.game_events["goal1"])

        if player.population >= 1000:
            if not "goal2" in self.obsolete_events:
                self.set_game_event(self.game_events["goal2"])

        if player.population >= 10000:
            if not "goal3" in self.obsolete_events:
                self.set_game_event(self.game_events["goal3"])

        self.end_game(player)
        # self.debug_events()

    def end_game(self, player):
        """ this checks for conditions to end the game"""
        for key, value in player.get_stock().items():
            if value < 0:
                if not key == "energy":
                    if not "end" in self.obsolete_events:
                        self.set_game_event(self.game_events["end"])

    def listen(self, events):
        self.update()
        mouseState = Mouse.getMouseState()
        for event in events:
            if mouseState == MouseState.CLICK:
                if not self.functions:
                    if not self._hidden:
                        self.close_event()
                        global_params.game_paused = False

                    self.hide()

    def draw(self):
        if not self._hidden:
            # image
            self.win.blit(self.image_scaled, self.surface_rect)
            # self.draw_frame()
            # title
            self.title_surface = self.title_font.render(self.title, self.font, colors.ui_dark)
            self.title_surface_rect = self.title_surface.get_rect()
            self.title_surface_rect.x = self.world_x + self.get_screen_width() / 2 - self.title_surface.get_width() / 2
            self.title_surface_rect.y = (self.world_y + self.get_screen_height() / 8)
            self.win.blit(self.title_surface, self.title_surface_rect)

            # body
            self.wrap_text(self.body, (self.get_position()[0] + self.get_screen_width() / 6,
                                       self.title_surface_rect.y + 60), self.size, self.font, colors.ui_dark)

            # end_text
            self.end_text_surface = self.font.render(self.end_text, self.font, colors.ui_dark)
            self.end_text_surface_rect = self.end_text_surface.get_rect()
            self.end_text_surface_rect.x = self.world_x + self.get_screen_width() / 2 - self.end_text_surface.get_width() / 2
            self.end_text_surface_rect.y = self.world_y + self.get_screen_height() - self.get_screen_height() / 3
            self.win.blit(self.end_text_surface, self.end_text_surface_rect)

            # buttons
            self.yes_button.set_position((
                self.world_x + self.get_screen_width() / 2 - self.yes_button.get_screen_width(),
                self.end_text_surface_rect.y + self.yes_button.get_screen_height() / 2))

            self.no_button.set_position((self.world_x + self.get_screen_width() / 2, self.yes_button.get_screen_y()))

            # sound
            pygame.mixer.music = sounds.intro_drama
            pygame.mixer.music.play(fade_ms=1000)

        else:
            pygame.mixer.Sound.fadeout(sounds.intro_drama, 5000)
            self.yes_button.hide()
            self.no_button.hide()
