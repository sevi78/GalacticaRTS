from source.configuration import global_params
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups


def navigate_to(obj, **kwargs):
    panzoom = pan_zoom_handler

    if not sprite_groups.ships.sprites():
        return
    """
    sets the world offset to the objects position
    """

    x_offset = kwargs.get("x_offset", 0)
    y_offset = kwargs.get("y_offset", 0)

    # get ship to navigate to if not object is set
    ship = kwargs.get("ship", None)

    if not obj and ship:
        obj = sprite_groups.ships.sprites()[0]

        # select ship by reorder the list
        first_item = sprite_groups.ships.sprites()[0]
        sprite_groups.ships.add(first_item)
        sprite_groups.ships.change_layer(first_item, len(sprite_groups.ships) - 1)
        global_params.app.ship = obj
        obj.set_info_text()

        # set the new position
        panzoom.world_offset_x, panzoom.world_offset_y = panzoom.screen_2_world(obj.rect.centerx - panzoom.screen_width / 2, obj.rect.centery - panzoom.screen_height / 2)
        return

    panzoom.world_offset_x, panzoom.world_offset_y = panzoom.screen_2_world(obj.get_screen_x() + x_offset - panzoom.screen_width / 2, obj.get_screen_y() + y_offset - panzoom.screen_height / 2)


def navigate_to_position(x, y):
    panzoom = pan_zoom_handler
    screen_x, screen_y = panzoom.world_2_screen(x, y)
    panzoom.world_offset_x, panzoom.world_offset_y = panzoom.screen_2_world(screen_x - panzoom.screen_width / 2, screen_y - panzoom.screen_height / 2)
