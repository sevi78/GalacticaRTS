from source.configuration import global_params
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship import PanZoomShip


class ShipFactory:
    def create_ship(self, name, x, y, parent, weapons, **kwargs):
        """ creates a ship from the image name like: schiff1_30x30"""
        data = kwargs.get("data", {})
        size_x, size_y = map(int, name.split("_")[1].split(".")[0].split("x"))
        name = name.split("_")[0]
        ship = PanZoomShip(global_params.win,
            x,
            y,
            size_x,
            size_y,
            pan_zoom_handler,
            f"{name}_30x30.png",
            debug=False,
            group="ships",
            parent=parent,
            rotate_to_target=True,
            move_to_target=True,
            align_image="center",
            layer=5,
            info_panel_alpha=80,
            current_weapon="laser",
            name=name,
            weapons=weapons,
            data=data,
            outline_thickness= 3,
            outline_threshold = 127)
        return ship

    def create_ships_from_data(self, data):
        for key, value in data["ships"].items():
            self.create_ship(
                data["ships"][key]["name"] + "_30x30.png",
                data["ships"][key]["world_x"],
                data["ships"][key]["world_y"], global_params.app, data["ships"][key]["weapons"], data=data)

    def delete_ships(self):
        for i in sprite_groups.ships.sprites():
            i.__delete__(i)
