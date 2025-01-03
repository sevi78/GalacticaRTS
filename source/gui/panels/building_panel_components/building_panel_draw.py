import pygame
from pygame_widgets.util import drawText

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.multimedia_library.images import get_image, scale_image_cached, rounded_surface
from source.text.text_formatter import format_number

SPECIAL_RIGHT_OFFSET = 60
SPECIAL_Y_OFFSET = 5

SMILEY_SIZE = 20
SPECIAL_TEXT_COLOR = "palegreen4"  # "chartreuse3"


class BuildingPanelDraw:
    def __init__(self):
        self.resource_image_size = (15, 15)
        self.population_image = scale_image_cached(get_image("population_25x25.png"), (25, 25))
        self.plus_image = scale_image_cached(
                get_image("plus_icon.png"), self.resource_image_size)
        self.plus_image_rect = self.plus_image.get_rect()

        self.minus_image = scale_image_cached(
                get_image("minus_icon.png"), self.resource_image_size)
        self.minus_image_rect = self.minus_image.get_rect()

        self.building_image = rounded_surface(scale_image_cached(get_image("building_icon.png"), self.resource_image_size), 3)
        self.building_image_rect = self.building_image.get_rect()

    def draw_planet_params(self, x):
        selected_planet = self.parent.selected_planet
        if selected_planet.owner == -1:
            return

        # draw owner
        drawText(self.win, f"owner: {config.app.players[selected_planet.owner].name}", self.frame_color, (
            x + self.spacing_x, self.world_y, self.get_screen_width(), 20), self.font, "left")

        self.world_y += self.spacing * 3

        # draw population text
        # population
        drawText(self.win, "population: " + str(int(selected_planet.economy_agent.population)) + "/" + format_number(selected_planet.economy_agent.population_limit, 1), self.frame_color, (
            x + self.spacing_x, self.world_y, self.get_screen_width(), 20), self.font, "left")

        # print ("selected_planet.specials_dict:", selected_planet.specials_dict)
        value = selected_planet.economy_agent.specials_dict["population_grow_factor"]["value"]
        operator = selected_planet.economy_agent.specials_dict["population_grow_factor"]["operator"]
        if float(value) > 0.0:
            if operator == "*":
                operator = "x"

            drawText(self.win, f"{operator}{str(value)}", SPECIAL_TEXT_COLOR, (
                x + self.screen_width - SPECIAL_RIGHT_OFFSET, self.world_y - SPECIAL_Y_OFFSET, self.get_screen_width(),
                20), self.special_font, "left")

        # image = scale_image_cached(get_image("population_25x25.png"), (25,25))
        self.win.blit(self.population_image, (x - 4, self.world_y))

        self.world_y += self.spacing * 3

        if self.parent.selected_planet.smiley_status:
            self.smiley = self.smiley_image_smile
        else:
            self.smiley = self.smiley_image_sad

        self.win.blit(self.smiley, (x - 1, self.world_y))

        # draw background planet icon
        image_name = self.parent.selected_planet.image_name_big
        # if self.parent.selected_planet.owner != -1:
        #     image = config.app.players[self.parent.selected_planet.owner].image

        self.planet_image = scale_image_cached(self.parent.selected_planet.image_raw, (150, 150))
        self.planet_image.set_alpha(128)
        self.win.blit(self.planet_image, self.surface_rect.midtop)
        self.world_y += self.spacing * 3

        # building slots:____________________________________________________________________________________________
        drawText(self.win, "building slots:  " + str(self.parent.selected_planet.economy_agent.building_slot_amount) + "/" + str(self.parent.selected_planet.economy_agent.building_slot_max_amount - 1), self.frame_color, (
            x + self.spacing_x, self.world_y, self.get_screen_width(), 20), self.font, "left")
        # plus icon
        # plus_image = scale_image_cached(
        #     get_image("plus_icon.png"), self.resource_image_size)

        # get rect for storage
        # plus_image_rect = plus_image.get_rect()
        self.plus_image_rect.x = x
        self.plus_image_rect.y = self.world_y
        self.plus_button_image["plus_icon"] = self.plus_image_rect
        self.win.blit(self.plus_image, (x, self.world_y))
        self.world_y += self.spacing * 2

        # minus icon
        # minus_image = scale_image_cached(
        #     get_image("minus_icon.png"), self.resource_image_size)

        # get rect for storage
        # minus_image_rect = minus_image.get_rect()
        self.minus_image_rect.x = x
        self.minus_image_rect.y = self.world_y
        self.minus_button_image["minus_icon"] = self.minus_image_rect
        self.win.blit(self.minus_image, (x, self.world_y))
        self.world_y += self.spacing * 3

        # buildings:_______________________________________________________________________________________________
        defence_units = building_factory.get_defence_unit_names()
        civil_buildings = [i for i in self.parent.selected_planet.economy_agent.buildings if not i in defence_units]

        drawText(self.win, "buildings:  " + str(len(civil_buildings)) + "/" + str(int(self.parent.selected_planet.economy_agent.buildings_max)), self.frame_color, (
            x + self.spacing_x, self.world_y, self.get_screen_width(), 20), self.font, "left")

        # image = scale_image_cached(get_image("building_icon.png"),self.resource_image_size)
        #
        # image_rect = image.get_rect()
        self.building_image_rect.x = x
        self.building_image_rect.y = self.world_y
        self.win.blit(self.building_image, self.building_image_rect)

        self.world_y += self.spacing * 3

        # draw an image for every type of building built, plus a counter text
        self.singleton_buildings = []
        for sb in self.parent.selected_planet.economy_agent.buildings:
            if not sb in self.singleton_buildings:
                self.singleton_buildings.append(sb)
        self.singleton_buildings_images = {}
        y = 0
        for b in self.singleton_buildings:
            # because of the dynamic creation of this panel, we cannot use a button, this would lead to memory leaks
            # and performance problems - so we just blit an image and get its rect as button surface

            image = rounded_surface(scale_image_cached(get_image(b + "_25x25.png"), self.resource_image_size), 3)

            # get rect for storage
            image_rect = image.get_rect()
            image_rect.x = x
            image_rect.y = self.world_y + y

            # store it
            self.singleton_buildings_images[b] = image_rect

            # blit it
            self.win.blit(image, image_rect)

            # building count
            value = self.parent.selected_planet.economy_agent.buildings.count(b)
            text = self.font.render(b + ": " + str(value) + "x", True, self.frame_color)
            self.win.blit(text, (x + self.spacing_x, self.world_y + y))

            y += self.spacing * 2
        self.world_y += y + self.spacing

        # PRODUCTION________________________________________________________________________________________________
        # production label
        self.planet_building_text = drawText(self.win, "production: ", self.frame_color, (
            self.surface_rect.x,
            self.world_y, self.get_screen_width(),
            self.surface.get_height()), self.font, "center")

        if self.parent.selected_planet.thumpsup_status:
            self.thumps_up = self.thumps_up_image_red
        else:
            self.thumps_up = self.thumps_up_image_green

        self.win.blit(self.thumps_up, (x, self.world_y))

        # production images and texts
        x = self.surface_rect.x + self.spacing
        # self.world_y= self.surface_rect.y + self.spacing * 15
        self.world_y += self.spacing * 3
        resources = self.parent.resources
        for r in resources:
            image = scale_image_cached(
                    get_image(r + "_25x25.png"), self.resource_image_size)
            self.win.blit(image, (x, self.world_y))

            # draw specials
            value_special = selected_planet.economy_agent.specials_dict[r]["value"]
            operator = selected_planet.economy_agent.specials_dict[r]["operator"]
            if operator == "*":
                operator = "x"
            text_ = ""
            if not str(value_special) == "0":
                text_ += f"  special: ({operator}{value_special})"
                text = self.special_font.render(operator + str(value_special), True,
                        pygame.color.THECOLORS[SPECIAL_TEXT_COLOR], )
                self.win.blit(text, (x + self.screen_width - SPECIAL_RIGHT_OFFSET, self.world_y - SPECIAL_Y_OFFSET))

            # draw resource
            # value = getattr(self.parent.selected_planet, "production_" + r)
            value = self.parent.selected_planet.economy_agent.production[r]
            text = self.font.render(r + ": " + str(value), True, self.frame_color)
            self.win.blit(text, (x + self.spacing_x, self.world_y))
            self.world_y += self.spacing * 2

        self.world_y += self.spacing * 2

        # GLOBAL PRODUCTION_________________________________________________________________________________________
        # global production label
        self.planet_building_text = drawText(self.win, "global production: ", self.frame_color, (
            self.surface_rect.x,
            self.world_y, self.get_screen_width(),
            self.surface.get_height()), self.font, "center")
        self.world_y += self.spacing * 3
        for r in resources:
            image = scale_image_cached(
                    get_image(r + "_25x25.png"), self.resource_image_size)
            self.win.blit(image, (x, self.world_y))

            if self.parent.selected_planet.owner != -1:
                value = self.parent.players[self.parent.selected_planet.owner].production[r]
            else:
                value = 0

            text = self.font.render(r + ": " + str(value), True, self.frame_color)
            self.win.blit(text, (x + self.spacing_x, self.world_y))

            self.world_y += self.spacing * 2
