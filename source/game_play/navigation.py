from source.configuration.game_config import config
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups


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
    panzoom = pan_zoom_handler
    screen_x, screen_y = panzoom.world_2_screen(x, y)
    panzoom.world_offset_x, panzoom.world_offset_y = panzoom.screen_2_world(screen_x - panzoom.screen_width / 2, screen_y - panzoom.screen_height / 2)


def navigate_to_ship_by_offset_index(self):
    # navigate to ship
    index = self.offset_index + 1
    if index < len(self.widgets):
        if self.widgets[index].obj:
            navigate_to_position(
                self.widgets[index].obj.screen_x, self.widgets[self.offset_index].obj.screen_y)


def navigate_to_planet_by_offset_index(self, **kwargs):
    select = kwargs.get('select', True)

    if self.offset_index < len(self.widgets):
        if self.widgets[self.offset_index].obj:
            navigate_to(self.widgets[self.offset_index].obj)
            if select:
                config.app.set_selected_planet(self.widgets[self.offset_index].obj)
