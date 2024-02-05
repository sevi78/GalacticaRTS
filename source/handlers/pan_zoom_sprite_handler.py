from pygame.sprite import LayeredUpdates

from source.gui.lod import inside_screen
from source.handlers import widget_handler
from source.handlers.widget_handler import WidgetHandler


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
            if not inside_screen(spr.rect.center, border=50):
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


class SpriteGroups:
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

    def update(self, *args, **kwargs):
        self.planets.update(*args)
        self.gif_handlers.update()
        self.collectable_items.update(*args)
        self.ufos.update(*args)

        self.missiles.update(*args)
        self.explosions.update(*args)
        self.target_objects.update(*args)
        self.moving_images.update()
        # self.ships.update(*args)

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
            self.target_objects.draw(surface)

        if WidgetHandler.layer_switch["7"]:
            WidgetHandler.draw_layer(events, 7)
            self.moving_images.draw(surface)

        if WidgetHandler.layer_switch["8"]:
            WidgetHandler.draw_layer(events, 8)

        if WidgetHandler.layer_switch["9"]:
            WidgetHandler.draw_layer(events, 9)

        if WidgetHandler.layer_switch["10"]:
            WidgetHandler.draw_layer(events, 10)

        # ships must be updated here, because they draw also... this is bullshit but... ;)
        self.ships.update()

    def listen(self, events):
        for i in self.planets:
            i.listen(events)


sprite_groups = SpriteGroups()
