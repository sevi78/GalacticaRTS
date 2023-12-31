import pygame

from source.app.scene_builder import SceneBuilder
from source.editors.building_edit import BuildingEdit
from source.editors.debug_edit import DebugEdit
from source.editors.font_edit import FontEdit
from source.editors.enemy_handler_edit import EnemyHandlerEdit
from source.editors.event_panel_edit import EventPanelEdit
from source.editors.level_edit import LevelEdit
from source.editors.level_select import LevelSelect
from source.editors.planet_edit import PlanetEdit
from source.editors.ship_edit import ShipEdit
from source.editors.trade_edit import TradeEdit
from source.editors.weapon_select import WeaponSelect
from source.game_play.enemy_handler import enemy_handler
from source.game_play.player import Player
from source.gui.panels.advanced_settings_panel import AdvancedSettingsPanel
from source.gui.panels.building_panel_components.game_time_widget import GameTime
from source.gui.panels.building_panel_components.building_panel import BuildingPanel
from source.gui.panels.event_panel import EventPanel
from source.gui.panels.info_panel import InfoPanel
from source.gui.panels.resource_panel import ResourcePanel
from source.gui.panels.settings_panel import SettingsPanel
from source.gui.tool_tip import ToolTip
from source.handlers.debug_handler import debugger
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import PanZoomHandler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.configuration import global_params
from source.handlers.file_handler import load_file

EDITOR_HEIGHT = 600

EDITOR_WIDTH = 700
TOP_SPACING = 5


class UIBuilder(SceneBuilder):
    """this creates all UI Elements:
    use SceneBuilder for Scene Elements like ships planets ect
    it also starts the game loop
    """

    def __init__(self, width, height):
        SceneBuilder.__init__(self, width, height)
        self.win = global_params.win

        # panzoom
        self.pan_zoom_handler = PanZoomHandler(
            global_params.win, global_params.WIDTH, global_params.HEIGHT, parent=self)

        # event panel
        self.create_event_panel()

        # editors
        self.event_panel_edit = None
        self.debug_edit = None
        self.ship_edit = None
        self.enemy_handler_edit = None
        self.font_edit = None
        self.planet_edit = None
        self.create_editors()

        self.clock = pygame.time.Clock()

        self.box_selection = None

        # set args
        self.world_width = width
        self.height = height
        self.icons = []
        self.selected_planet = None

        # player
        self.create_player()

        # building_panel
        self.create_building_panel()

        # settings panel
        self.create_settings_panel()

        # tooltip
        self.create_tooltip()

        # resource_panel
        self.create_resource_panel()

        # Info_panel
        self.info_panel = InfoPanel(self.win, x=0, y=self.settings_panel.surface_rect.bottom, width=240, height=300, isSubWidget=False, parent=self.resource_panel, layer=9)

        # build menu
        # self.build_menu = None
        # self.create_build_menu()
        # self.close_build_menu()

    def create_editors(self):
        width = EDITOR_WIDTH
        height = EDITOR_HEIGHT

        # editors

        self.weapon_select = WeaponSelect(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width*1.5 / 2,
            pygame.display.get_surface().get_rect().y,
            width*1.5, height*1.5, parent=self)

        self.level_select = LevelSelect(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, width, parent=self, obj=None)

        self.planet_edit = PlanetEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self, obj=sprite_groups.planets.sprites()[0])

        self.level_edit = LevelEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self)

        self.building_edit = BuildingEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self)

        self.font_edit = FontEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self)

        self.enemy_handler_edit = EnemyHandlerEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self, obj=enemy_handler)

        self.ship_edit = ShipEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self, obj=self.ship, layer=9)

        self.debug_edit = DebugEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self, obj=debugger, layer=9)

        self.event_panel_edit = EventPanelEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self, obj=self.event_panel, layer=9)

        self.trade_edit = TradeEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - width / 2,
            pygame.display.get_surface().get_rect().y,
            width, height, parent=self, obj=None, layer=9, game_paused=True)

    def create_player(self):
        self.player = Player(name="zork",
            color=pygame.Color('red'),
            energy=1000,
            food=1000,
            minerals=1000,
            water=1000,
            technology=1000,
            city=0,
            clock=0
            )

    def create_event_panel(self):
        w, h = 900, 600
        x = pygame.display.get_surface().get_width() / 2 - w / 2
        y = pygame.display.get_surface().get_height() / 2 - h / 2
        self.event_panel = EventPanel(win=self.win, x=x, y=y, width=w, height=h, center=True, parent=self, layer=9,
            interface_variables=load_file("event_panel.json"))

    def create_tooltip(self):
        # tooltip
        self.tooltip_instance = ToolTip(surface=self.win,
            x=100,
            y=100,
            width=100,
            height=100,
            color=pygame.colordict.THECOLORS["black"],
            text_color=self.frame_color,  # pygame.colordict.THECOLORS["darkslategray1"],
            isSubWidget=False, parent=self, layer=10)

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
            isSubWidget=False,
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
            isSubWidget=False,
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
            isSubWidget=False,
            size_x=size_x,
            size_y=size_y,
            spacing=spacing,
            parent=self,
            layer=9,
            icon_size=icon_size,
            anchor_right=self.building_panel.get_screen_x())

        self.advanced_settings_panel = AdvancedSettingsPanel(self.win,
            x=self.world_width - size_x * 2,
            y=spacing * 2,
            width=size_x - spacing,
            height=size_y,
            isSubWidget=False,
            size_x=size_x,
            size_y=size_y,
            spacing=spacing,
            parent=self,
            layer=9,
            icon_size=icon_size,
            anchor_right=self.building_panel.get_screen_x())

    def create_resource_panel(self):
        icon_size = 25
        size_x = 800  # doesnt matter, will be recalculated
        size_y = 35
        start_x = 250
        spacing = 150
        pos_x = start_x
        pos_y = 10

        self.resource_panel = ResourcePanel(self.win,
            x=pos_x,
            y=pos_y,
            width=size_x,
            height=size_y,
            isSubWidget=False,
            size_x=size_x,
            size_y=size_y,
            spacing=spacing,
            parent=self,
            layer=9,
            icon_size=icon_size,
            anchor_right=self.advanced_settings_panel.get_screen_x(), app=self)
