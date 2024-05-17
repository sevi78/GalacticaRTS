from source.configuration.game_config import config
from source.handlers import file_handler
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_rescue_drone import PanZoomRescueDrone
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship import PanZoomShip


class ShipFactory:
    def __init__(self):
        self.ship_sizes = {
            "spaceship": (30, 30),
            "cargoloader": (30, 30),
            "spacehunter": (30, 30),
            "spacestation": (30, 30),
            "rescue drone": (30, 30)
            }
        self.ship_settings = file_handler.load_file("ship_settings.json", "config")

    def create_ship(self, name: str, x: int, y: int, parent: object, weapons: dict, **kwargs: dict) -> [PanZoomShip, PanZoomRescueDrone]:
        """ creates a ship from the image name like: schiff1_30x30
            name, x, y, parent, weapons, **kwargs

            returns a PanZoomShip
        """
        data_ = kwargs.get("data", {})
        data = self.ship_settings[name]
        for key, value in data_.items():
            data[key] = value

        size_x, size_y = self.ship_sizes[name]  # map(int, name.split("_")[1].split(".")[0].split("x"))

        class_ = PanZoomShip
        if name == "rescue drone":
            class_ = PanZoomRescueDrone

        ship = class_(config.win,
                x,
                y,
                size_x,
                size_y,
                pan_zoom_handler,
                f"{name}.png",
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
                outline_thickness=3,
                outline_threshold=127,
                is_spacestation=True if name == "spacestation" else False,
                rotation_smoothing=10)

        # bloody hack, otherwise position of some ships is wrong, no idea why !! ? :(
        ship.world_x = x
        ship.world_y = y
        return ship

    def create_ships_from_data(self, data):
        for key, value in data["ships"].items():
            self.create_ship(
                    data["ships"][key]["name"],
                    data["ships"][key]["world_x"],
                    data["ships"][key]["world_y"], config.app, data["ships"][key]["weapons"], data=data["ships"][key])

    def delete_ships(self):
        for i in sprite_groups.ships.sprites():
            i.__delete__(i)


ship_factory = ShipFactory()
