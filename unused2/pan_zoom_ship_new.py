#
# import copy
# import math
# import random
# import time
#
# import pygame
# from pygame import Vector2
#
# from source.configuration.game_config import config
# from source.draw.arrow import draw_arrows_on_line_from_start_to_end
# from source.draw.scope import scope
# from source.economy.EconomyAgent import EconomyAgent
# from source.game_play.ranking import Ranking
# from source.gui.event_text import event_text
# from source.gui.interfaces.interface import InterfaceData
# from source.gui.lod import level_of_detail
# from source.gui.widgets.moving_image import MovingImage, SPECIAL_TEXT_COLOR
# from source.gui.widgets.progress_bar import ProgressBar
# from source.handlers.autopilot_handler import AutopilotHandler
# from source.handlers.color_handler import colors, get_average_color
# from source.handlers.diplomacy_handler import diplomacy_handler
# from source.handlers.file_handler import load_file
# from source.handlers.mouse_handler import mouse_handler, MouseState
# from source.handlers.orbit_handler import orbit_ship, set_orbit_object_id
# from source.handlers.pan_zoom_handler import pan_zoom_handler
# from source.handlers.pan_zoom_sprite_handler import sprite_groups
# from source.handlers.position_handler import rot_center, prevent_object_overlap
# from source.handlers.time_handler import time_handler
# from source.handlers.weapon_handler import WeaponHandler
# from source.handlers.widget_handler import WidgetHandler
# from source.multimedia_library.images import get_image, outline_image, get_gif, get_gif_frames, get_gif_fps, \
#     get_gif_duration, scale_image_cached
# from source.multimedia_library.sounds import sounds
# from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_state_engine import PanZoomShipStateEngine
# from source.pan_zoom_sprites.pan_zoom_ship_classes.spacestation import Spacestation
# from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
# from source.pan_zoom_sprites.pan_zoom_target_object import PanZoomTargetObject
# from source.path_finding.a_star_node_path_finding import Node
# from source.path_finding.pathfinding_manager import PathFindingManager
# from source.player.player_handler import player_handler
# from source.text.info_panel_text_generator import info_panel_text_generator
#
# GAME_OBJECT_SPEED = 2.0
#
# SHIP_SPEED = 1.5
# SHIP_GUN_POWER = 30
# SHIP_GUN_POWER_MAX = 50
# SHIP_INSIDE_SCREEN_BORDER = 10
# SHIP_ITEM_COLLECT_DISTANCE = 30
# SHIP_ROTATE_CORRECTION_ANGLE = 90
# SHIP_TARGET_OBJECT_RESET_DISTANCE = 15
# SHIP_RELOAD_MAX_DISTANCE = 300
# SHIP_RELOAD_MAX_DISTANCE_MAX = 600
# SHIP_ENERGY_USE = 0.1
# SHIP_ENERGY_USE_MAX = 10
# SHIP_ENERGY = 10000
# SHIP_ENERGY_MAX = 10000
# SHIP_ENERGY_RELOAD_RATE = 0.1
# SHIP_ORBIT_SPEED = 0.5
# SHIP_ORBIT_SPEED_MAX = 0.8
#
# EXPLOSION_RELATIVE_GIF_SIZE = 0.3
# SHRINK_FACTOR = 0.005
# TRAVEL_EXPERIENCE_FACTOR = 0.1
#
#
# class PanZoomShip(pygame.sprite.Sprite, InterfaceData):
#     def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
#         pygame.sprite.Sprite.__init__(self)
#         # VisibilityHandler.__init__(self)
#
#         # image/gif
#         self.win = win
#         self.image_name = image_name
#         self.gif = None
#         self.gif_frames = None
#         self.gif_fps = None
#         self.relative_gif_size = kwargs.get("relative_gif_size", 1.0)
#         self.loop_gif = kwargs.get("loop_gif", True)
#         self.kill_after_gif_loop = kwargs.get("kill_after_gif_loop", False)
#         self.appear_at_start = kwargs.get("appear_at_start", False)
#         self.shrink = 0.0 if self.appear_at_start else 1.0
#         self.gif_index = kwargs.get("gif_index", 1)
#         self.gif_start = time.time()
#         self.gif_animation_time = 0.1
#         self.current_time = 0
#         self.counter = 0
#         self.image_alpha = kwargs.get("image_alpha", None)
#
#         self.outline_thickness = kwargs.get("outline_thickness", 0)
#         self.outline_threshold = kwargs.get("outline_threshold", 0)
#         self.win = win
#         self.id = len(sprite_groups.ships)
#
#         # world
#         self.previous_world_x = None
#         self.previous_world_y = None
#         self.world_x = 0
#         self.world_y = 0
#         # self._world_x = x
#         # self._world_y = y
#         self.world_width = width  # kwargs.get("width", self.image.get_rect().width)
#         self.world_height = height  # kwargs.get("height", self.image.get_rect().height)
#         self.world_position = (0, 0)
#
#         self.zoomable = True
#         # # rotate
#         # self.rotation_direction = kwargs.get("rotation_direction", random.choice([1, -1]))
#         # self.rotation_speed = kwargs.get("rotation_speed", random.uniform(0.1, 1.0))
#         # self.rotation = 0
#
#         self.following_path = False
#         self.desired_orbit_radius_raw = 100
#         self.desired_orbit_radius = self.desired_orbit_radius_raw
#         self.desired_orbit_radius_max = 200
#         self.target = None
#         self.enemy = None
#         self.orbit_speed = SHIP_ORBIT_SPEED
#         self.orbit_speed_max = SHIP_ORBIT_SPEED_MAX
#
#         self.min_dist_to_other_ships = 80
#         self.min_dist_to_other_ships_max = 200
#         self.orbit_radius = 100 + self.id * 30
#         self.orbit_radius_max = 300
#         self.previous_position = (self.world_x, self.world_y)
#
#         # pathfinding
#         self.node = Node(self.world_x, self.world_y, self)
#         self.pathfinding_manager = PathFindingManager(self)
#         self._hidden = False
#         self._disabled = False
#         self.layer = kwargs.get("layer", 9)
#         self.widgets = []
#         self.layer = kwargs.get("layer", 0)
#         self.group = kwargs.get("group", None)
#         self.property = ""
#         self.name = kwargs.get("name", "no_name")
#         self.zoomable = kwargs.get("zoomable", True)
#         self.frame_color = colors.frame_color
#
#         if not self.image_name:
#             self.image_name = "no_icon.png"
#
#         if self.image_name.endswith(".png"):
#             self.image_raw = get_image(self.image_name)
#             self.image = copy.copy(self.image_raw)
#
#         elif self.image_name.endswith(".gif"):
#             self.gif = get_gif(self.image_name)
#             self.gif_frames = get_gif_frames(self.image_name)
#             self.gif_fps = get_gif_fps(self.image_name)
#             self.gif_animation_time = kwargs.get("gif_animation_time", get_gif_duration(self.image_name) / 1000)
#             self.image_raw = self.gif_frames[1]
#             self.image = copy.copy(self.image_raw)
#
#         if self.image_alpha:
#             self.image_raw.set_alpha(self.image_alpha)
#             self.image.set_alpha(self.image_alpha)
#
#         self.image_outline = outline_image(copy.copy(self.image), self.frame_color, self.outline_threshold, self.outline_thickness)
#         self.average_color = get_average_color(self.image_raw)
#
#         self.align_image = kwargs.get("align_image", "topleft")
#         self.enable_rotate = kwargs.get("enable_rotate", False)
#         self.rect = self.image.get_rect()
#         self.collide_rect = pygame.Rect(x, y, 20, 20)
#         self.rect.x = x
#         self.rect.y = y
#
#         # screen
#         self.lod = 0
#         self.screen_x = x
#         self.screen_y = y
#         self.screen_width = width
#         self.screen_height = height
#         self.screen_position = (self.screen_x, self.screen_y)
#
#         # world
#         self.previous_world_x = None
#         self.previous_world_y = None
#         self.world_x = 0
#         self.world_y = 0
#         # self._world_x = x
#         # self._world_y = y
#         self.world_width = width  # kwargs.get("width", self.image.get_rect().width)
#         self.world_height = height  # kwargs.get("height", self.image.get_rect().height)
#         self.world_position = (0, 0)
#         # # rotate
#         # self.rotation_direction = kwargs.get("rotation_direction", random.choice([1, -1]))
#         # self.rotation_speed = kwargs.get("rotation_speed", random.uniform(0.1, 1.0))
#         # self.rotation = 0
#         self.set_world_position((x, y))
#
#         # orbit
#         self.orbit_angle = None
#
#         # sound
#         self.sound = kwargs.get("sound", None)
#         self.debug = kwargs.get("debug", False)
#
#         self.initial_rotation = kwargs.get("initial_rotation", 0)
#         self.moving = False
#         self.rotation_smoothing = kwargs.get("rotation_smoothing", 10)
#         self.explode_if_target_reached = kwargs.get("explode_if_target_reached", False)
#         self.explosion_relative_gif_size = kwargs.get("explosion_relative_gif_size", 1.0)
#         self.explosion_name = kwargs.get("explosion_name", "explosion.gif")
#         self.exploded = False
#         self.attack_distance_raw = 5.0
#         self.attack_distance = self.attack_distance_raw
#         self.target = None
#         self.rotate_to_target = kwargs.get("rotate_to_target", True)
#         self.rotate_correction_angle = 0
#         self.prev_angle = None
#         self.move_to_target = kwargs.get("move_to_target", False)
#         self.target_position = Vector2(0, 0)
#         self.target_reached = False
#
#         # speed
#         self.speed = GAME_OBJECT_SPEED
#         self._on_hover = False
#         self.on_hover_release = False
#         self.clicked = False
#         # experience
#         self.experience = 0
#         self.experience_factor = 3000
#
#         # ranking
#         self.ranking = Ranking()
#         self.rank = "Cadet"
#
#         self.reload_max_distance_raw = SHIP_RELOAD_MAX_DISTANCE
#         self.reload_max_distance = self.reload_max_distance_raw
#         self.reload_max_distance_max_raw = SHIP_RELOAD_MAX_DISTANCE_MAX
#         self.reload_max_distance_max = self.reload_max_distance_max_raw
#
#         self.name = kwargs.get("name", "noname_ship")
#         self.type = "ship"
#         self.parent = kwargs.get("parent")
#         self.hum = sounds.hum1
#         self.sound_channel = 1
#         self.energy_use = SHIP_ENERGY_USE
#         self.energy_use_max = SHIP_ENERGY_USE_MAX
#         self.info_panel_alpha = kwargs.get("info_panel_alpha", 255)
#
#         # load_from_db Game variables
#         self.food = kwargs.get("food", 100)
#         self.food_max = 200
#         self.minerals = kwargs.get("minerals", 100)
#         self.minerals_max = 200
#         self.water = kwargs.get("water", 100)
#         self.water_max = 200
#         self.population = kwargs.get("population", 100)
#         self.population_max = 200
#         self.technology = kwargs.get("technology", 100)
#         self.technology_max = 200
#         self.energy_max = SHIP_ENERGY_MAX
#         self.energy = SHIP_ENERGY
#
#         self.resources = {
#             "minerals": self.minerals,
#             "food": self.food,
#             "energy": self.energy,
#             "water": self.water,
#             "technology": self.technology
#             }
#         self.specials = []
#
#         self.energy_reloader = None
#         self.energy_reload_rate = SHIP_ENERGY_RELOAD_RATE
#         self.move_stop = 0
#         self.crew = 7
#         self.crew_max = 12
#         self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
#                              "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]
#
#         # fog of war, no needed anymore
#         self.fog_of_war_radius = 100
#         self.fog_of_war_radius_max = 300
#
#         # upgrade
#         self.upgrade_factor = 1.5
#         self.upgrade_factor_max = 3.0
#
#         # tooltip
#         self.tooltip = ""
#
#         # uprade
#         ### ???? TODO: do we really need tht ? a ship is not a building isnt it ?
#         # self.building_slot_amount = 1
#         # self.building_cue = 0
#         # self.buildings_max = 10
#         # self.buildings = []
#
#         self.state_engine = PanZoomShipStateEngine(self)
#         self.state = "sleeping"
#         # functionality
#         # self.orbiting = False
#         self._selected = False
#         self.target = None
#         self.autopilot = kwargs.get("autopilot", False)
#
#         # pan_zoom_ship_draw
#         self.frame_color = colors.frame_color
#
#         # energy progress bar
#         self.progress_bar = ProgressBar(win=self.win,
#                 x=self.get_screen_x(),
#                 y=self.get_screen_y() + self.get_screen_height() + self.get_screen_height() / 5,
#                 width=self.get_screen_width(),
#                 height=5,
#                 progress=lambda: 1 / self.energy_max * self.energy,
#                 curved=True,
#                 completed_color=self.frame_color,
#                 layer=self.layer,
#                 parent=self
#                 )
#         self.economy_agent = EconomyAgent(self)
#
#         # init vars
#         self.is_spacestation = kwargs.get("is_spacestation", False)
#         self.spacestation = Spacestation(self) if self.is_spacestation else None
#
#         self.name = kwargs.get("name", "no_name")
#         self.data = kwargs.get("data", {})
#         self.owner = self.data.get("owner", -1)
#         self.player_color = pygame.color.THECOLORS.get(player_handler.get_player_color(self.owner))
#         self.item_collect_distance = SHIP_ITEM_COLLECT_DISTANCE
#         self.orbit_direction = 1  # random.choice([-1, 1])
#         self.speed = SHIP_SPEED
#         self.attack_distance_raw = 200
#         self.property = "ship"
#         self.rotate_correction_angle = SHIP_ROTATE_CORRECTION_ANGLE
#         self.orbit_object_name = kwargs.get("orbit_object_name", "")
#         self.orbit_object = None
#         self.orbit_angle = None
#         self.collect_text = ""
#
#         # target object
#         self.target_object = PanZoomTargetObject(config.win,
#                 pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
#                 25, 25, pan_zoom_handler, "target.gif", align_image="center", debug=False,
#                 group="target_objects", parent=self, zoomable=False, relative_gif_size=2.0)
#         self.target_object_reset_distance_raw = SHIP_TARGET_OBJECT_RESET_DISTANCE
#         self.target_object_reset_distance = self.target_object_reset_distance_raw
#
#         # sound
#         self.hum_playing = False
#
#         # orbit
#         self._orbit_object = None
#
#         # weapon handler
#         self.weapon_handler = WeaponHandler(self, kwargs.get("current_weapon", "laser"), weapons=kwargs.get("weapons", {}))
#
#         # autopilot
#         self.autopilot_handler = AutopilotHandler(self)
#         self.autopilot = False
#
#         # register
#         sprite_groups.ships.add(self)
#         if hasattr(self.parent, "box_selection"):
#             if not self in self.parent.box_selection.selectable_objects:
#                 self.parent.box_selection.selectable_objects.append(self)
#
#         # setup the ship
#         self.setup()
#
#         # interface
#         self.interface_variable_names = [
#             "food",
#             "minerals",
#             "water",
#             "technology",
#             "energy",
#             "crew",
#             "fog_of_war_radius",
#             "upgrade_factor",
#             "reload_max_distance_raw",
#             "attack_distance_raw",
#             "desired_orbit_radius_raw",
#             "speed",
#             "orbit_speed",
#             "orbit_radius",
#             "min_dist_to_other_ships",
#             "energy_use"
#             ]
#         # # init interface data
#         InterfaceData.__init__(self, self.interface_variable_names)
#
#         # register
#         if self.group:
#             getattr(sprite_groups, self.group).add(self)
#
#     def __repr__(self):
#         return (f"pan_zoom_ship: state: {self.state_engine.state}\n"
#                 f"moving: {self.moving}, following_path:{self.following_path}")
#
#     def __delete__(self, instance):
#         # remove all references
#         if self in sprite_groups.ships:
#             sprite_groups.ships.remove(self)
#
#         if self.target_object in sprite_groups.ships:
#             sprite_groups.ships.remove(self.target_object)
#
#         self.target_object.kill()
#
#         try:
#             if self in self.parent.box_selection.selectable_objects:
#                 self.parent.box_selection.selectable_objects.remove(self)
#         except:
#             pass
#         if hasattr(self, "progress_bar"):
#             WidgetHandler.remove_widget(self.progress_bar)
#
#         self.progress_bar = None
#         self.kill()
#
#     @property
#     def orbiting(self):
#         return self._orbiting
#
#     @orbiting.setter
#     def orbiting(self, value):
#         self._orbiting = value
#         if value:
#             if self.target:
#                 if hasattr(self.target, "id"):
#                     if not self.target.id == self.id:
#                         set_orbit_object_id(self, self.target.id)
#                     else:
#
#                         print("@orbiting.setter error: target.id == self.id!")
#                 else:
#                     print("@orbiting.setter error: target has no attr 'id'!")
#
#         # self.state_engine.set_state()
#
#     @property
#     def moving(self):
#         return self._moving
#
#     @moving.setter
#     def moving(self, value):
#         self._moving = value
#         if value == True:
#             self.orbiting = False
#             self.state_engine.set_state("moving")
#
#         # self.state_engine.set_state()
#
#     @property
#     def move_stop(self):
#         return self._move_stop
#
#     @move_stop.setter
#     def move_stop(self, value):
#         self._move_stop = value
#
#         if not hasattr(self, "state_engine"):
#             return
#         if value:
#             self.state_engine.set_state("move_stop")
#
#     @property
#     def image(self):
#         return self._image
#
#     @image.setter
#     def image(self, value):
#         self._image = value
#         if hasattr(self, "on_hover"):
#             if self.on_hover:
#                 self.image_outline = outline_image(copy.copy(self.image), self.frame_color, self.outline_threshold, self.outline_thickness)
#
#     @property
#     def on_hover(self):
#         return self._on_hover
#
#     @on_hover.setter
#     def on_hover(self, value):
#         self._on_hover = value
#         if value:
#             if not self._hidden:
#                 config.hover_object = self
#                 # print("on hover", self.name)
#         else:
#             if config.hover_object == self:
#                 config.hover_object = None
#
#     @property
#     def selected(self):
#         return self._selected
#
#     @selected.setter
#     def selected(self, value):
#         # print (f"owner: {self.owner}, config.player: {config.player}, config.app.game_client.id: {config.app.game_client.id}")
#         # make shure only onw ships can be selected
#         if self.owner == config.app.game_client.id:
#             self._selected = value
#
#     @property
#     def orbit_object(self):
#         return self._orbit_object
#
#     @orbit_object.setter
#     def orbit_object(self, value):
#         self._orbit_object = value
#
#         if value:
#             self.target = None
#             self.orbiting = True
#             self.orbit_direction = 1  # random.choice([-1, 1])
#             self.orbit_object_id = value.id
#             self.orbit_object_name = value.name
#         else:
#             self.orbiting = False
#             self.orbit_angle = None
#             self.orbit_object_id = -1
#             self.orbit_object_name = ""
#
#     @property
#     def enemy(self):
#         return self._enemy
#
#     @enemy.setter
#     def enemy(self, value):
#         self._enemy = value
#         if not value:
#             self.orbit_angle = None
#             self.orbit_object = None
#             self.target_reached = False
#
#     def set_speed(self):
#         # adjust speed if no energy
#         if self.move_stop > 0:
#             speed = self.speed / 10
#         else:
#             speed = self.speed
#         return speed
#
#     def set_desired_orbit_radius(self):
#         self.desired_orbit_radius = self.desired_orbit_radius_raw  # * self.get_zoom()
#
#     def set_target_object_reset_distance(self):
#         self.target_object_reset_distance = self.target_object_reset_distance_raw  # * self.get_zoom()
#
#     def set_reload_max_distance(self):
#         self.reload_max_distance = self.reload_max_distance_raw * self.get_zoom()
#         # pygame.draw.circle(self.win, pygame.color.THECOLORS["green"], self.rect.center, self.reload_max_distance, 1)
#
#     def set_distances(self):
#         self.set_attack_distance()
#         self.set_desired_orbit_radius()
#         self.set_target_object_reset_distance()
#         self.set_reload_max_distance()
#
#     def set_energy_reloader(self, obj):
#         self.energy_reloader = obj
#
#     def play_travel_sound(self):
#         # plays sound
#         if not self.hum_playing:
#             sounds.play_sound(self.hum, channel=self.sound_channel, loops=1000, fade_ms=500)
#             self.hum_playing = True
#
#     def develop_planet(self):
#         if self.target.explored:
#             return
#
#         self.set_experience(1000)
#         self.parent.info_panel.set_planet_image(self.target.image_raw)
#         self.target.get_explored(self.owner)
#
#     def reach_target(self, distance):
#         if not self.target:
#             return
#
#         if self.target.property == "ufo":
#             if distance <= self.attack_distance:
#                 self.moving = False
#                 self.reach_enemy()
#                 self.pathfinding_manager.reset()
#                 return
#
#         elif self.target.property == "planet":
#             if distance < self.desired_orbit_radius:
#                 self.reach_planet()
#
#                 # self.pathfinding_manager.reset()
#                 return
#
#         elif self.target.property == "ship":
#             if distance < self.desired_orbit_radius:
#                 self.target_reached = True
#                 self.moving = False
#                 self.orbit_object = self.target
#                 self.pathfinding_manager.reset()
#                 return
#
#         elif self.target.property == "item":
#             if distance < self.item_collect_distance:
#                 self.moving = False
#                 self.load_cargo()
#                 self.target.end_object()
#                 self.target = None
#                 self.target_reached = True
#                 self.pathfinding_manager.reset()
#                 return
#
#         elif self.target.property == "target_object":
#             if distance < self.target_object_reset_distance:
#                 self.moving = False
#                 self.target = None
#                 self.target_reached = True
#                 self.pathfinding_manager.reset()
#
#     def reach_enemy(self):
#         self.target_reached = True
#         self.orbit_object = self.target
#         self.enemy = self.orbit_object
#         self.moving = False
#
#     def reach_planet(self):
#         """ if a planet is reached, then depending on diplomacy and path_following, several scenarios will happen:
#
#             if the planet is hostile:
#                 attack the planet
#
#             if planet is inhabited:
#                 develop the planet
#         """
#
#         # develop planet
#         self.develop_planet()
#
#         # follow path: check if any waypoints left
#         if self.pathfinding_manager.path:
#             self.target_reached = False
#             self.pathfinding_manager.move_to_next_node()
#         else:
#             self.target_reached = True
#
#         # if no waypoints, target is reached
#         if self.target_reached:
#             # unload_cargo goods
#             if not self.target.type == "sun" and self.target.owner == self.owner or self.target.owner == -1:
#                 self.unload_cargo()
#
#             self.set_energy_reloader(self.target)
#
#             # sound stop
#             sounds.stop_sound(self.sound_channel)
#             self.hum_playing = False
#
#             # # open diplomacy edit to make war or peace
#             # if self.target.owner != self.owner:
#             #     config.app.diplomacy_edit.open(self.target.owner, self.owner)
#
#             # attack if hostile planet
#             if not diplomacy_handler.is_in_peace(self.target.owner, self.owner):
#                 self.reach_enemy()
#
#             # set orbit object ( also resets target)
#             self.orbit_object = self.target
#             self.moving = False
#
#     def follow_target(self, obj):
#         self.state_engine.set_state("attacking")
#         target_position = Vector2(obj.world_x, obj.world_y)
#         current_position = Vector2(self.world_x, self.world_y)
#
#         direction = target_position - current_position
#         distance = direction.length() * self.get_zoom()
#         speed_ = self.set_speed()
#
#         if distance > self.attack_distance:
#             direction.normalize()
#
#             # Get the speed of the obj
#             speed = 0.1
#             if obj.property in ["ship", "ufo"]:
#                 speed = (speed_ + obj.speed)
#             if obj.property == "planet":
#                 speed = obj.orbit_speed
#
#             if speed > self.set_speed():
#                 speed = self.set_speed()
#
#             # Calculate the displacement vector for each time step
#             displacement = direction * speed * time_handler.game_speed / config.fps
#             # print(f"displacement: {displacement}")
#
#             # Move the obj towards the target position with a constant speed
#             if config.app.game_client.is_host:
#                 self.world_x += displacement.x
#                 self.world_y += displacement.y
#
#             self.set_world_position((self.world_x, self.world_y))
#
#     def consume_energy_if_traveling(self):
#         # only subtract energy if some energy is left
#         if self.energy <= 0.0 or self.orbiting:
#             return
#
#         # subtract the traveled distance from the ships energy
#         traveled_distance = math.dist((self.world_x, self.world_y), self.previous_position)
#         self.energy -= traveled_distance * self.energy_use
#         self.set_experience(traveled_distance * TRAVEL_EXPERIENCE_FACTOR)
#
#     def get_max_travel_range(self) -> float:
#         """ returns the max distance in world coordinates the ship can move based on its energy """
#         return self.energy / self.energy_use
#
#     def get_zoom(self):
#         return pan_zoom_handler.zoom
#
#     def set_world_position(self, position):
#         self.world_position = position
#         self.world_x, self.world_y = position
#         self.screen_position = pan_zoom_handler.world_2_screen(self.world_x, self.world_y)
#
#         if self.zoomable:
#             self.screen_width = self.world_width * pan_zoom_handler.zoom * self.relative_gif_size
#             self.screen_height = self.world_height * pan_zoom_handler.zoom * self.relative_gif_size
#         else:
#             self.screen_width = self.world_width
#             self.screen_height = self.world_height
#
#         self.update_rect()
#
#     def get_screen_x(self):
#         return self.screen_x
#
#     def get_screen_y(self):
#         return self.screen_y
#
#     def get_screen_position(self):
#         return self.screen_position
#
#     def get_screen_width(self):
#         return self.screen_width
#
#     def set_screen_width(self, value):
#         self.screen_width = value
#
#     def set_screen_height(self, value):
#         self.screen_height = value
#
#     def get_screen_height(self):
#         return self.screen_height
#
#     def update_rect(self):
#         if not self.image_raw:
#             return
#
#         self.image = scale_image_cached(self.image_raw, (
#             self.screen_width * self.shrink, self.screen_height * self.shrink))
#
#         self.rect = self.image.get_rect()
#
#         self.align_image_rect()
#
#     def align_image_rect(self):
#         if self.align_image == "center":
#             self.rect.center = self.screen_position
#
#         elif self.align_image == "topleft":
#             self.rect.topleft = self.screen_position
#
#         elif self.align_image == "bottomleft":
#             self.rect.bottomleft = self.screen_position
#
#         elif self.align_image == "topright":
#             self.rect.topright = self.screen_position
#
#         elif self.align_image == "bottomright":
#             self.rect.bottomright = self.screen_position
#
#         self.collide_rect.center = self.rect.center
#
#     def update_gif_index(self):
#         if not self.gif:
#             return
#
#         if not self.gif_frames:
#             return
#
#         if self.gif_index == len(self.gif_frames):
#             if self.loop_gif:
#                 self.gif_index = 0
#             if self.kill_after_gif_loop:
#                 self.kill()
#                 return
#         else:
#             if self.gif_index == 1:
#                 if self.sound:
#                     sounds.play_sound(self.sound)
#
#         if time.time() > self.gif_start + self.gif_animation_time:
#             self.image_raw = self.gif_frames[self.gif_index]
#             self.gif_index += 1
#             self.gif_start += self.gif_animation_time
#
#     def appear(self):
#         if self.shrink >= 1.0:
#             self.appear_at_start = False
#             return
#         self.shrink += SHRINK_FACTOR
#
#     def disappear(self):
#         self.shrink -= SHRINK_FACTOR
#         if self.shrink <= SHRINK_FACTOR:
#             self.end_object(explode=False)
#
#     def update_pan_zoom_sprite(self):
#         # if self.get_game_paused():
#         #     return
#
#         if self.appear_at_start:
#             self.appear()
#         self.set_world_position((self.world_x, self.world_y))
#         self.update_gif_index()
#
#         # if self.debug or config.debug:
#         #     self.debug_object()
#
#     def set_visible(self):
#         if self._hidden:
#             self.show()
#         else:
#             self.hide()
#
#     def hide(self):
#         """hides self and its widgets
#         """
#         self._hidden = True
#         for i in self.widgets:
#             i.hide()
#
#     def show(self):
#         """shows self and its widgets
#         """
#         self._hidden = False
#         for i in self.widgets:
#             i.show()
#
#     def disable(self):
#         self._disabled = True
#
#     def enable(self):
#         self._disabled = False
#
#     def is_sub_widget(self):
#         return self._is_sub_widget
#
#     def is_visible(self):
#         return not self._hidden
#
#     def set_attack_distance(self):
#         self.attack_distance = self.attack_distance_raw * pan_zoom_handler.zoom
#
#     def set_target_position(self):
#         if hasattr(self.target, "property"):
#             if self.target.property == "planet":
#                 # self.target_position = pan_zoom_handler.zoom.screen_2_world(self.target.screen_x, self.target.screen_y)
#                 self.target_position = pan_zoom_handler.zoom.screen_2_world(self.target.rect.centerx, self.target.rect.centery)
#                 return
#
#             if self.target.property == "ship":
#                 self.target_position = self.target.rect.center
#
#             if self.target.property == "ufo":
#                 self.target_position = self.target.rect.center
#
#         if hasattr(self.target, "align_image"):
#             if self.target.align_image == "center":
#                 self.target_position = Vector2((self.target.world_x, self.target.world_y))
#
#             elif self.target.align_image == "topleft":
#                 self.target_position = Vector2((
#                     self.target.world_x + self.target.world_width / 2,
#                     self.target.world_y + self.target.world_height / 2))
#
#             elif self.target.align_image == "bottomleft":
#                 self.target_position = Vector2((
#                     self.target.world_x + self.target.world_width / 2,
#                     self.target.world_y - self.target.world_height / 2))
#
#             elif self.target.align_image == "topright":
#                 self.target_position = Vector2((
#                     self.target.world_x - self.target.world_width / 2,
#                     self.target.world_y + self.target.world_height / 2))
#
#             elif self.target.align_image == "bottomright":
#                 self.target_position = Vector2((
#                     self.target.world_x - self.target.world_width / 2,
#                     self.target.world_y - self.target.world_height / 2))
#
#     def rotate_image_to_target(self, **kwargs):
#         """
#         # 0 - image is looking to the right
#         # 90 - image is looking up
#         # 180 - image is looking to the left
#         # 270 - image is looking down
#         """
#
#         target = kwargs.get("target", self.target)
#         rotate_correction_angle = kwargs.get("rotate_correction_angle", self.rotate_correction_angle)
#
#         if target:
#             rel_x, rel_y = target.rect.centerx - self.rect.x, target.rect.centery - self.rect.y
#             angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - rotate_correction_angle
#         else:
#             if self.prev_angle:
#                 angle = self.prev_angle + 1
#             else:
#                 angle = self.initial_rotation
#
#         # Smoothing algorithm
#         if self.prev_angle:
#             diff = angle - self.prev_angle
#             if abs(diff) > self.rotation_smoothing:
#                 angle = self.prev_angle + 5 * (diff / abs(diff))
#
#         self.prev_angle = angle
#         new_image, new_rect = rot_center(self.image, angle, self.rect.x, self.rect.y, align="shipalign")
#         self.image = new_image
#         self.rect = new_rect
#
#     def move_towards_target(self):
#         self.state_engine.set_state("moving")
#         direction = self.target_position - Vector2(self.world_x, self.world_y)
#         distance = direction.length() * self.get_zoom()
#         speed = self.set_speed()
#
#         # Normalize the direction vector
#         if not direction.length() == 0.0:
#             try:
#                 direction.normalize()
#             except ValueError as e:
#                 print("move_towards_target: exc:", e)
#
#         # Calculate the displacement vector for each time step
#         displacement = direction * speed * time_handler.game_speed
#
#         # Calculate the number of time steps needed to reach the target position
#         time_steps = int(distance / speed) / self.get_zoom()
#
#         # Move the obj towards the target position with a constant speed
#         if time_steps:
#             if config.app.game_client.is_host:
#                 self.world_x += displacement.x / time_steps
#                 self.world_y += displacement.y / time_steps
#                 # self.set_world_position((self.world_x, self.world_y))
#
#         self.reach_target(distance / self.get_zoom())
#
#     def explode(self, **kwargs):
#         # self.explode_calls += 1
#         sound = kwargs.get("sound", None)
#         size = kwargs.get("size", (40, 40))
#
#         x, y = self.world_x, self.world_y
#         if not self.exploded:
#             explosion = PanZoomSprite(
#                     self.win, x, y, size[0], size[1], pan_zoom_handler.zoom, self.explosion_name,
#                     loop_gif=False, kill_after_gif_loop=True, align_image="center",
#                     relative_gif_size=self.explosion_relative_gif_size,
#                     layer=10, sound=sound, group="explosions", name="explosion")
#
#             self.exploded = True
#
#         if hasattr(self, "__delete__"):
#             self.__delete__(self)
#         self.kill()
#
#     def update_pan_zoom_game_object(self):
#         # pygame.draw.rect(self.win, self.frame_color, self.collide_rect, 1)
#         # if config.game_paused:
#         #     return
#         self.update_pan_zoom_sprite()
#         if config.game_paused:
#             return
#
#         self.set_attack_distance()
#
#         if self.target:
#             if self.rotate_to_target:
#                 self.rotate_image_to_target()
#
#             if self.move_to_target:
#                 self.moving = True
#                 self.set_target_position()
#                 self.move_towards_target()
#
#         if self.target_reached:
#             if self.explode_if_target_reached:
#                 self.explode()
#             if hasattr(self, "damage"):
#                 self.damage()
#
#     def drag(self, events):  # , **kwargs):
#         """ drag the widget """
#         # drag_from_parent_only = kwargs.get("drag_from_parent_only", False)
#         # sender =  kwargs.get("sender", None)
#
#         if not self.drag_enabled:
#             return
#
#         # if drag_from_parent_only:
#         #     if not sender:
#         #         return
#
#         # if self.resize_side:
#         #     return
#
#         old_x, old_y = self.world_x, self.world_y  # store old position
#         for event in events:
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if self.rect.collidepoint(event.pos):
#                     self.moving = True
#                     self.offset_x = self.world_x - event.pos[0]  # calculate the offset x
#                     self.offset_y = self.world_y - event.pos[1]  # calculate the offset y
#
#             elif event.type == pygame.MOUSEBUTTONUP:
#                 self.moving = False
#
#             elif event.type == pygame.MOUSEMOTION and self.moving:
#                 self.world_x = event.pos[0] + self.offset_x  # apply the offset x
#                 self.world_y = event.pos[1] + self.offset_y  # apply the offset y
#
#                 # limit y to avoid strange behaviour if close button is at the same spot as the editor open button
#                 if self.world_y < config.ui_top_limit: self.world_y = config.ui_top_limit
#
#                 # set rect
#                 self.rect.x = self.world_x
#                 self.rect.y = self.world_y
#
#                 # set drag cursor
#                 if config.app:
#                     config.app.cursor.set_cursor("drag")
#
#         self.reposition(old_x, old_y)
#
#     def set_experience(self, value):
#         self.experience += value
#         self.set_rank()
#
#     def set_rank(self):
#         # check if experience is big enough to upgrade
#         rank_value = int(self.experience / self.experience_factor)
#
#         # limit experience to int >0<8
#         if rank_value < 0:
#             rank_value = 0
#         elif rank_value > 8:
#             rank_value = 8
#
#         # get previous rank fot text generation
#         prev_rank = self.rank
#         self.rank = self.ranking.ranks[rank_value]
#
#         # set rank
#         prev_key = next((key for key, value in self.ranking.ranks.items() if value == prev_rank), None)
#         curr_key = next((key for key, value in self.ranking.ranks.items() if value == self.rank), None)
#
#         # generate feedback for player, set event_text and play sound
#         if curr_key > prev_key:
#             event_text.set_text("Congratulations !!! Rank increased from {} to {} !!!".format(prev_rank, self.rank), obj=self, sender=self.owner)
#             sounds.play_sound(sounds.rank_up)
#         elif curr_key < prev_key:
#             event_text.set_text("Shame on you !!! Rank decreased from {} to {} !!!".format(prev_rank, self.rank), obj=self, sender=self.owner)
#             sounds.play_sound(sounds.rank_down)
#
#     def select(self, value):
#         if not self.owner == config.app.game_client.id:
#             return
#         self.selected = value
#         if value:
#             sounds.play_sound("click", channel=7)
#             config.app.ship = self
#
#     def set_resources(self):
#         self.resources = {
#             "minerals": self.minerals,
#             "food": self.food,
#             "population": self.population,
#             "water": self.water,
#             "technology": self.technology
#             }
#
#     def set_info_text(self):
#         if not self == config.app.ship:
#             if self.collide_rect.collidepoint(pygame.mouse.get_pos()):
#                 text = info_panel_text_generator.create_info_panel_ship_text(self)
#                 self.parent.info_panel.set_text(text)
#                 self.parent.info_panel.set_planet_image(self.image_raw, alpha=self.info_panel_alpha)
#
#             return
#
#         text = info_panel_text_generator.create_info_panel_ship_text(self)
#         self.parent.info_panel.set_text(text)
#         self.parent.info_panel.set_planet_image(self.image_raw, alpha=self.info_panel_alpha)
#
#     def set_tooltip(self):
#         self.tooltip = f"{self.name}:  speed: {self.speed}"
#
#     def submit_tooltip(self):
#         if self.tooltip:
#             if self.tooltip != "":
#                 config.tooltip_text = self.tooltip
#
#     def reload_ship(self):
#         """ this reloads the ships energy"""
#         if not self.energy_reloader:
#             return
#         if self.energy_reloader:
#             dist = math.dist(self.rect.center, self.energy_reloader.rect.center)
#             if dist > self.reload_max_distance:
#                 return
#
#             # if reloader is a planet
#             if hasattr(self.energy_reloader, "type"):
#                 if self.energy_reloader.type == "planet":
#                     if self.energy_reloader.economy_agent.production["energy"] > 0:
#                         if self.energy_reloader.owner in self.parent.players.keys():
#                             if self.parent.players[self.energy_reloader.owner].stock[
#                                 "energy"] - self.energy_reload_rate * \
#                                     self.energy_reloader.economy_agent.production[
#                                         "energy"] > 0:
#                                 if self.energy < self.energy_max:
#                                     self.energy += self.energy_reload_rate * \
#                                                    self.energy_reloader.economy_agent.production[
#                                                        "energy"] * time_handler.game_speed
#                                     self.parent.players[self.energy_reloader.owner].stock["energy"] -= \
#                                         (
#                                                 self.energy_reload_rate * self.energy_reloader.economy_agent.production[
#                                             "energy"] * time_handler.game_speed
#                                         )
#                                     self.flickering()
#                                 else:
#                                     event_text.set_text(f"{self.name} reloaded successfully!!!", obj=self, sender=self.owner)
#                                     sounds.stop_sound(self.sound_channel)
#
#                     if self.energy_reloader.type == "sun":
#                         if self.energy < self.energy_max:
#                             self.energy += self.energy_reload_rate * time_handler.game_speed
#                             self.flickering()
#
#             # if relaoder is a ship
#             elif hasattr(self.energy_reloader, "crew"):
#                 if self.energy_reloader.energy > 0:
#                     if self.energy_reloader.energy - self.energy_reload_rate * time_handler.game_speed > 0:
#                         if self.energy < self.energy_max:
#                             self.energy += self.energy_reload_rate
#                             self.energy_reloader.energy -= self.energy_reload_rate * time_handler.game_speed
#                             self.flickering()
#                         else:
#                             event_text.set_text(f"{self.name} reloaded successfully!!!", obj=self, sender=self.owner)
#                             sounds.stop_sound(self.sound_channel)
#         else:
#             sounds.stop_sound(self.sound_channel)
#
#     def setup(self):
#         data = self.data
#         if not data:
#             data = load_file("ship_settings.json", "config")[self.name]
#
#         for key, value in data.items():
#             setattr(self, key, value)
#
#         # set orbit object
#         if self.orbit_object_id != -1 and self.orbit_object_name:
#             # if orbit object is in planets
#             if self.orbit_object_name in [i.name for i in sprite_groups.planets.sprites()]:
#                 self.orbit_object = [i for i in sprite_groups.planets.sprites() if
#                                      i.id == self.orbit_object_id and i.name == self.orbit_object_name][0]
#
#             # if orbit object is in ships
#             elif self.orbit_object_name in [i.name for i in sprite_groups.ships.sprites()]:
#                 self.orbit_object = [i for i in sprite_groups.ships.sprites() if
#                                      i.id == self.orbit_object_id and i.name == self.orbit_object_name][0]
#
#             # if orbit object is in ufos
#             elif self.orbit_object_name in [i.name for i in sprite_groups.ufos.sprites()]:
#                 self.orbit_object = [i for i in sprite_groups.ufos.sprites() if
#                                      i.id == self.orbit_object_id and i.name == self.orbit_object_name][0]
#
#         self.orbit_radius = 100 + (self.id * 30)
#
#     # TODO: this must be changed to economy_agent.
#     def load_cargo(self):
#         if self.target.collected:
#             return
#         self.collect_text = ""
#         waste_text = ""
#
#         for key, value in self.target.resources.items():
#             if value > 0:
#                 max_key = key + "_max"
#                 current_value = getattr(self, key)
#                 max_value = getattr(self, max_key)
#
#                 # Load as much resources as possible
#                 load_amount = min(value, max_value - current_value)
#                 setattr(self, key, current_value + load_amount)
#
#                 # Update collect_text
#                 self.collect_text += str(load_amount) + " of " + key + " "
#
#                 # Update waste_text
#                 if load_amount < value:
#                     waste_text += str(value - load_amount) + " of " + key + ", "
#
#                 # show what is loaded
#                 self.add_moving_image(key, "", value, (
#                     random.uniform(-0.8, 0.8), random.uniform(-1.0, -1.9)), 3, 30, 30, self, None)
#
#         special_text = " Specials: "
#         if len(self.target.specials) != 0:
#             for i in self.target.specials:
#                 self.specials.append(i)
#                 special_text += f"{i}"
#                 key_s, operand_s, value_s = i.split(" ")
#
#                 self.add_moving_image(key_s, operand_s, value_s, (0, random.uniform(-0.3, -0.6)), 5, 50, 50, self, None)
#
#         self.target.specials = []
#
#         if waste_text:
#             self.collect_text += f". because the ship's loading capacity was exceeded, the following resources were wasted: {waste_text[:-2]}!"
#
#         self.set_resources()
#         self.set_info_text()
#         sounds.play_sound(sounds.collect_success)
#
#         event_text.set_text(f"You are a Lucky Guy! you just found some resources: {special_text}, " + self.collect_text, obj=self, sender=self.owner)
#         self.target.collected = True
#
#     # TODO: this must be changed to economy_agent.
#     def unload_cargo(self):
#         text = ""
#         for key, value in self.resources.items():
#             if value > 0:
#                 text += key + ": " + str(value) + ", "
#                 if not key == "energy":
#                     # setattr(self.parent.players[self.owner], key, getattr(self.parent.players[self.owner], key) + value)
#                     self.parent.players[self.owner].stock[key] = self.parent.players[self.owner].stock[key] + value
#                     self.resources[key] = 0
#                     setattr(self, key, 0)
#                     if hasattr(config.app.resource_panel, key + "_icon"):
#                         target_icon = getattr(config.app.resource_panel, key + "_icon").rect.center
#                         if self.owner == config.app.game_client.id:
#                             self.add_moving_image(
#                                     key,
#                                     "",
#                                     value,
#                                     (random.uniform(-10.8, 10.8),
#                                      random.uniform(-1.0, -1.9)),
#                                     4,
#                                     30,
#                                     30,
#                                     self.target, target_icon)
#
#         special_text = ""
#         for i in self.specials:
#             self.target.economy_agent.specials.append(i)
#             special_text += f"found special: {i.split(' ')[0]} {i.split(' ')[1]} {i.split(' ')[2]}"
#             key_s, operand_s, value_s = i.split(" ")
#
#             if self.owner == config.app.game_client.id:
#                 self.add_moving_image(
#                         key_s,
#                         operand_s,
#                         value_s,
#                         (0, random.uniform(-0.3, -0.6)),
#                         5,
#                         50,
#                         50,
#                         self.target,
#                         None)
#         self.specials = []
#
#         if not text:
#             return
#
#         # set event text
#         event_text.set_text("unloading ship: " + text[:-2], obj=self, sender=self.owner)
#
#         # play sound
#         sounds.play_sound(sounds.unload_ship)
#
#     def add_moving_image(self, key, operand, value, velocity, lifetime, width, height, parent, target):
#         if operand == "*":
#             operand = "x"
#
#         if key == "buildings_max":
#             image_name = "building_icon.png"
#         else:
#             image_name = f"{key}_25x25.png"
#
#         image = get_image(image_name)
#         MovingImage(
#                 self.win,
#                 self.get_screen_x(),
#                 self.get_screen_y(),
#                 width,
#                 height,
#                 image,
#                 lifetime,
#                 velocity,
#                 f" {value}{operand}", SPECIAL_TEXT_COLOR,
#                 "georgiaproblack", 1, parent, target=target)
#
#     def open_weapon_select(self):
#         if not self.owner == config.app.game_client.id:
#             return
#
#         self.set_info_text()
#         if config.app.weapon_select.obj == self:
#             config.app.weapon_select.set_visible()
#         else:
#             config.app.weapon_select.obj = self
#
#     def set_target(self, **kwargs):
#         target = kwargs.get("target", sprite_groups.get_hit_object(lists=["ships", "planets", "collectable_items"]))
#         from_server = kwargs.get("from_server", None)
#
#         if target == self:
#             return
#
#         if target:
#             if not self.pathfinding_manager.path:
#                 self.target = target
#             else:
#                 self.pathfinding_manager.move_to_next_node()
#                 self.enemy = None
#
#             self.set_energy_reloader(target)
#         else:
#             self.target = self.target_object
#             self.enemy = None
#             self.orbit_object = None
#
#             # set target object position
#             self.target.world_x, self.target.world_y = pan_zoom_handler.get_mouse_world_position()
#             self.set_energy_reloader(None)
#
#         self.select(False)
#
#         # fix the case if attacking and setting new target
#         if self.target:
#             if self.target != self.enemy:
#                 self.enemy = None
#                 self.orbit_object = None
#                 self.state_engine.set_state("moving")
#
#         # send data to server, only if not called from server !!!
#         if not from_server:
#             config.app.game_client.send_message(self.get_network_data("set_target"))
#
#     def get_network_data(self, function: str):
#         if function == "set_target":
#             data = {
#                 "f": function,
#                 "object_sprite_group": self.group,
#                 "object_id": self.id,
#                 "target_sprite_group": self.target.group,
#                 "target_id": self.target.id,
#                 "target_type": self.target.type,
#                 "target_world_x": self.target.world_x,
#                 "target_world_y": self.target.world_y
#                 }
#
#             return data
#
#         if function == "position_update":
#             data = {
#                 "x": int(self.world_x),
#                 "y": int(self.world_y),
#                 "e": int(self.experience)
#                 }
#
#             return data
#
#     def activate_traveling(self):
#         if self.selected:
#             self.set_target()
#             self.orbit_object = None
#             hit_object = sprite_groups.get_hit_object()
#             if hit_object:
#                 self.set_energy_reloader(hit_object)
#
#             # follow path
#             if hasattr(self, "pathfinding_manager"):
#                 self.pathfinding_manager.follow_path(hit_object)
#
#     def handle_autopilot(self):
#         if self.autopilot:
#             self.autopilot_handler.update()
#
#         if config.enable_autopilot:
#             if not self.autopilot:
#                 self.autopilot = config.enable_autopilot
#
#     def handle_move_stop(self):
#         # move stopp reset
#         if self.energy > 0:
#             self.move_stop = 0
#         # move stopp
#         if self.energy <= 0:
#             self.move_stop = 1
#             sounds.stop_sound(self.sound_channel)
#
#     def reset_target(self):
#         if not hasattr(self.target, "property"):
#             if not self.moving:
#                 self.target = None
#         self.deselect()
#
#     def deselect(self):
#         if config.app.ship == self:
#             config.app.ship = None
#
#     def listen(self):
#         if not self.owner == config.app.game_client.id:
#             return
#         # if not config.player == config.app.player.owner:
#         #     return
#
#         config.app.tooltip_instance.reset_tooltip(self)
#         if not config.app.weapon_select._hidden:
#             return
#
#         if not self._hidden and not self._disabled:
#             mouse_state = mouse_handler.get_mouse_state()
#             x, y = mouse_handler.get_mouse_pos()
#
#             if self.collide_rect.collidepoint(x, y):
#                 if mouse_handler.double_clicks == 1:
#                     self.open_weapon_select()
#
#                 if mouse_state == MouseState.RIGHT_CLICK:
#                     if config.app.ship == self:
#                         self.select(True)
#
#                 if mouse_state == MouseState.LEFT_RELEASE and self.clicked:
#                     self.clicked = False
#
#                 elif mouse_state == MouseState.LEFT_CLICK:
#                     self.clicked = True
#                     self.select(True)
#                     config.app.ship = self
#
#                 elif mouse_state == MouseState.LEFT_DRAG and self.clicked:
#                     pass
#
#                 elif mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
#                     self.submit_tooltip()
#                     self.win.blit(scale_image_cached(self.image_outline, self.rect.size), self.rect)
#                     self.weapon_handler.draw_attack_distance()
#
#                     # set cursor
#                     config.app.cursor.set_cursor("ship")
#             else:
#                 # not mouse over object
#                 self.clicked = False
#                 if mouse_state == MouseState.LEFT_CLICK:
#                     self.reset_target()
#
#                 if mouse_state == MouseState.RIGHT_CLICK:
#                     self.activate_traveling()
#
#     def update(self):
#         # if not config.app.game_client.is_host:
#         #     return
#
#         # update pathfinder
#         # self.pathfinding_manager.update()
#
#         # update state engine
#         self.state_engine.update()
#
#         # update game object
#         self.update_pan_zoom_game_object()
#
#         # update progressbar position
#         self.progress_bar.set_progressbar_position()
#
#         # return if game paused
#         if config.game_paused:
#             return
#
#         # why setting th tooltip every frame ?? makes no sense --- but needet for correct work
#         self.set_tooltip()
#         self.listen()
#
#         self.set_distances()
#
#         # also setting the info text is questionable every frame
#         self.set_info_text()
#
#         # show/ hide target object
#         if self.state_engine.state == "moving":
#             if self.target == self.target_object:
#                 self.target_object.show()
#         else:
#             self.target_object.hide()
#
#         # handle progressbar visibility
#         # maybe we don't need inside screen here, because it is checked in WidgetHandler and pan_zoom_sprite_handler
#         if level_of_detail.inside_screen(self.rect.center):
#             self.progress_bar.show()
#             prevent_object_overlap(sprite_groups.ships, self.min_dist_to_other_ships)
#         else:
#             self.progress_bar.hide()
#
#         # draw selection and connections
#         if self.selected and self == config.app.ship:
#             self.draw_selection()
#             if self.orbit_object:
#                 self.draw_connections(self.orbit_object)
#
#             # why setting the info text again ???
#             self.set_info_text()
#
#         # travel
#         if self.target:  # and self == config.app.ship:
#             # ??? agan setting drawing the connections?
#             self.draw_connections(self.target)
#
#         # reload ship
#         if self.energy_reloader:
#             self.reload_ship()
#
#         self.handle_move_stop()
#
#         # reach target
#         if self.target_reached:
#             self.state_engine.set_state("sleeping")
#
#         # attack enemies
#         if self.enemy:
#             orbit_ship(self, self.enemy, self.orbit_speed, self.orbit_direction)
#             self.follow_target(self.enemy)
#             self.weapon_handler.attack(self.enemy)
#
#         # orbit around objects
#         if self.orbit_object:
#             orbit_ship(self, self.orbit_object, self.orbit_speed, self.orbit_direction)
#
#         # autopilot
#         self.handle_autopilot()
#
#         # consume energy for traveling
#         self.consume_energy_if_traveling()
#
#         # produce energy if spacestation
#         if self.spacestation:
#             self.spacestation.produce_energy()
#
#         # set previous position, used for energy consumption calculation
#         # make shure this is the last task, otherwise it would work(probably)
#         self.previous_position = (self.world_x, self.world_y)
#
#     def draw(self):  # unused
#         print("drawing ---")
#
#     def flickering(self):
#         if not level_of_detail.inside_screen(self.get_screen_position()):
#             return
#         # make flickering relaod stream :))
#         r0 = random.randint(-4, 5)
#         r = random.randint(-3, 4)
#         r1 = random.randint(0, 17)
#         r2 = random.randint(0, 9)
#
#         startpos = (self.rect.center[0] + r, self.rect.center[1] + r)
#         endpos = (self.energy_reloader.rect.center[0] + r0, self.energy_reloader.rect.center[1] + r0)
#
#         if r0 == 0:
#             return
#
#         if r == 3:
#             pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
#                     color=pygame.color.THECOLORS["yellow"], width=r2)
#
#         if r == 7:
#             pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
#                     color=pygame.color.THECOLORS["red"], width=r1)
#
#         if r == 2:
#             pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
#                     color=pygame.color.THECOLORS["white"], width=r * 2)
#
#         # pygame.mixer.Channel(2).play (sounds.electricity2)
#         # sounds.play_sound(sounds.electricity2, channel=self.sound_channel)
#         event_text.set_text("reloading spaceship: --- needs a lot of energy!", obj=self, sender=self.owner)
#
#     def draw_selection(self):
#         """ this handles how the ship is displayed on screen:
#             as a circle either in player color or in self.frame_color based on config.show_player_colors == True/False
#         """
#         if not self.owner == config.app.game_client.id:
#             return
#
#         if config.show_player_colors:
#             pygame.draw.circle(self.win, self.player_color, self.rect.center, self.get_screen_width(), int(6 * self.get_zoom()))
#         else:
#             pygame.draw.circle(self.win, self.frame_color, self.rect.center, self.get_screen_width(), int(6 * self.get_zoom()))
#
#     def draw_connections(self, target):
#         """
#         this calls draw_arrows_on_line_from_start_to_end
#         """
#
#         draw_arrows_on_line_from_start_to_end(
#                 surf=self.win,
#                 color=self.frame_color,
#                 start_pos=self.rect.center,
#                 end_pos=target.rect.center,
#                 width=1,
#                 dash_length=30,
#                 arrow_size=(0, 6),
#                 )




