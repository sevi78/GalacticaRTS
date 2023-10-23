import traceback

import pygame
from pygame_widgets.util import drawText

from source.app.app_helper import select_next_item_in_list

from source.configuration.economy_params import EconomyParams
from source.game_play.navigation import navigate_to
from source.gui.building_button_widget import BuildingButtonWidget
from source.gui.panels.building_panel_components.building_panel_constructor import BuildingPanelConstructor
from source.gui.panels.building_panel_components.building_panel_draw import BuildingPanelDraw
from source.gui.panels.building_panel_components.building_slot import BuildingSlot
from source.gui.panels.building_panel_components.planetary_defence_widget import PlanetaryDefenceWidget
from source.gui.panels.building_panel_components.space_harbor import SpaceHarbor
from source.gui.panels.toggle_switch import ToggleSwitch
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.multimedia_library.images import get_image
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import ui_rounded_corner_small_thickness
from source.multimedia_library.sounds import sounds


class BuildingPanel(WidgetBase, BuildingPanelConstructor, BuildingSlot, EconomyParams, BuildingPanelDraw):
    """

    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        EconomyParams.__init__(self)
        BuildingSlot.__init__(self)

        self.name = "building panel"
        self.init = 0
        self.zero_y = self.world_y
        self.planet_building_text = None
        self.planet_text = None
        self.hover = False

        self.frame_color = colors.frame_color
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.font_size = 18
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.resource_image_size = (15, 15)
        self.world_x = 0
        self.world_y = 0

        # # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.fill(self.bg_color)
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = x
        self.surface_rect.y = y
        self.size_x = kwargs.get("size_x")
        self.size_y = kwargs.get("size_y")
        self.spacing = kwargs.get("spacing")
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)

        # construct planet_surface
        self.planet_surface_size_y = 600
        self.planet_surface = pygame.surface.Surface((width, self.planet_surface_size_y))
        self.planet_surface.fill(self.bg_color)
        self.planet_surface.set_alpha(0)
        self.planet_surface_rect = self.planet_surface.get_rect()
        self.planet_surface_rect.x = x
        self.planet_surface_rect.y = y + height
        self.planet_surface_frame = pygame.draw.rect(self.win, self.frame_color, self.planet_surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)
        self.max_height = self.get_screen_y() + self.planet_surface_rect.height

        # planet image
        self.planet_image = None

        # # construct slider_____
        self.spacing_x = 35

        # construct icon_______________________________________________________________________________________________
        self.create_icons()

        # smiley and thumbsup
        self.smiley_size = 18
        self.smiley_image_sad = pygame.transform.scale(get_image("sad.png"), (self.smiley_size, self.smiley_size))
        self.smiley_image_smile = pygame.transform.scale(get_image("smile.png"), (self.smiley_size, self.smiley_size))
        self.smiley = self.smiley_image_smile

        self.thumps_up_size = 20
        self.thumps_up_image_red = pygame.transform.scale(pygame.transform.flip(get_image("thumps_upred.png"),
            True, True), (self.thumps_up_size, self.thumps_up_size))
        self.thumps_up_image_green = pygame.transform.scale(pygame.transform.flip(get_image("thumps_up.png"),
            True, False), (self.thumps_up_size, self.thumps_up_size))
        self.thumps_up = self.thumps_up_image_green

        self.sub_widget_height = 70
        font_size = 16
        # space harbor
        self.space_harbor = SpaceHarbor(self.win, self.world_x, self.world_y, self.get_screen_width(), self.sub_widget_height,
            isSubWidget=False, parent=self, layer=9, font_size=font_size)

        # planetary defence
        self.planetary_defence = PlanetaryDefenceWidget(self.win, self.world_x, self.world_y, self.get_screen_width(), self.sub_widget_height,
            isSubWidget=False, parent=self, layer=9, spacing=5, icon_size=25, font_size=font_size)

        # building constructor
        # self.building_button_widget = BuildingConstructorWidget(self.win, self.world_x, self.world_y, self.get_screen_width(), self.sub_widget_height,
        #     isSubWidget=False, parent=self, layer=9, font_size=font_size)

        self.building_button_widget = BuildingButtonWidget(win, 200, 100, 300, 200, self.parent,
            False, layer=4, parent=self, fixed_parent=True)
        # toggle switch to pop in or out
        self.toggle_switch = ToggleSwitch(self, 15, zero_y=self.planet_surface_rect.y)

    def set_info_text(self):
        global_params.app.info_panel.set_text(config.info_text)

    def set_planet_selection(self, value):
        try:
            # if empty list: do nothing
            my_list = self.parent.explored_planets
            if not my_list:
                return

            if sprite_groups.planets:
                if self.parent.selected_planet:
                    current_item = self.parent.selected_planet
                else:
                    current_item = sprite_groups.planets.sprites()[0]

                next = select_next_item_in_list(my_list, current_item, value)

                # set new selected planet
                # pan_zoom_handler.zoom = 1.8
                self.parent.set_selected_planet(next)
                navigate_to(self.parent.selected_planet)

        except Exception as e:
            print("building_panel.set_planet_selection: An error occurred:", e)
            traceback.print_exc()

    def show_planet_selection_buttons(self):
        if len(self.parent.explored_planets) > 1 and not self._hidden:
            self.planet_minus_arrow_button.show()
            self.planet_plus_arrow_button.show()
        else:
            self.planet_plus_arrow_button.hide()
            self.planet_minus_arrow_button.hide()

    def set_planet_building_display(self):
        """ sets text to the planet building texts based on buildings"""
        buildings = "None"
        if self.parent.selected_planet:

            buildings = ""
            for i in self.parent.selected_planet.buildings:
                buildings += i + ", "

            self.planet_buttons.show_building_buttons()

        return buildings

    def destroy_building(self, b):
        print("destroy_building", b)
        try:
            self.parent.selected_planet.buildings.remove(b)
        except ValueError as e:
            print("destroy_building error:", b, e)

        self.parent.selected_planet.calculate_production()
        self.parent.selected_planet.calculate_population()
        self.parent.selected_planet.set_population_limit()

        self.parent.event_text = f"you destroyed one {b}! You will not get anything back from it! ... what a waste ..."
        sounds.play_sound(sounds.destroy_building)

    def reposition(self):
        win = pygame.display.get_surface()
        width = win.get_width()

        # reposition
        self.surface_rect.x = width - self.surface.get_width()
        self.planet_surface_rect.x = self.surface_rect.x
        self.planet_minus_arrow_button.screen_x = self.surface_rect.x + self.spacing
        self.planet_plus_arrow_button.screen_x = self.surface_rect.x + self.get_screen_width() - self.spacing * 2 - self.arrow_size
        self.toggle_switch.reposition()

    def listen(self, events):
        # DESTROY BUILDINGS
        # check for mouse collision with image
        for building_name, image_rect in self.singleton_buildings_images.items():
            if image_rect.collidepoint(pygame.mouse.get_pos()):
                global_params.tooltip_text = f"Are you sure you want to destroy this {building_name}? You will probably not get anything back."

                # check for mouse click and destroy building
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.destroy_building(building_name)
            else:
                if global_params.tooltip_text == f"Are you sure you want to destroy this {building_name}? You will probably not get anything back.":
                    global_params.tooltip_text = ""

        # building slot upgrade and tooltip
        if self.parent.selected_planet:
            self.set_building_slot_tooltip_plus(events)
            self.set_building_slot_tooltip_minus(events)
            self.upgrade_building_slots(events)
            self.downgrade_building_slots(events)

        self.reset_building_slot_tooltip()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.set_planet_selection(1)
                elif event.key == pygame.K_LEFT:
                    self.set_planet_selection(-1)

    def draw(self):
        """
        draws the ui elements
        """
        # TIME__________________________________________________________________________________________________________
        # self.update_time()
        self.show_planet_selection_buttons()

        if self._hidden:
            return

        # PLANET Image _________________________________________________________________________________________________
        # draw planet_surface and frame
        self.planet_surface_frame = pygame.draw.rect(self.win, self.frame_color, self.planet_surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)
        self.win.blit(self.planet_surface, self.planet_surface_frame)

        # UI____________________________________________________________________________________________________________
        x = self.planet_surface_rect.x
        self.world_y = self.planet_surface_rect.y + self.spacing

        # planet text
        self.planet_text = drawText(self.win, self.parent.get_planet_name(), self.frame_color,
            (x, self.world_y, self.get_screen_width(), self.planet_surface.get_height()), self.font, "center")

        if self.parent.get_planet_name() == "???":
            self.planet_surface_rect.height = self.planet_minus_arrow_button.get_screen_height() + self.spacing
            self.toggle_switch.toggle_panel_icon.screen_y = self.world_y + self.toggle_switch.toggle_panel_icon.get_screen_height() + self.spacing

        x = self.planet_surface_rect.x + self.spacing
        self.world_y += self.spacing * 2

        if self.parent.selected_planet:
            if not self.parent.selected_planet.explored:
                # if not self.building_button_widget._hidden:
                #     self.building_button_widget.hide()
                return

            self.draw_planet_params(x)

        self.max_height = self.world_y + self.toggle_switch.toggle_size
        if "space harbor" in self.parent.selected_planet.buildings:
            self.max_height += self.sub_widget_height

        if "particle accelerator" in self.parent.selected_planet.buildings:
            self.max_height += self.sub_widget_height

        self.max_height += self.building_button_widget.max_height

        # adjust frame size_y
        self.planet_surface_rect.__setattr__("height", self.world_y - self.spacing * 3)

        if not self.init:
            self.reposition()
            self.init = 1

        self.reposition()
