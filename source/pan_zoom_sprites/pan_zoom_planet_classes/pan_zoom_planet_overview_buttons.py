import pygame

from source.factories.building_factory import building_factory
from source.gui.widgets.buttons.button import Button
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_economy import PanZoomPlanetEconomy
from source.multimedia_library.images import get_image


class PanZoomPlanetOverviewButtons(PanZoomPlanetEconomy):
    """
    """

    def __init__(self, **kwargs):
        PanZoomPlanetEconomy.__init__(self, kwargs)
        self.smiley_button = None
        self.thumpsup_button = None
        self.overview_buttons = []
        self.smiley_status = False
        self.thumpsup_status = False
        self.thumpsup_button_size = (18, 18)
        self.smiley_button_size = (20, 20)
        self.min_offset_y_to_text = 25

    def create_overview_buttons(self):
        """
        creates the overview icons for the planet
        """
        # thumpsup button
        self.thumpsup_button = Button(self.win,
            x=0,
            y=0,
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
        self.smiley_button = Button(self.win,
            x=0,
            y=0,
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
            layer=9,
            zoomable=False)

        self.overview_buttons.append(self.smiley_button)
        # technology_level
        self.technology_level_button = Button(self.win,
            x=0,
            y=0,
            width=self.smiley_button_size[0],
            height=self.smiley_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            ui_parent=self,
            tooltip="indicates the technology_level of the population", image=get_image(
                "badge1.png"),
            layer=9,
            zoomable=False)

        self.overview_buttons.append(self.technology_level_button)
        self.technology_level_button.hide()
        self.smiley_button.hide()
        self.thumpsup_button.hide()

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

    def set_thumpsup_status(self):
        # is everything in plus, show thumpsup green,otherwise red, set smiley to sad if no food production
        vl = []
        for key, value in self.production.items():
            if value < 0:
                vl.append(value)
        if len(vl) > 0:
            self.thumpsup_status = True
        else:
            self.thumpsup_status = False

    def set_smiley_status(self):
        if self.production["food"] > 0:
            self.smiley_status = True
        else:
            self.smiley_status = False

    def set_technology_level_status(self):
        self.set_rank_from_population(building_factory.get_build_population_minimum_list())
        # print("get_build_population_minimum_list", self.rank)

    def set_overview_images(self):
        if self.thumpsup_status:
            self.thumpsup_button.image_raw = pygame.transform.flip(pygame.transform.scale(
                get_image(
                    "thumps_upred.png"), self.thumpsup_button_size), True, True)
        else:
            self.thumpsup_button.image_raw = pygame.transform.flip(pygame.transform.scale(
                get_image(
                    "thumps_up.png"), self.thumpsup_button_size), True, False)

        if self.smiley_status:
            self.smiley_button.image_raw = get_image("smile.png")
        else:
            self.smiley_button.image_raw = get_image("sad.png")

        self.technology_level_button.image_raw = self.rank_images[str(self.rank)]

    def delete_overview_buttons(self):
        for i in self.overview_buttons:
            i.__del__()

    def delete_buttons(self):
        self.delete_overview_buttons()

    def set_overview_buttons_position(self):
        if not hasattr(self, "text_rect"):
            return

        self.smiley_button.set_screen_position(offset_x=self.rect.width / 2, offset_y=-self.min_offset_y_to_text)
        self.thumpsup_button.set_screen_position(offset_x=self.rect.width / 2 - 25, offset_y=-self.min_offset_y_to_text)
        self.technology_level_button.set_screen_position(offset_x=self.rect.width / 2 + 25, offset_y=-self.min_offset_y_to_text)
