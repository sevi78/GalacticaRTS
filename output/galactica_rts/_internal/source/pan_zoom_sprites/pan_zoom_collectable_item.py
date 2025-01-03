import pygame

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.interaction.interaction_handler import InteractionHandler
from source.multimedia_library.images import scale_image_cached
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite


class PanZoomCollectableItem(PanZoomSprite, InteractionHandler):
    """"""

    __slots__ = PanZoomSprite.__slots__ + ('property', 'info_text', 'tooltip', 'energy', 'food', 'minerals', 'water',
                                           'population', 'technology', 'resources', 'collect_text')

    # PanZoomMouseHandler
    # __slots__ += ("_on_hover", "on_hover_release")

    def __init__(self, win, x, y, width, height,image_name, **kwargs):
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom_handler, image_name, **kwargs)
        InteractionHandler.__init__(self)
        self.property = "item"
        self.type = "collectable item"
        self.info_text = kwargs.get("infotext")
        self.tooltip = kwargs.get("tooltip", None)
        self.resources = kwargs.get("resources", {})
        self.specials = kwargs.get("specials", [])
        self.collect_text = ""
        # self.name = "collectable item"
        self.collected = False
        self.id = kwargs.get("id", len(sprite_groups.collectable_items))

        sprite_groups.collectable_items.add(self)

    def end_object(self):
        sprite_groups.collectable_items.remove(self)
        self.kill()

    def listen(self):
        if not level_of_detail.inside_screen(self.get_screen_position()):
            return

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()

            if self.rect.collidepoint(mouse_handler.get_mouse_pos()):  # self.contains(x, y):
                if mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                    self.win.blit(scale_image_cached(self.image_outline, self.rect.size), self.rect)
                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            config.tooltip_text = self.tooltip

                    # set cursor
                    config.app.cursor.set_cursor("watch")

                # set info text on hover
                if self.info_text:
                    config.app.info_panel.set_text(self.info_text)
                    config.app.info_panel.set_planet_image(self.image_raw, size=self.image_raw.get_size())

    def update(self):
        self.update_pan_zoom_sprite()
        self.listen()

        config.app.tooltip_instance.reset_tooltip(self)
