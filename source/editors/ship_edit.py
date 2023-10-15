from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.interfaces.interface import Interface
from source.gui.widgets.selector import Selector
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups


class ShipEdit(Interface):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        Interface.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.create_selectors()
        self.create_save_button(lambda: self.parent.save_objects("ship_settings.json", sprite_groups.ships.sprites()), "save ship")
        self.create_close_button()

    def create_selectors(self):
        """"""
        x = self.world_x - ARROW_SIZE / 2 + self.world_width / 2
        y = self.world_y + self.text_spacing + TOP_SPACING * 2
        self.selector_ship = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "ships_list", "list": sprite_groups.ships.sprites()}, self, FONT_SIZE)

        self.selectors.append(self.selector_ship)

    def selector_callback(self, key, value):
        """this is the selector_callback function called from the selector to return the values to the editor"""
        if key == "ships":
            self.parent.ship = value
