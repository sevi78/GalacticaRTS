import math
import random

import pygame
from pygame import Vector2

from source.configuration.game_config import config
from source.draw.scope import scope
from source.gui.event_text import event_text
from source.gui.interfaces.interface import InterfaceData
from source.gui.lod import level_of_detail
from source.gui.widgets.moving_image import MovingImage, SPECIAL_TEXT_COLOR
from source.handlers.autopilot_handler import AutopilotHandler
from source.handlers.color_handler import colors
from source.handlers.file_handler import load_file
from source.handlers.mouse_handler import MouseState, mouse_handler
from source.handlers.orbit_handler import orbit_ship
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.position_handler import prevent_object_overlap
from source.handlers.weapon_handler import WeaponHandler
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image
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
from source.text.text_formatter import format_number


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

    # combined __slots__
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

        # init vars
        self.is_spacestation = kwargs.get("is_spacestation", False)
        self.spacestation = Spacestation(self) if self.is_spacestation else None

        self.name = kwargs.get("name", "no_name")
        self.data = kwargs.get("data", {})
        self.owner = self.data.get("owner", -1)
        self.player_color = pygame.color.THECOLORS.get(player_handler.get_player_color(self.owner))
        self.item_collect_distance = SHIP_ITEM_COLLECT_DISTANCE
        self.orbit_direction = random.choice([-1, 1])
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
        if hasattr(self.parent, "box_selection"):
            if not self in self.parent.box_selection.selectable_objects:
                self.parent.box_selection.selectable_objects.append(self)

        # init interface data
        InterfaceData.__init__(self, self.interface_variable_names)

        # setup the ship
        self.setup()

    def __repr__(self):
        return (f"pan_zoom_ship: state: {self.state_engine.state}\n"
                f"moving: {self.moving}, following_path:{self.following_path}")

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
        self.kill()

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

    def load_cargo(self):
        if self.target.collected:
            return
        self.collect_text = ""
        waste_text = ""

        for key, value in self.target.resources.items():
            if value > 0:
                max_key = key + "_max"
                current_value = getattr(self, key)
                max_value = getattr(self, max_key)

                # Load as much resources as possible
                load_amount = min(value, max_value - current_value)
                setattr(self, key, current_value + load_amount)

                # Update collect_text
                self.collect_text += str(load_amount) + " of " + key + " "

                # Update waste_text
                if load_amount < value:
                    waste_text += str(value - load_amount) + " of " + key + ", "

                # show what is loaded
                self.add_moving_image(key, "", value, (
                    random.uniform(-0.8, 0.8), random.uniform(-1.0, -1.9)), 3, 30, 30, self, None)

        special_text = " Specials: "
        if len(self.target.specials) != 0:
            for i in self.target.specials:
                self.specials.append(i)
                special_text += f"{i}"
                key_s, operand_s, value_s = i.split(" ")

                self.add_moving_image(key_s, operand_s, value_s, (0, random.uniform(-0.3, -0.6)), 5, 50, 50, self, None)

        self.target.specials = []

        if waste_text:
            self.collect_text += f". because the ship's loading capacity was exceeded, the following resources were wasted: {waste_text[:-2]}!"

        self.set_resources()
        self.set_info_text()
        sounds.play_sound(sounds.collect_success)

        event_text.set_text(f"You are a Lucky Guy! you just found some resources: {special_text}, " + self.collect_text, obj=self)
        self.target.collected = True

    def unload_cargo(self):
        text = ""
        for key, value in self.resources.items():
            if value > 0:
                text += key + ": " + str(value) + ", "
                if not key == "energy":
                    setattr(self.parent.players[self.owner], key, getattr(self.parent.players[self.owner], key) + value)
                    self.resources[key] = 0
                    setattr(self, key, 0)
                    if hasattr(config.app.resource_panel, key + "_icon"):
                        target_icon = getattr(config.app.resource_panel, key + "_icon").rect.center
                        self.add_moving_image(
                                key,
                                "",
                                value,
                                (random.uniform(-10.8, 10.8),
                                 random.uniform(-1.0, -1.9)),
                                4,
                                30,
                                30,
                                self.target, target_icon)

        special_text = ""
        for i in self.specials:
            self.target.specials.append(i)
            special_text += f"found special: {i.split(' ')[0]} {i.split(' ')[1]} {i.split(' ')[2]}"
            key_s, operand_s, value_s = i.split(" ")
            self.add_moving_image(
                    key_s,
                    operand_s,
                    value_s,
                    (0, random.uniform(-0.3, -0.6)),
                    5,
                    50,
                    50,
                    self.target,
                    None)
        self.specials = []

        if not text:
            return

        # set event text
        event_text.set_text("unloading ship: " + text[:-2], obj=self)

        # play sound
        sounds.play_sound(sounds.unload_ship)

    def add_moving_image(self, key, operand, value, velocity, lifetime, width, height, parent, target):
        if operand == "*":
            operand = "x"

        if key == "buildings_max":
            image_name = "building_icon.png"
        else:
            image_name = f"{key}_25x25.png"

        image = get_image(image_name)
        MovingImage(
                self.win,
                self.get_screen_x(),
                self.get_screen_y(),
                width,
                height,
                image,
                lifetime,
                velocity,
                f" {value}{operand}", SPECIAL_TEXT_COLOR,
                "georgiaproblack", 1, parent, target=target)

    def open_weapon_select(self):
        self.set_info_text()
        if config.app.weapon_select.obj == self:
            config.app.weapon_select.set_visible()
        else:
            config.app.weapon_select.obj = self

    def set_target(self, **kwargs):
        target = kwargs.get("target", sprite_groups.get_hit_object(lists=["ships", "planets"]))

        if target == self:
            return

        if target:
            if not self.pathfinding_manager.path:
                self.target = target
            else:
                # self.target = self.pathfinding_manager.path[1].owner
                self.pathfinding_manager.move_to_next_node()
                self.enemy = None

            self.set_energy_reloader(target)
        else:
            self.target = self.target_object
            self.enemy = None

            # set target object position
            self.target.world_x, self.target.world_y = self.pan_zoom.get_mouse_world_position()
            self.set_energy_reloader(None)

        self.select(False)

    def move_towards_target(self):
        self.state_engine.set_state("moving")
        direction = self.target_position - Vector2(self.world_x, self.world_y)
        distance = direction.length() * self.get_zoom()
        speed = self.set_speed()

        # Normalize the direction vector
        if not direction.length() == 0.0:
            try:
                direction.normalize()
            except ValueError as e:
                print("move_towards_target: exc:", e)

        # Calculate the displacement vector for each time step
        displacement = direction * speed * config.game_speed

        # Calculate the number of time steps needed to reach the target position
        time_steps = int(distance / speed) / self.get_zoom()

        # Move the obj towards the target position with a constant speed
        if time_steps:
            self.world_x += displacement.x / time_steps
            self.world_y += displacement.y / time_steps
            # self.set_world_position((self.world_x, self.world_y))

        self.reach_target(distance / self.get_zoom())

    def listen(self):
        config.app.tooltip_instance.reset_tooltip(self)
        if not config.app.weapon_select._hidden:
            return

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()

            if self.collide_rect.collidepoint(x, y):
                if mouse_handler.double_clicks == 1:
                    self.open_weapon_select()

                if mouse_state == MouseState.RIGHT_CLICK:
                    if config.app.ship == self:
                        self.select(True)

                if mouse_state == MouseState.LEFT_RELEASE and self.clicked:
                    self.clicked = False

                elif mouse_state == MouseState.LEFT_CLICK:
                    self.clicked = True
                    self.select(True)
                    config.app.ship = self

                elif mouse_state == MouseState.LEFT_DRAG and self.clicked:
                    pass

                elif mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                    self.submit_tooltip()
                    self.win.blit(pygame.transform.scale(self.image_outline, self.rect.size), self.rect)
                    self.weapon_handler.draw_attack_distance()

                    # set cursor
                    config.app.cursor.set_cursor("ship")
            else:
                # not mouse over object
                self.clicked = False
                if mouse_state == MouseState.LEFT_CLICK:
                    self.reset_target()

                if mouse_state == MouseState.RIGHT_CLICK:
                    self.activate_traveling()

    def activate_traveling(self):
        if self.selected:
            self.set_target()
            self.orbit_object = None
            hit_object = sprite_groups.get_hit_object()
            if hit_object:
                self.set_energy_reloader(hit_object)

            # follow path
            if hasattr(self, "pathfinding_manager"):
                self.pathfinding_manager.follow_path(hit_object)

    def reset_target(self):
        if not hasattr(self.target, "property"):
            if not self.moving:
                self.target = None
        self.deselect()

    def deselect(self):
        if config.app.ship == self:
            config.app.ship = None

    def update(self):
        # update pathfinder
        self.pathfinding_manager.update()

        # update state engine
        self.state_engine.update()

        # update game object
        self.update_pan_zoom_game_object()

        # update progressbar position
        self.progress_bar.set_progressbar_position()

        # return if game paused
        if config.game_paused:
            return

        # why setting th tooltip every frame ?? makes no sense ---
        self.set_tooltip()
        self.listen()
        if self.selected:
            pre_calculated_energy_use = self.energy_use * math.dist(self.rect.center, pygame.mouse.get_pos()) / pan_zoom_handler.zoom
            if config.app.weapon_select._hidden:
                scope.draw_scope(self.rect.center, self.get_max_travel_range(), {"energy use": format_number(pre_calculated_energy_use, 1)})
                scope.draw_range(self)

        self.set_distances()
        # pygame.draw.circle(self.win, self.frame_color, self.rect.center, self.attack_distance, 1)

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
            self.progress_bar.show()
            prevent_object_overlap(sprite_groups.ships, self.min_dist_to_other_ships)
        else:
            self.progress_bar.hide()

        # draw selection and connections
        if self.selected and self == config.app.ship:
            self.draw_selection()
            if self.orbit_object:
                self.draw_connections(self.orbit_object)
            # why setting the info text again ???
            self.set_info_text()

        # ??? again setting drawing the selection ?
        if self == config.app.ship:
            self.draw_selection()

        # travel
        if self.target and self == config.app.ship:
            # ??? agan setting drawing the connections?
            self.draw_connections(self.target)

        # reload ship
        if self.energy_reloader:
            # reload ship
            self.reload_ship()

        self.handle_move_stop()

        # reach target
        if self.target_reached:
            self.state_engine.set_state("sleeping")

        # attack enemies
        if self.enemy:
            orbit_ship(self, self.enemy, self.orbit_speed, self.orbit_direction)
            self.follow_target(self.enemy)
            self.weapon_handler.attack(self.enemy)

        # orbit around objects
        if self.orbit_object:
            orbit_ship(self, self.orbit_object, self.orbit_speed, self.orbit_direction)

        # again reload ship???
        if self.energy_reloader:
            # reload ship
            self.reload_ship()

        # autopilot
        self.handle_autopilot()

        # consume energy for traveling
        self.consume_energy_if_traveling()

        # produce energy if spacestation
        if self.spacestation:
            self.spacestation.produce_energy()

        # set previous position, used for energy consumption calculation
        # make shure this is the last task, otherwise it would work(probably)
        self.previous_position = (self.world_x, self.world_y)

        # pygame.draw.circle(self.win, colors.ui_white, self.rect.center,self.attack_distance, 1)

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

    def draw(self):  # unused
        print("drawing ---")
