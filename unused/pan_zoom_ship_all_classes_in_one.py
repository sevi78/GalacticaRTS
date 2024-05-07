import math
import random

import pygame
from pygame import Vector2

from source.configuration.game_config import config
from source.draw.arrow import draw_arrows_on_line_from_start_to_end
from source.draw.scope import scope
from source.game_play.ranking import Ranking
from source.gui.event_text import event_text
from source.gui.lod import level_of_detail
from source.gui.widgets.moving_image import MovingImage, SPECIAL_TEXT_COLOR
from source.gui.widgets.progress_bar import ProgressBar
from source.handlers.autopilot_handler import AutopilotHandler
from source.handlers.color_handler import colors
from source.handlers.file_handler import load_file
from source.handlers.mouse_handler import MouseState, mouse_handler
from source.handlers.orbit_handler import orbit_ship
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.player_handler import player_handler
from source.handlers.position_handler import prevent_object_overlap
from source.handlers.weapon_handler import WeaponHandler
from source.handlers.widget_handler import WidgetHandler
from source.interaction.interaction_handler import InteractionHandler
from source.interfaces.interface import InterfaceData
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
from source.path_finding.a_star_node_path_finding import Node
from source.path_finding.pathfinding_manager import pathfinding_manager
from source.text.text_formatter import format_number

import math

import pygame.mouse

from source.configuration.game_config import config
from source.gui.event_text import event_text
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_state_engine import PanZoomShipStateEngine
from source.text.info_panel_text_generator import info_panel_text_generator

SHIP_SPEED = 1.5
SHIP_GUN_POWER = 30
SHIP_GUN_POWER_MAX = 50
SHIP_INSIDE_SCREEN_BORDER = 10
SHIP_ITEM_COLLECT_DISTANCE = 30
SHIP_ROTATE_CORRECTION_ANGLE = 90
SHIP_TARGET_OBJECT_RESET_DISTANCE = 15
SHIP_RELOAD_MAX_DISTANCE = 300
SHIP_RELOAD_MAX_DISTANCE_MAX = 600
SHIP_ENERGY_USE = 1
SHIP_ENERGY_USE_MAX = 10
SHIP_ENERGY = 10000
SHIP_ENERGY_MAX = 10000
SHIP_ENERGY_RELOAD_RATE = 0.1
SHIP_ORBIT_SPEED = 0.5
SHIP_ORBIT_SPEED_MAX = 0.6


