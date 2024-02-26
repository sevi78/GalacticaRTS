import threading
import pygame
from pygame.sprite import LayeredUpdates

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.gui.widgets.container_widget import ContainerWidgetItem, WIDGET_SIZE
from source.handlers import widget_handler
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image, get_gif, get_gif_frames


class PanZoomLayeredUpdates(LayeredUpdates):
    def __init__(self, *sprites, **kwargs):
        LayeredUpdates.__init__(self, *sprites, **kwargs)

    def draw(self, surface, bgsurf=None, special_flags=0):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect

        for spr in self.sprites():
            if spr._hidden:
                if spritedict[spr] is not init_rect:
                    dirty_append(spritedict[spr])
                    spritedict[spr] = init_rect
                continue

            rec = spritedict[spr]
            if not level_of_detail.inside_screen(spr.rect.center):
                if rec is not init_rect:
                    dirty_append(rec)
                spritedict[spr] = init_rect
                continue

            newrect = surface_blit(spr.image, spr.rect, None, special_flags)
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect

        return dirty


class SpriteGroups:  # original
    def __init__(self):
        # self.layered_updates = PanZoomLayeredUpdates()
        # self.planets = self.layered_updates
        # self.gif_handlers = self.layered_updates
        # self.collectable_items = self.layered_updates
        # self.ufos = self.layered_updates
        # self.ships = self.layered_updates
        # self.missiles = self.layered_updates
        # self.explosions = self.layered_updates
        # self.target_objects = self.layered_updates
        # self.state_images = self.layered_updates
        self.planets = PanZoomLayeredUpdates(default_layer=0)
        self.gif_handlers = PanZoomLayeredUpdates(default_layer=1)
        self.collectable_items = PanZoomLayeredUpdates(default_layer=2)
        self.ufos = PanZoomLayeredUpdates(default_layer=0)
        self.ships = PanZoomLayeredUpdates(default_layer=4)
        self.missiles = PanZoomLayeredUpdates(default_layer=5)
        self.explosions = PanZoomLayeredUpdates(default_layer=6)
        self.target_objects = PanZoomLayeredUpdates(default_layer=7)
        self.moving_images = PanZoomLayeredUpdates(default_layer=8)
        self.state_images = PanZoomLayeredUpdates(default_layer=8)



    def update(self, *args, **kwargs):
        # self.layered_updates.update(*args)
        self.planets.update(*args)
        self.gif_handlers.update()
        self.collectable_items.update(*args)
        self.ufos.update(*args)
        self.ships.update(*args)
        self.missiles.update(*args)
        self.explosions.update(*args)
        self.target_objects.update(*args)
        self.moving_images.update()
        self.state_images.update()

    def draw(self, surface, **kwargs):
        events = kwargs.get("events")
        widget_handler.update(events)

        if WidgetHandler.layer_switch["0"]:
            self.planets.draw(surface)
            WidgetHandler.draw_layer(events, 0)
            self.gif_handlers.draw(surface)

        if WidgetHandler.layer_switch["1"]:
            WidgetHandler.draw_layer(events, 1)
            self.collectable_items.draw(surface)

        if WidgetHandler.layer_switch["2"]:
            WidgetHandler.draw_layer(events, 2)
            self.ufos.draw(surface)

        if WidgetHandler.layer_switch["3"]:
            WidgetHandler.draw_layer(events, 3)
            self.ships.draw(surface)

        if WidgetHandler.layer_switch["4"]:
            WidgetHandler.draw_layer(events, 4)
            self.missiles.draw(surface)

        if WidgetHandler.layer_switch["5"]:
            WidgetHandler.draw_layer(events, 5)
            self.explosions.draw(surface)

        if WidgetHandler.layer_switch["6"]:
            WidgetHandler.draw_layer(events, 6)

        if WidgetHandler.layer_switch["7"]:
            WidgetHandler.draw_layer(events, 7)
            self.target_objects.draw(surface)

        if WidgetHandler.layer_switch["8"]:
            self.moving_images.draw(surface)
            self.state_images.draw(surface)
            WidgetHandler.draw_layer(events, 8)

        if WidgetHandler.layer_switch["9"]:
            WidgetHandler.draw_layer(events, 9)

        if WidgetHandler.layer_switch["10"]:
            WidgetHandler.draw_layer(events, 10)

        # ships must be updated here, because they draw also... this is bullshit but... ;)
        # self.ships.update()

    def convert_sprite_groups_to_image_widget_list(self, sprite_group) -> list:
        return [ContainerWidgetItem(config.app.win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE,
            image=get_image(_.image_name) if not _.image_name.endswith(".gif") else get_gif_frames(_.image_name)[0],
            obj=_, index=index) for index, _ in enumerate(sprite_group)]

    def listen(self, events):
        for i in self.planets:
            i.listen(events)

    def get_hit_object(self, **kwargs: {list}) -> object or None:
        filter = kwargs.get("filter", [])
        lists = ["planets", "ships", "ufos", "collectable_items", "celestial_objects"]
        if filter:
            lists -= filter

        for list_name in lists:
            if hasattr(self, list_name):
                for obj in getattr(self, list_name):
                    if obj.rect.collidepoint(pygame.mouse.get_pos()):
                        return obj

        return None


