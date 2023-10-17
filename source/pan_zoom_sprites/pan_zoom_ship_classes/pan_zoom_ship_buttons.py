from source.gui.widgets.buttons.image_button import ImageButton
from source.utils import global_params
from source.multimedia_library.images import get_image


class PanZoomShipButtons:
    """
    """

    def __init__(self):
        self.visible = False
        self.speed_up_button = ImageButton(global_params.win, self.get_screen_x(), self.get_screen_y() + self.get_screen_height(), 32, 32,
            isSubWidget=False, image=get_image("speed_up.png"),
            onClick=lambda: print("Ok"))
        self.radius_button = ImageButton(global_params.win, self.get_screen_x() + self.get_screen_width(), self.get_screen_y() + self.get_screen_height(),
            32, 32, isSubWidget=False, image=get_image("radius.png"),
            onClick=lambda: print("Ok"))

    def reposition_buttons(self):
        self.spacing = 15
        self.speed_up_button.set_position((
            self.get_screen_x() + self.get_screen_width() + self.spacing,
            self.get_screen_y() + self.get_screen_height()))
        self.radius_button.set_position((self.get_screen_x() + self.get_screen_width() + self.spacing,
                                         self.get_screen_y() + self.get_screen_height() - self.spacing * 3))

    def hide_buttons(self):
        self.speed_up_button.hide()
        self.radius_button.hide()

    def show_buttons(self):
        return
        self.speed_up_button.show()
        self.radius_button.show()
