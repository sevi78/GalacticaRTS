import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

from source.configuration.game_config import config
from source.draw.circles import draw_transparent_circle
from source.gui.lod import level_of_detail
from source.gui.widgets.widget_base_components.visibilty_handler import VisibilityHandler
from source.handlers.color_handler import colors
from source.handlers.garbage_handler import garbage_handler
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.handlers.orbit_handler import orbit_with_constant_distance
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.handlers.widget_handler import WidgetHandler
from source.interaction.interaction_handler import InteractionHandler
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_defence import PanZoomPlanetDefence
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_draw import PanZoomPlanetDraw
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_orbit_draw import draw_orbits
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_overview_buttons import \
    PanZoomPlanetOverviewButtons
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_params import PanZoomPlanetParams
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_position_handler import \
    PanZoomPlanetPositionHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
from source.path_finding.a_star_node_path_finding import Node

ORBIT_RESOLUTION = 360


class PanZoomPlanet(PanZoomSprite, VisibilityHandler, PanZoomPlanetOverviewButtons, PanZoomPlanetDraw,
        PanZoomPlanetParams, PanZoomPlanetPositionHandler, InteractionHandler):
    """ Main functionalities: """
    # __slots__ = PanZoomSprite.__slots__ + (
    #     'orbit_radius', 'font_size', 'font', '_on_hover', 'on_hover_release', 'size_x',
    #     'size_y', 'resources', 'buildings', 'buildings_max', 'population', 'population_limit', 'population_grow',
    #     'alien_population', 'building_slot_amount', 'building_slot_upgrades', 'building_slot_upgrade_prices',
    #     'building_slot_upgrade_energy_consumption', 'building_slot_max_amount', 'building_cue', 'specials',
    #     'possible_resources', 'production', 'production_water', 'production_energy', 'production_food',
    #     'production_minerals', 'production_population', 'production_technology', 'population_buildings',
    #     'population_buildings_values', 'building_buttons_energy', 'building_buttons_water', 'building_buttons_food',
    #     'building_buttons_minerals', 'building_buttons', 'building_buttons_list', 'building_buttons_visible',
    #     'overview_buttons', 'smiley_status', 'thumpsup_status', 'frame_color', 'gif_handler', 'type',
    #     'parent', 'screen_size', 'target', 'moving', 'tooltip', 'id', 'level', 'fog_of_war_radius', 'explored',
    #     'just_explored', 'moveable', 'orbit_speed', 'orbit_object', 'orbit_distance', 'string', 'start_time', 'wait',
    #     'selected', 'on_click', 'info_text', 'info_text_raw', 'thumpsup_button_size', 'thumpsup_button',
    #     'smiley_button_size', 'smiley_button', 'planet_defence')

    __slots__ = PanZoomSprite.__slots__ + (
        'orbit_radius', 'font_size', 'font', '_on_hover', 'on_hover_release', 'size_x',
        'size_y', 'overview_buttons', 'smiley_status', 'thumpsup_status', 'frame_color', 'gif_handler', 'type',
        'parent', 'screen_size', 'target', 'moving', 'tooltip', 'id', 'level', 'fog_of_war_radius', 'explored',
        'just_explored', 'moveable', 'orbit_speed', 'orbit_object', 'orbit_distance', 'string', 'start_time', 'wait',
        'selected', 'on_click', 'info_text', 'info_text_raw', 'thumpsup_button_size', 'thumpsup_button',
        'smiley_button_size', 'smiley_button', 'planet_defence')

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        # inherit the base class
        PanZoomPlanetParams.__init__(self, kwargs)
        VisibilityHandler.__init__(self, **kwargs)
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        InteractionHandler.__init__(self)
        PanZoomPlanetPositionHandler.__init__(self, x, y, width, height, **kwargs)
        PanZoomPlanetOverviewButtons.__init__(self, **kwargs)
        PanZoomPlanetDraw.__init__(self, **kwargs)

        self.name = kwargs.get("name", "noname_planet")
        self.type = kwargs.get("type", "")
        self.parent = kwargs.get("parent")
        self.screen_size = (config.width_current, config.height_current)
        self.target = None
        self.moving = False
        self.tooltip = kwargs.get("tooltip", "")
        self.id = kwargs.get("id", len(sprite_groups.planets))
        self.level = kwargs.get("level", 1)
        self.fog_of_war_radius = self.get_screen_width() * 1.5
        self.explored = False
        self.just_explored = False
        self.property = "planet"
        self.moveable = kwargs.get("moveable", False)
        self.orbit_speed_raw = kwargs.get("orbit_speed")
        self.orbit_speed = kwargs.get("orbit_speed")
        self.orbit_object = None
        self.orbit_object_id = kwargs.get("orbit_object_id")
        self.orbit_distance = 0
        self.orbit_angle = kwargs.get("orbit_angle", None)
        self.world_x = x
        self.world_y = y

        self.zoomable = True
        self.string = "?"

        self.win = win
        self.start_time = time_handler.time
        self.wait = kwargs.get("wait", 1.0)
        self.selected = False

        # energy, only used for beeing attacked
        self.energy = 100000

        # load_from_db Game variables___________________________________________________________________________________
        self.info_text = kwargs.get("info_text")
        self.info_text_raw = kwargs.get("info_text")

        # buttons
        self.create_overview_buttons()

        # planet defence
        self.planet_defence = PanZoomPlanetDefence(self)

        # pathfinding
        self.node = Node(self.world_x, self.world_y, self)

        # setup loaded data
        self.data = kwargs.get("data", {})
        for key, value in self.data.items():
            # if key in self.economy_agent.__dict__:
            if hasattr(self.economy_agent, key):
                setattr(self.economy_agent, key, value)
            else:
                setattr(self, key, value)

        # register the button
        sprite_groups.planets.add(self)

    def get_network_data(self, function: str) -> dict:
        if function == "position_update":
            data = {
                "id": self.id,
                "x": int(self.world_x),
                "y": int(self.world_y),
                "p": int(self.economy_agent.population)
                }

            return data

    def __repr__(self):
        return self.name

    def __delete__(self):
        if hasattr(self, "planet_defence"):
            garbage_handler.delete_all_references(self, self.planet_defence)
            self.planet_defence.emp.__delete__(self.planet_defence.emp)
            WidgetHandler.remove_widget(self.planet_defence.emp)
            self.planet_defence.emp = None
            del self.planet_defence

        for i in self.overview_buttons:
            WidgetHandler.remove_widget(i)
        self.overview_buttons = []

        WidgetHandler.remove_widget(self.smiley_button)
        WidgetHandler.remove_widget(self.thumpsup_button)
        self.smiley_button = None
        self.thumpsup_button = None
        self.overview_buttons = []
        if self.gif_handler:
            self.gif_handler.end_object()
        self.gif = None
        self.gif_frames = None
        self.children = None
        self.gif_handler = None

        if self in config.app.explored_planets:
            config.app.explored_planets.remove(self)
        self.kill()

        del self

    def select(self, value):
        self.selected = value

    def move(self, events, child):
        if not config.edit_mode:
            return

        if not self.moveable:
            return

        # if config.app.level_edit._hidden:
        #     return

        panzoom = pan_zoom_handler

        for event in events:
            # ignore all inputs while any text input is active
            if config.text_input_active:
                return

            # handle events
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.collide_rect.collidepoint(event.pos):
                    self.moving = True
                    config.enable_pan = not self.moving

            elif event.type == MOUSEBUTTONUP:
                self.moving = False
                config.enable_pan = not self.moving

            # now move the object
            elif event.type == MOUSEMOTION and self.moving:
                x, y = panzoom.screen_2_world(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                x1, y1 = panzoom.screen_2_world(self.orbit_object.screen_x, self.orbit_object.screen_y)
                self.world_x = x
                self.world_y = y

                # move childs
                # satelites = [i for i in sprite_groups.planets if i.orbit_object == self]
                # for satelite in satelites:
                #     x, y = panzoom.screen_2_world(pygame.mouse.get_pos()[0] + satelite.screen_x, pygame.mouse.get_pos()[1] +satelite.screen_y)
                #
                #     x1, y1 = panzoom.screen_2_world(self.screen_x, self.screen_y)
                #     if satelite.orbit_object:
                #         # self.orbit_angle = get_orbit_angle(self.world_x, self.world_y, self.orbit_object.x, self.orbit_object.y)
                #         # satelite.orbit_angle = math.radians(get_orbit_angle(x, y, x1, y1))
                #         # set_orbit_distance(satelite, satelite.orbit_object)
                #         satelite.setX(x)
                #         satelite.setY(y)

                #     self.orbit_distance = self.set_orbit_distance(self.orbit_object)
                #
                # print(self.orbit_angle, self.orbit_distance, self.offset)

    def debug_planet(self):
        if config.debug:
            pygame.draw.circle(self.win, colors.select_color, self.rect.center, 10, 1)
            pygame.draw.rect(self.win, self.frame_color, self.rect, 1)

            if self.gif:
                pygame.draw.rect(self.win, pygame.color.THECOLORS["red"], self.gif_handler.rect, 1)

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        self.move(events, None)

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()

            if self.collide_rect.collidepoint(x, y):
                if mouse_handler.double_clicks == 1:
                    config.app.diplomacy_edit.open(self.owner, config.app.game_client.id)

                if mouse_state == MouseState.RIGHT_CLICK:
                    self.parent.set_selected_planet(self)

                if mouse_state == MouseState.LEFT_RELEASE and self.clicked:
                    self.clicked = False

                elif mouse_state == MouseState.LEFT_CLICK:
                    self.clicked = True
                    self.parent.set_selected_planet(self)
                    # config.app.player_edit.player_buildings_overview.set_buildings(self)

                    # config.app.player_edit.planet_buildings_overview.set_buildings(self)
                    # if config.app.player_edit.planet_buildings_overview._hidden:
                    #     config.app.player_edit.planet_buildings_overview.set_visible()

                elif mouse_state == MouseState.LEFT_DRAG and self.clicked:
                    pass

                elif mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                    self.draw_hover_circle()
                    if self.tooltip != "":
                        config.tooltip_text = self.tooltip
                        config.app.info_panel.set_text(self.info_text)
                        config.app.info_panel.set_planet_image(self.image_raw)

                    draw_transparent_circle(self.win, self.frame_color, self.rect.center, self.planet_defence.attack_distance, 20)
                    self.draw_specials()
                    self.draw_alien_population_icons()
                    self.show_overview_button()

                    # set cursor
                    config.app.cursor.set_cursor("watch")
            else:
                self.clicked = False

    def update(self):
        self.set_screen_position()
        self.update_pan_zoom_sprite()
        self.handle_overview_buttons()
        self.planet_defence.update()

        # setting orbit object every frame?? yes , because in __init__ not all planets are created at this moment
        if not self.orbit_object:
            if len([i for i in sprite_groups.planets if i.id == self.orbit_object_id]) > 0:
                self.orbit_object = [i for i in sprite_groups.planets if i.id == self.orbit_object_id][0]

        if not config.game_paused:
            orbit_with_constant_distance(self, self.orbit_object, self.orbit_speed, 1)

        # not needed in update, draw called from sprite_handler

        if not level_of_detail.inside_screen(self.rect.center):
            # dirty hack to make the overview buttons disappear if self is outside screen
            for i in self.overview_buttons:
                i._hidden = True

            return

        self.draw()

    def draw(self):
        draw_orbits(self)
        self.set_display_color()
        self.draw_cross()
        self.draw_player_colors()
        if self.show_text:
            self.draw_text()


