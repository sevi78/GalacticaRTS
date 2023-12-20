import pygame.draw
from pygame_widgets import Mouse
from pygame_widgets.mouse import MouseState
from source.gui.lod import inside_screen
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_mouse_handler import PanZoomMouseHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
from source.utils import global_params


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
            mouseState = Mouse.getMouseState()
            if self.rect.collidepoint(pygame.mouse.get_pos()):  # self.contains(x, y):
                if mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            global_params.tooltip_text = self.tooltip

                    if self.info_text:
                        global_params.app.info_panel.set_text(self.info_text)


    def update(self):
        self.update_pan_zoom_sprite()
        self.listen()

        global_params.app.tooltip_instance.reset_tooltip(self)
        # if global_params.debug:
        #     self.debug_object()
