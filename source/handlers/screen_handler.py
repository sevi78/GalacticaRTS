import os

import pygame
from pygame import Surface, SurfaceType

from source.configuration.game_config import config


class ScreenHandler:
    def __init__(
            self, width: int = 1920, height: int = 1080, tiles: int = 2, tile_index: int = 0, alignment: int = 0
            ) -> None:

        self.width = width
        self.height = height
        self.tiles = tiles
        self.tile_index = tile_index
        self.alignment = alignment

    def set_screen_tiled(
            self, width: int = 1920, height: int = 1080, tiles: int = 2, tile_index: int = 0, alignment: int = 0
            ) -> Surface | SurfaceType | None:

        if hasattr(config.app, "game_client"):
            config.app.game_client.send_message(
                    {
                        "f": "set_screen_tiled",
                        "width": width,
                        "height": height,
                        "tiles": tiles,
                        "tile_index": None,
                        "alignment": alignment
                        })

            return None
        else:
            self.handle_set_screen_tiled(width, height, tiles, tile_index, alignment)

    def handle_set_screen_tiled(
            self, width: int = 1920, height: int = 1080, tiles: int = 2, tile_index: int = 0, alignment: int = 0
            ) -> Surface | SurfaceType:

        self.width = width
        self.height = height
        self.tiles = tiles
        if tile_index is None:
            if config.app.game_client.id is not None:
                self.tile_index = config.app.game_client.id
        self.alignment = alignment

        display = pygame.display.get_num_displays() - 1

        # vertical
        if alignment == 1:  # Vertical alignment
            new_height = self.height // self.tiles
            new_width = self.width
            x = 0
            y = self.tile_index * new_height

        # Horizontal alignment (default)
        else:
            new_width = self.width // self.tiles
            new_height = self.height
            x = self.tile_index * new_width
            y = 0

        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
        screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE, display=display)
        pygame.display.set_caption("Galactica RTS")

        return screen


screen_handler = ScreenHandler()
