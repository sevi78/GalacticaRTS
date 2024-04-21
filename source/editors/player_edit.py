import pygame

from source.configuration.game_config import config
from source.editors.auto_economy_edit import AutoEconomyEdit
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.inputbox import InputBox
from source.handlers.file_handler import write_file
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.player_handler import player_handler
from source.multimedia_library.images import get_image

ARROW_SIZE = 20
FONT_SIZE = int(ARROW_SIZE * .8)


class PlayerEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.data = player_handler.get_players()

        # setup image dict
        self.player_image_names = {}
        for player_name, dict_ in self.data.items():
            for key, value in dict_.items():
                if key == 'image_name':
                    self.player_image_names[player_name] = value

        #  widgets
        self.widgets = []
        self.create_close_button()
        self.create_inputboxes()
        self.create_save_button(lambda: self.save_settings(), "save settings")

        # editor
        # auto_economy_edit
        self.auto_economy_edit = None

        # hide initially
        self.hide()

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
        spacing_x = 80

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

        # create items
        for player in ordered_data.keys():
            player_index = int(player.split("_")[1])

            # create player image button
            image_name = self.player_image_names[player]
            button_size = 40
            icon = ImageButton(win=self.win,
                x=self.world_x + x + int(spacing_x / 2),
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
                onClick=lambda player_index_=player_index: self.open_auto_economy_edit(player_index_),
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
            x += spacing_x

            # set data boxes from file
            x += spacing_x
            for key, value in ordered_data[player].items():
                if not key.startswith("production_"):
                    # images
                    self.create_resource_images(key, resources, x)

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
            icon = ImageButton(win=self.win,
                x=self.world_x + x,
                y=self.world_y + TOP_SPACING + 20,
                width=button_size,
                height=button_size,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(get_image("score_icon.png"), (button_size, button_size)),
                tooltip="score_icon",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                onClick=lambda: print("no function"),
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
                # print(f"i.text:{i.text}, i.key:{i.key}, i.kwargs:{i.kwargs}")
                if "player" in i.kwargs:
                    player_index = int(i.kwargs["player"].split("_")[1])
                    player = config.app.players[player_index]
                    if "/" in i.text:
                        # print(f"i.text:{i.text}, i.key:{i.key}, i.kwargs:{i.kwargs}")
                        if i.key == "population":
                            i.set_text(f"{int(player_handler.get_current_stock(player_index)[i.key])}"
                                       f"/{int(config.app.players[player_index].population_limit)}")
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

                    if i.key == "ships_count":
                        # planet_count = len([i for i in sprite_groups.planets.sprites() if i.owner == player_index])
                        ships = len(player.get_all_ships())
                        i.set_text(f"{ships}")

                    if i.key == "score_count":
                        i.set_text(f"{player.score}")

    def open_auto_economy_edit(self, player_id: int):
        if not hasattr(config.app, "auto_economy_edit") or not config.app.auto_economy_edit:
            editor = AutoEconomyEdit(
                pygame.display.get_surface(),
                self.world_x,
                self.world_y + self.world_height / 2,
                900, 300,
                parent=self,
                obj=None,
                layer=9,
                ignore_other_editors=True
                )

            # attach to app
            setattr(config.app, "auto_economy_edit", editor)
            config.app.auto_economy_edit.set_visible()

            # attach to self.editors
            self.editors = []
            self.editors.append(editor)

        config.app.auto_economy_edit.player_id = player_id
        config.app.auto_economy_edit.set_player(player_id)

    def close(self):
        config.set_global_variable("edit_mode", True)
        if self.auto_economy_edit:
            self.auto_economy_edit.__del__()
        self.auto_economy_edit = None

        if config.app.auto_economy_edit:
            config.app.auto_economy_edit.__del__()
            config.app.auto_economy_edit = None
        self.editors = []
        config.tooltip_text = ""
        self.hide()

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)
            self.update_inputboxes()

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Players:")
