import time

import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers.diplomacy_handler import diplomacy_handler
from source.multimedia_library.images import get_image, outline_image

BUTTON_SIZE = 25
IMAGE_SIZE = 45


class DiplomacyEdit(EditorBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)
        # vars
        # self.opening_time = time.time()
        self.text = ""
        self.enemy_image = None

        #  widgets
        self.widgets = []

        # create widgets
        self.create_buttons()

        # hide initially
        self.opening_time = time.time()
        self.hide()

    def create_buttons(self) -> None:
        agree_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE * 3,
                y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("peace_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                image_raw=pygame.transform.scale(
                        get_image("peace_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="lets be friends!",
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=10,
                on_click=lambda: diplomacy_handler.update_diplomacy_status("peace"),
                name="agree_button"
                )

        self.buttons.append(agree_button)
        self.widgets.append(agree_button)

        decline_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE - BUTTON_SIZE / 2,
                y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(get_image("war_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                image_raw=pygame.transform.scale(get_image("war_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="f@ck iu!!!",
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=10,
                on_click=lambda: diplomacy_handler.update_diplomacy_status("war"),
                name="decline_button"
                )

        self.buttons.append(decline_button)
        self.widgets.append(decline_button)

        self.max_height = BUTTON_SIZE * 2
        for i in self.buttons:
            i.hide()

    def set_enemy_image(self):
        """
        sets the image and outlines it based on war or peace
        """
        self.enemy_image = pygame.transform.scale(get_image(
                config.app.players[diplomacy_handler.enemy_index].image_name), (IMAGE_SIZE, IMAGE_SIZE))

        if diplomacy_handler.is_in_peace(diplomacy_handler.player_index, diplomacy_handler.enemy_index):
            self.enemy_image = outline_image(self.enemy_image, color=pygame.color.THECOLORS.get("green"), threshold=127, thickness=0)
        else:
            self.enemy_image = outline_image(self.enemy_image, color=pygame.color.THECOLORS.get("red"), threshold=127, thickness=0)

    def open(self, enemy_index: int, player_index: int) -> None:
        if enemy_index == -1:
            return

        diplomacy_handler.set_enemy_and_player(enemy_index, player_index)
        # self.set_visible()
        self.show()
        self.opening_time = time.time()

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

            if not self.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if self.opening_time < time.time() - 0.3:
                        self.hide()

    def draw_enemy_image(self):
        if self.enemy_image:
            self.win.blit(self.enemy_image, (self.world_x + self.get_screen_width() * 0.65, self.world_y + TOP_SPACING))

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_enemy_image()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 16, self.text)