#
#
# import copy
# import math
# import random
# import time
# import pygame
# from pygame import Vector2
#
# from source.configuration.game_config import config
# from source.draw.arrow import draw_arrows_on_line_from_start_to_end
# from source.draw.scope import scope
# from source.economy.EconomyAgent import EconomyAgent
# from source.game_play.ranking import Ranking
# from source.gui.event_text import event_text
# from source.gui.interfaces.interface import InterfaceData
# from source.gui.lod import level_of_detail
# from source.gui.widgets.moving_image import MovingImage, SPECIAL_TEXT_COLOR
# from source.gui.widgets.progress_bar import ProgressBar
# from source.handlers.autopilot_handler import AutopilotHandler
# from source.handlers.color_handler import colors, get_average_color
# from source.handlers.diplomacy_handler import diplomacy_handler
# from source.handlers.file_handler import load_file
# from source.handlers.mouse_handler import mouse_handler, MouseState
# from source.handlers.orbit_handler import orbit_ship, set_orbit_object_id
# from source.handlers.pan_zoom_handler import pan_zoom_handler
# from source.handlers.pan_zoom_sprite_handler import sprite_groups
# from source.handlers.position_handler import rot_center, prevent_object_overlap
# from source.handlers.time_handler import time_handler
# from source.handlers.weapon_handler import WeaponHandler
# from source.handlers.widget_handler import WidgetHandler
# from source.multimedia_library.images import get_image, outline_image, get_gif, get_gif_frames, get_gif_fps, get_gif_duration, scale_image_cached
# from source.multimedia_library.sounds import sounds
# from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_state_engine import PanZoomShipStateEngine
# from source.pan_zoom_sprites.pan_zoom_ship_classes.spacestation import Spacestation
# from source.pan_zoom_sprites.pan_zoom_target_object import PanZoomTargetObject
# from source.path_finding.a_star_node_path_finding import Node
# from source.path_finding.pathfinding_manager import PathFindingManager
# from source.player.player_handler import player_handler
# from source.text.info_panel_text_generator import info_panel_text_generator
#
# GAME_OBJECT_SPEED = 2.0
# SHIP_SPEED = 1.5
# SHIP_GUN_POWER = 30
# SHIP_GUN_POWER_MAX = 50
# SHIP_INSIDE_SCREEN_BORDER = 10
# SHIP_ITEM_COLLECT_DISTANCE = 30
# SHIP_ROTATE_CORRECTION_ANGLE = 90
# SHIP_TARGET_OBJECT_RESET_DISTANCE = 15
# SHIP_RELOAD_MAX_DISTANCE = 300
# SHIP_RELOAD_MAX_DISTANCE_MAX = 600
# SHIP_ENERGY_USE = 0.1
# SHIP_ENERGY_USE_MAX = 10
# SHIP_ENERGY = 10000
# SHIP_ENERGY_MAX = 10000
# SHIP_ENERGY_RELOAD_RATE = 0.1
# SHIP_ORBIT_SPEED = 0.5
# SHIP_ORBIT_SPEED_MAX = 0.8
# EXPLOSION_RELATIVE_GIF_SIZE = 0.3
# SHRINK_FACTOR = 0.005
# TRAVEL_EXPERIENCE_FACTOR = 0.1
#
# class PanZoomShip(pygame.sprite.Sprite, InterfaceData):
#     def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
#         pygame.sprite.Sprite.__init__(self)
#         self.win = win
#         self.image_name = image_name
#         self.setup_graphics(kwargs)
#         self.setup_position(x, y, width, height)
#         self.setup_resources(kwargs)
#         self.setup_ship_properties(kwargs)
#         self.setup_state_and_handlers()
#         self.setup_interface()
#         sprite_groups.ships.add(self)
#
#     def setup_graphics(self, kwargs):
#         self.gif = None
#         self.gif_frames = None
#         self.gif_fps = None
#         self.relative_gif_size = kwargs.get("relative_gif_size", 1.0)
#         self.loop_gif = kwargs.get("loop_gif", True)
#         self.kill_after_gif_loop = kwargs.get("kill_after_gif_loop", False)
#         self.appear_at_start = kwargs.get("appear_at_start", False)
#         self.shrink = 0.0 if self.appear_at_start else 1.0
#         self.gif_index = kwargs.get("gif_index", 1)
#         self.gif_start = time.time()
#         self.gif_animation_time = 0.1
#         self.current_time = 0
#         self.counter = 0
#         self.image_alpha = kwargs.get("image_alpha", None)
#         self.outline_thickness = kwargs.get("outline_thickness", 0)
#         self.outline_threshold = kwargs.get("outline_threshold", 0)
#         self.load_image()
#
#     def setup_position(self, x, y, width, height):
#         self.world_x = x
#         self.world_y = y
#         self.world_width = width
#         self.world_height = height
#         self.screen_x = x
#         self.screen_y = y
#         self.screen_width = width
#         self.screen_height = height
#         self.speed = SHIP_SPEED
#         self.moving = False
#         self.rotation = 0
#         self.orbit_angle = None
#         self.orbit_direction = 1
#         self.orbit_speed = SHIP_ORBIT_SPEED
#         self.orbit_radius = 100 + self.id * 30
#
#     def setup_resources(self, kwargs):
#         self.food = kwargs.get("food", 100)
#         self.minerals = kwargs.get("minerals", 100)
#         self.water = kwargs.get("water", 100)
#         self.population = kwargs.get("population", 100)
#         self.technology = kwargs.get("technology", 100)
#         self.energy = SHIP_ENERGY
#         self.energy_max = SHIP_ENERGY_MAX
#         self.energy_reload_rate = SHIP_ENERGY_RELOAD_RATE
#
#     def setup_ship_properties(self, kwargs):
#         self.name = kwargs.get("name", "noname_ship")
#         self.type = "ship"
#         self.owner = kwargs.get("data", {}).get("owner", -1)
#         self.player_color = pygame.color.THECOLORS.get(player_handler.get_player_color(self.owner))
#         self.crew = 7
#         self.crew_max = 12
#         self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse",
#                              "sam the souvenir dealer", "jean-jaques the artist",
#                              "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]
#
#     def setup_state_and_handlers(self):
#         self.state_engine = PanZoomShipStateEngine(self)
#         self.state = "sleeping"
#         self.autopilot = False
#         self.autopilot_handler = AutopilotHandler(self)
#         self.weapon_handler = WeaponHandler(self, "laser", weapons={})
#         self.economy_agent = EconomyAgent(self)
#         self.ranking = Ranking()
#         self.rank = "Cadet"
#         self.experience = 0
#         self.experience_factor = 3000
#
#     def setup_interface(self):
#         self.interface_variable_names = [
#             "food", "minerals", "water", "technology", "energy", "crew",
#             "fog_of_war_radius", "upgrade_factor", "reload_max_distance_raw",
#             "attack_distance_raw", "desired_orbit_radius_raw", "speed",
#             "orbit_speed", "orbit_radius", "min_dist_to_other_ships", "energy_use"
#         ]
#         InterfaceData.__init__(self, self.interface_variable_names)
#
#     def load_image(self):
#         if self.image_name.endswith(".png"):
#             self.image_raw = get_image(self.image_name)
#             self.image = copy.copy(self.image_raw)
#         elif self.image_name.endswith(".gif"):
#             self.gif = get_gif(self.image_name)
#             self.gif_frames = get_gif_frames(self.image_name)
#             self.gif_fps = get_gif_fps(self.image_name)
#             self.gif_animation_time = get_gif_duration(self.image_name) / 1000
#             self.image_raw = self.gif_frames[1]
#             self.image = copy.copy(self.image_raw)
#
#         if self.image_alpha:
#             self.image_raw.set_alpha(self.image_alpha)
#             self.image.set_alpha(self.image_alpha)
#
#         self.image_outline = outline_image(copy.copy(self.image), colors.frame_color, self.outline_threshold, self.outline_thickness)
#         self.average_color = get_average_color(self.image_raw)
#
#     def update(self):
#         self.state_engine.update()
#         self.reload_energy()
#         if self.moving:
#             self.update_position()
#
#     def update_position(self):
#         # Update ship's position based on its current state
#         pass
#
#     def draw(self, surface):
#         rotated_image, rect = rot_center(self.image, self.rotation, self.screen_x, self.screen_y)
#         surface.blit(rotated_image, rect)
#
#     def reload_energy(self):
#         self.energy = min(self.energy + self.energy_reload_rate, self.energy_max)
#
#     def set_world_position(self, position):
#         self.world_x, self.world_y = position
#
#     def move(self, dx, dy):
#         self.world_x += dx
#         self.world_y += dy
#         self.moving = True
#
#     @property
#     def orbiting(self):
#         return self._orbiting
#
#     @orbiting.setter
#     def orbiting(self, value):
#         self._orbiting = value
#         if value and self.target and hasattr(self.target, "id"):
#             if self.target.id != self.id:
#                 set_orbit_object_id(self, self.target.id)
#
#     @property
#     def moving(self):
#         return self._moving
#
#     @moving.setter
#     def moving(self, value):
#         self._moving = value
#         if value:
#             self.orbiting = False
#             self.state_engine.set_state("moving")
#
#     @property
#     def move_stop(self):
#         return self._move_stop
#
#     @move_stop.setter
#     def move_stop(self, value):
#         self._move_stop = value
#         if hasattr(self, "state_engine") and value:
#             self.state_engine.set_state("move_stop")
#
#     @property
#     def image(self):
#         return self._image
#
#     @image.setter
#     def image(self, value):
#         self._image = value
#         if hasattr(self, "on_hover") and self.on_hover:
#             self.image_outline = outline_image(copy.copy(self.image), self.frame_color, self.outline_threshold, self.outline_thickness)
#
#     @property
#     def on_hover(self):
#         return self._on_hover
#
#     @on_hover.setter
#     def on_hover(self, value):
#         self._on_hover = value
#         if value and not self._hidden:
#             config.hover_object = self
#         elif config.hover_object == self:
#             config.hover_object = None
#
#     @property
#     def selected(self):
#         return self._selected
#
#     @selected.setter
#     def selected(self, value):
#         if self.owner == config.app.game_client.id:
#             self._selected = value
#
#     @property
#     def orbit_object(self):
#         return self._orbit_object
#
#     @orbit_object.setter
#     def orbit_object(self, value):
#         self._orbit_object = value
#         if value:
#             self.target = None
#             self.orbiting = True
#             self.orbit_direction = 1
#             self.orbit_object_id = value.id
#             self.orbit_object_name = value.name
#         else:
#             self.orbiting = False
#             self.orbit_angle = None
#             self.orbit_object_id = -1
#             self.orbit_object_name = ""
#
#     def __del__(self):
#         if self in sprite_groups.ships:
#             sprite_groups.ships.remove(self)
#         if hasattr(self, "target_object") and self.target_object in sprite_groups.ships:
#             sprite_groups.ships.remove(self.target_object)
#             self.target_object.kill()
#         if hasattr(self, "progress_bar"):
#             WidgetHandler.remove_widget(self.progress_bar)
#         self.kill()






