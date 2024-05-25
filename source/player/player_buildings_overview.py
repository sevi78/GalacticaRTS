import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.factories.building_factory import building_factory
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers.color_handler import get_average_color, colors
from source.multimedia_library.images import get_image


class PlayerBuildingsOverview(EditorBase):
    """

    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.player_index = 0
        self.max_chart_height = 200

        #  widgets
        self.widgets = []

        # hide initially
        self.hide()
        self.create_buttons()

    def set_player_index(self, player_index_):
        self.player_index = player_index_

    def create_buttons(self):
        categories = building_factory.get_all_possible_categories()
        categories.remove("ship")
        categories.remove("weapons")

        # create categories icons
        x = 0
        y = self.world_y + self.max_chart_height
        button_size = 25
        for i in categories:
            # create player image button
            image_name = f"{i}_25x25.png"

            icon = ImageButton(win=self.win,
                    x=self.world_x + x + self.text_spacing,
                    y=self.world_y + TOP_SPACING + y,
                    width=button_size,
                    height=button_size,
                    isSubWidget=False,
                    parent=self,
                    image=pygame.transform.scale(get_image(image_name), (button_size, button_size)),
                    tooltip=i,
                    info_text="",
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    onClick=lambda: print("no function"),
                    name=i,
                    textColour=self.frame_color,
                    font_size=12,
                    textHAlign="center",
                    textVAlign="below_the_bottom",
                    outline_thickness=0,
                    outline_threshold=1
                    )

            self.buttons.append(icon)
            self.widgets.append(icon)
            icon.hide()
            x += button_size
        y -= 60

        self.max_height = y + TOP_SPACING + self.text_spacing * 3
        self.screen_width = x + (self.text_spacing * 2)
        self.draw_frame()
        self.create_close_button(x=self.rect.topright[
                                       0] - self.text_spacing - button_size / 2, y=self.world_y + TOP_SPACING)

    def draw_bar_charts__(self):  # only all levels of building combined
        player = config.app.players[self.player_index]
        all_buildings = player.get_all_buildings()
        all_buildings_amount = len(all_buildings)

        for button in self.buttons:
            if button.name in building_factory.get_all_possible_categories():
                category = button.name
                possible_buildings = building_factory.get_building_names(category)

                # get amount of building fitting to the category
                amount = 0
                for _ in possible_buildings:
                    if _ in all_buildings:
                        amount += all_buildings.count(_)

                # calc height of chart
                if amount > 0:
                    chart_height = 100 / all_buildings_amount * amount
                else:
                    chart_height = 1

                # draw rect
                pygame.draw.rect(
                        self.win,
                        get_average_color(button.image, consider_alpha=True),
                        pygame.Rect(
                                button.world_x + button.world_width / 4,
                                button.world_y - chart_height - button.world_width / 4,
                                button.world_width / 2,
                                chart_height))

                # draw text
                button.set_text(f"{amount}")

    def draw_bar_charts(self):  # with sub levels
        player = config.app.players[self.player_index]
        all_buildings = player.get_all_buildings()
        all_buildings_amount = len(all_buildings)

        for button in self.buttons:
            if button.name in building_factory.get_all_possible_categories():
                category = button.name
                possible_buildings = building_factory.get_building_names(category)
                # get amount of building fitting to the category
                # -1 == all, others based on index (building level)
                amounts = {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

                # check if building in possible_buildings and all buildings
                for _ in possible_buildings:
                    if _ in all_buildings:
                        # add to amounts "all"
                        amounts[-1] += all_buildings.count(_)

                        # add to amounts by index
                        for index in range(len(possible_buildings)):
                            if _ == possible_buildings[index]:
                                amounts[index] += all_buildings.count(_)

                # calc height of chart
                if amounts[-1] > 0:
                    chart_height = 100 / all_buildings_amount * amounts[-1]
                else:
                    chart_height = 1

                # draw rect
                pygame.draw.rect(
                        self.win,
                        get_average_color(button.image, consider_alpha=True),
                        pygame.Rect(
                                button.world_x + button.world_width / 4,
                                button.world_y - chart_height - button.world_width / 4,
                                button.world_width / 2,
                                chart_height), 0, 5)

                # draw text
                button.set_text(f"{amounts[-1]}")

                # draw sub charts
                for sub_index in range(0, len(amounts) - 1):
                    # calc height of chart
                    if amounts[-1] > 0:
                        if amounts[sub_index] > 0:
                            sub_chart_height = chart_height / amounts[-1] * amounts[sub_index]
                        else:
                            sub_chart_height = 1

                        # draw rect
                        pygame.draw.rect(
                                self.win,
                                colors.ui_darker,
                                pygame.Rect(
                                        button.world_x + button.world_width / 4 + (sub_index * button.world_width / 6),
                                        button.world_y - sub_chart_height - button.world_width / 4,
                                        (button.world_width / 6) - 1,
                                        sub_chart_height - 1), 1, 3)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 18, f"buildings of {config.app.players[self.player_index].name}:")
            self.draw_bar_charts()
