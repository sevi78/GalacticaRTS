from source.configuration.game_config import config
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship import PanZoomShip


def navigate_to(obj, **kwargs):  # should not be used !! use navigate_to_position, use for planets
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
    index_ = kwargs.get("index_", None)

    if not obj and ship:
        if index_:
            obj = sprite_groups.ships.sprites()[index_]
        else:
            obj = sprite_groups.ships.sprites()[0]

        # select ship by reorder the list
        first_item = sprite_groups.ships.sprites()[0]
        sprite_groups.ships.add(first_item)
        sprite_groups.ships.change_layer(first_item, len(sprite_groups.ships) - 1)
        config.app.ship = obj
        obj.set_info_text()

        # set the new position
        panzoom.world_offset_x, panzoom.world_offset_y = panzoom.screen_2_world(obj.rect.centerx - panzoom.screen_width / 2, obj.rect.centery - panzoom.screen_height / 2)
        return

    panzoom.world_offset_x, panzoom.world_offset_y = panzoom.screen_2_world(obj.get_screen_x() + x_offset - panzoom.screen_width / 2, obj.get_screen_y() + y_offset - panzoom.screen_height / 2)


def navigate_to_position(x, y):  # use for ships
    """
        use obj.world_x, obj.world_y  as input for navigation
    """

    panzoom = pan_zoom_handler
    screen_x, screen_y = panzoom.world_2_screen(x, y)
    panzoom.world_offset_x, panzoom.world_offset_y = panzoom.screen_2_world(screen_x - panzoom.screen_width / 2, screen_y - panzoom.screen_height / 2)


def navigate_to_game_object_by_index(self):
    """
    use obj.world_x, obj.world_y  as input for navigation
    """

    if self.offset_index < len(self.widgets):
        obj = self.widgets[self.offset_index].obj
        if obj:
            if obj.__class__.__name__ == 'PanZoomPlanet':
                navigate_to(obj)
                # select
                config.app.set_selected_planet(obj)

            if isinstance(obj, PanZoomShip):
                navigate_to_position(obj.world_x, obj.world_y)
                # select
                config.app.ship = obj
                selected = [i.selected for i in sprite_groups.ships.sprites() if not i == obj]
