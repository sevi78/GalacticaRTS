from pygame.sprite import LayeredUpdates
from source.gui.lod import inside_screen
from source.handlers import widget_handler


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
        self.ufos = PanZoomLayeredUpdates()
        self.planets = PanZoomLayeredUpdates()
        self.missiles = PanZoomLayeredUpdates()
        self.ships = PanZoomLayeredUpdates()
        self.collectable_items = PanZoomLayeredUpdates()
        self.explosions = PanZoomLayeredUpdates()
        self.target_objects = PanZoomLayeredUpdates()
        self.quadrants = PanZoomLayeredUpdates()
        self.grids = PanZoomLayeredUpdates()
        self.celestial_objects = PanZoomLayeredUpdates()
        self.moving_images = PanZoomLayeredUpdates()
        self.gif_handlers = PanZoomLayeredUpdates()

    def __str__(self):
        return (f"ufos: {len(self.ufos)}, missiles: {len(self.missiles)} ships:"
                f" {len(self.ships)} planets: {len(self.planets)} collectable_items:{len(self.collectable_items)} "
                f"explosions: {len(self.explosions)} target_objects: {self.target_objects} quadrants: {self.quadrants}")

    def update(self, *args, **kwargs):
        self.celestial_objects.update(*args)
        self.ufos.update(*args)
        self.planets.update(*args)
        self.missiles.update(*args)
        self.ships.update(*args)
        self.collectable_items.update(*args)
        self.explosions.update(*args)
        self.target_objects.update(*args)
        self.quadrants.update(*args)
        self.moving_images.update()
        self.gif_handlers.update()

    def draw(self, surface, **kwargs):
        events = kwargs.get("events")
        self.ufos.draw(surface)
        self.missiles.draw(surface)
        self.ships.draw(surface)
        self.collectable_items.draw(surface)
        self.explosions.draw(surface)
        self.target_objects.draw(surface)
        self.moving_images.draw(surface)
        self.gif_handlers.draw(surface)
        widget_handler.update(events)

    def listen(self, events):
        for i in self.planets:
            i.listen(events)


sprite_groups = SpriteGroups()
