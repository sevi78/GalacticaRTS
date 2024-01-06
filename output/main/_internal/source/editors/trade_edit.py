import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.checkbox import Checkbox
from source.gui.widgets.moving_image import MovingImage, SPECIAL_TEXT_COLOR
from source.gui.widgets.selector import Selector
from source.multimedia_library.images import get_image, resize_image
from source.utils import global_params


class TradeEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget=False, **kwargs)

        self.trader_image_pos = (0,0)
        self.player_image_pos = (0, 0)
        self.player = None
        self.trader = None

        self.image_size = 80
        self.player_image = self.scale_image("spaceship_30x30.png", (60, 60))
        self.trader_image = self.scale_image("ufo_60x21.png", (60, 60))
        self.arrow_image = self.flip_and_scale_image("arrow-left.png", (60, 60))

        self.resources = ["minerals", "food", "water", "technology", "energy"]
        self.trader_resources = dict.fromkeys(self.resources, 0)
        self.player_resources = dict.fromkeys(self.resources, 0)

        self.value_list = list(range(-1000, 1000))
        self.selectors = []

        self.widgets = []

        self.create_widgets()

        # hide initially
        self.hide()

    def scale_image(self, image_name, size):
        return pygame.transform.scale(get_image(image_name), size)

    def flip_and_scale_image(self, image_name, size):
        return pygame.transform.flip(self.scale_image(image_name, size), flip_x=1, flip_y=1)

    def create_widgets(self):
        self.create_selectors()
        self.create_close_button()
        self.create_buttons()
        self.set_selector_current_value()

    def create_buttons(self):
        button_size = 32
        agree_button = ImageButton(win=self.win,
            x=self.get_screen_x() + self.get_screen_width() / 2 + button_size / 2,
            y=self.max_height + button_size / 2,
            width=button_size,
            height=button_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("thumps_up.png"), (button_size, button_size)),
            tooltip="agree!",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=self.layer,
            onClick=lambda: self.agree(),
            name="agree_button"
            )

        agree_button.hide()

        self.buttons.append(agree_button)
        self.widgets.append(agree_button)

    def create_selectors(self):
        x = self.world_x + self.world_width * 0.6
        y = 130

        for key, value in self.player_resources.items():
            setattr(self, f"selector_player_{key}", Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
                100, {"list_name": key + "_list", "list": self.value_list}, self, FONT_SIZE, repeat_clicks=True))

            button_size = 32
            checkbox = Checkbox(
                self.win, self.get_screen_x() + self.trader_image.get_width() * 4.7, self.world_y + y, 30, 30, isSubWidget=False,
                color=self.frame_color,
                key=key, tooltip=key, onClick=lambda: print("OKOKOK"), layer=9, parent=self)

            self.checkboxes.append(checkbox)
            self.widgets.append(checkbox)
            y += self.spacing_y

        self.max_height = y + ARROW_SIZE

    def draw_images(self):
        self.trader_image_pos = (
        self.get_screen_x() + self.trader_image.get_width() / 3, self.get_screen_y() + self.get_screen_height() / 3.5)
        self.player_image_pos = (
        self.get_screen_x() + self.trader_image.get_width() * 2.25, self.get_screen_y() + self.get_screen_height() / 4)

        self.win.blit(self.trader_image, self.trader_image_pos)
        self.win.blit(self.arrow_image, (
        self.get_screen_x() + self.arrow_image.get_width() * 2, self.get_screen_y() + self.get_screen_height() / 4))
        self.win.blit(self.player_image, self.player_image_pos)

    def setup_trader(self, player, trader):
        self.trader = trader
        self.player = player
        self.set_images()

        for selector in self.selectors:
            for resource in self.resources:
                if selector.key == resource:
                    player_max_resource = getattr(self.player, resource + "_max")
                    trader_max_resource = getattr(self.trader, resource + "_max")
                    selector.list = list(range(-player_max_resource, trader_max_resource))
                    selector.text_adds = f"/{getattr(self.player, resource)}"

        self.player.set_info_text()

    def set_images(self):
        self.player_image = resize_image(self.player.image_raw, (self.image_size, self.image_size))
        self.trader_image = resize_image(self.trader.image_raw, (self.image_size, self.image_size))

    def set_selector_current_value(self):
        for selector in self.selectors:
            selector.set_current_value(0)

    def selector_callback(self, key, value):
        self.get_checkbox_values()
        self.set_resources(key, value)

    def set_resources(self, key, value):
        if key in self.checkbox_values:
            self.player_resources[key] = value
            self.trader_resources[key] = -value
        else:
            self.player_resources[key] = 0
            self.trader_resources[key] = 0

    def get_checkbox_values(self):
        self.checkbox_values = [checkbox.key for checkbox in self.checkboxes if checkbox.checked]
        for selector in self.selectors:
            self.set_resources(selector.key, selector.current_value)

    def draw(self):
        #pygame.draw.circle(self.win, self.frame_color, self.player_image.get_rect().center, 20,2)
        pygame.draw.circle(self.win, self.frame_color, self.player_image_pos, 20, 2)
        #self.set_screen_position()
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_images()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Trader:")

    def agree(self):

        for resource in self.resources:
            player_resource = getattr(self.player, resource)
            setattr(self.player, resource, player_resource + self.player_resources[resource])
            setattr(self.trader, resource, player_resource - self.player_resources[resource])

            MovingImage(
                win=self.win,
                x=self.player_image.get_rect().x,
                y=self.player_image.get_rect().y,
                width=25,
                height=25,
                image=get_image(f"{resource}_25x25.png"),
                lifetime=1,
                velocity=(-0.1, 0.1),
                text=str(self.trader_resources[resource]),
                text_color=SPECIAL_TEXT_COLOR,
                fontname="georgiaproblack",
                loops= 1,
                parent= self.trader_image_pos,
                target= self.player_image_pos)


        self.player.set_info_text()
        self.parent.info_panel.draw()
