import pygame

from source.configuration.game_config import config
from source.draw.dashed_line import draw_dashed_line
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.factories.building_factory import building_factory
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers.color_handler import get_average_color, colors, dim_color
from source.multimedia_library.images import get_image, scale_image_cached


class PlayerBuildingsOverview(EditorBase):
    """
    PlayerBuildingsOverview class represents a widget for displaying player buildings overview in a game.


    Attributes:
    - title_font_size: Font size for the title displayed in the widget.
    - h_icons_pos: Dictionary to store positions of icons.
    - player_index: Index of the player for which the overview is displayed.
    - max_chart_height: Maximum height of the chart.
    - resource_font_size: Font size for displaying resource information.
    - resource_buttons_built: Flag to track if resource buttons have been built.
    - widgets: List to store all widgets in the overview.

    Methods:
    - set_player_index(player_index_): Set the player index for the overview.
    - create_buttons(): Create buttons for different categories of buildings.
    - draw_bar_charts(): Draw bar charts for building categories.
    - draw_horizontal_bar_charts(): Draw horizontal bar charts for individual buildings.
    - listen(events): Listen for user interactions and handle them.
    - draw(): Draw the player buildings overview widget on the screen.
    """

    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)
        self.title_font_size = 18
        self.h_icons_pos = {}
        self.player_index = 0
        self.max_chart_height = 120
        self.resource_font_size = 10
        self.resource_font = pygame.sysfont.SysFont(config.font_name, self.resource_font_size)
        self.resource_buttons_built = False
        self.buildings = None
        self.title_text = config.app.players[self.player_index].name

        self.set_player_index(self.player_index)
        #  widgets
        self.widgets = []

        # hide initially
        self.hide()
        self.create_buttons()

    def set_player_index(self, player_index_):
        self.player_index = player_index_
        self.title_text = config.app.players[self.player_index].name
        self.buildings = config.app.players[self.player_index].get_all_buildings()

    # def set_buildings(self, planet: PanZoomPlanet):
    #     self.planet = planet
    #     self.buildings = planet.economy_agent.buildings
    #     self.title_text = planet.name

    def create_buttons(self):
        categories = building_factory.get_all_possible_categories()
        categories.remove("ship")
        categories.remove("weapons")

        # create categories icons
        x = 0
        y = self.world_y + self.max_chart_height + self.title_font_size + 10
        button_size = 25
        for i in categories:
            # create player image button
            image_name = f"{i}_25x25.png"

            icon = ImageButton(win=self.win,
                    x=self.world_x + x + self.text_spacing,
                    y=self.world_y + TOP_SPACING + y,
                    width=button_size,
                    height=button_size,
                    is_sub_widget=False,
                    parent=self,
                    image=scale_image_cached(get_image(image_name), (button_size, button_size)),
                    tooltip=i,
                    info_text="",
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    on_click=lambda: print("no function"),
                    name=i,
                    text_color=self.frame_color,
                    font_size=12,
                    text_h_align="center",
                    text_v_align="below_the_bottom",
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

    def draw_bar_charts(self):  # with sub levels
        player = config.app.players[self.player_index]
        all_buildings = self.buildings  # player.get_all_buildings()
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

    def draw_horizontal_bar_charts(self):
        """ this should draw bar charts for every building in buildings.json from the player
            the drawing should be below all other items
        """
        player = config.app.players[self.player_index]
        all_buildings = self.buildings  # player.get_all_buildings()
        all_buildings_amount = len(all_buildings)

        y = self.world_y + self.max_chart_height + 130  # Adjust y position to be below other drawings
        index_ = 0
        for button in self.buttons:
            if button.name in building_factory.get_all_possible_categories():
                button_size = 25

                # build resource buttons only once
                if not self.resource_buttons_built:
                    image_name = f"{button.name}_25x25.png"
                    icon = ImageButton(win=self.win,
                            x=self.world_x + self.text_spacing,
                            y=y,
                            width=button_size,
                            height=button_size,
                            is_sub_widget=False,
                            parent=self,
                            image=scale_image_cached(get_image(image_name), (button_size, button_size)),
                            tooltip=button.name,
                            info_text="",
                            frame_color=self.frame_color,
                            moveable=False,
                            include_text=True,
                            layer=self.layer,
                            on_click=lambda: print("no function"),
                            name=f"{button.name}_h__{index_}",
                            text_color=self.frame_color,
                            font_size=12,
                            text_h_align="center",
                            text_v_align="right_outside",
                            outline_thickness=0,
                            outline_threshold=1
                            )
                    self.buttons.append(icon)
                    self.widgets.append(icon)
                    self.h_icons_pos[index_] = icon.rect.center

                # adjust positions for lines
                else:
                    for i in self.buttons:
                        if "__" in i.name:
                            index = int(i.name[-1])
                            self.h_icons_pos[index] = i.rect.center

                # draw charts
                category = button.name
                possible_buildings = building_factory.get_building_names(category)
                best_buildings = []
                building_production_scores_sums = {key: 0 for key in building_factory.get_all_building_names()}

                for building in possible_buildings:
                    # get amount of this building
                    amount = all_buildings.count(building)

                    # calc width of chart
                    if amount > 0:
                        chart_width = 100 / all_buildings_amount * amount
                    else:
                        chart_width = 1

                    # draw rect
                    color = get_average_color(button.image, consider_alpha=True)
                    pygame.draw.rect(
                            self.win,
                            color,
                            pygame.Rect(
                                    self.world_x + button_size + self.text_spacing * 2,
                                    y + button.world_width / 2,
                                    chart_width,
                                    button.world_width / 3
                                    ),
                            0,
                            3
                            )

                    player = config.app.players[self.player_index]
                    best_buildings = []

                    all_planets = player.get_all_planets()
                    chart_width = 0
                    if all_planets:
                        building_production_scores_sums = {
                            planet.name: planet.economy_agent.building_production_scores_sums for planet in
                            player.get_all_planets()}

                        summed_building_production_scores_average = {}
                        min_value = 100.0
                        max_value = 0.0
                        lowest_production_score_keys = []

                        for planet_name, building_production_scores_sum in building_production_scores_sums.items():
                            for key, value in building_production_scores_sum.items():
                                if key == building:
                                    if value < min_value:
                                        min_value = value
                                    elif value > max_value:
                                        max_value = value

                        c = 0
                        for planet_name, building_production_scores_sum in building_production_scores_sums.items():
                            for key, value in building_production_scores_sum.items():
                                if key == building:
                                    chart_width += value
                                    c += 1
                                    if value == min_value:
                                        if not key in lowest_production_score_keys:
                                            lowest_production_score_keys.append(key)

                        chart_width /= c
                        best_buildings = lowest_production_score_keys
                        color = pygame.color.THECOLORS.get("red") if building in best_buildings else pygame.color.THECOLORS.get("orange")

                    # sum_score
                    pygame.draw.rect(
                            self.win,
                            color,
                            pygame.Rect(
                                    self.world_x + button_size + self.text_spacing * 2,
                                    y + button.world_width / 2,
                                    chart_width,
                                    button.world_width / 3
                                    ),
                            1,
                            3
                            )

                    # draw text
                    text = self.resource_font.render(f"{building}: {amount}", 0, self.frame_color)
                    self.win.blit(text, (self.world_x + button_size + self.text_spacing * 2, y))

                    # draw lines
                    start_pos = self.h_icons_pos[index_]
                    end_pos = (self.world_x + button_size + self.text_spacing * 2, y + self.resource_font_size / 2)
                    draw_dashed_line(self.win, dim_color(color, 160, 0, False), start_pos, end_pos, 1, 5)

                    y += button.world_width / 2 + 10  # Adjust y position for the next bar

            # set y for new rows(category)
            y += button.world_width / 2
            index_ += 1

        self.max_height = 800
        self.resource_buttons_built = True

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, self.title_font_size, f"buildings of {self.title_text}:")
            self.draw_bar_charts()
            self.draw_horizontal_bar_charts()
