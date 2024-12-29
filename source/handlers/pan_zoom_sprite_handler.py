import pygame
from pygame.sprite import LayeredUpdates, LayeredDirty, Group

from source.configuration.game_config import config
from source.gui.container.container_widget import ContainerWidgetItem, WIDGET_SIZE
from source.gui.lod import level_of_detail
from source.handlers import widget_handler
# from source.handlers.position_handler import prevent_object_overlap
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image, get_gif_frames
from source.pan_zoom_sprites.pan_zoom_ship_test2.pan_zoom_layered_update_test2 import ShipLayeredUpdates2

"""
TODO: clean up the mess here !!! 

we might not use so many different Updaes classes.

- check wich of them need visible , _hidden ect ... 

"""

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


class UniverseLayeredUpdates(pygame.sprite.LayeredUpdates):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if spr.inside_screen:
                if hasattr(spr, "image"):
                # if spr.image:
                    self.spritedict[spr] = surface_blit(spr.image, spr.rect)
                else:
                    spr.draw()
            if spr.debug:
                spr.debug_object()
        self.lostsprites = []

class ReloaderLayeredUpdates(pygame.sprite.LayeredUpdates):

    """
    this class handles the updates and drawing of all sprites, only if they are visible
    """
    def __init__(self):
        super().__init__()

    def draw(self, *args, **kwargs):
        sprites = self.sprites()
        for spr in sprites:
            if spr.visible:
                spr.draw()




class SpriteGroups:  # original
    def __init__(self):
        self.planets = PanZoomLayeredUpdates(default_layer=0)
        self.gif_handlers = PanZoomLayeredUpdates(default_layer=1)
        self.collectable_items = PanZoomLayeredUpdates(default_layer=2)
        self.ufos = PanZoomLayeredUpdates(default_layer=0)
        self.ships = PanZoomLayeredUpdates(default_layer=4)
        self.ships2 = ShipLayeredUpdates2()
        self.missiles =LayeredUpdates(default_layer=5)
        self.explosions = PanZoomLayeredUpdates(default_layer=6)
        self.target_objects = PanZoomLayeredUpdates(default_layer=7)
        self.moving_images = PanZoomLayeredUpdates(default_layer=8)
        self.state_images = PanZoomLayeredUpdates(default_layer=4)
        self.universe = UniverseLayeredUpdates(defaults_layer=0)
        self.energy_reloader = ReloaderLayeredUpdates()
        # self.energy_reloader = LayeredUpdates(default_layer=0)
        # self.energy_reloader = Group(default_layer=0)


    def get_hit_object__(self, **kwargs: {list}) -> object or None:# very slow
        """ returns an object that is at mouse position

            optional(kwargs):

            use 'filter' to filter out the sprite_groups that are not involved
            or use 'lists' as parameter to get only the objects in these lists

            default lists are:
            ["planets", "ships", "ufos", "collectable_items", "celestial_objects"]


        """
        filter_ = kwargs.get("filter", [])
        lists = kwargs.get("lists", ["planets", "ships", "ufos", "collectable_items", "celestial_objects"])

        if filter_:
            lists -= filter_

        for list_name in lists:
            if hasattr(self, list_name):
                for obj in getattr(self, list_name):
                    if obj.collide_rect.collidepoint(pygame.mouse.get_pos()):
                        return obj

        return None

    def get_hit_object(self, **kwargs):
        filter_ = kwargs.get("filter", [])
        lists = kwargs.get("lists", ["planets", "ships", "ufos", "collectable_items", "celestial_objects"])
        lists = [l for l in lists if l not in filter_]

        mouse_pos = pygame.mouse.get_pos()

        for list_name in lists:
            if hasattr(self, list_name):
                sprite_list = getattr(self, list_name)
                collided = sprite_list.get_sprites_at(mouse_pos)
                if collided:
                    return collided[0]

        return None

    def get_nearest_obj_by_type(self, sprite_group, key, caller):
        """
        returns the nearest obj:

        params:
        sprite_groups: the sprite_group to search for
        key: the type of the obj, like moon sun or planet
        caller: the reference object to calculate the distance
        """
        objects = [obj for obj in sprite_group if obj.type == key]
        if objects:
            return min(objects, key=lambda obj: pygame.math.Vector2(obj.rect.center).distance_to(caller.rect.center))
        return None

    def get_nearest_obj(self, sprite_group, caller):
        if sprite_group:
            return min(sprite_group, key=lambda
                obj: pygame.math.Vector2(obj.rect.center).distance_to(caller.rect.center))
        return None

    def sort_sprites_by_distance(self, sprite_group, caller):
        if sprite_group:
            return sorted(sprite_group, key=lambda
                obj: pygame.math.Vector2(obj.rect.center).distance_to(caller.rect.center))
        return []

    def convert_sprite_groups_to_container_widget_items_list(
            self, sprite_group_name, sort_by=None, reverse=True, **kwargs
            ) -> list:

        # If a sort_by attribute is provided, sort the sprite_group by that attribute
        sprite_group = getattr(sprite_groups, sprite_group_name)

        if config.show_human_player_only:
            # Create a new SpriteGroup with only human player sprites
            human_player_sprites = [sprite for sprite in sprite_group if sprite.owner == config.app.game_client.id]

            # Create a new SpriteGroup with the filtered sprites
            new_sprite_group = type(sprite_group)()  # Create a new instance of the same SpriteGroup type
            for sprite in human_player_sprites:
                new_sprite_group.add(sprite)

            sprite_group = new_sprite_group

        if sort_by is not None:
            # Convert sprite_group to a list for sorting
            sprite_list = sprite_group.sprites()
            # handle the case if the sprite_group is empty
            if not sprite_list:
                return []

            if hasattr(sprite_list[0].economy_agent, sort_by):
                sorted_sprites = sorted(sprite_list, key=lambda x: getattr(x.economy_agent, sort_by), reverse=reverse)
            else:
                sorted_sprites = sorted(sprite_list, key=lambda x: getattr(x, sort_by), reverse=reverse)

            # Create a new sorted SpriteGroup
            sorted_sprite_group = type(sprite_group)()
            for sprite in sorted_sprites:
                sorted_sprite_group.add(sprite)

            sprite_group = sorted_sprite_group

        item_buttons = kwargs.get("item_buttons", {})
        parent = kwargs.get("parent", None)
        return [ContainerWidgetItem(
                config.app.win,
                0,
                WIDGET_SIZE * index,
                WIDGET_SIZE,
                WIDGET_SIZE,
                image=get_image(_.image_name) if not _.image_name.endswith(".gif") else get_gif_frames(_.image_name)[0],
                obj=_,
                index=index + 1,
                item_buttons=item_buttons,
                parent=parent)
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
        self.ships2.update(*args)
        self.missiles.update(*args)
        self.explosions.update(*args)
        self.target_objects.update(*args)
        self.universe.update(*args)
        self.energy_reloader.update()


    def draw(self, surface, **kwargs):
        events = kwargs.get("events")
        widget_handler.update(events)
        self.universe.draw(surface)

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
            self.energy_reloader.draw(surface)
            self.ships.draw(surface)
            self.ships2.draw(surface)

        if WidgetHandler.layer_switch["4"]:
            WidgetHandler.draw_layer(events, 4)
            self.missiles.draw(surface)
            self.state_images.draw(surface)

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

        self.moving_images.update()




sprite_groups = SpriteGroups()
