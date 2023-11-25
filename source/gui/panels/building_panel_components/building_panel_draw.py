import pygame
from pygame_widgets.util import drawText

from source.factories.building_factory import building_factory
from source.multimedia_library.images import images, pictures_path, get_image
from source.utils.text_formatter import format_number

SMILEY_SIZE = 20


class BuildingPanelDraw:

    def draw_planet_params(self, x):
        # draw population text
        # population
        drawText(self.win, "population: " + str(int(self.parent.selected_planet.population)) + "/" + format_number(self.parent.selected_planet.population_limit, 1), self.frame_color, (
            x + self.spacing_x, self.world_y, self.get_screen_width(), 20), self.font, "left")
        image = get_image("city_25x25.png")
        self.win.blit(image, (x, self.world_y))
        self.world_y += self.spacing * 3

        if self.parent.selected_planet.smiley_status:
            self.smiley = self.smiley_image_smile
        else:
            self.smiley = self.smiley_image_sad

        self.win.blit(self.smiley, (x, self.world_y))

        # draw background planet icon
        name = self.parent.selected_planet.name
        pic = name + "_150x150.png"
        if pic in images[pictures_path]["planets"].keys():
            self.planet_image = get_image(pic)
        else:
            self.planet_image = pygame.transform.scale(self.parent.selected_planet.image_raw.copy(), (150, 150))
        self.planet_image.set_alpha(128)
        self.win.blit(self.planet_image, self.surface_rect.midtop)
        self.world_y += self.spacing * 3

        # building slots:____________________________________________________________________________________________
        drawText(self.win, "building slots:  " + str(self.parent.selected_planet.building_slot_amount) + "/" + str(self.parent.selected_planet.building_slot_max_amount - 1), self.frame_color, (
            x + self.spacing_x, self.world_y, self.get_screen_width(), 20), self.font, "left")
        # plus icon
        plus_image = pygame.transform.scale(
            get_image("plus_icon.png"), self.resource_image_size)

        # get rect for storage
        plus_image_rect = plus_image.get_rect()
        plus_image_rect.x = x
        plus_image_rect.y = self.world_y
        self.plus_button_image["plus_icon"] = plus_image_rect
        self.win.blit(plus_image, (x, self.world_y))
        self.world_y += self.spacing * 2

        # minus icon
        minus_image = pygame.transform.scale(
            get_image("minus_icon.png"), self.resource_image_size)

        # get rect for storage
        minus_image_rect = minus_image.get_rect()
        minus_image_rect.x = x
        minus_image_rect.y = self.world_y
        self.minus_button_image["minus_icon"] = minus_image_rect
        self.win.blit(minus_image, (x, self.world_y))
        self.world_y += self.spacing * 3

        # buildings:_______________________________________________________________________________________________
        defence_units = building_factory.get_defence_unit_names()
        civil_buildings = [i for i in self.parent.selected_planet.buildings if not i in defence_units]

        drawText(self.win, "buildings:  " + str(len(civil_buildings)) + "/" + str(int(self.parent.selected_planet.buildings_max)), self.frame_color, (
            x + self.spacing_x, self.world_y, self.get_screen_width(), 20), self.font, "left")
        self.world_y += self.spacing * 3

        # draw an image for every type of building built, plus a counter text
        self.singleton_buildings = []
        for sb in self.parent.selected_planet.buildings:
            if not sb in self.singleton_buildings:
                self.singleton_buildings.append(sb)
        self.singleton_buildings_images = {}
        y = 0
        for b in self.singleton_buildings:
            # because of the dynamic creation of this panel, we cannot use a button, this would lead to memory leaks
            # and performance problems - so we just blit an image and get its rect as button surface

            image = pygame.transform.scale(get_image(b + "_25x25.png"),
                self.resource_image_size)

            # get rect for storage
            image_rect = image.get_rect()
            image_rect.x = x
            image_rect.y = self.world_y + y

            # store it
            self.singleton_buildings_images[b] = image_rect

            # blit it
            self.win.blit(image, image_rect)

            # building count
            value = self.parent.selected_planet.buildings.count(b)
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
            image = pygame.transform.scale(
                images[pictures_path]["resources"][r + "_25x25.png"], self.resource_image_size)
            self.win.blit(image, (x, self.world_y))
            value = getattr(self.parent.selected_planet, "production_" + r)
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
            image = pygame.transform.scale(
                images[pictures_path]["resources"][r + "_25x25.png"], self.resource_image_size)
            self.win.blit(image, (x, self.world_y))
            value = self.parent.player.production[r]
            text = self.font.render(r + ": " + str(value), True, self.frame_color)
            self.win.blit(text, (x + self.spacing_x, self.world_y))

            self.world_y += self.spacing * 2
