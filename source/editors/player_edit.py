import pygame

from source.configuration.game_config import config
from source.editors.auto_economy_edit import AutoEconomyEdit
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.inputbox import InputBox
from source.gui.widgets.score_plotter import ScorePlotter
from source.handlers.diplomacy_handler import diplomacy_handler
from source.handlers.image_handler import overblit_button_image
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.player_handler import player_handler
from source.multimedia_library.images import get_image
from source.text.text_formatter import format_number

DIPLOMACY_BUTTON_SIZE = 25
PLOTTER_SURFACE_HEIGHT = 500
PLOTTER_SURFACE_GAP = 10
SPACING_X = 90


class PlayerEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        self.data = player_handler.get_players()

        # images
        self.peace_image = pygame.transform.scale(get_image("peace_icon.png"), (
            DIPLOMACY_BUTTON_SIZE, DIPLOMACY_BUTTON_SIZE))
        self.war_image = pygame.transform.scale(get_image("war_icon.png"), (
            DIPLOMACY_BUTTON_SIZE, DIPLOMACY_BUTTON_SIZE))

        #  widgets
        self.widgets = []
        self.create_close_button()
        self.create_inputboxes()

        # max_height
        self.max_height_raw = 960
        self.max_height = self.max_height_raw
        self.max_height_if_editors_closed = 460

        # score plotter
        self.score_plotter = None
        self.score_plotter = ScorePlotter(
                self.win,
                self.world_x + PLOTTER_SURFACE_GAP,
                self.world_y + 400,
                self.rect.width - PLOTTER_SURFACE_GAP,
                PLOTTER_SURFACE_HEIGHT,
                parent=self,
                save=False,
                drag_enabled=False)
        self.show_plotter = True

        # auto_economy_edit
        self.auto_economy_edit = AutoEconomyEdit(
                pygame.display.get_surface(),
                self.world_x,
                self.world_y + self.world_y + 400 - TOP_SPACING,
                900, PLOTTER_SURFACE_HEIGHT,
                parent=self,
                obj=None,
                layer=9,
                ignore_other_editors=True,
                save=False,
                drag_enabled=False
                )

        self.show_auto_economy_edit = True

        # dirty hack to make attached editors hide at startup
        self.enable_plotter()
        self.enable_auto_economy_edit(0)

        # hide initially
        self.hide()

    def set_max_height(self):
        """ sets the editors max_height based on the enabled sub editors, if any of them is enabled or not"""
        if self.score_plotter.isEnabled() or self.auto_economy_edit.isEnabled():
            self.max_height = self.max_height_raw
        else:
            self.max_height = self.max_height_if_editors_closed

    def enable_plotter(self):
        self.show_plotter = not self.show_plotter

        if self.show_plotter:
            self.score_plotter.enable()
            self.score_plotter.show()
        else:
            self.score_plotter.disable()
            self.score_plotter.hide()

        self.set_max_height()

    def enable_auto_economy_edit(self, player_id: int):
        self.show_auto_economy_edit = not self.show_auto_economy_edit
        self.auto_economy_edit.player_id = player_id
        self.auto_economy_edit.set_player(player_id)

        if self.show_auto_economy_edit:
            self.auto_economy_edit.enable()
            self.auto_economy_edit.show()
        else:
            self.auto_economy_edit.disable()
            self.auto_economy_edit.hide()

        self.set_max_height()

    def create_variable_boxes(self, h, key, ordered_data, player, value, x, y):
        text = f"{value}"
        if "production_" + key in ordered_data[player].keys():
            text += f"/{ordered_data[player]['production_' + key]}"
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

    def create_resource_images(self, key, resources, x):
        if key in resources:
            image_name_resource = key + "_25x25.png"
            button_size_resource = 25
            icon = ImageButton(win=self.win,
                    x=self.world_x + x,
                    y=self.world_y + TOP_SPACING + 20,
                    width=button_size_resource,
                    height=button_size_resource,
                    isSubWidget=False,
                    parent=self,
                    image=pygame.transform.scale(get_image(image_name_resource), (
                        button_size_resource, button_size_resource)),
                    tooltip=key,
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    onClick=lambda: print("no function"),
                    name=key,
                    textColour=self.frame_color,
                    font_size=12,
                    info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                    textHAlign="right_outside",
                    outline_thickness=0,
                    outline_threshold=1
                    )

            self.buttons.append(icon)
            self.widgets.append(icon)

    def create_inputboxes(self):
        h = 18
        x = 0
        y = TOP_SPACING
        spacing_x = 90

        # Define the desired order of keys including 'name' and 'color'
        order = ["name", "color", "water", "energy", "food", "minerals", "technology", "population"]
        production_order = ["production_" + key for key in order if key not in ["name", "color"]]
        all_keys = order + production_order

        # Create a new dictionary with ordered keys for each player
        ordered_data = {
            player: {key: self.data[player][key] for key in all_keys if key in self.data[player]}
            for player in self.data
            }

        # define filter
        resources = ["water", "energy", "food", "minerals", "technology", "population"]

        resource_images_built = False
        planet_icon_built = False
        buildings_icon_built = False
        ships_icon_built = False
        score_icon_built = False

        # create items
        for player in ordered_data.keys():
            player_index = int(player.split("_")[1])

            # create player image button
            image_name = player_handler.player_image_names[player]
            button_size = 40
            icon = ImageButton(win=self.win,
                    x=self.world_x + x + int(spacing_x / 6),
                    y=self.world_y + TOP_SPACING + y,
                    width=button_size,
                    height=button_size,
                    isSubWidget=False,
                    parent=self,
                    image=pygame.transform.scale(get_image(image_name), (button_size, button_size)),
                    tooltip=player,
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    onClick=lambda player_index_=player_index: self.enable_auto_economy_edit(player_index_),
                    name=player,
                    textColour=self.frame_color,
                    font_size=12,
                    info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                    textHAlign="right_outside",
                    outline_thickness=0,
                    outline_threshold=1
                    )

            self.buttons.append(icon)
            self.widgets.append(icon)
            x += button_size + int(spacing_x / 6)

            # diplomacy
            peace = diplomacy_handler.is_in_peace(player_index, config.player)
            if peace:
                diplomacy_image = pygame.transform.scale(get_image("peace_icon.png"), (
                    DIPLOMACY_BUTTON_SIZE, DIPLOMACY_BUTTON_SIZE))
            else:
                diplomacy_image = pygame.transform.scale(get_image("war_icon.png"), (
                    DIPLOMACY_BUTTON_SIZE, DIPLOMACY_BUTTON_SIZE))

            icon = ImageButton(win=self.win,
                    x=self.world_x + x + int(spacing_x / 6),
                    y=self.world_y + TOP_SPACING + y + DIPLOMACY_BUTTON_SIZE / 3,
                    width=DIPLOMACY_BUTTON_SIZE,
                    height=DIPLOMACY_BUTTON_SIZE,
                    isSubWidget=False,
                    parent=self,
                    image=diplomacy_image,
                    tooltip="set diplomacy",
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    onClick=lambda
                        player_index_=player_index: config.app.diplomacy_edit.open(player_index_, config.player),
                    name=f"diplomacy{player_index}",
                    textColour=self.frame_color,
                    font_size=12,
                    info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                    textHAlign="right_outside",
                    outline_thickness=0,
                    outline_threshold=1
                    )

            self.buttons.append(icon)
            self.widgets.append(icon)

            # set resource images
            x += DIPLOMACY_BUTTON_SIZE + int(spacing_x / 3)
            tmp_x = x
            if not resource_images_built:
                for key, value in ordered_data[player].items():
                    if not key.startswith("production_"):
                        # images
                        self.create_resource_images(key, resources, x)
                        x += spacing_x
            resource_images_built = True

            # set data boxes from file
            x = tmp_x
            for key, value in ordered_data[player].items():
                if not key.startswith("production_"):
                    # input boxes
                    self.create_variable_boxes(h, key, ordered_data, player, value, x, y)
                    x += spacing_x

            # set others
            button_size = 25
            # planets
            self.widgets.append(
                    InputBox(
                            self.win,
                            self.world_x + x,
                            self.world_y + TOP_SPACING + y,
                            self.spacing_x * 2,
                            h,
                            text=f"{'planets:'}",
                            parent=self,
                            key="planets",
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
                            text=f"{len([i for i in sprite_groups.planets.sprites() if i.owner == player_index])}",
                            parent=self,
                            key="planets_count",
                            draw_frame=False,
                            player=player)
                    )
            if not planet_icon_built:
                icon = ImageButton(win=self.win,
                        x=self.world_x + x,
                        y=self.world_y + TOP_SPACING + 20,
                        width=button_size,
                        height=button_size,
                        isSubWidget=False,
                        parent=self,
                        image=pygame.transform.scale(get_image("Zeta Bentauri_60x60.png"), (button_size, button_size)),
                        tooltip="planet_icon",
                        frame_color=self.frame_color,
                        moveable=False,
                        include_text=True,
                        layer=self.layer,
                        onClick=lambda: print("no function"),
                        name="planet_icon",
                        textColour=self.frame_color,
                        font_size=12,
                        info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                        textHAlign="right_outside",
                        outline_thickness=0,
                        outline_threshold=1
                        )

                self.buttons.append(icon)
                self.widgets.append(icon)
                planet_icon_built = True

            x += spacing_x

            # buildings
            self.widgets.append(
                    InputBox(
                            self.win,
                            self.world_x + x,
                            self.world_y + TOP_SPACING + y,
                            self.spacing_x * 2,
                            h,
                            text=f"{'buildings:'}",
                            parent=self,
                            key="buildings",
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
                            text="",
                            parent=self,
                            key="buildings_count",
                            draw_frame=False,
                            player=player)
                    )
            if not buildings_icon_built:
                icon = ImageButton(win=self.win,
                        x=self.world_x + x,
                        y=self.world_y + TOP_SPACING + 20,
                        width=button_size,
                        height=button_size,
                        isSubWidget=False,
                        parent=self,
                        image=pygame.transform.scale(get_image("buildings_icon.png"), (button_size, button_size)),
                        tooltip="buildings_icon",
                        frame_color=self.frame_color,
                        moveable=False,
                        include_text=True,
                        layer=self.layer,
                        onClick=lambda: print("no function"),
                        name="buildings_icon",
                        textColour=self.frame_color,
                        font_size=12,
                        info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                        textHAlign="right_outside",
                        outline_thickness=0,
                        outline_threshold=1
                        )

                self.buttons.append(icon)
                self.widgets.append(icon)
                buildings_icon_built = True
            x += spacing_x

            # ships
            self.widgets.append(
                    InputBox(
                            self.win,
                            self.world_x + x,
                            self.world_y + TOP_SPACING + y,
                            self.spacing_x * 2,
                            h,
                            text=f"{'ships:'}",
                            parent=self,
                            key="ships",
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
                            text="",
                            parent=self,
                            key="ships_count",
                            draw_frame=False,
                            player=player)
                    )
            if not ships_icon_built:
                icon = ImageButton(win=self.win,
                        x=self.world_x + x,
                        y=self.world_y + TOP_SPACING + 20,
                        width=button_size,
                        height=button_size,
                        isSubWidget=False,
                        parent=self,
                        image=pygame.transform.scale(get_image("spacehunter_30x30.png"), (button_size, button_size)),
                        tooltip="ships_icon",
                        frame_color=self.frame_color,
                        moveable=False,
                        include_text=True,
                        layer=self.layer,
                        onClick=lambda: print("no function"),
                        name="ships_icon",
                        textColour=self.frame_color,
                        font_size=12,
                        info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                        textHAlign="right_outside",
                        outline_thickness=0,
                        outline_threshold=1
                        )

                self.buttons.append(icon)
                self.widgets.append(icon)
                ships_icon_built = True

            # space harbor icon
            button_size_ = int(button_size / 2)
            icon = ImageButton(win=self.win,
                    x=self.world_x + x + 46,
                    y=self.world_y + TOP_SPACING + y,
                    width=button_size_,
                    height=button_size_,
                    isSubWidget=False,
                    parent=self,
                    image=pygame.transform.scale(get_image("space harbor_25x25.png"), (button_size_, button_size_)),
                    tooltip="space harbor_icon",
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    onClick=lambda: print("no function"),
                    name=f"space harbor_icon{player_index}",
                    textColour=self.frame_color,
                    font_size=12,
                    info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                    textHAlign="right_outside",
                    outline_thickness=0,
                    outline_threshold=1
                    )


            self.buttons.append(icon)
            self.widgets.append(icon)

            x += spacing_x

            # score
            self.widgets.append(
                    InputBox(
                            self.win,
                            self.world_x + x,
                            self.world_y + TOP_SPACING + y,
                            self.spacing_x * 2,
                            h,
                            text=f"{'score:'}",
                            parent=self,
                            key="score",
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
                            text="",
                            parent=self,
                            key="score_count",
                            draw_frame=False,
                            player=player)
                    )

            # score icon
            if not score_icon_built:
                icon = ImageButton(win=self.win,
                        x=self.world_x + x,
                        y=self.world_y + TOP_SPACING + 20,
                        width=button_size,
                        height=button_size,
                        isSubWidget=False,
                        parent=self,
                        image=pygame.transform.scale(get_image("score_icon.png"), (button_size, button_size)),
                        tooltip="open score plotter",
                        frame_color=self.frame_color,
                        moveable=False,
                        include_text=True,
                        layer=self.layer,
                        onClick=lambda: self.enable_plotter(),
                        name="score_icon",
                        textColour=self.frame_color,
                        font_size=12,
                        info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                        textHAlign="right_outside",
                        outline_thickness=0,
                        outline_threshold=1
                        )

                self.buttons.append(icon)
                self.widgets.append(icon)
                score_icon_built = True

            x += spacing_x
            x = 0
            y += h * 3

        self.max_height = self.world_y + self.world_height + y

    def update_diplomacy_button_image(self):
        for i in self.buttons:
            if i.name.startswith("diplomacy"):
                player_index = int(i.name.split("diplomacy")[1])

                if not diplomacy_handler.is_in_peace(player_index, config.player):
                    i.setImage(self.war_image)
                else:
                    i.setImage(self.peace_image)

    def update_space_harbor_icon(self):
        for player in config.app.players:
            space_harbor_icon = [i for i in self.widgets if i.name == f'space harbor_icon{player}'][0]
            space_harbor_icon._hidden = "space harbor" not in config.app.players[player].get_all_buildings()



    def update_inputboxes(self):
        for i in self.widgets:
            if i.__class__.__name__ == "InputBox":
                # print(f"i.text:{i.text}, i.key:{i.key}, i.kwargs:{i.kwargs}")
                if "player" in i.kwargs:
                    player_index = int(i.kwargs["player"].split("_")[1])
                    player = config.app.players[player_index]
                    if "/" in i.text:
                        # print(f"i.text:{i.text}, i.key:{i.key}, i.kwargs:{i.kwargs}")
                        if i.key == "population":
                            i.set_text(f"{int(player_handler.get_current_stock(player_index)[i.key])}"
                                       f"/{format_number(int(config.app.players[player_index].population_limit))}")
                        else:
                            if i.key in ["energy", "food", "minerals", "water", "technology"]:
                                i.set_text(f"{int(player_handler.get_current_stock(player_index)[i.key])}"
                                           f"/{int(player_handler.get_current_production(player_index)[i.key])}")
                    else:
                        # set colors
                        if i.text in player_handler.player_colors.values():
                            i.text = f"{player_handler.player_colors[player_index]}"
                            i.set_text(f"{i.text}", color=player_handler.player_colors[player_index])

                    if i.key == "planets_count":
                        i.set_text(f"{len([i for i in sprite_groups.planets.sprites() if i.owner == player_index])}")

                    if i.key == "buildings_count":
                        # planet_count = len([i for i in sprite_groups.planets.sprites() if i.owner == player_index])
                        buildings = len(player.get_all_buildings())
                        # slots = sum([i.buildings_max for i in sprite_groups.planets.sprites() if
                        #              i.owner == player_index])
                        slots = player.get_all_building_slots()
                        i.set_text(f"{buildings}/{slots}")

                        if player.busted:
                            self.overblit_player_image(player_index, False)
                        else:
                            self.overblit_player_image(player_index, True)

                    if i.key == "ships_count":
                        # planet_count = len([i for i in sprite_groups.planets.sprites() if i.owner == player_index])
                        ships = len(player.get_all_ships())
                        i.set_text(f"{ships}")

                    if i.key == "score_count":
                        i.set_text(f"{player.score}")

    def overblit_player_image(self, player_index, value):
        button = [i for i in self.buttons if i.name == f"player_{player_index}"][0]
        overblit_button_image(button, "busted.png", value, offset_x=-8, offset_y=-5, size=(56, 56), outline=True)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)
            self.update_inputboxes()
            self.update_space_harbor_icon()

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Players:")
