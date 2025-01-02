import pygame
from pygame import Vector2
from pygame_widgets.util import drawText

from source.configuration.game_config import config
from source.economy.EconomyAgent import EconomyAgent
from source.gui.interfaces.interface import InterfaceData
from source.gui.lod import level_of_detail
from source.handlers.autopilot_handler import AutopilotHandler
from source.handlers.color_handler import colors
from source.handlers.file_handler import load_file
from source.handlers.orbit_handler import orbit_ship
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.weapons.weapon_handler import WeaponHandler
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import rotate_image_to
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_draw import PanZoomShipDraw
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_interaction import PanZoomShipInteraction
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_moving import PanZoomShipMoving
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_params import PanZoomShipParams, \
    SHIP_ITEM_COLLECT_DISTANCE, SHIP_SPEED, SHIP_ROTATE_CORRECTION_ANGLE, SHIP_TARGET_OBJECT_RESET_DISTANCE
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_ranking import PanZoomShipRanking
from source.pan_zoom_sprites.pan_zoom_ship_classes.spacestation import Spacestation
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_game_object import PanZoomGameObject
from source.pan_zoom_sprites.pan_zoom_target_object import PanZoomTargetObject
from source.player.player_handler import player_handler


# disabled_functions = ["draw_connections", "draw_selection"]
# for i in disabled_functions:
#     disabler.disable(i)