class PanZoomShip(PanZoomGameObject):  # , PanZoomShipParams, PanZoomShipMoving, PanZoomShipRanking, PanZoomShipDraw, PanZoomShipInteraction, InterfaceData):
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

        self._move_stop = False
        self.move_stop = False
        self.orbiting = False
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        # InteractionHandler.__init__(self)

        self.state_engine = None
        # functionality
        # self.orbiting = False
        self._selected = False
        self.target = None
        self.autopilot = False


        self.frame_color = colors.frame_color

        # energy progress bar
        self.progress_bar = ProgressBar(win=self.win,
                x=self.get_screen_x(),
                y=self.get_screen_y() + self.get_screen_height() + self.get_screen_height() / 5,
                width=self.get_screen_width(),
                height=5,
                progress=lambda: 1 / self.energy_max * self.energy,
                curved=True,
                completedColour=self.frame_color,
                layer=self.layer,
                parent=self
                )
        # experience
        self.experience = 0
        self.experience_factor = 3000

        # ranking
        self.ranking = Ranking()
        self.rank = "Cadet"

        # PanZoomShipParams.__init__(self, **kwargs)
        # PanZoomShipMoving.__init__(self, kwargs)
        # PanZoomShipRanking.__init__(self)
        # PanZoomShipDraw.__init__(self, kwargs)
        # PanZoomShipInteraction.__init__(self)
        self.id = len(sprite_groups.ships)
        self.reload_max_distance_raw = SHIP_RELOAD_MAX_DISTANCE
        self.reload_max_distance = self.reload_max_distance_raw
        self.reload_max_distance_max_raw = SHIP_RELOAD_MAX_DISTANCE_MAX
        self.reload_max_distance_max = self.reload_max_distance_max_raw

        self.name = kwargs.get("name", "noname_ship")
        self.type = "ship"
        self.parent = kwargs.get("parent")
        self.hum = sounds.hum1
        self.sound_channel = 1
        self.energy_use = SHIP_ENERGY_USE
        self.energy_use_max = SHIP_ENERGY_USE_MAX
        self.info_panel_alpha = kwargs.get("info_panel_alpha", 255)

        # load_from_db Game variables
        self.food = kwargs.get("food", 100)
        self.food_max = 200
        self.minerals = kwargs.get("minerals", 100)
        self.minerals_max = 200
        self.water = kwargs.get("water", 100)
        self.water_max = 200
        self.population = kwargs.get("population", 100)
        self.population_max = 200
        self.technology = kwargs.get("technology", 100)
        self.technology_max = 200
        self.energy_max = SHIP_ENERGY_MAX
        self.energy = SHIP_ENERGY

        self.resources = {
            "minerals": self.minerals,
            "food": self.food,
            "energy": self.energy,
            "water": self.water,
            "technology": self.technology
            }
        self.specials = []

        self.energy_reloader = None
        self.energy_reload_rate = SHIP_ENERGY_RELOAD_RATE
        self.move_stop = 0
        self.crew = 7
        self.crew_max = 12
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war, no needed anymore
        self.fog_of_war_radius = 100
        self.fog_of_war_radius_max = 300

        # upgrade
        self.upgrade_factor = 1.5
        self.upgrade_factor_max = 3.0

        # tooltip
        self.tooltip = ""

        # uprade
        self.building_slot_amount = 1
        self.building_cue = 0
        self.buildings_max = 10
        self.buildings = []

        self.desired_orbit_radius_raw = 100
        self.desired_orbit_radius = self.desired_orbit_radius_raw
        self.desired_orbit_radius_max = 200
        self.target = None
        self.enemy = None
        self.orbit_speed = SHIP_ORBIT_SPEED
        self.orbit_speed_max = SHIP_ORBIT_SPEED_MAX
        self.zoomable = True
        self.min_dist_to_other_ships = 80
        self.min_dist_to_other_ships_max = 200
        self.orbit_radius = 100 + self.id * 30
        self.orbit_radius_max = 300
        self.previous_position = (self.world_x, self.world_y)

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

        # pathfinding
        self.node = Node(self.world_x, self.world_y, self)
        self.path = None

        # setup the ship
        self.setup()

    def __delete__(self, instance):
        # remove all references
        # if self in self.parent.ships:
        #     self.parent.ships.remove(self)
        self.state_engine.__del__()
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

        self.orbit_radius = 100 + self.id * 30

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def orbit_object(self):
        return self._orbit_object

    @orbit_object.setter
    def orbit_object(self, value):
        self._orbit_object = value

        if value:
            self.target = None
            self.orbiting = True
            self.orbit_direction = random.choice([-1, 1])
            self.orbit_object_id = value.id
            self.orbit_object_name = value.name
        else:
            self.orbiting = False
            self.orbit_angle = None
            self.orbit_object_id = -1
            self.orbit_object_name = ""

    @property
    def enemy(self):
        return self._enemy

    @enemy.setter
    def enemy(self, value):
        self._enemy = value
        if not value:
            self.orbit_angle = None
            self.orbit_object = None
            self.target_reached = False

    def select(self, value):
        self.selected = value
        if value:
            sounds.play_sound("click", channel=7)
            config.app.ship = self

    @property
    def orbiting(self):
        return self._orbiting

    @orbiting.setter
    def orbiting(self, value):
        self._orbiting = value
        if value:
            if self.target:
                self.set_orbit_object_id(self.target.id)

        if not hasattr(self, "state_engine"):
            self.state_engine = PanZoomShipStateEngine(self)
        self.state_engine.set_state()

    @property
    def moving(self):
        return self._moving

    @moving.setter
    def moving(self, value):
        self._moving = value
        if value == True:
            self.orbiting = False

        if not hasattr(self, "state_engine"):
            self.state_engine = PanZoomShipStateEngine(self)

        self.state_engine.set_state()

    @property
    def move_stop(self):
        return self._move_stop

    @move_stop.setter
    def move_stop(self, value):
        self._move_stop = value

        if not hasattr(self, "state_engine"):
            return
        self.state_engine.set_state()

    def set_experience(self, value):
        self.experience += value
        self.set_rank()

    def set_rank(self):
        # check if experience is big enough to upgrade
        rank_value = int(self.experience / self.experience_factor)

        # limit experience to int >0<8
        if rank_value < 0:
            rank_value = 0
        elif rank_value > 8:
            rank_value = 8

        # get previous rank fot text generation
        prev_rank = self.rank
        self.rank = self.ranking.ranks[rank_value]

        # set rank
        prev_key = next((key for key, value in self.ranking.ranks.items() if value == prev_rank), None)
        curr_key = next((key for key, value in self.ranking.ranks.items() if value == self.rank), None)

        # generate feedback for player, set event_text and play sound
        if curr_key > prev_key:
            event_text.set_text("Congratulations !!! Rank increased from {} to {} !!!".format(prev_rank, self.rank), obj=self)
            sounds.play_sound(sounds.rank_up)
        elif curr_key < prev_key:
            event_text.set_text("Shame on you !!! Rank decreased from {} to {} !!!".format(prev_rank, self.rank), obj=self)
            sounds.play_sound(sounds.rank_down)

    def set_speed(self):
        # adjust speed if no energy
        if self.move_stop > 0:
            speed = self.speed / 10
        else:
            speed = self.speed
        return speed

    def set_attack_distance(self):
        self.attack_distance = self.attack_distance_raw * self.get_zoom()

    def set_desired_orbit_radius(self):
        self.desired_orbit_radius = self.desired_orbit_radius_raw * self.get_zoom()

    def set_target_object_reset_distance(self):
        self.target_object_reset_distance = self.target_object_reset_distance_raw * self.get_zoom()

    def set_reload_max_distance(self):
        self.reload_max_distance = self.reload_max_distance_raw * self.get_zoom()

    def set_distances(self):
        self.set_attack_distance()
        self.set_desired_orbit_radius()
        self.set_target_object_reset_distance()
        self.set_reload_max_distance()

    def set_energy_reloader(self, obj):
        self.energy_reloader = obj

    def move_towards_target(self):
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

        self.reach_target(distance)

    def play_travel_sound(self):
        # plays sound
        if not self.hum_playing:
            sounds.play_sound(self.hum, channel=self.sound_channel, loops=1000, fade_ms=500)
            self.hum_playing = True

    def develop_planet(self):
        if self.target.explored:
            return

        self.set_experience(1000)
        self.parent.info_panel.set_planet_image(self.target.image_raw)
        self.target.get_explored(self.owner)

    def reach_target(self, distance):
        if self.target.property == "ufo":
            if distance <= self.attack_distance:
                self.moving = False
                self.reach_enemy()
                return

        elif self.target.property == "planet":
            if distance < self.desired_orbit_radius:
                self.reach_planet()
                self.target_reached = True
                self.moving = False
                self.orbit_object = self.target
                return

        elif self.target.property == "ship":
            if distance < self.desired_orbit_radius:
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

    def reach_enemy(self):
        self.target_reached = True
        self.orbit_object = self.target
        self.enemy = self.orbit_object
        self.moving = False

    def reach_planet(self):
        self.moving = False
        self.develop_planet()

        # unload_cargo goods
        if not self.target.type == "sun" and self.target.owner == self.owner or self.target.owner == -1:
            self.unload_cargo()

        self.set_energy_reloader(self.target)

        sounds.stop_sound(self.sound_channel)
        self.hum_playing = False

        if self.target.owner != self.owner:
            config.app.diplomacy_edit.open(self.target.owner, self.owner)

        # attack if hostile planet
        if not diplomacy_handler.is_in_peace(self.target.owner, config.player):
            self.reach_enemy()

    def follow_path(self):
        # update the nodes position
        self.node.update(self.world_x, self.world_y)

        # path follow
        if self.path:
            end_node = self.path[-1]
            self.path = []
            pathfinding_manager.generate_path(self.node, end_node, self.get_max_travel_range(), self)
            if self.path:
                self.target = self.path[1].owner

    def follow_target(self, obj):
        target_position = Vector2(obj.world_x, obj.world_y)
        current_position = Vector2(self.world_x, self.world_y)

        direction = target_position - current_position
        distance = direction.length() * self.get_zoom()
        speed_ = self.set_speed()

        if distance > self.attack_distance:
            direction.normalize()

            # Get the speed of the obj
            speed = 0.1
            if obj.property in ["ship", "ufo"]:
                speed = (speed_ + obj.speed)
            if obj.property == "planet":
                speed = obj.orbit_speed

            if speed > self.set_speed():
                speed = self.set_speed()

            # Calculate the displacement vector for each time step
            displacement = direction * speed * config.game_speed / config.fps
            # print(f"displacement: {displacement}")

            # Move the obj towards the target position with a constant speed
            self.world_x += displacement.x
            self.world_y += displacement.y

    def consume_energy_if_traveling(self):
        # only subtract energy if some energy is left
        if self.energy <= 0.0 or self.orbiting:
            return

        # subtract the traveled distance from the ships energy
        traveled_distance = math.dist((self.world_x, self.world_y), self.previous_position)
        self.energy -= traveled_distance * self.energy_use
        self.set_experience(traveled_distance * TRAVEL_EXPERIENCE_FACTOR)

    def get_max_travel_range(self):
        return self.energy / self.energy_use

    def set_resources(self):
        self.resources = {
            "minerals": self.minerals,
            "food": self.food,
            "population": self.population,
            "water": self.water,
            "technology": self.technology
            }

    def set_info_text(self):
        if not self == config.app.ship:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                text = info_panel_text_generator.create_info_panel_ship_text(self)
                self.parent.info_panel.set_text(text)
                self.parent.info_panel.set_planet_image(self.image_raw, alpha=self.info_panel_alpha)

            return

        text = info_panel_text_generator.create_info_panel_ship_text(self)
        self.parent.info_panel.set_text(text)
        self.parent.info_panel.set_planet_image(self.image_raw, alpha=self.info_panel_alpha)

    def set_tooltip(self):
        self.tooltip = f"{self.name}:  speed: {self.speed}"

    def submit_tooltip(self):
        if self.tooltip:
            if self.tooltip != "":
                config.tooltip_text = self.tooltip

    def reload_ship(self):
        """ this reloads the ships energy"""
        if self.energy_reloader:
            dist = math.dist(self.rect.center, self.energy_reloader.rect.center)
            if dist > self.reload_max_distance:
                return

            # if reloader is a planet
            if hasattr(self.energy_reloader, "production"):
                if self.energy_reloader.production["energy"] > 0:
                    if self.energy_reloader.owner in self.parent.players.keys():
                        if self.parent.players[self.energy_reloader.owner].energy - self.energy_reload_rate * \
                                self.energy_reloader.production[
                                    "energy"] > 0:
                            if self.energy < self.energy_max:
                                self.energy += self.energy_reload_rate * self.energy_reloader.production[
                                    "energy"] * config.game_speed
                                self.parent.players[self.energy_reloader.owner].energy -= self.energy_reload_rate * \
                                                                                          self.energy_reloader.production[
                                                                                              "energy"] * config.game_speed
                                self.flickering()
                            else:
                                event_text.set_text("PanZoomShip reloaded successfully!!!", obj=self)
                                sounds.stop_sound(self.sound_channel)

                if self.energy_reloader.type == "sun":
                    if self.energy < self.energy_max:
                        self.energy += self.energy_reload_rate * config.game_speed
                        self.flickering()

            # if relaoder is a ship
            elif hasattr(self.energy_reloader, "crew"):
                if self.energy_reloader.energy > 0:
                    if self.energy_reloader.energy - self.energy_reload_rate * config.game_speed > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate
                            self.energy_reloader.energy -= self.energy_reload_rate * config.game_speed
                            self.flickering()
                        else:
                            event_text.set_text("PanZoomShip reloaded successfully!!!", obj=self)
                            sounds.stop_sound(self.sound_channel)
        else:
            sounds.stop_sound(self.sound_channel)

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
                        self.add_moving_image(key, "", value, (random.uniform(-10.8, 10.8), random.uniform(-1.0, -1.9)),
                                4, 30, 30, self.target, target_icon)

        special_text = ""
        for i in self.specials:
            self.target.specials.append(i)
            special_text += f"found special: {i.split(' ')[0]} {i.split(' ')[1]} {i.split(' ')[2]}"
            key_s, operand_s, value_s = i.split(" ")
            self.add_moving_image(key_s, operand_s, value_s, (
                0, random.uniform(-0.3, -0.6)), 5, 50, 50, self.target, None)
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

    def set_target(self):
        target = sprite_groups.get_hit_object()
        if target == self:
            return

        if target:
            if not self.path:
                self.target = target

            else:
                self.target = self.path[1].owner
            self.set_energy_reloader(target)
        else:
            self.target = self.target_object
            self.enemy = None

            # set target object position
            self.target.world_x, self.target.world_y = self.pan_zoom.get_mouse_world_position()
            self.set_energy_reloader(None)

        self.select(False)

    def listen(self):
        config.app.tooltip_instance.reset_tooltip(self)
        if not config.app.weapon_select._hidden:
            return

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()

            if self.rect.collidepoint(x, y):

                # if mouse_state == MouseState.MIDDLE_RELEASE:
                if mouse_handler.double_clicks == 1:
                    self.open_weapon_select()

                if mouse_state == MouseState.RIGHT_CLICK:
                    if config.app.ship == self:
                        if self.selected:
                            pass
                            # self.select(False)
                        else:
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
                    # self.draw_hover_circle()
                    self.win.blit(pygame.transform.scale(self.image_outline, self.rect.size), self.rect)
                    # self.win.blit(self.image_outline, self.rect)

                    self.weapon_handler.draw_attack_distance()

                    # set cursor
                    config.app.cursor.set_cursor("ship")
            else:
                # not mouse over object
                self.clicked = False

                if mouse_state == MouseState.LEFT_CLICK:
                    # if self.selected:
                    #     self.select(False)
                    if not hasattr(self.target, "property"):
                        if not self.moving:
                            self.target = None

                    if config.app.ship == self:
                        config.app.ship = None

                if mouse_state == MouseState.RIGHT_CLICK:
                    if self.selected:
                        self.set_target()
                        self.orbit_object = None
                        if sprite_groups.get_hit_object():
                            self.set_energy_reloader(sprite_groups.get_hit_object())

                # draw path
                if self == config.app.ship:
                    hit_object = sprite_groups.get_hit_object(lists=["planets", "ships"])
                    if hit_object:
                        pathfinding_manager.update_nodes()
                        pathfinding_manager.generate_path(self.node, hit_object.node, self.get_max_travel_range(), self)

    def update(self):
        # path following
        self.follow_path()

        # update some stuff
        self.state_engine.update()
        self.update_pan_zoom_game_object()
        self.progress_bar.set_progressbar_position()
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

        # also setting the info text is questionable every frame
        self.set_info_text()
        if self.moving:
            if self.target == self.target_object:
                self.target_object.show()

        else:
            self.target_object.hide()

        # maybe we dont need inside screen here, because it is checked in WidgetHandler and pan_zoom_sprite_handler
        if level_of_detail.inside_screen(self.rect.center):
            self.progress_bar.show()
            prevent_object_overlap(sprite_groups.ships, self.min_dist_to_other_ships)
        else:
            # self.hide_buttons()
            self.progress_bar.hide()

        if self.selected:
            self.draw_selection()
            if self.orbit_object:
                self.draw_connections(self.orbit_object)
            # why setting the info text again ???
            self.set_info_text()

        if self == config.app.ship:
            self.draw_selection()

        # travel
        if self.target:
            self.draw_connections(self.target)

        if self.energy_reloader:
            # reload ship
            self.reload_ship()

        # move stopp reset
        if self.energy > 0:
            self.move_stop = 0

        # move stopp
        if self.energy <= 0:
            self.move_stop = 1
            sounds.stop_sound(self.sound_channel)

        if self.target_reached:
            self.moving = False

        if self.enemy:
            orbit_ship(self, self.enemy, self.orbit_speed, self.orbit_direction)
            # if self.enemy.property in ["ship", "ufo"]:
            self.follow_target(self.enemy)

            self.weapon_handler.attack(self.enemy)

            # if self.enemy.attitude < 50:
            #     self.weapon_handler.attack(self.enemy)
            # else:
            #     config.app.trade_edit.setup_trader(self, self.enemy)
            #     config.app.trade_edit.set_visible()
            #     self.enemy = None
            #     # self.target = None
            #     # self.moving = False
            #     print("here to setup trader")

        if self.orbit_object:
            orbit_ship(self, self.orbit_object, self.orbit_speed, self.orbit_direction)

        if self.energy_reloader:
            # reload ship
            self.reload_ship()

        if self.autopilot:
            self.autopilot_handler.update()

        if config.enable_autopilot:
            if not self.autopilot:
                self.autopilot = config.enable_autopilot

        # consume energy for traveling
        self.consume_energy_if_traveling()

        # produce energy if spacestation
        if self.spacestation:
            self.spacestation.produce_energy()

        # set previous position, used for energy consumation calculation
        # make shure this is the last task, otherwise it would work(probably)
        self.previous_position = (self.world_x, self.world_y)

    def flickering(self):
        if not level_of_detail.inside_screen(self.get_screen_position()):
            return
        # make flickering relaod stream :))
        r0 = random.randint(-4, 5)
        r = random.randint(-3, 4)
        r1 = random.randint(0, 17)
        r2 = random.randint(0, 9)

        startpos = (self.rect.center[0] + r, self.rect.center[1] + r)
        endpos = (self.energy_reloader.rect.center[0] + r0, self.energy_reloader.rect.center[1] + r0)

        if r0 == 0:
            return

        if r == 3:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                    color=pygame.color.THECOLORS["yellow"], width=r2)

        if r == 7:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                    color=pygame.color.THECOLORS["red"], width=r1)

        if r == 2:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                    color=pygame.color.THECOLORS["white"], width=r * 2)

        # pygame.mixer.Channel(2).play (sounds.electricity2)
        # sounds.play_sound(sounds.electricity2, channel=self.sound_channel)
        event_text.set_text("reloading spaceship: --- needs a lot of energy!", obj=self)

    def draw_selection(self):
        """ this handles how the ship is displayed on screen"""
        if config.show_player_colors:
            pygame.draw.circle(self.win, self.player_color, self.rect.center, self.get_screen_width(), int(6 * self.get_zoom()))
        else:
            pygame.draw.circle(self.win, self.frame_color, self.rect.center, self.get_screen_width(), int(6 * self.get_zoom()))

    def draw_connections(self, target):
        draw_arrows_on_line_from_start_to_end(
                surf=self.win,
                color=self.frame_color,
                start_pos=self.rect.center,
                end_pos=target.rect.center,
                width=1,
                dash_length=30,
                arrow_size=(0, 6),
                )

    def draw(self):  # unused
        print("drawing ---")