import copy
import math
import time
import pygame
from pygame import Vector2

from source.gui.lod import level_of_detail
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image, scale_image_cached, rotate_image_cached, get_gif_duration, get_gif_frames, get_gif_fps
from database.config.universe_config import WORLD_RECT

class PanZoomImage(pygame.sprite.Sprite):
    __slots__ = (
        '_layer', 'win', 'world_x', 'world_y', 'world_width', 'world_height',
        'inside_screen', 'debug', 'last_zoom', 'last_world_offset_x', 'last_world_offset_y',
        'rect', 'screen_position_changed', 'image_name', 'image_raw', 'image',
        'image_alpha', 'rotation_angle', '_last_rotation_angle', 'initial_rotation'
    )

    def __init__(
        self,
        win,
        world_x,
        world_y,
        world_width,
        world_height,
        layer=0,
        group=None,
        image_name="no_image.png",
        image_alpha=None,
        rotation_angle=0,
        initial_rotation=0
    ):
        super().__init__()
        self.world_rect = WORLD_RECT
        self.win = win
        self.world_x = world_x
        self.world_y = world_y
        self.world_width = world_width
        self.world_height = world_height
        self._layer = layer
        self.rect = pygame.Rect(world_x, world_y, world_width, world_height)
        self.inside_screen = False
        self.debug = False
        self.screen_position_changed = True
        self.last_zoom = pan_zoom_handler.zoom
        self.last_world_offset_x = pan_zoom_handler.world_offset_x
        self.last_world_offset_y = pan_zoom_handler.world_offset_y

        self.image_name = image_name
        self.image_raw = get_image(self.image_name)
        self.image = copy.copy(self.image_raw)
        self.image_alpha = image_alpha
        self.rotation_angle = rotation_angle
        self._last_rotation_angle = 0
        self.initial_rotation = initial_rotation

        if self.image_alpha:
            self.image_raw.set_alpha(self.image_alpha)
            self.image.set_alpha(self.image_alpha)

        self.apply_transform(self.world_width, self.world_height)

        if group:
            group.add(self)

    def _pan_zoom_changed(self):
        changed = (self.last_zoom != pan_zoom_handler.zoom or
                   self.last_world_offset_x != pan_zoom_handler.world_offset_x or
                   self.last_world_offset_y != pan_zoom_handler.world_offset_y)
        if changed:
            self.last_zoom = pan_zoom_handler.zoom
            self.last_world_offset_x = pan_zoom_handler.world_offset_x
            self.last_world_offset_y = pan_zoom_handler.world_offset_y
        return changed

    def update(self):
        if self.screen_position_changed or self._pan_zoom_changed():
            screen_width, screen_height = self._update_screen_position()
            self.apply_transform(screen_width, screen_height)
            self.screen_position_changed = False
            self.inside_screen = level_of_detail.inside_screen(self.rect.center)

    def set_position(self, world_x, world_y):
        self.world_x = world_x
        self.world_y = world_y
        self.screen_position_changed = True

    def _update_screen_position(self):
        screen_x, screen_y = pan_zoom_handler.world_2_screen(self.world_x, self.world_y)
        screen_width = self.world_width * pan_zoom_handler.zoom
        screen_height = self.world_height * pan_zoom_handler.zoom
        self.rect.center = (screen_x, screen_y)
        self.rect.size = (screen_width, screen_height)
        return screen_width, screen_height

    def rotation_angle_changed(self):
        return self.rotation_angle != self._last_rotation_angle

    def apply_transform(self, screen_width, screen_height):
        scaled_image = scale_image_cached(self.image_raw, (screen_width, screen_height))
        if self.rotation_angle_changed() or self.initial_rotation:
            self.image = rotate_image_cached(scaled_image, self.rotation_angle)
            self._last_rotation_angle = self.rotation_angle
            if self.initial_rotation:
                self.image_raw = self.image
                self.initial_rotation = False
        else:
            self.image = scaled_image
        self.rect = self.image.get_rect(center=pan_zoom_handler.world_2_screen(self.world_x, self.world_y))

    def rotate(self, angle):
        self.rotation_angle += angle
        self.screen_position_changed = True

    def draw(self):
        if self.inside_screen:
            self.win.blit(self.image, self.rect)

