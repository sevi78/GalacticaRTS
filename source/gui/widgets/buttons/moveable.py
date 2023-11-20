from source.utils import global_params


class Moveable:
    """this class is used to get the correct position of the buttons attached to the planets
    """

    def __init__(self, x, y, width, height, kwargs):
        self.ui_parent = kwargs.get("ui_parent", None)
        self.ui_parent_offset_x = 0
        self.ui_parent_offset_y = 0
        self.set_ui_parent_offset(x, y)

    def set_ui_parent_offset(self, x, y):
        if self.ui_parent:
            try:
                self.ui_parent_offset_x = self.ui_parent.get_screen_x() - x
                self.ui_parent_offset_y = self.ui_parent.get_screen_y() - y
            except AttributeError:
                self.ui_parent_offset_x = self.ui_parent.get_rect().x - x
                self.ui_parent_offset_y = self.ui_parent.get_rect().y - y

    def set_pos_centered_on_top(self):
        h_offset = 0
        if not global_params.planet_button_display_on_panel:
            len_buttons = len(self.ui_parent.planet_button_array.getButtons()) - len(self.ui_parent.overview_buttons)

        else:
            len_buttons = len(self.ui_parent.overview_buttons)

        if self in self.ui_parent.overview_buttons:
            h_offset = 4

        self.set_position((self.ui_parent.center[0] - self.ui_parent_offset_x - (
                len_buttons * self.get_screen_width() / 2), self.ui_parent.center[
                               1] + h_offset - self.ui_parent_offset_y - self.ui_parent.get_screen_height() / 2))

    def update_position(self):

        """
        this sets the position . and also to set building buttons of planet to its panel-position

        why the hell: spacing_x = global_params.app.building_panel.spacing_x, why refer to building pane ???
        """
        # set planet_button_array to panel
        if hasattr(self, "ui_parent"):
            if self.ui_parent:
                if global_params.planet_button_display_on_panel:
                    if self.parent == global_params.app.selected_planet:
                        x = global_params.app.building_panel.surface_rect.x
                        y = global_params.app.building_panel.max_height + self.get_screen_height() * 6
                        spacing_x = global_params.app.building_panel.spacing_x
                        self.set_position((x - self.ui_parent_offset_x + spacing_x / 2, y - self.ui_parent_offset_y))

        else:
            pass
            #print ("Button.movable.update_position: no ui_parent!!", self, self.parent, self.name)

            #     else:
            #         self.set_pos_centered_on_top()
            #
            # # set planet_button_array to planet
            # else:
            #     self.set_pos_centered_on_top()
