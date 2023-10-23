# initialize pygame and window
import os

import pygame

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import SpriteGroups
from source.database.saveload import load_file

# load settings
settings = load_file("settings.json")

global font_name
font_name = settings["font_name"]  # "bahnschrift"#'comicsansms'#'corbel'#"consolas"#"candara"

global WIDTH
WIDTH = int(settings["WIDTH"][0][0])  # windowsize[0]

global HEIGHT
HEIGHT = int(settings["HEIGHT"][0][0])  # windowsize[1]

global WIDTH_MINIMIZED
WIDTH_MINIMIZED = 1400

global HEIGHT_MINIMIZED
HEIGHT_MINIMIZED = 800

global WIDTH_CURRENT
WIDTH_CURRENT = WIDTH

global HEIGHT_CURRENT
HEIGHT_CURRENT = HEIGHT

global win
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.DOUBLEBUF)

# root path
# dirty hack to get version of the game based on the folder name
file_path = os.path.dirname(os.path.realpath(__file__))
abs_root = os.path.split(file_path)[0]

global root
root = abs_root.split(os.sep)[-1]
dirpath = os.path.dirname(os.path.realpath(__file__))

global pictures_path
pictures_path = os.path.split(dirpath)[0].split("source")[0] + "pictures" + os.sep

# Sounds
from source.multimedia_library.sounds import Sounds

global sounds
sounds = Sounds()

# Game variables
global moveable
moveable = settings["moveable"]  # True

global app
app = None

global tooltip_text
tooltip_text = ""

global game_paused
game_paused = False

global time_factor
time_factor = int(settings["time_factor"])  # 1

global game_speed
game_speed = int(settings["game_speed"])  # 10

global fps
fps = int(settings["fps"])  # 60

global scene_width
scene_width = int(settings["scene_width"])  # 60

global scene_height
scene_height = int(settings["scene_height"])  # 60

global quadrant_amount
quadrant_amount = 1

global draw_background_image
draw_background_image = settings["draw_background_image"]

global building_editor_draw
building_editor_draw = False

global enable_zoom
enable_zoom = settings["enable_zoom"]  # False

global enable_pan
enable_pan = settings["enable_pan"]

global debug
debug = settings["debug"]

global enable_orbit
enable_orbit = settings["enable_orbit"]

global enable_game_events
enable_game_events = settings["enable_game_events"]

global show_orbit
show_orbit = True

global show_grid
show_grid = False

global text_input_active
text_input_active = False

global copy_object
copy_object = None

global hover_object
hover_object = None

global edit_mode
edit_mode = False

global planet_button_display_on_panel
planet_button_display_on_panel = False

global ui_rounded_corner_radius_small
ui_rounded_corner_radius_small = 8

global ui_rounded_corner_radius_big
ui_rounded_corner_radius_big = 20

global ui_rounded_corner_small_thickness
ui_rounded_corner_small_thickness = 1

global ui_rounded_corner_big_thickness
ui_rounded_corner_big_thickness = 5

global draw_universe
draw_universe = True

# global sprites
# sprites = pygame.sprite.LayeredUpdates()
#
# global ufos
# ufos = pygame.sprite.LayeredUpdates()
#
# global planets
# planets = pygame.sprite.LayeredUpdates()
#
# global missiles
# missiles = pygame.sprite.LayeredUpdates()