class PanZoomGif(PanZoomImage):
    __slots__ = PanZoomImage.__slots__ + (
        'gif_name', 'gif_frames', 'gif_fps', 'gif_animation_time', 'gif_index',
        'loop_gif', 'kill_after_gif_loop', 'gif_start'
    )

    def __init__(
        self,
        win,
        world_x,
        world_y,
        world_width,
        world_height,
        layer=0,
        group=None,
        gif_name=None,
        gif_index=0,
        gif_animation_time=None,
        loop_gif=True,
        kill_after_gif_loop=False,
        image_alpha=None,
        rotation_angle=0,
    ):
        super().__init__(win, world_x, world_y, world_width, world_height, layer, group, gif_name, image_alpha, rotation_angle)
        self.gif_name = gif_name
        self.gif_frames = get_gif_frames(self.gif_name)
        self.gif_fps = get_gif_fps(self.gif_name)
        self.gif_animation_time = gif_animation_time or get_gif_duration(self.gif_name) / 1000
        self.gif_index = gif_index
        self.loop_gif = loop_gif
        self.kill_after_gif_loop = kill_after_gif_loop
        self.gif_start = time.time()
        self.image_raw = self.gif_frames[1]
        self.image = copy.copy(self.image_raw)

    def update(self):
        old_gif_index = self.gif_index
        self.update_gif_index()
        if self.screen_position_changed or self._pan_zoom_changed() or self.gif_index != old_gif_index:
            screen_width, screen_height = self._update_screen_position()
            self.apply_transform(screen_width, screen_height)
            self.screen_position_changed = False
            self.inside_screen = level_of_detail.inside_screen(self.rect.center)

    def update_gif_index(self):
        current_time = time.time()
        if current_time > self.gif_start + self.gif_animation_time:
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.image_raw = self.gif_frames[self.gif_index]
            self.gif_start = current_time
        if self.gif_index == 0 and not self.loop_gif:
            if self.kill_after_gif_loop:
                self.kill()

