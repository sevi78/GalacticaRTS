import pygame

from source.app.scene_builder import SceneBuilder
from source.auto_economy.auto_economy_calculator_edit import AutoEconomyCalculatorEdit
from source.configuration.game_config import config
from source.editors.building_edit import BuildingEdit
from source.editors.client_edit import network_config
from source.editors.debug_edit import DebugEdit
from source.editors.diplomacy_edit import DiplomacyEdit
from source.editors.enemy_handler_edit import EnemyHandlerEdit
from source.editors.planet_edit import PlanetEdit
from source.editors.save_game_edit import SaveGameEdit
from source.editors.ship_edit import ShipEdit
from source.game_play.enemy_handler import enemy_handler
from source.gui.panels.advanced_settings_panel import AdvancedSettingsPanel
from source.gui.panels.building_panel_components.building_panel import BuildingPanel
from source.gui.panels.building_panel_components.game_time_widget import GameTime
from source.gui.panels.event_panel import EventPanel
from source.gui.panels.info_panel import InfoPanel
from source.gui.panels.resource_panel import ResourcePanel
from source.gui.panels.settings_panel import SettingsPanel
from source.gui.panels.view_panel import ViewPanel
from source.gui.tool_tip import ToolTip
from source.gui.widgets.background_image import BackgroundGradient
from source.handlers.debug_handler import debugger
from source.handlers.file_handler import load_file
from source.network.client.client import Client
# from source.network.client.web_socket_client import WebSocketClient
from source.player.player import Player
from source.player.player_edit import PlayerEdit
from source.player.player_handler import player_handler
from source.trading.add_deal_edit import AddDealEdit
from source.weapons.weapon_select import WeaponSelect

EDITOR_HEIGHT = 600

EDITOR_WIDTH = 700
TOP_SPACING = 5

BACKGROUND_GRADIENT_DRAW = False
BACKGROUND_GRADIENT_FADE_RANGE = 80


