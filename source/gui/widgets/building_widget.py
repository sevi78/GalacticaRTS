# import copy
import copy

import pygame


from source.configuration.game_config import config
from source.factories.weapon_factory import weapon_factory
from source.gui.widgets.buttons.button import Button
# from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.progress_bar import ProgressBar
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.handlers.garbage_handler import garbage_handler
from source.handlers.orbit_handler import set_orbit_object_id
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image, overblit_button_image, scale_image_cached, rounded_surface
from source.multimedia_library.sounds import sounds

PROGRESSBAR_UPDATE_RATE_IN_SECONDS = 0.1
FONT_SIZE = 10


class BuildingWidget(WidgetBase):
    """
    A widget that displays information about a building, including a button,
    progress bar, and text showing the building name and progress percentage.

    This widget manages the building process, updates progress, and handles
    user interactions for immediate building.

    Attributes:
        name (str): The name of the building.
        receiver: The object receiving the building = PanZoomPlanet
        key (str): The key for the building value.
        value: The value for the building.
        is_building (bool): Flag indicating if the building is being constructed.
        button (Button): The button widget for user interaction.
        progress_bar (ProgressBar): The progress bar widget showing build progress.

    Methods:
        update_progressbar(): Updates the progress bar based on game time and speed.
        set_building_to_receiver(): Finalizes the building process.
        draw(): Renders the widget and its components.
        delete(): Removes the widget and its references.
        listen(events): Handles user input events.
    """

    def __init__(
            self, win: pygame.Surface, x: int, y: int, width: int, height: int, name: str, receiver: object, key: str,
            value: int, **kwargs
            ):
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
            self.image = scale_image_cached(get_image(self.name + "_25x25.png"), (25, 25))
        else:
            self.image = scale_image_cached(get_image(self.name + ".png"), (25, 25))

        self.building_production_time = kwargs.get("building_production_time")

        self.button = Button(self.win,
                x=self.dynamic_x + self.get_screen_height() / 2,
                y=self.dynamic_y,
                width=self.get_screen_height(),
                height=self.get_screen_height(),
                image=rounded_surface(self.image,3),
                on_click=lambda: self.function("do nothing"),
                transparent=True,
                image_hover_surface_alpha=255,
                parent=config.app,
                tooltip=self.tooltip, layer=self.layer)

        self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)

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

        self.overblit_image_name = None
        if self.receiver.owner > -1:
            self.overblit_image_name = self.receiver.image_name#config.app.players[self.receiver.owner].image_name

        self.frame_color = colors.frame_color#.receiver.player_color
        self._hidden = self.receiver.owner != config.app.game_client.id

        # building_widget_handler.add_building_widget(self)
        config.app.building_widget_list.append(self)

    def __repr__(self):
        return f"{self.name}: {self.receiver}"

    def update_progressbar(self):
        game_speed = time_handler.game_speed
        current_time = time_handler.time
        production_time = self.building_production_time
        relative_production_time = production_time / game_speed

        if current_time - self.progress_bar_start_time > self.progress_bar_update_rate:
            progress_increment = (1 / relative_production_time) * self.progress_bar_update_rate
            self.progress_bar.percent += progress_increment
            self.progress_bar.percent = min(max(self.progress_bar.percent, 0), 1)
            self.progress_bar_start_time = current_time

    def set_building_to_receiver(self):
        if self.receiver.owner == -1:
            print(f"set_building_to_receiver: You can't build on this planet!: {self.receiver.name}")
            return

        planet_defence_upgrades = ["cannon", "missile"]

        # get weapons of the receiver
        weapons = None
        if self.receiver.property == "ship":
            weapons = self.receiver.weapon_handler.all_weapons.keys()

        sounds.play_sound("success", channel=7)
        self.receiver.economy_agent.building_cue -= 1

        # if building is a ship
        if self.name in self.ship_names:
            x, y = pan_zoom_handler.screen_2_world(self.receiver.rect.centerx, self.receiver.rect.centery)
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

        # if building is a planet defense
        if self.name in planet_defence_upgrades:
            self.receiver.economy_agent.buildings.append(self.name)
            return

        # if building is a weapon
        if weapons:
            # if already has the weapon
            if self.name in weapons:
                if self.name in self.receiver.weapon_handler.weapons.keys():
                    # upgrade the weapon
                    self.receiver.weapon_handler.weapons[self.name]["level"] += 1

                    # if weapon is the selected weapon, update current weapon
                    if self.name == self.receiver.weapon_handler.current_weapon_select:
                        self.receiver.weapon_handler.current_weapon = self.receiver.weapon_handler.weapons[self.name]

                # if not has weapon, install it
                else:
                    self.receiver.weapon_handler.weapons[
                        self.name] = copy.deepcopy(weapon_factory.get_weapon(self.name))

                    # if weapon is the selected weapon, update current weapon
                    if self.name == self.receiver.weapon_handler.current_weapon_select:
                        self.receiver.weapon_handler.current_weapon = self.receiver.weapon_handler.weapons[self.name]

                # update weapon_select editor
                if config.app.game_client.id == self.receiver.owner:
                    config.app.weapon_select.obj = self.receiver
                    config.app.weapon_select.update()
                else:
                    # update selection
                    self.receiver.weapon_handler.current_weapon_select = self.name
                return

        self.receiver.economy_agent.buildings.append(self.name)
        self.receiver.economy_agent.set_technology_upgrades(self.name)
        player = config.app.players[self.receiver.owner]
        self.receiver.economy_agent.set_population_limit()
        self.receiver.economy_agent.calculate_production()
        config.app.calculate_global_production(player)
        config.app.tooltip_instance.reset_tooltip(self)

    def function(self, arg):
        player = config.app.players[self.receiver.owner]
        config.tooltip_text = ""
        if self.immediately_build_cost < player.stock["technology"] and self.receiver.owner == config.player:
            self.build_immediately()

    def set_tooltip(self):
        self.button.tooltip = f"Are you sure you want to build this {self.name} immediately? This will cost you {self.immediately_build_cost} technology units. {self.receiver}"

    def build_immediately(self):
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
        # if self in building_widget_handler.building_widget_list:
        #     building_widget_handler.building_widget_list.remove(self)
        # building_widget_handler.delete_building_widget(self)

        if self.progress_bar:
            self.progress_bar.__del__()
        if self.button:
            self.button.__del__()
        self.__del__()
        garbage_handler.delete_all_references(self, self.progress_bar)
        garbage_handler.delete_all_references(self, self.button)
        garbage_handler.delete_all_references(self, self)

    def update_visibility(self):
        self._hidden = self.receiver.owner != config.app.game_client.id
        if self.button:
            self.button._hidden = self._hidden
        if self.progress_bar:
            self.progress_bar._hidden = self._hidden
        if self._hidden:
            self.hide()

    def listen(self, events):
        if self._hidden:
            return

        for event in events:
            if not self.button:
                return
            if self.button.rect.collidepoint(pygame.mouse.get_pos()):
                self.immediately_build_cost = int((1 - self.progress_bar.percent) * self.building_production_time)
                self.set_tooltip()

    def draw_(self):
        """
        Reposition the elements dynamically, draw elements if visible,
        and delete the widget if progress is finished.
        """
        # display only the sidgnet belonging to the player
        # self.update_visibility()

        # update the progress bar
        if not time_handler.game_speed == 0 and not config.game_paused:
            self.update_progressbar()

        # error handling for the case the level gets loaded after the widget is created
        try:  # TODO: fix this
            self.cue_id = config.app.building_widget_list.index(self)
        except ValueError as e:
            print(f"building_widget.draw: ValueError: {e}, deleting widget...")
            self.delete()
            return

        if self.progress_bar.percent == 1:
            self.set_building_to_receiver()
            self.delete()
            return

        if self._hidden:
            return


        # set position and size fo the widget
        widget_height = self.get_screen_height()
        self.dynamic_x = config.app.ui_helper.anchor_right
        spacing = 5

        # win = pygame.display.get_surface()
        height = self.win.get_height()


        owner_list = [_ for _ in config.app.building_widget_list if _.receiver.owner == config.app.game_client.id]
        display_cue_id = owner_list.index(self)
        y = height - spacing - widget_height - widget_height * display_cue_id

        # create rect
        self.surface_rect = pygame.Rect(self.dynamic_x, y, self.get_screen_width(), self.get_screen_height())
        self.draw_frame()

        # button
        if self.button:
            self.button.image_hover_surface.set_alpha(0)
            self.button.set_position((config.app.ui_helper.anchor_right, y))

        # progress_bar
        if self.progress_bar:
            self.progress_bar.set_screen_width(config.app.building_panel.get_screen_width() - self.button.get_screen_width() - 15)
            self.progress_bar.set_position((
                self.dynamic_x + self.button.get_screen_width() + 5, y + self.button.get_screen_height() / 2))

        # draw widgets text
        self.text = f"{self.name}: {int(self.progress_bar.percent * 100)}%/ {config.app.ui_helper.hms(self.building_production_time)}"
        self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)
        self.win.blit(self.text_render, (self.dynamic_x + self.button.get_screen_width(), self.button.screen_y + 2))

        # draw picture of the owner
        overblit_button_image(self.button, self.overblit_image_name, False, offset_x=5, size=(
        25, 25), outline=True, color=self.receiver.player_color)

    def draw(self):
        """
        Reposition the elements dynamically, draw elements if visible,
        and delete the widget if progress is finished.
        """
        # display only the widget belonging to the player
        self.update_visibility()

        # update the progress bar
        if not time_handler.game_speed == 0 and not config.game_paused:
            self.update_progressbar()

        # error handling for the case the level gets loaded after the widget is created
        # do we need to set the cue id ? probably it will not work if any other widget is finished,
        # then the position will be wrong
        # try:  # TODO: fix this
        #     self.cue_id = config.app.building_widget_list.index(self)
        # except ValueError as e:
        #     print(f"building_widget.draw: ValueError: {e}, deleting widget...")
        #     self.delete()
        #     return
        if not self in config.app.building_widget_list:
            self.delete()
            return

        if self.progress_bar.percent == 1:
            self.set_building_to_receiver()
            self.delete()
            return

        if self._hidden:
            return

        # get the widgets belonging to the player
        owner_list = [_ for _ in config.app.building_widget_list if _.receiver.owner == config.app.game_client.id]

        # set position
        self.dynamic_x = config.app.ui_helper.anchor_right
        y = self.win.get_height() - 5 - self.get_screen_height() - self.get_screen_height() * owner_list.index(self)

        # create rect
        self.surface_rect = pygame.Rect(self.dynamic_x, y, self.get_screen_width(), self.get_screen_height())
        self.draw_frame()

        # button
        if self.button:
            self.button.image_hover_surface.set_alpha(0)
            self.button.set_position((config.app.ui_helper.anchor_right, y))

        # progress_bar
        if self.progress_bar:
            self.progress_bar.set_screen_width(config.app.building_panel.get_screen_width() - self.button.get_screen_width() - 15)
            self.progress_bar.set_position((
                self.dynamic_x + self.button.get_screen_width() + 5, y + self.button.get_screen_height() / 2))

        # draw widgets text
        self.text = f"{self.name}: {int(self.progress_bar.percent * 100)}%/ {config.app.ui_helper.hms(self.building_production_time)}"
        self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)
        self.win.blit(self.text_render, (self.dynamic_x + self.button.get_screen_width(), self.button.screen_y + 2))

        # draw picture of the owner
        # overblit_button_image(self.button, self.overblit_image_name, False, offset_x=10, size=(
        # 15, 15), outline=False, color=self.receiver.player_color)
