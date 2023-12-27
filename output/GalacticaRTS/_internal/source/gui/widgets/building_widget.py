import copy
import time

import pygame

from source.factories.weapon_factory import weapon_factory
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.buttons.button import Button
from source.gui.widgets.progress_bar import ProgressBar
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.physics.orbit import set_orbit_object_id
from source.utils import global_params
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds


class BuildingWidget(WidgetBase):
    """Main functionalities:

    The BuildingWidget class is responsible for creating and managing the widgets that represent buildings in the game. It creates a button with an image, a progress bar, and text that displays the building's name and progress. It also handles the logic for building a building, including calculating the cost and updating the planet's production and population limit. When the building is complete, it removes itself from the list of building widgets and adds the building to the planet's list of buildings.

    Methods:
    - __init__: Initializes the BuildingWidget object with the necessary parameters and creates the button, progress bar, and text.
    - set_building_to_planet: Handles the logic for building a building, including updating the reciever's production and population limit.
    - draw: Repositions the elements dynamically, draws the elements, and deletes the widget when the building is complete.
    - delete: Removes the widget from the list of building widgets and deletes the widget and its references.
    - listen: Handles mouse events and sets the tooltip for the button.
    - function: Builds the building immediately and removes the widget.

    Fields:
    - win: The surface on which to draw the widget.
    - x, y: The coordinates of the top left corner of the widget.
    - width, height: The width and height of the widget.
    - name: The name of the building.
    - reciever: The reciever object on which the building is being built.
    - key: The key for the building's production value.
    - value: The value of the building's production.
    - immediately_build_cost: The cost to build the building immediately.
    - tooltip: The tooltip for the button.
    - dynamic_x, dynamic_y: The dynamic coordinates of the widget.
    - cue_id: The position of the widget in the list of building widgets.
    - font, fontsize: The font and font size for the text.
    - spacing: The spacing between elements.
    - image: The image for the button.
    - button: The button object.
    - text_render: The rendered text for the widget.
    - progress_bar_width, progress_bar_height: The width and height of the progress bar.
    - startTime: The time at which the building started being built.
    - progress_time: The time it takes to build the building.
    - progress_bar: The progress bar object."""

    def __init__(self, win, x, y, width, height, name, reciever, key, value, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)
        self.layer = kwargs.get("layer")
        self.text = name + ":"
        self.name = name
        self.reciever = reciever
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

        self.progress_time = kwargs.get("building_production_time")

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
        self.progress_bar_width = kwargs.get("progress_bar_width", 100)
        self.progress_bar_height = kwargs.get("progress_bar_height", 10)
        self.startTime = time.time()

        self.progress_bar = ProgressBar(win=self.win,
            x=self.dynamic_x + self.button.get_screen_width(),
            y=self.button.screen_y + self.progress_bar_height / 2,
            width=self.progress_bar_width,
            height=self.progress_bar_height,
            progress=lambda: (time.time() - self.startTime) / self.progress_time,
            curved=True,
            completedColour=self.frame_color, layer=self.layer
            )

        # register
        global_params.app.building_widget_list.append(self)

    def set_building_to_reciever(self):
        """
        overgive the values stores for the reciever: wich building to append, sets population limit, calculates production
        and calls calculate_global_production()
        and plays some nice sound :)
        :return:
        """
        ships = ["spaceship", "cargoloader", "spacehunter"]
        # technology_upgrades = ["university"]
        planet_defence_upgrades = ["cannon", "missile"]
        weapons = None
        if self.reciever.property == "ship":
            weapons = self.reciever.all_weapons.keys()

        sounds.play_sound("success", channel=7)

        # remove self from planets building cue:
        self.reciever.building_cue -= 1

        # if it is a ship, no calculation has to be done, return
        if self.name in ships:
            x, y = pan_zoom_handler.screen_2_world(self.reciever.screen_x, self.reciever.screen_y)
            ship = global_params.app.ship_factory.create_ship(self.name + "_30x30.png", x, y, global_params.app)
            set_orbit_object_id(ship, self.reciever.id)
            return

        if self.name in planet_defence_upgrades:
            self.reciever.buildings.append(self.name)
            return

        if weapons:
            if self.name in weapons:

                # upgrade
                if self.name in self.reciever.weapons.keys():
                    self.reciever.weapons[self.name]["level"] += 1
                else:
                    # buy it
                    self.reciever.weapons[self.name] = copy.deepcopy(weapon_factory.get_weapon(self.name))
                    # if global_params.app.ship == self.reciever:
                    global_params.app.weapon_select.obj = self.reciever
                    global_params.app.weapon_select.update()

                print(f"self.reciever: {self.reciever}, self.reciever.weapons({self.name}):{self.reciever.weapons[self.name]['level']}\n"
                      f"all_weapons: {global_params.app.weapon_select.all_weapons[self.name]['level']}")
                return

        # append to recievers building list
        self.reciever.buildings.append(self.name)
        self.reciever.set_technology_upgrades(self.name)

        # set new value to recievers production
        setattr(self.reciever, self.name, getattr(self.reciever, "production_" + self.key) - self.value)
        setattr(global_params.app.player, self.name, getattr(global_params.app.player, self.key) - self.value)

        self.reciever.set_population_limit()
        self.reciever.calculate_production()
        global_params.app.calculate_global_production()
        global_params.app.tooltip_instance.reset_tooltip(self)

    def draw(self):
        """
        reposition the elements dynamically, draw elements, and finally deletes itself
        """

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
        self.text = self.name + ": " + str(int(self.progress_bar.percent * 100)) + "%/ " + str(global_params.app.ui_helper.hms(self.progress_time))
        self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)
        self.win.blit(self.text_render, (self.dynamic_x + self.button.get_screen_width(), self.button.screen_y + 2))

        # move down if place is free
        for i in range(len(global_params.app.building_widget_list)):
            if global_params.app.building_widget_list[i] == self:
                self.cue_id = global_params.app.building_widget_list.index(global_params.app.building_widget_list[i])

        # if progress is finished, set building to reciever
        if self.progress_bar.percent == 1:
            self.set_building_to_reciever()

            # finally delete it and its references
            self.delete()

    def delete(self):
        if self in global_params.app.building_widget_list:
            global_params.app.building_widget_list.remove(self)
        self.__del__()
        self.progress_bar.__del__()
        self.button.__del__()

    def listen(self, events):
        for event in events:
            if self.button.rect.collidepoint(pygame.mouse.get_pos()):
                self.immediately_build_cost = int((1 - self.progress_bar.percent) * self.progress_time)
                self.set_tooltip()

    def function(self, arg):
        global_params.tooltip_text = ""
        self.build_immediately()
        self.set_building_to_reciever()
        self.delete()

    def set_tooltip(self):
        self.button.tooltip = f"are you sure to build this {self.name} immediately? this will cost you {self.immediately_build_cost} technology units?{self.reciever}"

    def build_immediately(self):
        global_params.app.player.technology -= self.immediately_build_cost
