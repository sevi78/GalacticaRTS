import pygame

from source.gui.lod import inside_screen
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_mouse_handler import PanZoomMouseHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
from source.configuration import global_params


class PanZoomCollectableItem(PanZoomSprite, PanZoomMouseHandler):
    """"""

    __slots__ = PanZoomSprite.__slots__ + ('property', 'info_text', 'tooltip', 'energy', 'food', 'minerals', 'water',
                                           'population', 'technology', 'resources', 'collect_text')

    # PanZoomMouseHandler
    __slots__ += ("_on_hover", "on_hover_release")

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        PanZoomMouseHandler.__init__(self)
        self.property = "item"
        self.type = "collectable item"
        self.info_text = kwargs.get("infotext")
        self.tooltip = kwargs.get("tooltip", None)
        self.energy = kwargs.get("energy", 0)
        self.food = kwargs.get("food", 0)
        self.minerals = kwargs.get("minerals", 0)
        self.water = kwargs.get("water", 0)
        self.population = kwargs.get("population", 0)
        self.technology = kwargs.get("technology", None)
        self.resources = {"water": self.water, "energy": self.energy, "food": self.food, "minerals": self.minerals, "technology": self.technology}
        self.specials = kwargs.get("specials", [])
        self.collect_text = ""
        self.name = "collectable item"
        self.collected = False

        sprite_groups.collectable_items.add(self)

    def end_object(self):
        sprite_groups.collectable_items.remove(self)
        self.kill()

    def listen(self):
        if not inside_screen(self.get_screen_position(), border=100):
            return

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()

            if self.rect.collidepoint(mouse_handler.get_mouse_pos()):  # self.contains(x, y):
                if mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                    self.win.blit(pygame.transform.scale(self.image_outline,self.rect.size), self.rect)
                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            global_params.tooltip_text = self.tooltip

                    if self.info_text:
                        global_params.app.info_panel.set_text(self.info_text)
                        global_params.app.info_panel.set_planet_image(self.image_raw, size=self.image_raw.get_size())

    def update(self):
        self.update_pan_zoom_sprite()
        self.listen()

        global_params.app.tooltip_instance.reset_tooltip(self)

