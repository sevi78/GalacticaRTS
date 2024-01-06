from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship import PanZoomShip
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.configuration import global_params


class ShipFactory:
    def create_ship(self, name, x, y, parent):
        """ creates a ship from the image name like: schiff1_30x30"""
        size_x, size_y = map(int, name.split("_")[1].split(".")[0].split("x"))
        name = name.split("_")[0]
        ship = PanZoomShip(global_params.win, x, y, size_x, size_y, pan_zoom_handler, f"{name}_30x30.png",
            debug=False, group="ships", parent=parent, rotate_to_target=True, move_to_target=True,
            align_image="center", layer=1, info_panel_alpha=80, current_weapon="laser", name=name)
        return ship

    def delete_ships(self):
        for i in sprite_groups.ships.sprites():
            i.__delete__(i)
