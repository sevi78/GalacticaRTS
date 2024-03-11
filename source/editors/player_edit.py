import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.widgets.inputbox import InputBox
from source.handlers.file_handler import write_file
from source.handlers.player_handler import player_handler

ARROW_SIZE = 20
FONT_SIZE = int(ARROW_SIZE * .8)


class PlayerEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.data = player_handler.get_players()

        #  widgets
        self.widgets = []
        self.create_close_button()
        self.create_inputboxes()
        self.create_save_button(lambda: self.save_settings(), "save settings")

        # hide initially
        self.hide()

    def create_inputboxes(self):
        h = 18
        x = 0
        y = TOP_SPACING
        spacing_x = 80
        for player in self.data.keys():
            x += spacing_x
            for key, value in self.data[player].items():
                if not key.startswith("production_"):
                    text = f"{value}"
                    if "production_" + key in self.data[player].keys():
                        text += f"/{self.data[player]['production_' + key]}"

                    self.widgets.append(
                        InputBox(
                            self.win,
                            self.world_x + x,
                            self.world_y + TOP_SPACING + y,
                            self.spacing_x * 2,
                            h,
                            text=f"{key}:",
                            parent=self,
                            key=key,
                            draw_frame=False,
                            player=player)
                        )

                    self.widgets.append(
                        InputBox(
                            self.win,
                            self.world_x + x,
                            self.world_y + TOP_SPACING + y + h,
                            self.spacing_x * 2,
                            h,
                            text=f"{text}",
                            parent=self,
                            key=key,
                            draw_frame=False,
                            player=player)
                        )
                    x += spacing_x
            x = 0
            y += h * 3
        self.max_height = self.world_y + self.world_height + y

    def save_settings(self):
        data = {}
        for i in self.selectors:
            data[i.key] = i.current_value
        write_file("players.json", "config", data)

    def update_inputboxes(self):
        for i in self.widgets:
            if i.__class__.__name__ == "InputBox":
                if "player" in i.kwargs:
                    if "/" in i.text:
                        player_index = int(i.kwargs["player"].split("_")[1])
                        i.set_text(f"{int(player_handler.get_current_stock(player_index)[i.key])}"
                                   f"/{int(player_handler.get_current_production(player_index)[i.key])}")
                    # set colors
                    if i.text in pygame.color.THECOLORS:
                        i.set_text(f"{i.text}", color= pygame.color.THECOLORS[i.text])
    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)
            self.update_inputboxes()

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Players:")
