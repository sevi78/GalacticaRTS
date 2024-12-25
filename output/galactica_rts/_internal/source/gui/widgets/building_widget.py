import copy

import pygame

from source.configuration.game_config import config
from source.factories.weapon_factory import weapon_factory
from source.gui.widgets.buttons.button import Button
from source.gui.widgets.progress_bar import ProgressBar
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.garbage_handler import garbage_handler
from source.handlers.orbit_handler import set_orbit_object_id
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image, overblit_button_image
from source.multimedia_library.sounds import sounds

PROGRESSBAR_UPDATE_RATE_IN_SECONDS = 0.1
FONT_SIZE = 10


class BuildingWidget(WidgetBase):
    """
    Summary:

    The BuildingWidget class is a subclass of WidgetBase and represents a widget that displays information about a
    building. It includes a button for building the corresponding building, a progress bar to show the building
    progress, and text to display the building name and progress percentage.

    Example Usage:

    # Create a BuildingWidget instance
    building_widget = BuildingWidget(win, x, y, width, height, name, receiver, key, value, **kwargs)

    # Update the progress bar
    building_widget.update_progressbar()

    # Set the building to the receiver
    building_widget.set_building_to_receiver()

    # Draw the widget
    building_widget.draw()

    # Delete the widget
    building_widget.delete()

    # Listen for events
    building_widget.listen(events)
    Code Analysis
    Main functionalities
    Display building information including name, progress bar, and text
    Update the progress bar based on the building production time and game speed
    Set the building to the receiver and perform necessary calculations
    Draw the widget on the screen and reposition its elements dynamically
    Delete the widget and its references
    Listen for events and handle button interactions

    Methods:

    __init__(self, win, x, y, width, height, name, receiver, key, value, **kwargs): Initializes the BuildingWidget
    instance with the given parameters and sets up its properties.

    update_progressbar(self): Updates the progress bar based on the building production time and game speed.

    set_building_to_receiver(self): Sets the building to the receiver and performs necessary calculations.

    draw(self): Repositions the elements dynamically, draws the widget on the screen, and deletes itself if the progress
    is finished.
    delete(self): Deletes the widget and its references.

    listen(self, events): Listens for events and handles button interactions.

    function(self, arg): Performs a function when the button is clicked.

    set_tooltip(self): Sets the tooltip for the button.

    build_immediately(self): Builds the building immediately by deducting the necessary technology units.

    Fields:

    layer: The layer of the widget.
    text: The text to display on the widget.
    name: The name of the building.
    receiver: The receiver object for the building.
    key: The key for the building value.
    value: The value for the building.
    immediately_build_cost: The cost for immediately building the building.
    tooltip: The tooltip text for the button.
    is_building: A flag indicating if the building is being built.
    win: The window surface.
    dynamic_x: The dynamic x position of the widget.
    cue_id: The cue id of the widget.
    spacing: The spacing between widgets.
    font_size: The font size for the text.
    font: The font for the text.
    image: The image for the button.
    building_production_time: The production time for the building.
    button: The button widget.
    text_render: The rendered text for the widget.
    progress_bar_update_rate: The update rate for the progress bar.
    progress_bar_start_time: The start time for the progress bar.
    progress_bar_width: The width of the progress bar.
    progress_bar_height: The height of the progress bar.
    start_time: The start time of the widget.
    progress_bar: The progress bar widget.
    dynamic_y: The dynamic y position of the widget.
    buildings: The list of buildings for the receiver.
    button: The button widget.
    building_widget_list: The list of building widgets.
    game_speed: The game speed.
    tooltip_instance: The tooltip instance.
    info_panel: The info panel widget.
    progress_increment: The progress increment for the progress bar.
    current_time: The current time.
    production_time: The production time for the building.
    relative_production_time: The relative production time for the building.
    ships: The list of ship names.
    planet_defence_upgrades: The list of planet defence upgrades.
    weapons: The list of weapons for the receiver.
    debug_text: The debug text for the widget.

    """

    def __init__(self, win, x, y, width, height, name, receiver, key, value, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)
        self.layer = kwargs.get("layer")
        self.text = name + ":"
        self.name = name
        self.receiver = receiver
        self.key = key
        self.value = value
        self.immediately_build_cost = 0
        self.tooltip = kwargs.get("tooltip", "no tooltip set yet!")
        self.is_building = kwargs.get("is_building", True)
        self.ship_names = kwargs.get("ship_names", [])

        # get the position and size
        self.win = pygame.display.get_surface()
        height = win.get_height()
        self.dynamic_x = config.app.ui_helper.anchor_right
        self.cue_id = len(config.app.building_widget_list)
        self.spacing = 5
        self.dynamic_y = height - self.spacing - self.get_screen_height() - self.get_screen_height() * self.cue_id
        self.font_size = kwargs.get("fontsize", FONT_SIZE)
        self.font = pygame.font.SysFont(kwargs.get("fontname", config.font_name), self.font_size)
        self.spacing = kwargs.get("spacing", 15)

        if self.is_building:
            self.image = pygame.transform.scale(get_image(self.name + "_25x25.png"), (25, 25))
        else:
            self.image = pygame.transform.scale(get_image(self.name + ".png"), (25, 25))

        self.building_production_time = kwargs.get("building_production_time")

        # button
        self.button = Button(self.win,
                x=self.dynamic_x + self.get_screen_height() / 2,
                y=self.dynamic_y,
                width=self.get_screen_height(),
                height=self.get_screen_height(),
                image=self.image,
                on_click=lambda: self.function("do nothing"),
                transparent=True,
                image_hover_surface_alpha=255,
                parent=config.app,
                tooltip=self.tooltip, layer=self.layer)

        # text
        self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)

        # progress bar
        self.progress_bar_update_rate = PROGRESSBAR_UPDATE_RATE_IN_SECONDS
        self.progress_bar_start_time = time_handler.time
        self.progress_bar_width = kwargs.get("progress_bar_width", 100)
        self.progress_bar_height = kwargs.get("progress_bar_height", 10)
        self.start_time = time_handler.time

        self.progress_bar = ProgressBar(win=self.win,
                x=self.dynamic_x + self.button.get_screen_width(),
                y=self.button.screen_y + self.progress_bar_height / 2,
                width=self.progress_bar_width,
                height=self.progress_bar_height,
                progress=lambda: 0,
                curved=True,
                completed_color=self.frame_color, layer=self.layer, ignore_progress=True)

        self.surface_rect = pygame.Rect(self.dynamic_x, self.dynamic_y, self.get_screen_width(), self.get_screen_height())

        # overblit image
        self.overblit_image_name = None
        if self.receiver.owner > -1:
            self.overblit_image_name = config.app.players[self.receiver.owner].image_name

        # frame owner coloring
        self.frame_color = self.receiver.player_color
        # register
        config.app.building_widget_list.append(self)

    def __repr__(self):
        return f"{self.name}: {self.receiver}"

    def update_progressbar(self) -> None:
        # get game speed
        game_speed = time_handler.game_speed

        # get current time
        current_time = time_handler.time

        # production time
        production_time = self.building_production_time

        # relative_production_time
        relative_production_time = production_time / game_speed

        # check if timer is ready
        if current_time - self.progress_bar_start_time > self.progress_bar_update_rate:
            # calculate the progress increment, taking into account the update rate
            progress_increment = (1 / relative_production_time) * self.progress_bar_update_rate

            # set value to progressbar
            self.progress_bar.percent += progress_increment

            # Ensure the adjusted progress percentage is within [0, 1]
            self.progress_bar.percent = min(max(self.progress_bar.percent, 0), 1)

            # reset timer
            self.progress_bar_start_time = current_time

    def set_building_to_receiver(self):
        """
        overgive the values stores for the receiver: wich building to append, sets population limit, calculates production
        and calls calculate_global_production()
        and plays some nice sound :)
        :return:
        """
        # this should be fixed
        if self.receiver.owner == -1:
            print(f"set_building_to_receiver: You can't build on this planet!: {self.receiver.name}")
            return

        # technology_upgrades = ["university"]
        planet_defence_upgrades = ["cannon", "missile"]
        weapons = None
        if self.receiver.property == "ship":
            weapons = self.receiver.weapon_handler.all_weapons.keys()

        sounds.play_sound("success", channel=7)

        # remove self from planets building cue:
        self.receiver.economy_agent.building_cue -= 1

        # if it is a ship, no calculation has to be done, return : name, x, y, parent, weapons, **kwargs):
        if self.name in self.ship_names:
            x, y = pan_zoom_handler.screen_2_world(self.receiver.rect.centerx, self.receiver.rect.centery)

            # set autopilot true for all players except human player (0)
            autopilot = self.receiver.owner != 0
            ship = config.app.ship_factory.create_ship(
                    self.name,
                    x,
                    y,
                    config.app,
                    {},
                    data={"owner": self.receiver.owner, "autopilot": autopilot},
                    owner=self.receiver.owner)

            set_orbit_object_id(ship, self.receiver.id)

            return

        if self.name in planet_defence_upgrades:
            self.receiver.economy_agent.buildings.append(self.name)
            return

        if weapons:
            if self.name in weapons:
                # upgrade
                if self.name in self.receiver.weapon_handler.weapons.keys():
                    self.receiver.weapon_handler.weapons[self.name]["level"] += 1
                else:
                    # buy it
                    self.receiver.weapon_handler.weapons[
                        self.name] = copy.deepcopy(weapon_factory.get_weapon(self.name))
                    # if config.app.ship == self.receiver:
                    config.app.weapon_select.obj = self.receiver
                    config.app.weapon_select.update()

                print(f"self.receiver: {self.receiver}, self.receiver.weapons({self.name}):{self.receiver.weapon_handler.weapons[self.name]['level']}\n"
                      f"all_weapons: {config.app.weapon_select.all_weapons[self.name]['level']}")
                return

        # append to receivers building list
        self.receiver.economy_agent.buildings.append(self.name)
        self.receiver.economy_agent.set_technology_upgrades(self.name)

        # set new value to receivers production
        # setattr(self.receiver, self.name, getattr(self.receiver, "production_" + self.key) - self.value)

        # set new value to player production
        player = config.app.players[self.receiver.owner]
        # setattr(player, self.name, getattr(player, self.key) - self.value)

        # calculate production
        self.receiver.economy_agent.set_population_limit()
        self.receiver.economy_agent.calculate_production()
        config.app.calculate_global_production(player)
        config.app.tooltip_instance.reset_tooltip(self)

        # # debug
        # debug_text = f"lifetime of building widget: {self.name} was: {time_handler.time - self.start_time}, building_production time is:{self.building_production_time} at game_speed:{time_handler.game_speed}"
        # event_text.text = debug_text
        # config.app.info_panel.set_text(debug_text)
        # print(debug_text)

    def function(self, arg):
        player = config.app.players[self.receiver.owner]
        config.tooltip_text = ""
        if self.immediately_build_cost < player.stock["technology"] and self.receiver.owner == config.player:
            self.build_immediately()

    def set_tooltip(self):
        self.button.tooltip = f"are you sure to build this {self.name} immediately? this will cost you {self.immediately_build_cost} technology units?{self.receiver}"

    

    def build_immediately(self):
        """ !!! make shure the correct player is adressed!!!"""
        if config.app.game_client.connected:
            message = {
                "f": "build_immediately",
                "cue_id": self.cue_id
                }

            config.app.game_client.send_message(message)
        else:
            self.handle_build_immediately(self.cue_id)

    def handle_build_immediately(self, cue_id: int):

        player = config.app.players[self.receiver.owner]
        player.stock["technology"] -= self.immediately_build_cost
        self.set_building_to_receiver()
        self.delete()

    def delete(self):
        if self in config.app.building_widget_list:
            config.app.building_widget_list.remove(self)
        if self.progress_bar:
            self.progress_bar.__del__()
        if self.button:
            self.button.__del__()
        self.__del__()
        garbage_handler.delete_all_references(self, self.progress_bar)
        garbage_handler.delete_all_references(self, self.button)
        garbage_handler.delete_all_references(self, self)

    def listen(self, events):
        for event in events:
            if not self.button:
                return
            if self.button.rect.collidepoint(pygame.mouse.get_pos()):
                self.immediately_build_cost = int((1 - self.progress_bar.percent) * self.building_production_time)
                self.set_tooltip()

    def draw(self):
        """
        reposition the elements dynamically, draw elements, and finally deletes itself
        """

        # show owner
        overblit_button_image(self.button, self.overblit_image_name, False, offset_x=5, size=(
            25, 25), outline=True, color=self.receiver.player_color)

        # update progress bar
        if not time_handler.game_speed == 0 and not config.game_paused:
            self.update_progressbar()

        # reposition
        widget_height = self.get_screen_height()
        self.dynamic_x = config.app.ui_helper.anchor_right
        spacing = 5

        # get the position and size
        win = pygame.display.get_surface()
        height = win.get_height()
        y = height - spacing - widget_height - widget_height * self.cue_id

        # frame
        self.surface_rect = pygame.Rect(self.dynamic_x, y, self.get_screen_width(), self.get_screen_height())
        self.draw_frame()

        # button
        self.button.image_hover_surface.set_alpha(0)
        self.button.set_position((config.app.ui_helper.anchor_right, y))

        # progress_bar
        self.progress_bar.set_screen_width(config.app.building_panel.get_screen_width() - self.button.get_screen_width() - 15)
        self.progress_bar.set_position((
            self.dynamic_x + self.button.get_screen_width() + 5, y + self.button.get_screen_height() / 2))

        # draw widgets text
        self.text = self.name + ": " + str(int(self.progress_bar.percent * 100)) + "%/ " + str(config.app.ui_helper.hms(self.building_production_time))
        self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)
        self.win.blit(self.text_render, (self.dynamic_x + self.button.get_screen_width(), self.button.screen_y + 2))

        # move down if place is free
        for i in range(len(config.app.building_widget_list)):
            if config.app.building_widget_list[i] == self:
                self.cue_id = config.app.building_widget_list.index(config.app.building_widget_list[i])

        # if progress is finished, set building to receiver
        if self.progress_bar.percent == 1:
            self.set_building_to_receiver()

            # finally delete it and its references
            self.delete()
