import random

import pygame
from pygame import Vector2

from source.draw import scope
from source.gui.event_text import event_text
from source.gui.lod import inside_screen
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_buttons import PanZoomShipButtons
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_draw import PanZoomShipDraw
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_interaction import PanZoomShipInteraction
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_moving import PanZoomShipMoving
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_params import PanZoomShipParams, \
    SHIP_ITEM_COLLECT_DISTANCE, SHIP_SPEED, SHIP_ROTATE_CORRECTION_ANGLE, SHIP_TARGET_OBJECT_RESET_DISTANCE, \
    SHIP_GUN_POWER_MAX, SHIP_GUN_POWER, SHIP_INSIDE_SCREEN_BORDER
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_ranking import PanZoomShipRanking
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_game_object import PanZoomGameObject
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_mouse_handler import PanZoomMouseHandler
from source.pan_zoom_sprites.pan_zoom_target_object import PanZoomTargetObject
from source.utils import global_params
from source.interaction.mouse import Mouse, MouseState
from source.utils.positioning import prevent_object_overlap, orbit, get_distance
from source.database.saveload import load_file


class PanZoomShip(PanZoomGameObject, PanZoomShipParams, PanZoomShipMoving, PanZoomShipRanking, PanZoomShipButtons, PanZoomShipDraw, PanZoomMouseHandler, PanZoomShipInteraction):
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
        PanZoomShipButtons.__init__(self)
        PanZoomShipDraw.__init__(self, kwargs)
        PanZoomMouseHandler.__init__(self)
        PanZoomShipInteraction.__init__(self)

        self.item_collect_distance = SHIP_ITEM_COLLECT_DISTANCE
        self.orbit_direction = random.choice([-1, 1])
        self.speed = SHIP_SPEED
        self.id = len(sprite_groups.ships)
        self.property = "ship"
        self.rotate_correction_angle = SHIP_ROTATE_CORRECTION_ANGLE
        self.orbit_object = None
        self.orbit_angle = None
        self.collect_text = ""

        self.target_object = PanZoomTargetObject(global_params.win,
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
            60, 60, pan_zoom_handler, "target.gif", align_image="center", debug=False,
            group="target_objects", parent=self, zoomable=False, relative_gif_size=2.0)
        self.target_object_reset_distance_raw = SHIP_TARGET_OBJECT_RESET_DISTANCE
        self.target_object_reset_distance = self.target_object_reset_distance_raw

        # sound
        self.hum_playing = False

        # orbit
        self._orbit_object = None

        # gun
        self.gun_power = SHIP_GUN_POWER
        self.gun_power_max = SHIP_GUN_POWER_MAX

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
            ]

        # register
        sprite_groups.ships.add(self)
        if hasattr(self.parent, "box_selection"):
            if not self in self.parent.box_selection.selectable_objects:
                self.parent.box_selection.selectable_objects.append(self)

    def setup(self):
        data = load_file("ship_settings.json")
        for name, dict in data.items():
            if name == self.name:
                for key, value in dict.items():
                    if key in self.__dict__:
                        setattr(self, key, value)

        self.orbit_radius = 100 + self.id * 30

    def set_target(self):
        target = self.get_hit_object()
        if target == self:
            return

        if target:
            self.target = target
            self.set_energy_reloader(target)
        else:
            self.target = self.target_object
            self.enemy = None

            # set target object position
            self.target.world_x, self.target.world_y = self.pan_zoom.get_mouse_world_position()
            self.set_energy_reloader(None)

        self.select(False)

    def move_towards_target(self):
        direction = self.target_position - Vector2(self.world_x, self.world_y)
        distance = direction.length() * self.get_zoom()
        speed = self.set_speed()

        # Normalize the direction vector
        if not direction == 0:
            direction.normalize()

        # Calculate the displacement vector for each time step
        displacement = direction * speed * global_params.time_factor

        # Calculate the number of time steps needed to reach the target position
        time_steps = int(distance / speed) / self.get_zoom()

        # Move the obj towards the target position with a constant speed
        if time_steps:
            self.world_x += displacement.x / time_steps
            self.world_y += displacement.y / time_steps

        self.reach_target(distance)

    def follow_target(self, obj):
        target_position = Vector2(obj.world_x, obj.world_y)
        current_position = Vector2(self.world_x, self.world_y)

        direction = target_position - current_position
        distance = direction.length() * self.get_zoom()
        speed_ = self.set_speed()

        if distance > self.attack_distance:
            direction.normalize()

            # Get the speed of the obj

            speed = (speed_ + obj.speed)
            if speed > self.set_speed():
                speed = self.set_speed()

            # Calculate the displacement vector for each time step
            displacement = direction * speed * global_params.time_factor / global_params.fps

            # Move the obj towards the target position with a constant speed
            self.world_x += displacement.x
            self.world_y += displacement.y

    def reach_target(self, distance):
        if self.target.property == "ufo":
            if distance <= self.attack_distance:
                self.moving = False
                self.reach_enemy()
                return

            # print("reached_ufo")
        elif self.target.property == "planet":
            # Check the distance
            if distance < self.desired_orbit_radius:
                self.reach_planet()
                self.target_reached = True
                self.moving = False
                self.orbit_object = self.target
                return

        elif self.target.property == "item":
            if distance < self.item_collect_distance:
                self.moving = False

                self.load_cargo()
                self.target.end_object()
                self.target = None
                self.target_reached = True
                return

        elif self.target.property == "target_object":

            if distance < self.target_object_reset_distance:
                self.moving = False
                self.target = None
                self.target_reached = True

    def attack(self, defender):
        if not inside_screen(self.get_screen_position()):
            return

        r0 = random.randint(-4, 5)
        r = random.randint(-3, 4)

        startpos = (self.rect.centerx, self.rect.centery)
        endpos = (defender.rect.centerx + r0, defender.rect.centery + r0)

        # shoot laser
        if r == 2 and defender.energy > 0:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["white"], width=2)

            # make damage to target
            defender.energy -= self.gun_power
            sounds.play_sound(sounds.laser)

        if defender.energy <= defender.energy_max / 2:
            defender.target = self

        if defender.energy <= 0:
            # explode
            defender.end_object()
            self.enemy = None

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

        if waste_text:
            self.collect_text += ". because the ship's loading capacity was exceeded, the following resources were wasted: " + waste_text[
                                                                                                                               :-2] + " !"

        self.set_resources()
        self.set_info_text()
        sounds.play_sound(sounds.collect_success)
        event_text.text = "You are a Lucky Guy! you just found some resources: " + self.collect_text
        self.target.collected = True

    def unload_cargo(self):
        text = ""
        for key, value in self.resources.items():
            if value > 0:
                text += key + ": " + str(value) + ", "
                setattr(self.parent.player, key, getattr(self.parent.player, key) + value)
                self.resources[key] = 0
                setattr(self, key, 0)

        if not text:
            return

        event_text.text = "unloading ship: " + text[:-2]
        sounds.play_sound(sounds.unload_ship)

    def listen(self):
        global_params.app.tooltip_instance.reset_tooltip(self)

        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.rect.collidepoint(x, y):  # self.contains(x, y): #
                if mouseState == MouseState.RIGHT_CLICK:
                    if global_params.app.ship == self:
                        if self.selected:
                            pass
                            # self.select(False)
                        else:
                            self.select(True)

                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.select(True)
                    global_params.app.ship = self

                elif mouseState == MouseState.DRAG and self.clicked:
                    pass

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.submit_tooltip()
                    self.draw_hover_circle()
            else:
                self.clicked = False

                if mouseState == MouseState.CLICK:
                    # if self.selected:
                    #     self.select(False)
                    if not hasattr(self.target, "property"):
                        if not self.moving:
                            self.target = None

                    if global_params.app.ship == self:
                        global_params.app.ship = None

                if mouseState == MouseState.RIGHT_CLICK:
                    if self.selected:
                        self.set_target()
                        self.orbit_object = None
                        if self.get_hit_object():
                            self.set_energy_reloader(self.get_hit_object())

    def update(self):
        self.update_pan_zoom_game_object()
        self.progress_bar.set_progressbar_position()
        if global_params.game_paused:
            return

        self.set_tooltip()
        self.listen()
        self.reposition_buttons()

        scope.draw_scope(self)
        self.set_distances()

        self.set_info_text()
        if self.moving:
            if self.target == self.target_object:
                self.target_object.show()

            self.set_experience(1)
            if self.target:
                self.calculate_travel_cost(get_distance(self.rect.center, self.target.rect.center))

        else:
            self.target_object.hide()

        if inside_screen(self.rect.center, border=SHIP_INSIDE_SCREEN_BORDER):
            self.progress_bar.show()
            self.draw_state()
            self.draw_rank_image()
            prevent_object_overlap(sprite_groups.ships, self.min_dist_to_other_ships)
        else:
            self.hide_buttons()
            self.progress_bar.hide()

        if self.selected:
            self.draw_selection()
            self.set_info_text()
            self.show_buttons()
        else:
            self.hide_buttons()

        # travel
        if self.target:
            self.draw_connections()

        if self.energy_reloader:
            # reload ship
            self.reload_ship()

        # move stopp reset
        if self.energy > 0:
            self.move_stop = 0

        # move stopp
        if self.energy <= 0:
            self.move_stop += 1

            sounds.stop_sound(self.sound_channel)
            self.draw_noenergy_image()
            self.set_experience(-1)

        self.low_energy_warning()

        if self.target_reached:
            self.moving = False

        if self.enemy:
            orbit(self, self.enemy, self.orbit_speed, self.orbit_direction)
            self.follow_target(self.enemy)
            self.attack(self.enemy)

        if self.orbit_object:
            orbit(self, self.orbit_object, self.orbit_speed, self.orbit_direction)

        if self.energy_reloader:
            # reload ship
            self.reload_ship()
