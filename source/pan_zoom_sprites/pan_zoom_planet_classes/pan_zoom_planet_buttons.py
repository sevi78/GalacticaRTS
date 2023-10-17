import copy

import pygame

import source
from source.configuration.config import technology_upgrades

from source.gui.widgets.buttons.button import Button
from source.gui.widgets.buttons.button_array import ButtonArray
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_economy import PanZoomPlanetEconomy
from source.utils.colors import colors
from source.multimedia_library.images import get_image


class PanZoomPlanetButtons(PanZoomPlanetEconomy):
    """Main functionalities:
    The PanZoomPlanetButtons class is responsible for creating and managing the UI elements for a planet, including building
    icons, overview icons, and buttons. It allows the user to hide and show building buttons, set building button
    tooltips, and create a planet button array. The class also includes methods for deleting building and resource buttons.

    Methods:
    - hide_building_buttons(): hides all building buttons
    - show_building_buttons(): shows building buttons for a specific resource
    - show_overview_button(): shows or hides overview buttons based on whether the planet has been explored
    - set_building_button_tooltip(): sets the tooltip for a building button
    - create_planet_button_array(): creates the UI elements for the planet, including building icons, overview icons,
      and buttons
    - delete_building_buttons(): deletes all building buttons
    - delete_resource_buttons(): deletes all resource buttons

    Fields:
    - overview_buttons: a list of overview buttons
    - building_buttons: a dictionary of building buttons for each resource
    - building_buttons_list: a list of all building button arrays
    - thumpsup_button_size: the size of the thumps up button
    - thumpsup_button: the thumps up button
    - smiley_button_size: the size of the smiley button
    - smiley_button: the smiley button
    - planet_button_array: the planet button array
    - possible_resources: a list of possible resources for the planet

    """

    def __init__(self, **kwargs):
        PanZoomPlanetEconomy.__init__(self, kwargs)
        self.building_buttons_visible = []
        self.overview_buttons = []
        self.check_image = get_image("check.png")
        self.smiley_status = False
        self.thumpsup_status = False

    def get_building_buttons_visible_state(self, resource, value):
        if not resource in self.building_buttons_visible and value == 1:
            self.building_buttons_visible.append(resource)

        if resource in self.building_buttons_visible and value == 0:
            self.building_buttons_visible.remove(resource)

    def set_building_buttons_visible_state_all_true(self):
        self.building_buttons_visible = copy.copy(self.possible_resources)

    def reset_building_buttons_visible_state(self):
        self.building_buttons_visible = []
        self.hide_building_buttons()

    def hide_building_buttons(self):
        for buttonarray in self.building_buttons_list:
            buttonarray.hide()
            for button in buttonarray.getButtons():
                button.hide()

    def show_building_buttons(self, resource):
        """
        shows the buildong button only if planet is explored
        :param resource:
        """

        if self.building_buttons[resource].isVisible():
            self.building_buttons[resource].hide()
            for button in self.building_buttons[resource].getButtons():
                button.hide()
                self.get_building_buttons_visible_state(resource, 0)

        else:
            self.building_buttons[resource].show()
            for button in self.building_buttons[resource].getButtons():
                button.show()
                self.get_building_buttons_visible_state(resource, 1)

    def show_planet_button_array(self):
        for resource_button in self.planet_button_array.getButtons():
            if not self.type == "sun":
                resource_button.show()

    def hide_planet_button_array(self):
        for resource_button in self.planet_button_array.getButtons():
            resource_button.hide()

    def show_overview_button(self):
        """
        shows the overview buttons if planet is explored
        """

        for i in self.overview_buttons:
            if self.explored:
                if not self.type == "sun":
                    i.show()
                    i.enable()
            else:
                i.hide()
                i.disable()

    def hide_overview_button(self):
        """
        hides the overview buttons
        """

        for i in self.overview_buttons:
            i.hide()
            i.disable()

    def set_building_button_tooltip(self, i):
        """
        creates tooltops for the buttons
        :param i:
        """
        return_list = []
        price_list = []
        production_list = []
        population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        # prices
        text = ""
        for building in self.parent.buildings[i.name]:
            if building[0] == "a":
                text = "to build an " + building + " you need: "
            else:
                text = "to build a " + building + " you need: "

            for key, value in source.configuration.config.prices[building].items():
                if value > 0:
                    text += key + ": " + str(value) + ", "
            text = text[:-2]

            price_list.append(text)

        # production
        text = ""
        for building in self.parent.buildings[i.name]:
            # population
            if building in self.population_buildings:
                text = ". a " + building + " increases the planets population limit by " + str(
                    population_buildings_values[building]) + "  "

            # production
            elif building[0] == "a":
                text = " . an " + building + " will produce: "
            else:
                text = " . a " + building + " will produce: "

            for key, value in source.configuration.config.production[building].items():
                if value > 0:
                    text += key + ": " + str(value) + ", "
                #
                # elif value < 0:
                #     text += "but it will also cost you " + key + ": " +  str(value) + " everytime it produces something!, "

            if building == "university":
                text += f"it will increase the maximum buildings on the planet by {technology_upgrades[building]['buildings_max']}, "

            if building == "space harbor":
                text += f"this will allow you to build space ships!, "

            text = text[:-2]

            production_list.append(text)

        for i in range(len(price_list)):
            return_list.append(price_list[i] + production_list[i])

        return return_list

    def create_planet_button_array(self):
        # print("create_planet_button_array")
        """
        creates the ui elements for the planet:
        building icons, overview icons, buttons ect
        :return:
        """
        self.building_buttons = {}
        self.building_buttons_list = []
        self.overview_buttons = []
        slot_image_size = 25
        x = self.screen_x
        y = self.screen_y - self.get_screen_height() / 2

        # resource icons
        images_scaled = [pygame.transform.scale(
            get_image(i + "_25x25.png"), (slot_image_size, slot_image_size))
            for i in self.possible_resources]

        self.planet_button_array = ButtonArray(self.win,
            x=x,
            y=y,
            width=len(self.possible_resources) * slot_image_size,
            height=slot_image_size + 1,
            shape=(len(self.possible_resources), 1), border=1, bottomBorder=0, rightBorder=0, leftBorder=0, topBorder=0,
            images=images_scaled,
            borderThickness=2, inactiveBorderColours=[colors.frame_color for i in range(6)],

            tooltips=self.possible_resources,
            onClicks=(
                lambda: self.show_building_buttons(self.possible_resources[0]),
                lambda: self.show_building_buttons(self.possible_resources[1]),
                lambda: self.show_building_buttons(self.possible_resources[2]),
                lambda: self.show_building_buttons(self.possible_resources[3]),
                lambda: self.show_building_buttons(self.possible_resources[4]),
                lambda: self.show_building_buttons(self.possible_resources[5])
                ),
            parents=[self, self, self, self, self, self],
            ui_parents=[self, self, self, self, self, self],
            names=self.possible_resources,
            layers=[9, 9, 9, 9, 9, 9],
            inactiveColours=[colors.background_color for i in range(6)],
            borderColours=[colors.frame_color for i in range(6)])

        # building buttons
        for i in self.planet_button_array.getButtons():
            images_scaled = [
                get_image(self.parent.buildings[i.name][0] + "_25x25.png"),
                get_image(self.parent.buildings[i.name][1] + "_25x25.png"),
                get_image(self.parent.buildings[i.name][2] + "_25x25.png")]

            scaled_images = [pygame.transform.scale(image, (slot_image_size, slot_image_size)) for image in
                             images_scaled]
            info_texts = [
                source.configuration.info_text.create_info_panel_building_text()[self.parent.buildings[i.name][0]],
                source.configuration.info_text.create_info_panel_building_text()[self.parent.buildings[i.name][1]],
                source.configuration.info_text.create_info_panel_building_text()[self.parent.buildings[i.name][2]]]

            building_buttons = ButtonArray(self.win,
                x=i.get_screen_x(),
                y=y - slot_image_size - slot_image_size - i.get_screen_height(),
                width=slot_image_size + 1,
                height=3 * slot_image_size,
                shape=(1, 3),
                border=1, bottomBorder=0, rightBorder=0, leftBorder=0, topBorder=0,
                images=scaled_images,
                borderThickness=0,
                texts=[self.parent.buildings[i.name][0], self.parent.buildings[i.name][1],
                       self.parent.buildings[i.name][2]],
                tooltips=self.set_building_button_tooltip(i),

                parents=[self, self, self],
                ui_parents=[self, self, self],
                names=self.parent.buildings[i.name],
                textColours=[(0, 0, 0), (0, 0, 0), (0, 0, 0)],
                font_sizes=[0, 0, 0],
                info_texts=info_texts,
                layers=[9, 9, 9, 9, 9, 9]
                )

            # hide initially
            building_buttons.hide()
            self.planet_button_array.hide()

            # register
            self.building_buttons[i.name] = building_buttons
            self.building_buttons_list.append(building_buttons)

        # thumpsup button
        self.thumpsup_button_size = (18, 18)
        self.thumpsup_button = Button(self.win,
            x=self.screen_x - slot_image_size,
            y=self.planet_button_array.get_screen_y(),
            width=self.thumpsup_button_size[0],
            height=self.thumpsup_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            ui_parent=self,
            tooltip="indicates whether the production is in plus ",
            image=pygame.transform.flip(pygame.transform.scale(get_image(
                "thumps_up.png"), self.thumpsup_button_size), True, False),
            layer=9)

        self.overview_buttons.append(self.thumpsup_button)

        # smiley
        self.smiley_button_size = (20, 20)
        self.smiley_button = Button(self.win,
            x=self.screen_x - slot_image_size * 2,
            y=self.planet_button_array.get_screen_y(),
            width=self.smiley_button_size[0],
            height=self.smiley_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            ui_parent=self,
            tooltip="indicates the satisfaction of the population", image=get_image(
                "smile.png"),
            layer=9)

        self.smiley_button.hide()
        self.thumpsup_button.hide()

        self.overview_buttons.append(self.smiley_button)
        self.hide_building_buttons()
        self.planet_button_array.hide()

    def delete_building_buttons(self):
        # delete building_buttons
        for buttonarray in self.building_buttons_list:
            for button in buttonarray.getButtons():
                button.__del__()
            buttonarray.__del__()

    def delete_resource_buttons(self):
        for resource_button in self.planet_button_array.getButtons():
            resource_button.__del__()

    def delete_overview_buttons(self):
        for i in self.overview_buttons:
            i.__del__()

    def delete_buttons(self):
        self.delete_building_buttons()
        self.delete_resource_buttons()
        self.delete_overview_buttons()
