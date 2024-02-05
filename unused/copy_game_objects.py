import pygame

from source.factories.planet_factory import planet_factory
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet import PanZoomPlanet
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.configuration import global_params
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image


class CopyObject:
    """ copies objects
    """

    def __init__(self):
        self.frame_color = colors.frame_color
        self.copy_object = None
        self.new_object = None

    def handle_events(self, events):
        for event in events:
            ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL
            edit_mode = global_params.edit_mode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ctrl_pressed and edit_mode:
                self.copy_object = self.get_object_at_mouse_position()
                if self.copy_object:
                    self.new_object = self.create_new_object()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and ctrl_pressed and edit_mode:
                self.copy_object = None
                self.new_object = None

            elif event.type == pygame.MOUSEMOTION and self.new_object:
                self.move_new_object_to_mouse()

            if event.type == pygame.KEYDOWN and ctrl_pressed:
                if event.key == pygame.K_c:
                    self.copy_object = global_params.app.selected_planet
                elif event.key == pygame.K_v:
                    self.create_new_object()

    def get_object_at_mouse_position(self):
        for obj in sprite_groups.planets:
            if obj.rect.collidepoint(pygame.mouse.get_pos()):
                return obj

    def create_new_object(self):
        if self.new_object:
            return
        if not self.copy_object:
            return

        app = global_params.app
        panzoom = pan_zoom_handler

        x, y = pygame.mouse.get_pos()
        planet_name = self.copy_object.name  # + "_" + str(len(app.planets))
        # Create planet object
        self.new_planet = PanZoomPlanet(
            global_params.win,
            x, y,
            self.copy_object.get_screen_width(), self.copy_object.get_screen_height(), isSubWidget=False,
            image_name=self.copy_object.image_name_small,
            pan_zoom=panzoom,
            image=get_image(self.copy_object.image_name_small),
            transparent=True,
            info_text=self.copy_object.info_text,
            text=planet_name,
            textColour=self.frame_color,
            property="planet",
            name=planet_name,
            parent=app,
            tooltip="send your ship to explore the planet!",
            possible_resources=self.copy_object.possible_resources,
            moveable=True,
            textVAlign="below_the_bottom",
            layer=3,
            id=self.copy_object.id,
            string=planet_name,
            )

        ignorable_params = ["x", "y", "_x", "_y", "name", "id"]
        for key, value in self.copy_object.__dict__.items():
            if not key in ignorable_params:
                setattr(self.new_planet, key, value)

        # Set size
        self.new_planet.size_x = self.copy_object.size_x
        self.new_planet.size_y = self.copy_object.size_y

        # Set position
        x, y = panzoom.screen_2_world(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.new_planet.world_x, self.new_planet.world_y = x, y

        # no idea why this is needed, without no resoure buttons ... ??? :)
        self.new_planet.update_planet_resources(self.copy_object.possible_resources)
        self.copy_object.update_planet_resources(self.copy_object.possible_resources)

        self.new_planet.id = len(sprite_groups.planets.sprites())
        self.new_planet.set_planet_name()
        planet_factory.save_planets()

    def move_new_object_to_mouse(self):
        x, y = pygame.mouse.get_pos()
        self.new_object.x = x
        self.new_object.y = y

    def update(self, events):
        self.handle_events(events)

    def __repr__(self):
        return f"CopyObject(copy_object={self.copy_object}, new_object={self.new_object})"


def create_copy_agent():
    copy_agent = CopyObject()
    return copy_agent
