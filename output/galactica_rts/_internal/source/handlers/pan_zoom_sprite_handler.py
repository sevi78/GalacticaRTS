import threading
import pygame
from pygame.sprite import LayeredUpdates

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.gui.container.container_widget import ContainerWidgetItem, WIDGET_SIZE
from source.handlers import widget_handler
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image, get_gif_frames


class PanZoomLayeredUpdates(LayeredUpdates):
    def __init__(self, *sprites, **kwargs):
        LayeredUpdates.__init__(self, *sprites, **kwargs)

    def draw(self, surface, bgsurf=None, special_flags=0):
        spritedict = self.spritedict

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

            newrect = surface.blit(spr.image, spr.rect, None, special_flags)
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

    def get_hit_object(self, **kwargs: {list}) -> object or None:
        """ returns an object that is at mouse position

            optional(kwargs):

            use 'filter' to filter out the sprite_groups that are not involved
            or use 'lists' as parameter to get only the objects in these lists

            default lists are:
            ["planets", "ships", "ufos", "collectable_items", "celestial_objects"]


        """
        filter = kwargs.get("filter", [])
        lists = kwargs.get("lists", ["planets", "ships", "ufos", "collectable_items", "celestial_objects"])

        if filter:
            lists -= filter

        for list_name in lists:
            if hasattr(self, list_name):
                for obj in getattr(self, list_name):
                    if obj.collide_rect.collidepoint(pygame.mouse.get_pos()):
                        return obj

        return None

    def get_nearest_obj_by_type(self, sprite_group, key, caller):
        objects = [obj for obj in sprite_group if obj.type == key]
        if objects:
            return min(objects, key=lambda obj: pygame.math.Vector2(obj.rect.center).distance_to(caller.rect.center))
        return None

    def get_nearest_obj(self, sprite_group, caller):
        if sprite_group:
            return min(sprite_group, key=lambda
                obj: pygame.math.Vector2(obj.rect.center).distance_to(caller.rect.center))
        return None

    def convert_sprite_groups_to_image_widget_list(self, sprite_group_name, sort_by=None, reverse=True) -> list:
        # If a sort_by attribute is provided, sort the sprite_group by that attribute
        sprite_group = getattr(self, sprite_group_name)
        if sort_by is not None:
            sprite_group = sorted(sprite_group, key=lambda x: getattr(x, sort_by), reverse=reverse)

        return [ContainerWidgetItem(
                config.app.win,
                0,
                WIDGET_SIZE * index,
                WIDGET_SIZE,
                WIDGET_SIZE,
                image=get_image(_.image_name) if not _.image_name.endswith(".gif") else get_gif_frames(_.image_name)[0],
                obj=_,
                index=index + 1)
            for index, _ in enumerate(sprite_group)]

    def listen(self, events):
        for i in self.planets:
            i.listen(events)

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

    def draw(self, surface, **kwargs):
        events = kwargs.get("events")
        widget_handler.update(events)

        if WidgetHandler.layer_switch["0"]:
            self.planets.draw(surface)
            if config.show_universe:
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
            WidgetHandler.draw_layer(events, 8)

        if WidgetHandler.layer_switch["9"]:
            WidgetHandler.draw_layer(events, 9)

        if WidgetHandler.layer_switch["10"]:
            WidgetHandler.draw_layer(events, 10)


sprite_groups = SpriteGroups()
