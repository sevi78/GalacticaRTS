import pygame


class ShipLayeredUpdates2_(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()
        self.events = []

    def update(self, *args):
        for sprite in self.sprites():
            sprite.update(*args)
            for event in self.events:
                if hasattr(sprite, 'listen'):
                    sprite.listen(event)
        self.events.clear()

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if spr.inside_screen:
                spr.draw()
                # if spr.image:
                #     self.spritedict[spr] = surface_blit(spr.image, spr.rect)
                # else:
                #     spr.draw()
            if spr.debug:
                spr.debug_object()
        self.lostsprites = []

    def handle_events(self, events):
        self.events.extend(events)



class ShipLayeredUpdates2(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        """draw all sprites in the right order onto the passed surface

        LayeredUpdates.draw(surface): return Rect_list

        """
        # spritedict = self.spritedict
        # surface_blit = surface.blit
        # dirty = self.lostsprites
        # self.lostsprites = []
        # dirty_append = dirty.append
        # init_rect = self._init_rect
        # for spr in self.sprites():
        #     rec = spritedict[spr]
        #     newrect = surface_blit(spr.image, spr.rect)
        #     if rec is init_rect:
        #         dirty_append(newrect)
        #     else:
        #         if newrect.colliderect(rec):
        #             dirty_append(newrect.union(rec))
        #         else:
        #             dirty_append(newrect)
        #             dirty_append(rec)
        #     spritedict[spr] = newrect
        # return dirty

        for spr in self.sprites():
            spr.draw()



