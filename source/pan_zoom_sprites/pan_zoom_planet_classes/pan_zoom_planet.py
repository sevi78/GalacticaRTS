import time

import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame_widgets.mouse import Mouse, MouseState
from source.database.database_access import create_connection, get_database_file_path
from source.gui.building_button_widget import BuildingButtonWidget

from source.gui.lod import inside_screen
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_orbit_draw import draw_orbits
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_position_handler import \
    PanZoomPlanetPositionHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_visibility_handler import PanZoomVisibilityHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_debug import GameObjectDebug
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_mouse_handler import PanZoomMouseHandler
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_overview_buttons import \
    PanZoomPlanetOverviewButtons
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_defence import PanZoomPlanetDefence
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_draw import PanZoomPlanetDraw
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_params import PanZoomPlanetParams
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_save_load import PanZoomPlanetSaveLoad
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.utils import global_params
from source.utils.colors import colors
from source.multimedia_library.images import images, get_image
from source.utils.positioning import limit_positions, orbit


class PanZoomPlanet(PanZoomSprite, PanZoomVisibilityHandler, PanZoomPlanetOverviewButtons, PanZoomPlanetDraw, PanZoomPlanetSaveLoad,
    PanZoomPlanetParams, PanZoomPlanetPositionHandler, PanZoomMouseHandler):
    """ Main functionalities:

    """
    __slots__ = PanZoomSprite.__slots__ + (
        'orbit_radius', 'font_size', 'font', '_on_hover', 'on_hover_release', 'size_x',
        'size_y', 'resources', 'buildings', 'buildings_max', 'population', 'population_limit', 'population_grow',
        'alien_population', 'building_slot_amount', 'building_slot_upgrades', 'building_slot_upgrade_prices',
        'building_slot_upgrade_energy_consumption', 'building_slot_max_amount', 'building_cue', 'specials',
        'possible_resources', 'production', 'production_water', 'production_energy', 'production_food',
        'production_minerals', 'production_city', 'production_technology', 'population_buildings',
        'population_buildings_values', 'building_buttons_energy', 'building_buttons_water', 'building_buttons_food',
        'building_buttons_minerals', 'building_buttons', 'building_buttons_list', 'building_buttons_visible',
        'overview_buttons', 'check_image', 'smiley_status', 'thumpsup_status', 'frame_color', 'gif_handler',
        'has_atmosphere', 'atmosphere', 'atmosphere_raw', 'type', 'parent', 'screen_size', 'target',
        'moving', 'tooltip', 'id', 'level', 'fog_of_war_radius', 'explored', 'just_explored', 'moveable', 'orbit_speed',
        'orbit_object', 'orbit_distance', 'string', 'start_time', 'wait', 'selected', 'onClick',
        'info_text', 'info_text_raw', 'planet_button_array', 'thumpsup_button_size', 'thumpsup_button',
        'smiley_button_size', 'smiley_button', 'planet_defence')

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        # inherit the base class
        PanZoomPlanetParams.__init__(self, kwargs)
        PanZoomVisibilityHandler.__init__(self, **kwargs)
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        PanZoomMouseHandler.__init__(self)
        PanZoomPlanetPositionHandler.__init__(self, x, y, width, height, **kwargs)
        PanZoomPlanetOverviewButtons.__init__(self, **kwargs)
        PanZoomPlanetDraw.__init__(self, **kwargs)
        PanZoomPlanetSaveLoad.__init__(self)

        self.type = kwargs.get("type", "")
        self.parent = kwargs.get("parent")
        self.screen_size = (global_params.WIDTH_CURRENT, global_params.HEIGHT_CURRENT)
        self.target = None
        self.moving = False
        self.tooltip = kwargs.get("tooltip", "")
        self.id = kwargs.get("id", len(sprite_groups.planets))
        self.level = kwargs.get("level", 1)
        self.fog_of_war_radius = self.get_screen_width() * 1.5
        self.explored = False
        self.just_explored = False

        self.set_atmosphere()

        self.property = "planet"
        self.moveable = kwargs.get("moveable", False)
        self.orbit_speed = kwargs.get("orbit_speed")
        self.orbit_object = None
        self.orbit_object_id = 0
        self.orbit_distance = 0
        self.orbit_angle = None
        self.world_x = x
        self.world_y = y

        self.zoomable = True
        self.string = "?"

        self.win = win
        self.start_time = time.time()
        self.wait = kwargs.get("wait", 1.0)
        self.selected = False

        self.onClick = lambda: self.execute(kwargs)

        # load_from_db Game variables___________________________________________________________________________________
        self.info_text = kwargs.get("info_text")
        self.info_text_raw = kwargs.get("info_text")

        # buttons
        # self.planet_button_array = None
        # self.create_planet_button_array()
        self.create_overview_buttons()
        self.building_button_widget = BuildingButtonWidget(win, 200, 100, 300, 200, self.parent, False, layer=4, parent=self, fixed_parent=True)

        # planet defence
        self.planet_defence = PanZoomPlanetDefence(self)

        # register the button
        sprite_groups.planets.add(self)
        # self.hide_planet_button_array()

        PanZoomPlanetSaveLoad.__init__(self)
        self.load_from_db()

        # self.update_pan_zoom_sprite()

    def __repr__(self):
        return self.name

    def __delete__(self, instance):
        print("planet.__delete__")
        self.delete_building_buttons()
        self.delete_resource_buttons()

        del self

    def select(self, value):
        self.selected = value

    def move(self, events, child):
        if not global_params.edit_mode:
            return

        if not self.moveable:
            return

        panzoom = pan_zoom_handler

        for event in events:
            # ignore all inputs while any text input is active
            if global_params.text_input_active:
                return

            # handle events
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.moving = True
                    global_params.enable_pan = not self.moving

            elif event.type == MOUSEBUTTONUP:
                self.moving = False
                global_params.enable_pan = not self.moving

                # self.orbit_angle = get_orbit_angle(self.screen_x, self.screen_y, self.orbit_object.screen_x, self.orbit_object.screen_y)
                #

            # now move the object
            elif event.type == MOUSEMOTION and self.moving:
                x, y = panzoom.screen_2_world(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                x1, y1 = panzoom.screen_2_world(self.orbit_object.screen_x, self.orbit_object.screen_y)
                if self.orbit_object:
                    pass
                    # self.orbit_angle = get_orbit_angle(self.world_x, self.world_y, self.orbit_object.x, self.orbit_object.y)
                    # self.orbit_angle = math.radians(get_orbit_angle(x, y, x1, y1))
                    # self.orbit_angle = get_orbit_angle(x, y, x1, y1)
                    # set_orbit_angle(self, get_orbit_angle(x, y, x1, y1))
                    # set_orbit_distance(self, self.orbit_object)
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

    def reset_planet(self):
        return
        print("reset_planet")
        self.delete_buttons()
        self.reset_building_buttons_visible_state()

        conn = create_connection(get_database_file_path())
        cur = conn.cursor()

        image_name = cur.execute(f"select image_name_small from planets where id = {self.id}").fetchone()[0]
        width, height = map(int, image_name.split("_")[1].split(".")[0].split("x"))

        self.__init__(
            win=global_params.win,
            x=cur.execute(f"select world_x from planets where id = {self.id}").fetchone()[0],
            y=cur.execute(f"select world_y from planets where id = {self.id}").fetchone()[0],
            width=int(cur.execute(f"select world_width from planets where id = {self.id}").fetchone()[0]),
            height=int(cur.execute(f"select world_height from planets where id = {self.id}").fetchone()[0]),
            pan_zoom=pan_zoom_handler,
            image_name=image_name,
            isSubWidget=False,
            image=get_image(
                cur.execute(f"select image_name_small from planets where id = {self.id}").fetchone()[0]),
            transparent=True,
            info_text=cur.execute(f"select info_text from planets where id = {self.id}").fetchone()[0],
            text=cur.execute(f"select name from planets where id = {self.id}").fetchone()[0],
            textColour=self.frame_color,
            property="planet",
            name=cur.execute(f"select name from planets where id = {self.id}").fetchone()[0],
            parent=self.parent,
            tooltip="send your ship to explore the planet!",
            possible_resources=eval(
                cur.execute(f"select possible_resources from planets where id = {self.id}").fetchone()[0]),
            moveable=global_params.moveable,
            hover_image=get_image("selection_150x150.png"),
            has_atmosphere=cur.execute(f"SELECT has_atmosphere FROM planets WHERE id = {self.id}").fetchone()[0],
            textVAlign="below_the_bottom",
            layer=3,
            id=self.id,
            orbit_object_id=cur.execute(f"select orbit_object_id from planets where id = {self.id}").fetchone()[0],
            image_name_small=cur.execute(f"select image_name_small from planets where id = {self.id}").fetchone()[0],
            image_name_big=cur.execute(f"select image_name_big from planets where id = {self.id}").fetchone()[0],
            buildings_max=cur.execute(f"select buildings_max from planets where id = {self.id}").fetchone()[0],
            orbit_speed=cur.execute(f"select orbit_speed from planets where id = {self.id}").fetchone()[0],
            orbit_angle=cur.execute(f"select orbit_angle from planets where id = {self.id}").fetchone()[0],
            building_slot_amount=
            cur.execute(f"select building_slot_amount from planets where id = {self.id}").fetchone()[0],
            alien_population=cur.execute(f"select alien_population from planets where id = {self.id}").fetchone()[0],
            specials=cur.execute(f"select specials from planets where id = {self.id}").fetchone()[0],
            type=cur.execute(f"select type from planets where id = {self.id}").fetchone()[0],
            )

        self.buildings = []

        self.load_from_db()
        self.explored = False
        self.just_explored = False
        # self.set_orbit_distance(self.orbit_object)

        conn.close()

    def debug_planet(self):
        if global_params.debug:
            pygame.draw.circle(self.win, colors.select_color, self.center, 10, 1)
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
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.rect.collidepoint(x, y):
                if mouseState == MouseState.RIGHT_CLICK:
                    self.parent.set_selected_planet(self)

                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    # self.onRelease(*self.onReleaseParams)

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    # self.onClick(*self.onClickParams)
                    self.parent.set_selected_planet(self)

                elif mouseState == MouseState.DRAG and self.clicked:
                    pass

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.draw_hover_circle()

                    if self.tooltip != "":
                        global_params.tooltip_text = self.tooltip
            else:
                if mouseState == MouseState.RIGHT_CLICK:
                    pass
                    # self.reset_building_buttons_visible_state()

                self.clicked = False

    def update(self):
        self.set_screen_position()
        self.update_pan_zoom_sprite()
        draw_orbits(self)

        global_params.app.tooltip_instance.reset_tooltip(self)
        self.planet_defence.defend()
        self.set_planet_name()

        # may we will not need these
        if global_params.planet_button_display_on_panel:
            # self.hide_planet_button_array()
            self.hide_overview_button()
        elif self.explored:
            # self.show_planet_button_array()
            self.show_overview_button()
            self.set_overview_buttons_position()

        if not self.orbit_object:
            self.orbit_angle = None
            self.orbit_object = [i for i in sprite_groups.planets if i.id == self.orbit_object_id][0]

        if not global_params.game_paused:
            orbit(self, self.orbit_object, self.orbit_speed, 1)


        if not inside_screen(self.rect.center):
            return

        self.draw()

    def draw(self):
        self.draw_image()
        if self.gif_handler:
            self.gif_handler.draw()

        self.draw_selection_circle()
        self.draw_text()