class PanZoomShip(PanZoomGameObject, PanZoomShipParams, PanZoomShipMoving, PanZoomShipRanking, PanZoomShipDraw, PanZoomShipInteraction, InterfaceData):
    # __slots__ = PanZoomGameObject.__slots__ + ('item_collect_distance', 'orbit_direction', 'speed', 'id', 'property',
    #                                            'rotate_correction_angle', 'orbit_object', 'orbit_angle', 'collect_text',
    #                                            'target_object', 'target_object_reset_distance_raw',
    #                                            'target_object_reset_distance', 'hum_playing', '_orbit_object',
    #                                            'gun_power', 'gun_power_max', 'interface_variable_names')
    #
    # # PanZoomShipParams
    # __slots__ += ('id', 'reload_max_distance_raw', 'reload_max_distance', 'reload_max_distance_max_raw',
    #               'reload_max_distance_max', 'name', 'parent', 'hum', 'sound_channel', 'energy_use', 'food', 'food_max',
    #               'minerals', 'minerals_max', 'water', 'water_max', 'population', 'population_max', 'technology',
    #               'technology_max', 'resources', 'energy_max', 'energy', 'energy_reloader', 'energy_reload_rate',
    #               'move_stop', 'crew', 'crew_max', 'crew_members', 'fog_of_war_radius', 'fog_of_war_radius_max',
    #               'upgrade_factor', 'upgrade_factor_max', 'tooltip')
    #
    # # PanZoomShipMoving
    # __slots__ += ('attack_distance_raw', 'attack_distance', 'attack_distance_max', 'desired_orbit_radius_raw',
    #               'desired_orbit_radius', 'desired_orbit_radius_max', 'target', 'enemy', '_moving', '_orbiting',
    #               'orbit_speed', 'orbit_speed_max', 'zoomable', 'min_dist_to_other_ships',
    #               'min_dist_to_other_ships_max', 'orbit_radius', 'orbit_radius_max')
    #
    # # PanZoomShipRanking
    # __slots__ += ('experience', 'experience_factor', 'rank', 'ranks', 'rank_images')
    #
    # # PanZoomShipButtons
    # __slots__ += ("visible", "speed_up_button", "radius_button")
    #
    # # PanZoomShipDraw
    # __slots__ += ('frame_color', 'noenergy_image', 'noenergy_image_x', 'noenergy_image_y', 'moving_image',
    #               'sleep_image', 'orbit_image', 'rank_image_pos', 'progress_bar')
    #
    # # PanZoomMouseHandler
    # __slots__ += ("_on_hover", "on_hover_release")
    #
    # # PanZoomShipInteraction
    # __slots__ += ('orbiting', '_selected', 'target')
    #
    # # combined __slots__
    # __slots__ = PanZoomGameObject.__slots__ + ("id", 'item_collect_distance', 'orbit_direction', 'speed', 'property',
    #              'rotate_correction_angle', 'orbit_object', 'orbit_angle', 'collect_text',
    #              'target_object', 'target_object_reset_distance_raw',
    #              'target_object_reset_distance', 'hum_playing', '_orbit_object',
    #              'gun_power', 'gun_power_max', 'interface_variable_names',
    #              'reload_max_distance_raw', 'reload_max_distance', 'reload_max_distance_max_raw',
    #              'reload_max_distance_max', 'name', 'parent', 'hum', 'sound_channel', 'energy_use', 'food', 'food_max',
    #              'minerals', 'minerals_max', 'water', 'water_max', 'population', 'population_max', 'technology',
    #              'technology_max', 'resources', 'energy_max', 'energy', 'energy_reloader', 'energy_reload_rate',
    #              'move_stop', 'crew', 'crew_max', 'crew_members', 'fog_of_war_radius', 'fog_of_war_radius_max',
    #              'upgrade_factor', 'upgrade_factor_max', 'tooltip', 'attack_distance_raw', 'attack_distance', 'attack_distance_max', 'desired_orbit_radius_raw',
    #              'desired_orbit_radius', 'desired_orbit_radius_max', 'enemy', '_moving', '_orbiting',
    #              'orbit_speed', 'orbit_speed_max', 'zoomable', 'min_dist_to_other_ships',
    #              'min_dist_to_other_ships_max', 'orbit_radius', 'orbit_radius_max', 'experience', 'experience_factor', 'rank', 'ranks', 'rank_images',
    #              'visible', 'speed_up_button', 'radius_button', 'frame_color', 'noenergy_image', 'noenergy_image_x', 'noenergy_image_y', 'moving_image',
    #              'sleep_image', 'orbit_image', 'rank_image_pos', 'progress_bar', '_on_hover', 'on_hover_release', 'orbiting', '_selected')

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        PanZoomShipParams.__init__(self, **kwargs)
        PanZoomShipMoving.__init__(self, kwargs)
        PanZoomShipRanking.__init__(self)
        PanZoomShipDraw.__init__(self, kwargs)
        PanZoomShipInteraction.__init__(self, kwargs)
        self.economy_agent = EconomyAgent(self)

        # init vars
        self.is_spacestation = kwargs.get("is_spacestation", False)
        self.spacestation = Spacestation(self) if self.is_spacestation else None

        self.name = kwargs.get("name", "no_name")
        self.data = kwargs.get("data", {})
        self.owner = self.data.get("owner", -1)
        self.player_color = pygame.color.THECOLORS.get(player_handler.get_player_color(self.owner))
        self.item_collect_distance = SHIP_ITEM_COLLECT_DISTANCE
        self.orbit_direction = 1  # random.choice([-1, 1])
        self.speed = SHIP_SPEED
        self.attack_distance_raw = 200
        self.property = "ship"
        self.rotate_correction_angle = SHIP_ROTATE_CORRECTION_ANGLE
        self.orbit_object_name = kwargs.get("orbit_object_name", "")
        self.orbit_object = None
        self.orbit_angle = None
        self.collect_text = ""

        # target object
        self.target_object = PanZoomTargetObject(config.win,
                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                25, 25, pan_zoom_handler, "target.gif", align_image="center", debug=False,
                group="target_objects", parent=self, zoomable=False, relative_gif_size=2.0)
        self.target_object_reset_distance_raw = SHIP_TARGET_OBJECT_RESET_DISTANCE
        self.target_object_reset_distance = self.target_object_reset_distance_raw

        # sound
        self.hum_playing = False

        # orbit
        self._orbit_object = None

        # interface
        self.interface_variable_names = [
            "food",
            "minerals",
            "water",
            "technology",
            "energy",
            "crew",
            "fog_of_war_radius",
            "upgrade_factor",
            "reload_max_distance_raw",
            "attack_distance_raw",
            "desired_orbit_radius_raw",
            "speed",
            "orbit_speed",
            "orbit_radius",
            "min_dist_to_other_ships",
            "energy_use"
            ]

        # weapon handler
        self.weapon_handler = WeaponHandler(self, kwargs.get("current_weapon", "laser"), weapons=kwargs.get("weapons", {}))

        # autopilot
        self.autopilot_handler = AutopilotHandler(self)
        self.autopilot = False

        # register
        sprite_groups.ships.add(self)

        # init interface data
        InterfaceData.__init__(self, self.interface_variable_names)

        # setup the ship
        self.setup()

    # def __repr__(self):
    #     return (f"pan_zoom_ship: state: {self.state_engine.state}\n"
    #             f"moving: {self.moving}, following_path:{self.following_path}")

    def __delete__(self, instance):
        # remove all references
        if self in sprite_groups.ships:
            sprite_groups.ships.remove(self)

        if self.target_object in sprite_groups.ships:
            sprite_groups.ships.remove(self.target_object)

        self.target_object.kill()

        try:
            if self in self.parent.box_selection.selectable_objects:
                self.parent.box_selection.selectable_objects.remove(self)
        except:
            pass
        if hasattr(self, "progress_bar"):
            WidgetHandler.remove_widget(self.progress_bar)

        self.progress_bar = None

        self.state_engine.end_object()
        self.state_engine = None
        self.kill()

    def end_object(self):
        self.__delete__(self)

    # def update_rect(self):
    #     if not self.image_raw:
    #         return
    #     if hasattr(self, "angle"):
    #         self.image = rotate_image_cached( scale_image_cached(self.image_raw, (self.screen_width * self.shrink, self.screen_height * self.shrink)), self.angle  +self.rotate_correction_angle)
    #     else:
    #         self.image = scale_image_cached(self.image_raw, (self.screen_width * self.shrink, self.screen_height * self.shrink))
    #
    #
    #     self.rect = self.image.get_rect()
    #
    #     self.align_image_rect()

    # def update_rect(self):
    #     pass

    def setup(self):
        data = self.data
        if not data:
            data = load_file("ship_settings.json", "config")[self.name]

        for key, value in data.items():
            setattr(self, key, value)

        # set orbit object
        if self.orbit_object_id != -1 and self.orbit_object_name:
            # if orbit object is in planets
            if self.orbit_object_name in [i.name for i in sprite_groups.planets.sprites()]:
                self.orbit_object = [i for i in sprite_groups.planets.sprites() if
                                     i.id == self.orbit_object_id and i.name == self.orbit_object_name][0]

            # if orbit object is in ships
            elif self.orbit_object_name in [i.name for i in sprite_groups.ships.sprites()]:
                self.orbit_object = [i for i in sprite_groups.ships.sprites() if
                                     i.id == self.orbit_object_id and i.name == self.orbit_object_name][0]

            # if orbit object is in ufos
            elif self.orbit_object_name in [i.name for i in sprite_groups.ufos.sprites()]:
                self.orbit_object = [i for i in sprite_groups.ufos.sprites() if
                                     i.id == self.orbit_object_id and i.name == self.orbit_object_name][0]

        self.orbit_radius = 100 + (self.id * 30)

    def open_weapon_select(self):
        if not self.owner == config.app.game_client.id:
            return

        self.set_info_text()
        if config.app.weapon_select.obj == self:
            config.app.weapon_select.set_visible()
        else:
            config.app.weapon_select.obj = self

    def set_target(self, **kwargs):
        target = kwargs.get("target", sprite_groups.get_hit_object(lists=["ships", "planets", "collectable_items",
                                                                          "ufos"]))
        from_server = kwargs.get("from_server", None)

        if target == self:
            return

        if target:
            if not self.pathfinding_manager.path:
                self.target = target
            else:
                self.pathfinding_manager.move_to_next_node()
                self.enemy = None

            self.set_energy_reloader(target)
        else:
            self.target = self.target_object
            self.enemy = None
            self.orbit_object = None

            # set target object position
            self.target.world_x, self.target.world_y = pan_zoom_handler.get_mouse_world_position()
            self.set_energy_reloader(None)

        self.select(False)

        # fix the case if attacking and setting new target
        if self.target:
            if self.target != self.enemy:
                self.enemy = None
                self.orbit_object = None
                self.state_engine.set_state("moving")

        # send data to server, only if not called from server !!!
        if not from_server:
            config.app.game_client.send_message(self.get_network_data("set_target"))

    def get_network_data(self, function: str):
        if function == "set_target":
            data = {
                "f": function,
                "object_sprite_group": self.group,
                "object_id": self.id,
                "target_sprite_group": self.target.group,
                "target_id": self.target.id,
                "target_type": self.target.type,
                "target_world_x": self.target.world_x,
                "target_world_y": self.target.world_y
                }

            return data

        if function == "position_update":
            data = {
                "x": int(self.world_x),
                "y": int(self.world_y),
                "e": int(self.experience)
                }

            return data

    def activate_traveling(self):
        if self.selected:
            self.set_target()
            self.orbit_object = None
            hit_object = sprite_groups.get_hit_object(lists=["ships", "planets", "collectable_items"])
            if hit_object:
                self.set_energy_reloader(hit_object)

            # follow path
            if hasattr(self, "pathfinding_manager"):
                self.pathfinding_manager.follow_path(hit_object)

    def handle_autopilot(self):
        if self.autopilot:
            self.autopilot_handler.update()

        if config.enable_autopilot:
            if not self.autopilot:
                self.autopilot = config.enable_autopilot

    def handle_move_stop(self):
        # move stopp reset
        if self.energy > 0:
            self.move_stop = 0
        # move stopp
        if self.energy <= 0:
            self.move_stop = 1
            sounds.stop_sound(self.sound_channel)

    def reset_target(self):
        if not hasattr(self.target, "property"):
            if not self.moving:
                self.target = None
        self.deselect()

    # def deselect(self):
    #     if config.app.ship == self:
    #         config.app.ship = None

    def move_towards_target(self):
        self.state_engine.set_state("moving")
        direction = self.target_position - Vector2(self.world_x, self.world_y)
        distance = direction.length() * pan_zoom_handler.get_zoom()
        speed = self.set_speed()

        # Normalize the direction vector
        if not direction.length() == 0.0:
            try:
                direction.normalize()
            except ValueError as e:
                print("move_towards_target: exc:", e)

        # Calculate the displacement vector for each time step
        displacement = direction * speed * time_handler.game_speed

        # Calculate the number of time steps needed to reach the target position
        time_steps = int(distance / speed) / pan_zoom_handler.get_zoom()

        # Move the obj towards the target position with a constant speed
        if time_steps:
            if config.app.game_client.is_host:
                self.world_x += displacement.x / time_steps
                self.world_y += displacement.y / time_steps
                # self.set_world_position((self.world_x, self.world_y))

        self.reach_target(distance / pan_zoom_handler.get_zoom())



    def update(self):
        # if not config.app.game_client.is_host:
        #     return

        # update pathfinder
        # self.pathfinding_manager.update()

        # update state engine
        self.state_engine.handle_state()
        self.state_engine.update()

        # update game object
        self.update_pan_zoom_game_object()

        # update progressbar position
        self.progress_bar.set_progressbar_position()

        # return if game paused
        if config.game_paused:
            return

        # why setting th tooltip every frame ?? makes no sense --- but needet for correct work
        self.set_tooltip()
        self.listen()

        self.set_distances()

        # also setting the info text is questionable every frame
        self.set_info_text()

        # show/ hide target object
        if self.state_engine.state == "moving":
            if self.target == self.target_object:
                self.target_object.show()
        else:
            self.target_object.hide()

        # handle progressbar visibility
        # maybe we don't need inside screen here, because it is checked in WidgetHandler and pan_zoom_sprite_handler
        if level_of_detail.inside_screen(self.rect.center):
            if config.show_ship_state:
                self.progress_bar.show()
            else:
                self.progress_bar.hide()
            # prevent_object_overlap(sprite_groups.ships, self.min_dist_to_other_ships)
        else:
            self.progress_bar.hide()

        """ TODO:check out logic here """
        # draw selection and connections
        if self.selected:
            self.state_engine.set_state("waiting for order")
            if self == config.app.ship:
                self.draw_selection()
                # if self.orbit_object:
                #     self.draw_connections(self.orbit_object)

                # why setting the info text again ???
                # self.set_info_text()

            if not self.target and not self.energy_reloader:
                self.angle = rotate_image_to(self, pygame.mouse.get_pos(), self.rotate_correction_angle)

        # travel
        if self.target:  # and self == config.app.ship:
            # ??? agan setting drawing the connections?
            self.draw_connections(self.target)
            # self.reach_target(math.dist(self.rect.center, self.target.rect.center))

        """until here"""
        # reload ship
        if self.energy_reloader:
            self.reload_ship()

        # update electro discharge, that thing that shows the electricity for reloading the ship
        self.update_electro_discharge()

        # move ship
        self.handle_move_stop()

        # reach target
        if self.target_reached and not self.selected:
            self.state_engine.set_state("sleeping")

        # attack enemies
        if self.enemy:
            orbit_ship(self, self.enemy, self.orbit_speed, self.orbit_direction)
            self.state_engine.set_state("attacking")
            # self.follow_target(self.enemy)
            self.weapon_handler.attack(self.enemy)
            self.weapon_handler.update_gun_positions()

        # orbit around objects
        if self.orbit_object:
            orbit_ship(self, self.orbit_object, self.orbit_speed, self.orbit_direction)

        # autopilot
        self.handle_autopilot()

        # consume energy for traveling
        self.consume_energy_if_traveling()

        # produce energy if spacestation
        if self.spacestation:
            self.spacestation.produce_energy()

        # set previous position, used for energy consumption calculation
        # make shure this is the last task, otherwise it wouldn't work(probably)
        self.previous_position = (self.world_x, self.world_y)

        # self.rot_rect.draw(self.win)
        # self.weapon_handler.weapon_rack.draw(self.win)

        if not self.owner == 0:
            return


        # state_variables = self.state_engine.state_variables
        # x,y = 260, 80
        # for t in state_variables:
        #     drawText(self.parent.win, f"{t}: {getattr(self, t)}", colors.frame_color, (
        #         x,y, 400, 30), pygame.sysfont.SysFont(config.font_name, 16), "left")
        #
        #     y += 18

    def draw(self):  # unused
        print("drawing ---")