class UIBuilder(SceneBuilder):
    """this creates all UI Elements:
    use SceneBuilder for Scene Elements like ships planets ect
    it also starts the game loop
    """

    def __init__(self, width, height):
        SceneBuilder.__init__(self, width, height)

        self.win = config.win

        # panels
        self.view_panel = None
        self.building_panel = None
        self.game_time = None
        self.advanced_settings_panel = None
        self.resource_panel = None
        self.settings_panel = None
        self.event_panel = None
        self.create_event_panel()

        # editors
        self.event_panel_edit = None
        self.debug_edit = None
        self.ship_edit = None
        self.enemy_handler_edit = None
        self.font_edit = None
        self.planet_edit = None
        self.settings_edit = None
        self.economy_overview = None
        self.add_deal_edit = None
        self.trade_edit = None
        self.building_edit = None
        self.save_game_edit = None
        self.weapon_select = None
        self.diplomacy_edit = None
        self.player_edit = None

        self.create_editors()

        # box selection
        self.box_selection = None
        self.tooltip_instance = None

        # set args
        self.world_width = width
        self.height = height
        self.icons = []
        self.selected_planet = None

        # players
        self.player = None  # this is the human player, default index 0
        self.players = {}

        # initialize game_client
        # network_config = load_file("network_config.json", "config")
        self.game_client = Client(network_config["host"], network_config["port"])
        # self.game_client = WebSocketClient()

        # building_panel
        self.create_building_panel()

        # settings panel
        self.create_settings_panel()

        # tooltip
        self.create_tooltip()

        # resource_panel
        self.create_resource_panel()

        # Info_panel
        self.info_panel = InfoPanel(
                self.win,
                x=0,
                y=self.settings_panel.surface_rect.bottom,
                width=240,
                height=300,
                is_sub_widget=False,
                parent=self.resource_panel,
                layer=9)

        # background image (gradient)
        self.background_gradient = BackgroundGradient(
                self.win,
                0,
                0,
                1920,
                1080,
                is_sub_widget=False,
                layer=8,
                draw_gradient=BACKGROUND_GRADIENT_DRAW,
                fade_range=BACKGROUND_GRADIENT_FADE_RANGE)

    def create_editors(self):
        width = EDITOR_WIDTH
        height = EDITOR_HEIGHT
        spacing_y = 0

        # editors
        diplomacy_edit_width = 460
        self.diplomacy_edit = DiplomacyEdit(
                self.win,
                int(pygame.display.get_surface().get_width() / 2 - diplomacy_edit_width / 2),
                int(pygame.display.get_surface().get_height() / 2),
                diplomacy_edit_width,
                60,
                False,
                obj=None,
                layer=10,
                parent=self,
                ignore_other_editors=True,
                save=False)

        self.weapon_select = WeaponSelect(
                pygame.display.get_surface(),
                pygame.display.get_surface().get_rect().centerx - width * 1.5 / 2,
                pygame.display.get_surface().get_rect().y + spacing_y,
                width,
                height,
                parent=self)

        self.planet_edit = PlanetEdit(
                pygame.display.get_surface(),
                pygame.display.get_surface().get_rect().centerx - width / 2,
                pygame.display.get_surface().get_rect().y + spacing_y,
                width,
                height,
                parent=self,
                obj=None)

        self.save_game_edit = SaveGameEdit(
                pygame.display.get_surface(),
                pygame.display.get_surface().get_rect().centerx - width / 2,
                pygame.display.get_surface().get_rect().y + spacing_y,
                800,
                height,
                parent=self,
                obj=None)

        self.building_edit = BuildingEdit(
                pygame.display.get_surface(),
                pygame.display.get_surface().get_rect().centerx - width / 2,
                pygame.display.get_surface().get_rect().y,
                width,
                height,
                parent=self)

        self.enemy_handler_edit = EnemyHandlerEdit(
                pygame.display.get_surface(),
                pygame.display.get_surface().get_rect().centerx - width / 2,
                pygame.display.get_surface().get_rect().y + spacing_y,
                width,
                height,
                parent=self,
                obj=enemy_handler)

        self.ship_edit = ShipEdit(
                pygame.display.get_surface(),
                pygame.display.get_surface().get_rect().centerx - width / 2,
                pygame.display.get_surface().get_rect().y + spacing_y,
                width,
                height,
                parent=self,
                obj=self.ship,
                layer=9)

        self.debug_edit = DebugEdit(
                pygame.display.get_surface(),
                pygame.display.get_surface().get_rect().centerx - width / 2,
                pygame.display.get_surface().get_rect().y + spacing_y,
                width, height, parent=self, obj=debugger, layer=9)

        # self.trade_edit = TradeEdit(pygame.display.get_surface(),
        #         pygame.display.get_surface().get_rect().centerx - width / 2,
        #         pygame.display.get_surface().get_rect().y + spacing_y,
        #         width,
        #         height,
        #         parent=self,
        #         obj=None,
        #         layer=9)  # , game_paused=True)

        self.add_deal_edit = AddDealEdit(
                pygame.display.get_surface(),
                int(pygame.display.get_surface().get_width() / 2),
                pygame.display.get_surface().get_rect().y + spacing_y,
                width,
                height,
                parent=self,
                obj=None,
                layer=9)  # , game_paused=True)

        # self.settings_edit = SettingsEdit(
        #         pygame.display.get_surface(),
        #         pygame.display.get_surface().get_rect().centerx - width / 2,
        #         pygame.display.get_surface().get_rect().y + spacing_y,
        #         int(width / 1.5),
        #         height,
        #         parent=self,
        #         obj=None,
        #         layer=9)  # , game_paused=True)

        self.auto_economy_calculator_edit = AutoEconomyCalculatorEdit(
                pygame.display.get_surface(),
                pygame.display.get_surface().get_rect().centerx - width / 2,
                pygame.display.get_surface().get_rect().y + spacing_y,
                int(width / 1.5),
                height,
                parent=self,
                obj=None,
                layer=9)  # , game_paused=True)

    def create_players(self, data=dict) -> None:
        # for some stupid reason, i cant move this to player_handler: RuntimeError: dictionary changed size during iteration
        for key, value in data.items():
            player_id = data[key]["player"]
            self.players[player_id] = Player(
                    name=data[key]["name"],
                    species=data[key]["species"],
                    color=player_handler.get_player_color(player_id),
                    stock={
                        "energy": 1000,
                        "food": 1000,
                        "minerals": 1000,
                        "water": 1000,
                        "technology": 1000,
                        "population": 0
                        },
                    production={
                        "energy": 0,
                        "food": 0,
                        "minerals": 0,
                        "water": 0,
                        "technology": 0,
                        "population": 0
                        },
                    clock=0,
                    owner=player_id,
                    image_name=data[key]["image_name"],
                    enemies=data[key]["enemies"]
                    )

        # set active (human) player
        self.player = self.players[0]

    def create_event_panel(self):
        w, h = 900, 600
        x = pygame.display.get_surface().get_width() / 2 - w / 2
        y = pygame.display.get_surface().get_height() / 2 - h / 2
        self.event_panel = EventPanel(
                win=self.win,
                x=x,
                y=y,
                width=w,
                height=h,
                center=True,
                parent=self,
                layer=9,
                interface_variables=load_file("event_panel.json", "config"),
                game_paused=True)

    def create_tooltip(self):
        # tooltip
        self.tooltip_instance = ToolTip(surface=self.win,
                x=100,
                y=100,
                width=100,
                height=100,
                color=pygame.colordict.THECOLORS["black"],
                text_color=self.frame_color,  # pygame.colordict.THECOLORS["darkslategray1"],
                is_sub_widget=False,
                parent=self,
                layer=10)

    def create_building_panel(self):
        # building_panel
        size_x = 250
        size_y = 35
        spacing = 10
        self.building_panel = BuildingPanel(self.win,
                x=self.world_width - size_x,
                y=spacing,
                width=size_x - spacing,
                height=size_y,
                is_sub_widget=False,
                size_x=size_x,
                size_y=size_y,
                spacing=spacing,
                parent=self,
                layer=9)

        self.game_time = GameTime(self.win,
                x=self.world_width - size_x,
                y=spacing,
                width=size_x - spacing,
                height=size_y,
                is_sub_widget=True,
                size_x=size_x,
                size_y=size_y,
                spacing=spacing,
                layer=9)

    def create_settings_panel(self):
        icon_size = 25
        size_x = 800  # doesnt matter, will be recalculated
        size_y = 35
        spacing = TOP_SPACING

        self.settings_panel = SettingsPanel(self.win,
                x=self.world_width - size_x,
                y=spacing * 2,
                width=size_x - spacing,
                height=size_y,
                is_sub_widget=False,
                size_x=size_x,
                size_y=size_y,
                spacing=spacing,
                parent=self,
                layer=9,
                icon_size=icon_size,
                anchor_right=self.building_panel.get_screen_x())

        self.advanced_settings_panel = AdvancedSettingsPanel(self.win,
                x=self.settings_panel.surface_frame.right,
                y=self.settings_panel.surface_frame.bottom,
                width=size_x - spacing,
                height=size_y,
                is_sub_widget=False,
                size_x=size_x,
                size_y=size_y,
                spacing=spacing,
                parent=self,
                layer=9,
                icon_size=icon_size,
                anchor_right=self.building_panel.get_screen_x())

        self.view_panel = ViewPanel(self.win,
                x=self.settings_panel.surface_frame.left,
                y=self.settings_panel.surface_frame.bottom,
                width=size_x - spacing,
                height=size_y,
                is_sub_widget=False,
                size_x=size_x,
                size_y=size_y,
                spacing=spacing,
                parent=self,
                layer=9,
                icon_size=icon_size,
                anchor_right=self.settings_panel.get_screen_x())

    def create_resource_panel(self):
        icon_size = 25
        size_x = 800  # doesnt matter, will be recalculated
        size_y = 35
        start_x = 250
        spacing = 142
        pos_x = start_x
        pos_y = 10

        self.resource_panel = ResourcePanel(self.win,
                x=pos_x,
                y=pos_y,
                width=size_x,
                height=size_y,
                is_sub_widget=False,
                size_x=size_x,
                size_y=size_y,
                spacing=spacing,
                parent=self,
                layer=9,
                icon_size=icon_size,
                anchor_right=self.advanced_settings_panel.get_screen_x(),
                app=self)

    def create_player_edit(self, num_players: int):
        width, height = 1200, 1200

        # make shure its deleted before creating a new one
        if hasattr(self, 'player_edit') and self.player_edit is not None:
            self.player_edit.__del__()
            del self.player_edit

        # create a new one
        self.player_edit = PlayerEdit(pygame.display.get_surface(),
                int(pygame.display.get_surface().get_width() / 2 - width / 2),
                pygame.display.get_surface().get_rect().y,
                width, height, parent=self, obj=None, layer=9, ignore_other_editors=True, drag_enabled=False, save=False, num_players=num_players)
