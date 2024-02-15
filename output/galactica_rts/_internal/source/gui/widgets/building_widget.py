import copy
import time

import pygame

from source.configuration import global_params
from source.factories.weapon_factory import weapon_factory
from source.gui.widgets.buttons.button import Button
from source.gui.widgets.progress_bar import ProgressBar
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.orbit_handler import set_orbit_object_id
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds

PROGRESSBAR_UPDATE_RATE_IN_SECONDS = 0.1


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

        # get the position and size
        self.win = pygame.display.get_surface()
        height = win.get_height()
        self.dynamic_x = global_params.app.ui_helper.anchor_right
        self.cue_id = len(global_params.app.building_widget_list)
        self.spacing = 5
        self.dynamic_y = height - self.spacing - self.get_screen_height() - self.get_screen_height() * self.cue_id
        self.font_size = kwargs.get("fontsize", 15)
        self.font = pygame.font.SysFont(kwargs.get("fontname", global_params.font_name), kwargs.get("fontsize", 15))
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
            onClick=lambda: self.function("do nothing"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=global_params.app,
            tooltip=self.tooltip, layer=self.layer)

        # text
        self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)

        # progress bar
        self.progress_bar_update_rate = PROGRESSBAR_UPDATE_RATE_IN_SECONDS
        self.progress_bar_start_time = time.time()
        self.progress_bar_width = kwargs.get("progress_bar_width", 100)
        self.progress_bar_height = kwargs.get("progress_bar_height", 10)
        self.start_time = time.time()

        self.progress_bar = ProgressBar(win=self.win,
            x=self.dynamic_x + self.button.get_screen_width(),
            y=self.button.screen_y + self.progress_bar_height / 2,
            width=self.progress_bar_width,
            height=self.progress_bar_height,
            progress=lambda: 0,
            curved=True,
            completedColour=self.frame_color, layer=self.layer, ignore_progress=True)

        # register
        global_params.app.building_widget_list.append(self)

    def update_progressbar(self) -> None:
        # get game speed
        game_speed = global_params.game_speed

        # get current time
        current_time = time.time()

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
        ships = ["spaceship", "cargoloader", "spacehunter"]
        # technology_upgrades = ["university"]
        planet_defence_upgrades = ["cannon", "missile"]
        weapons = None
        if self.receiver.property == "ship":
            weapons = self.receiver.weapon_handler.all_weapons.keys()

        sounds.play_sound("success", channel=7)

        # remove self from planets building cue:
        self.receiver.building_cue -= 1

        # if it is a ship, no calculation has to be done, return
        if self.name in ships:
            x, y = pan_zoom_handler.screen_2_world(self.receiver.screen_x, self.receiver.screen_y)
            ship = global_params.app.ship_factory.create_ship(self.name + "_30x30.png", x, y, global_params.app, {})
            set_orbit_object_id(ship, self.receiver.id)
            return

        if self.name in planet_defence_upgrades:
            self.receiver.buildings.append(self.name)
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
                    # if global_params.app.ship == self.receiver:
                    global_params.app.weapon_select.obj = self.receiver
                    global_params.app.weapon_select.update()

                print(f"self.receiver: {self.receiver}, self.receiver.weapons({self.name}):{self.receiver.weapon_handler.weapons[self.name]['level']}\n"
                      f"all_weapons: {global_params.app.weapon_select.all_weapons[self.name]['level']}")
                return

        # append to receivers building list
        self.receiver.buildings.append(self.name)
        self.receiver.set_technology_upgrades(self.name)

        # set new value to receivers production
        setattr(self.receiver, self.name, getattr(self.receiver, "production_" + self.key) - self.value)
        setattr(global_params.app.player, self.name, getattr(global_params.app.player, self.key) - self.value)

        self.receiver.set_population_limit()
        self.receiver.calculate_production()
        global_params.app.calculate_global_production()
        global_params.app.tooltip_instance.reset_tooltip(self)

        # # debug
        # debug_text = f"lifetime of building widget: {self.name} was: {time.time() - self.start_time}, building_production time is:{self.building_production_time} at game_speed:{global_params.game_speed}"
        # event_text.text = debug_text
        # global_params.app.info_panel.set_text(debug_text)
        # print(debug_text)

    def function(self, arg):
        global_params.tooltip_text = ""
        self.build_immediately()
        self.set_building_to_receiver()
        self.delete()

    def set_tooltip(self):
        self.button.tooltip = f"are you sure to build this {self.name} immediately? this will cost you {self.immediately_build_cost} technology units?{self.receiver}"

    def build_immediately(self):
        global_params.app.player.technology -= self.immediately_build_cost

    def delete(self):
        if self in global_params.app.building_widget_list:
            global_params.app.building_widget_list.remove(self)
        self.__del__()
        self.progress_bar.__del__()
        self.button.__del__()

    def listen(self, events):
        for event in events:
            if self.button.rect.collidepoint(pygame.mouse.get_pos()):
                self.immediately_build_cost = int((1 - self.progress_bar.percent) * self.building_production_time)
                self.set_tooltip()

    def draw(self):
        """
        reposition the elements dynamically, draw elements, and finally deletes itself
        """

        # update progress bar
        self.update_progressbar()
        # reposition
        widget_height = self.get_screen_height()
        self.dynamic_x = global_params.app.ui_helper.anchor_right
        spacing = 5

        # get the position and size
        win = pygame.display.get_surface()
        height = win.get_height()
        y = height - spacing - widget_height - widget_height * self.cue_id

        # button
        self.button.image_hover_surface.set_alpha(0)
        self.button.set_position((global_params.app.ui_helper.anchor_right, y))

        # progress_bar
        self.progress_bar.setWidth(global_params.app.building_panel.get_screen_width() - self.button.get_screen_width() - 15)
        self.progress_bar.set_position((
            self.dynamic_x + self.button.get_screen_width() + 5, y + self.button.get_screen_height() / 2))

        # draw widgets text
        self.text = self.name + ": " + str(int(self.progress_bar.percent * 100)) + "%/ " + str(global_params.app.ui_helper.hms(self.building_production_time))
        self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)
        self.win.blit(self.text_render, (self.dynamic_x + self.button.get_screen_width(), self.button.screen_y + 2))

        # move down if place is free
        for i in range(len(global_params.app.building_widget_list)):
            if global_params.app.building_widget_list[i] == self:
                self.cue_id = global_params.app.building_widget_list.index(global_params.app.building_widget_list[i])

        # if progress is finished, set building to receiver
        if self.progress_bar.percent == 1:
            self.set_building_to_receiver()

            # finally delete it and its references
            self.delete()