#
#
# import copy
# import time
#
# import pygame
#
# from source.configuration.game_config import config
# from source.factories.weapon_factory import weapon_factory
# from source.gui.widgets.widget_base_components.widget_base import WidgetBase
# from source.gui.widgets.buttons.button import Button
# from source.gui.widgets.progress_bar import ProgressBar
# from source.handlers.orbit_handler import set_orbit_object_id
# from source.handlers.pan_zoom_handler import pan_zoom_handler
#
# from source.multimedia_library.images import get_image
# from source.multimedia_library.sounds import sounds
#
#
# class BuildingWidget(WidgetBase):
#     """Main functionalities:
#
#     The BuildingWidget class is responsible for creating and managing the widgets that represent buildings in the game. It creates a button with an image, a progress bar, and text that displays the building's name and progress. It also handles the logic for building a building, including calculating the cost and updating the planet's production and population limit. When the building is complete, it removes itself from the list of building widgets and adds the building to the planet's list of buildings.
#
#     Methods:
#     - __init__: Initializes the BuildingWidget object with the necessary parameters and creates the button, progress bar, and text.
#     - set_building_to_planet: Handles the logic for building a building, including updating the receiver's production and population limit.
#     - draw: Repositions the elements dynamically, draws the elements, and deletes the widget when the building is complete.
#     - delete: Removes the widget from the list of building widgets and deletes the widget and its references.
#     - listen: Handles mouse events and sets the tooltip for the button.
#     - function: Builds the building immediately and removes the widget.
#
#     Fields:
#     - win: The surface on which to draw the widget.
#     - x, y: The coordinates of the top left corner of the widget.
#     - width, height: The width and height of the widget.
#     - name: The name of the building.
#     - receiver: The receiver object on which the building is being built.
#     - key: The key for the building's production value.
#     - value: The value of the building's production.
#     - immediately_build_cost: The cost to build the building immediately.
#     - tooltip: The tooltip for the button.
#     - dynamic_x, dynamic_y: The dynamic coordinates of the widget.
#     - cue_id: The position of the widget in the list of building widgets.
#     - font, fontsize: The font and font size for the text.
#     - spacing: The spacing between elements.
#     - image: The image for the button.
#     - button: The button object.
#     - text_render: The rendered text for the widget.
#     - progress_bar_width, progress_bar_height: The width and height of the progress bar.
#     - startTime: The time at which the building started being built.
#     - progress_time: The time it takes to build the building.
#     - progress_bar: The progress bar object."""
#
#     def __init__(self, win, x, y, width, height, name, receiver, key, value, **kwargs):
#         super().__init__(win, x, y, width, height, **kwargs)
#         self.layer = kwargs.get("layer")
#         self.text = name + ":"
#         self.name = name
#         self.receiver = receiver
#         self.key = key
#         self.value = value
#         self.immediately_build_cost = 0
#         self.tooltip = kwargs.get("tooltip", "no tooltip set yet!")
#         self.is_building = kwargs.get("is_building", True)
#
#         # get the position and size
#         self.win = pygame.display.get_surface()
#         height = win.get_height()
#         self.dynamic_x = config.app.ui_helper.anchor_right
#         self.cue_id = len(config.app.building_widget_list)
#         self.spacing = 5
#         self.dynamic_y = height - self.spacing - self.get_screen_height() - self.get_screen_height() * self.cue_id
#         self.font_size = kwargs.get("fontsize", 15)
#         self.font = pygame.font.SysFont(kwargs.get("fontname", config.font_name), kwargs.get("fontsize", 15))
#         self.spacing = kwargs.get("spacing", 15)
#         if self.is_building:
#             self.image = scale_image_cached(get_image(self.name + "_25x25.png"), (25, 25))
#         else:
#             self.image = scale_image_cached(get_image(self.name + ".png"), (25, 25))
#
#         self.progress_time = kwargs.get("building_production_time")
#
#         # button
#         self.button = Button(self.win,
#             x=self.dynamic_x + self.get_screen_height() / 2,
#             y=self.dynamic_y,
#             width=self.get_screen_height(),
#             height=self.get_screen_height(),
#             image=self.image,
#             onClick=lambda: self.function("do nothing"),
#             transparent=True,
#             image_hover_surface_alpha=255,
#             parent=config.app,
#             tooltip=self.tooltip, layer=self.layer)
#
#         # text
#         self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)
#
#         # progress bar
#         self.progress_bar_width = kwargs.get("progress_bar_width", 100)
#         self.progress_bar_height = kwargs.get("progress_bar_height", 10)
#         self.startTime = time.time()
#
#         self.progress_bar = ProgressBar(win=self.win,
#             x=self.dynamic_x + self.button.get_screen_width(),
#             y=self.button.screen_y + self.progress_bar_height / 2,
#             width=self.progress_bar_width,
#             height=self.progress_bar_height,
#             progress=lambda: (time.time() - self.startTime) / self.progress_time,
#             curved=True,
#             completedColour=self.frame_color, layer=self.layer
#             )
#
#         # register
#         config.app.building_widget_list.append(self)
#
#     def set_building_to_receiver(self):
#         """
#         overgive the values stores for the receiver: wich building to append, sets population limit, calculates production
#         and calls calculate_global_production()
#         and plays some nice sound :)
#         :return:
#         """
#         ships = ["spaceship", "cargoloader", "spacehunter"]
#         # technology_upgrades = ["university"]
#         planet_defence_upgrades = ["cannon", "missile"]
#         weapons = None
#         if self.receiver.property == "ship":
#             weapons = self.receiver.all_weapons.keys()
#
#         sounds.play_sound("success", channel=7)
#
#         # remove self from planets building cue:
#         self.receiver.building_cue -= 1
#
#         # if it is a ship, no calculation has to be done, return
#         if self.name in ships:
#             x, y = pan_zoom_handler.screen_2_world(self.receiver.screen_x, self.receiver.screen_y)
#             ship = config.app.ship_factory.create_ship(self.name + "_30x30.png", x, y, config.app)
#             set_orbit_object_id(ship, self.receiver.id)
#             return
#
#         if self.name in planet_defence_upgrades:
#             self.receiver.buildings.append(self.name)
#             return
#
#         if weapons:
#             if self.name in weapons:
#
#                 # upgrade
#                 if self.name in self.receiver.weapons.keys():
#                     self.receiver.weapons[self.name]["level"] += 1
#                 else:
#                     # buy it
#                     self.receiver.weapons[self.name] = copy.deepcopy(weapon_factory.get_weapon(self.name))
#                     # if global_params.app.ship == self.receiver:
#                     config.app.weapon_select.obj = self.receiver
#                     config.app.weapon_select.update()
#
#                 print(f"self.receiver: {self.receiver}, self.receiver.weapons({self.name}):{self.receiver.weapons[self.name]['level']}\n"
#                       f"all_weapons: {config.app.weapon_select.all_weapons[self.name]['level']}")
#                 return
#
#         # append to receivers building list
#         self.receiver.buildings.append(self.name)
#         self.receiver.set_technology_upgrades(self.name)
#
#         # set new value to receivers production
#         setattr(self.receiver, self.name, getattr(self.receiver, "production_" + self.key) - self.value)
#         setattr(config.app.player, self.name, getattr(config.app.player, self.key) - self.value)
#
#         self.receiver.set_population_limit()
#         self.receiver.calculate_production()
#         config.app.calculate_global_production()
#         config.app.tooltip_instance.reset_tooltip(self)
#
#     def draw(self):
#         """
#         reposition the elements dynamically, draw elements, and finally deletes itself
#         """
#
#         # reposition
#         widget_height = self.get_screen_height()
#         self.dynamic_x = config.app.ui_helper.anchor_right
#         spacing = 5
#
#         # get the position and size
#         win = pygame.display.get_surface()
#         height = win.get_height()
#         y = height - spacing - widget_height - widget_height * self.cue_id
#
#         # button
#         self.button.image_hover_surface.set_alpha(0)
#         self.button.set_position((config.app.ui_helper.anchor_right, y))
#
#         # progress_bar
#         self.progress_bar.set_screen_width(config.app.building_panel.get_screen_width() - self.button.get_screen_width() - 15)
#         self.progress_bar.set_position((
#             self.dynamic_x + self.button.get_screen_width() + 5, y + self.button.get_screen_height() / 2))
#
#         # draw widgets text
#         self.text = self.name + ": " + str(int(self.progress_bar.percent * 100)) + "%/ " + str(config.app.ui_helper.hms(self.progress_time))
#         self.text_render = self.font.render(self.text, True, self.frame_color, self.font_size)
#         self.win.blit(self.text_render, (self.dynamic_x + self.button.get_screen_width(), self.button.screen_y + 2))
#
#         # move down if place is free
#         for i in range(len(config.app.building_widget_list)):
#             if config.app.building_widget_list[i] == self:
#                 self.cue_id = config.app.building_widget_list.index(config.app.building_widget_list[i])
#
#         # if progress is finished, set building to receiver
#         if self.progress_bar.percent == 1:
#             self.set_building_to_receiver()
#
#             # finally delete it and its references
#             self.delete()
#
#     def delete(self):
#         if self in config.app.building_widget_list:
#             config.app.building_widget_list.remove(self)
#         self.__del__()
#         self.progress_bar.__del__()
#         self.button.__del__()
#
#     def listen(self, events):
#         for event in events:
#             if self.button.rect.collidepoint(pygame.mouse.get_pos()):
#                 self.immediately_build_cost = int((1 - self.progress_bar.percent) * self.progress_time)
#                 self.set_tooltip()
#
#     def function(self, arg):
#         config.tooltip_text = ""
#         self.build_immediately()
#         self.set_building_to_receiver()
#         self.delete()
#
#     def set_tooltip(self):
#         self.button.tooltip = f"are you sure to build this {self.name} immediately? this will cost you {self.immediately_build_cost} technology units?{self.receiver}"
#
#     def build_immediately(self):
#         config.app.player.technology -= self.immediately_build_cost
