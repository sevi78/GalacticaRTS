import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.multimedia_library.images import get_image

BUTTON_SIZE = 25


class DeclareWarEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        # vars
        self.enemy_index = None
        self.player_index = None
        self.text = ""

        #  widgets
        self.widgets = []

        # create widgets
        self.create_buttons()

        # hide initially
        self.hide()

    def create_buttons(self) -> None:
        agree_button = ImageButton(win=self.win,
            x=self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE * 3,
            y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
            width=BUTTON_SIZE,
            height=BUTTON_SIZE,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("thumps_up.png"), (BUTTON_SIZE, BUTTON_SIZE)),
            image_raw=pygame.transform.scale(
                get_image("thumps_up.png"), (BUTTON_SIZE, BUTTON_SIZE)),
            tooltip="agree!",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=9,
            onClick=lambda: self.agree(),
            name="agree_button"
            )

        self.buttons.append(agree_button)
        self.widgets.append(agree_button)

        decline_button = ImageButton(win=self.win,
            x=self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE - BUTTON_SIZE / 2,
            y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
            width=BUTTON_SIZE,
            height=BUTTON_SIZE,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.flip(
                pygame.transform.scale(get_image("thumps_upred.png"), (BUTTON_SIZE, BUTTON_SIZE)), 1, 1),
            image_raw=pygame.transform.flip(
                pygame.transform.scale(get_image("thumps_upred.png"), (BUTTON_SIZE, BUTTON_SIZE)), 1, 1),
            tooltip="decline!",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=9,
            onClick=lambda: self.decline(),
            name="decline_button"
            )

        self.buttons.append(decline_button)
        self.widgets.append(decline_button)

        self.max_height = BUTTON_SIZE * 2
        for i in self.buttons:
            i.hide()

    def set_enemy_and_player(self, enemy_index: int, player_index: int) -> None:
        self.player_index = player_index
        self.enemy_index = enemy_index
        self.text = f"Do you want declare war to {config.app.players[self.enemy_index].name}?"

    def agree(self) -> None:
        player_enemies = config.app.players[self.player_index].enemies
        enemy_enemies = config.app.players[self.enemy_index].enemies

        if not self.enemy_index in player_enemies:
            player_enemies.append(self.enemy_index)
            enemy_enemies.append(self.player_index)

        print(f"declare_war_edit: agree: player.enemies: {player_enemies}, enemy.enemies: {enemy_enemies} ")
        self.hide()

    def decline(self):
        player_enemies = config.app.players[self.player_index].enemies
        enemy_enemies = config.app.players[self.enemy_index].enemies

        if self.enemy_index in player_enemies:
            player_enemies.remove(self.enemy_index)
            enemy_enemies.remove(self.player_index)

        print(f"declare_war_edit: decline: player.enemies: {player_enemies}, enemy.enemies: {enemy_enemies} ")
        self.hide()

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 16, self.text)