# Define a function that will be the target of the thread
def update_sprite_group(group, *args):
    group.update(*args)


class SpriteGroups__:  # multithreading
    def __init__(self):

        self.sprite_groups = {
            'planets': PanZoomLayeredUpdates(default_layer=0),
            'gif_handlers': PanZoomLayeredUpdates(default_layer=1),
            'collectable_items': PanZoomLayeredUpdates(default_layer=2),
            'ufos': PanZoomLayeredUpdates(default_layer=0),
            'ships': PanZoomLayeredUpdates(default_layer=4),
            'missiles': PanZoomLayeredUpdates(default_layer=5),
            'explosions': PanZoomLayeredUpdates(default_layer=6),
            'target_objects': PanZoomLayeredUpdates(default_layer=7),
            'moving_images': PanZoomLayeredUpdates(default_layer=8),
            'state_images': PanZoomLayeredUpdates(default_layer=8)
            }
        for key, value in self.sprite_groups.items():
            setattr(self, key, value)

    def convert_sprite_groups_to_image_widget_list(self, sprite_group) -> list:
        return [ContainerWidgetItem(config.app.win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE,
            image=get_image(_.image_name) if not _.image_name.endswith(".gif") else get_gif_frames(_.image_name)[0],
            obj=_, index=index) for index, _ in enumerate(sprite_group)]

    def listen(self, events):
        for i in self.planets:
            i.listen(events)

    def get_hit_object(self, **kwargs: {list}) -> object or None:
        filter = kwargs.get("filter", [])
        lists = ["planets", "ships", "ufos", "collectable_items", "celestial_objects"]
        if filter:
            lists -= filter

        for list_name in lists:
            if hasattr(self, list_name):
                for obj in getattr(self, list_name):
                    if obj.rect.collidepoint(pygame.mouse.get_pos()):
                        return obj

        return None

    def update__(self, *args, **kwargs):
        threads = []
        for group_name, group in self.sprite_groups.items():
            # Create a new Thread object with the target function and arguments
            thread = threading.Thread(target=update_sprite_group, args=(group, *args))
            threads.append(thread)
            thread.start()  # Start the thread

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def update(self, *args, **kwargs):
        self.planets.update(*args)
        self.gif_handlers.update()
        self.collectable_items.update(*args)
        self.ufos.update(*args)
        self.ships.update(*args)
        self.missiles.update(*args)
        self.explosions.update(*args)
        self.target_objects.update(*args)
        self.moving_images.update()
        self.state_images.update()

    def draw(self, surface, **kwargs):#orog
        events = kwargs.get("events")
        threads = []

        widget_handler.update(events)

        for layer, group in enumerate(self.sprite_groups.values()):
            if WidgetHandler.layer_switch[str(layer)]:

                WidgetHandler.draw_layer(events, layer)
                group.draw(surface)


    # mulithreading
    # def draw(self, surface, **kwargs):
    #     events = kwargs.get("events")
    #     threads = []
    #
    #     widget_handler.update(events)
    #
    #     for layer, group in enumerate(self.sprite_groups.values()):
    #         if WidgetHandler.layer_switch[str(layer)]:
    #             # Create a new Thread object with the target function and arguments
    #             thread = threading.Thread(target=self._draw_group, args=(events, layer, group, surface))
    #             threads.append(thread)
    #             thread.start()  # Start the thread
    #
    #     # Wait for all threads to complete
    #     for thread in threads:
    #         thread.join()
    #
    # def _draw_group(self, events, layer, group, surface):
    #     WidgetHandler.draw_layer(events, layer)
    #     group.draw(surface)
class SpriteGroups__:  # doesn work yet, needs to refactor all registration to it
    def __init__(self):
        self.sprite_groups = {
            'planets': PanZoomLayeredUpdates(default_layer=0),
            'gif_handlers': PanZoomLayeredUpdates(default_layer=1),
            'collectable_items': PanZoomLayeredUpdates(default_layer=2),
            'ufos': PanZoomLayeredUpdates(default_layer=0),
            'ships': PanZoomLayeredUpdates(default_layer=4),
            'missiles': PanZoomLayeredUpdates(default_layer=5),
            'explosions': PanZoomLayeredUpdates(default_layer=6),
            'target_objects': PanZoomLayeredUpdates(default_layer=7),
            'moving_images': PanZoomLayeredUpdates(default_layer=8)
            }

    def update(self, *args, **kwargs):
        for group in self.sprite_groups.values():
            group.update(*args)

    def draw(self, surface, **kwargs):
        events = kwargs.get("events")
        widget_handler.update(events)

        for layer, group in enumerate(self.sprite_groups.values()):
            if WidgetHandler.layer_switch[str(layer)]:
                WidgetHandler.draw_layer(events, layer)
                group.draw(surface)


sprite_groups = SpriteGroups()