# class GlobalParams__:
#     def __init__(self, settings):
#         self.font_name = settings["font_name"]
#         self.world_width = int(settings["WIDTH"][0][0])
#         self.height = int(settings["HEIGHT"][0][0])
#         self.width_minimized = 1400
#         self.height_minimized = 800
#         self.width_current = self.world_width
#         self.height_current = self.height
#         self.win = pygame.display.set_mode((self.world_width, self.height), pygame.RESIZABLE, pygame.DOUBLEBUF)
#         self.file_path = os.path.dirname(os.path.realpath(__file__))
#         self.abs_root = os.path.split(self.file_path)[0]
#         self.root = self.abs_root.split(os.sep)[-1]
#         self.dirpath = os.path.dirname(os.path.realpath(__file__))
#         self.pictures_path = os.path.split(self.dirpath)[0].split("source")[0] + "pictures" + os.sep
#         self.sounds = Sounds()
#         self.moveable = settings["moveable"]
#         self.tooltip_text = ""
#         self.game_paused = False
#         self.time_factor = int(settings["time_factor"])
#         self.game_speed = int(settings["game_speed"])
#         self.fps = int(settings["fps"])
#         self.scene_width = int(settings["scene_width"])
#         self.scene_height = int(settings["scene_height"])
#         self.draw_background_image = settings["draw_background_image"]
#         self.building_editor_draw = False
#         self.enable_zoom = settings["enable_zoom"]
#         self.enable_pan = settings["enable_pan"]
#         self.debug = settings["debug"]
#         self.enable_orbit = settings["enable_orbit"]
#         self.enable_game_events = settings["enable_game_events"]
#         self.show_orbit = True
#         self.show_grid = False
#         self.text_input_active = False
#         self.copy_object = None
#         self.hover_object = None
#         self.edit_mode = False
#         self.planet_button_display_on_panel = False
#         self.ui_rounded_corner_radius_small = 8
#         self.ui_rounded_corner_radius_big = 20
#         self.ui_rounded_corner_small_thickness = 1
#         self.ui_rounded_corner_big_thickness = 5
#         self.draw_universe = True
#
#
# class GlobalParams__:
#     settings = {
#         "font_name": "bahnschrift",
#         "WIDTH": [[800]],
#         "HEIGHT": [[600]],
#         "moveable": True,
#         "time_factor": 1,
#         "game_speed": 10,
#         "fps": 60,
#         "scene_width": 60,
#         "scene_height": 60,
#         "draw_background_image": True,
#         "enable_zoom": False,
#         "enable_pan": True,
#         "debug": False,
#         "enable_orbit": False,
#         "enable_game_events": True
#         }
#
#     font_name = settings["font_name"]
#
#     WIDTH = int(settings["WIDTH"][0][0])
#     HEIGHT = int(settings["HEIGHT"][0][0])
#
#     WIDTH_MINIMIZED = 1400
#     HEIGHT_MINIMIZED = 800
#
#     WIDTH_CURRENT = WIDTH
#     HEIGHT_CURRENT = HEIGHT
#
#     win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.DOUBLEBUF)
#
#     file_path = os.path.dirname(os.path.realpath(__file__))
#     abs_root = os.path.split(file_path)[0]
#
#     root = abs_root.split(os.sep)[-1]
#     dirpath = os.path.dirname(os.path.realpath(__file__))
#
#     pictures_path = os.path.split(dirpath)[0].split("source")[0] + "pictures" + os.sep
#
#     from source.multimedia_library.sounds import Sounds
#     sounds = Sounds()
#
#     moveable = settings["moveable"]
#     app = None
#
#     tooltip_text = ""
#     game_paused = False
#     time_factor = int(settings["time_factor"])
#     game_speed = int(settings["game_speed"])
#     fps = int(settings["fps"])
#     scene_width = int(settings["scene_width"])
#     scene_height = int(settings["scene_height"])
#     draw_background_image = settings["draw_background_image"]
#     building_editor_draw = False
#     enable_zoom = settings["enable_zoom"]
#     enable_pan = settings["enable_pan"]
#     debug = settings["debug"]
#     enable_orbit = settings["enable_orbit"]
#     enable_game_events = settings["enable_game_events"]
#     show_orbit = True
#     show_grid = False
#     text_input_active = False
#     copy_object = None
#     hover_object = None
#     edit_mode = False
#     planet_button_display_on_panel = False
#     ui_rounded_corner_radius_small = 8
#     ui_rounded_corner_radius_big = 20
#     ui_rounded_corner_small_thickness = 1
#     ui_rounded_corner_big_thickness = 5
#     draw_universe = True
#
#
# class GlobalParams:
#     sprite_groups = SpriteGroups()
#     font_name = "bahnschrift"
#     WIDTH = 800
#     HEIGHT = 600
#     WIDTH_MINIMIZED = 1400
#     HEIGHT_MINIMIZED = 800
#     WIDTH_CURRENT = WIDTH
#     HEIGHT_CURRENT = HEIGHT
#     win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.DOUBLEBUF)
#     file_path = os.path.dirname(os.path.realpath(__file__))
#     abs_root = os.path.split(file_path)[0]
#     root = abs_root.split(os.sep)[-1]
#     dirpath = os.path.dirname(os.path.realpath(__file__))
#     pictures_path = os.path.split(dirpath)[0].split("source")[0] + "pictures" + os.sep
#     from source.multimedia_library.sounds import Sounds
#     sounds = Sounds()
#     moveable = True
#     app = None
#     tooltip_text = ""
#     game_paused = False
#     time_factor = 1
#     game_speed = 10
#     fps = 60
#     scene_width = 60
#     scene_height = 60
#     draw_background_image = True
#     building_editor_draw = False
#     enable_zoom = False
#     enable_pan = True
#     debug = False
#     enable_orbit = False
#     enable_game_events = True
#     show_orbit = True
#     show_grid = False
#     text_input_active = False
#     copy_object = None
#     hover_object = None
#     edit_mode = False
#     planet_button_display_on_panel = False
#     ui_rounded_corner_radius_small = 8
#     ui_rounded_corner_radius_big = 20
#     ui_rounded_corner_small_thickness = 1
#     ui_rounded_corner_big_thickness = 5
#     draw_universe = True
#
#
# global_params = GlobalParams()

# from global_params import GlobalParams
#
# window_width, window_height = GlobalParams.get_window_size()
# fps = GlobalParams.get_fps()


# def set_global_variable__(key, value, **kwargs):
#     var = kwargs.get("var", None)
#
#     if var:
#         if getattr(global_params, var):
#             setattr(global_params, var, False)
#         else:
#             setattr(global_params, var, True)
#
#     if getattr(global_params, key):
#         setattr(global_params, key, False)
#     else:
#         setattr(global_params, key, True)
#
#
# def set_global_variable__(key, value, **kwargs):
#
#             setattr(global_params, key, False)
#         else:
#             setattr(global_params, key, True)
#
#     if getattr(global_params, key):
#         setattr(global_params, key, False)
#     else:
#         setattr(global_params, key, True)