class MovableRotatableMixin:
    def move(self, dx, dy):
        self.world_x += dx * time_handler.game_speed
        self.world_y += dy * time_handler.game_speed
        self.world_x, self.world_y = self.wraparound(self.world_x, self.world_y)
        self.screen_position_changed = True

    def wraparound(self, world_x, world_y):
        center_x, center_y = self.world_rect.center
        radius = min(self.world_rect.width, self.world_rect.height) / 2
        dx = world_x - center_x
        dy = world_y - center_y
        distance_squared = dx ** 2 + dy ** 2
        if distance_squared > radius ** 2:
            angle = math.atan2(dy, dx)
            new_x = center_x - radius * math.cos(angle)
            new_y = center_y - radius * math.sin(angle)
            return new_x, new_y
        else:
            return world_x, world_y

    def rotate(self, angle):
        self.rotation_angle += angle
        self.screen_position_changed = True

class PanZoomMovingRotatingSprite(MovableRotatableMixin, PanZoomImage):
    __slots__ = PanZoomImage.__slots__ + ('rotation_speed', 'movement_speed', 'direction')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotation_speed = 0
        self.movement_speed = 0
        self.direction = Vector2(1, 0)

    def update(self):
        super().update()
        self.rotate(self.rotation_speed * time_handler.game_speed)
        self.move(self.direction.x * self.movement_speed, self.direction.y * self.movement_speed)

