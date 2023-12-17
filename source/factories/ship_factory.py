from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ships import Spacehunter, Spaceship, Cargoloader
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params

class ShipFactory:
    def create_ship(self, name, x, y, parent):

        """ creates a ship from the image name like: schiff1_30x30"""
        size_x, size_y = map(int, name.split("_")[1].split(".")[0].split("x"))
        name = name.split("_")[0]
        class_ = name[0].upper() + name[1:]

        if class_ == "Spaceship":
            ship = Spaceship(global_params.win, x, y, size_x, size_y, pan_zoom_handler, "spaceship_30x30.png",
                debug=False, group="ships", parent=parent, rotate_to_target=True, move_to_target=True,
                align_image="center", layer=1, info_panel_alpha=80)

        if class_ == "Spacehunter":
            ship = Spacehunter(global_params.win, x, y, size_x, size_y, pan_zoom_handler, "spacehunter_30x30.png",
                debug=False, group="ships", parent=parent, rotate_to_target=True, move_to_target=True,
                align_image="center", layer=1, info_panel_alpha=80)

        if class_ == "Cargoloader":
            ship = Cargoloader(global_params.win, x, y, size_x + 20, size_y + 20, pan_zoom_handler, "cargoloader_30x30.png",
                debug=False, group="ships", parent=parent, rotate_to_target=True, move_to_target=True,
                align_image="center", layer=1, info_panel_alpha=80)

        return ship

    def delete_ships(self):
        for i in sprite_groups.ships.sprites():
            i.__delete__(i)

