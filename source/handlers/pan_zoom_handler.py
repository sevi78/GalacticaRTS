import pygame as pg
import pygame.transform

from source.handlers.file_handler import load_file
from source.configuration.global_params import win, WIDTH, HEIGHT

settings = load_file("settings.json", "config")


# Zoom with mousewheel, pan with left mouse button


class PanZoomHandler:
    """Main functionalities:
    The PanZoomHandler class is responsible for handling panning and zooming of the screen in a Pygame application.
    It allows the user to zoom in and out using the mouse wheel while holding down the control key, and to pan the
    screen by clicking and dragging the mouse.
    It also provides a method for navigating to a specific object on the screen.

    Methods:
    - listen(events): handles events and updates the screen accordingly
    - pan(mouse_x, mouse_y): pans the screen based on the mouse position
    - world_2_screen(world_x, world_y): converts world coordinates to screen coordinates
    - screen_2_world(screen_x, screen_y): converts screen coordinates to world coordinates
    - navigate_to(obj, **kwargs): sets the world offset to the position of a specified object, or the first ship in the
      parent's list of ships if no object is specified

    Fields:
    - key_pressed: boolean indicating whether a key is currently pressed
    - ctrl_pressed: boolean indicating whether the control key is currently pressed
    - zoomable: boolean indicating whether the screen is currently zoomable
    - parent: reference to the parent object
    - zoomable_widgets: list of zoomable widgets
    - screen_width: width of the screen
    - screen_height: height of the screen
    - legacy_screen: Pygame surface used for resizing the screen
    - screen: Pygame surface representing the screen
    - new_screen: unused variable
    - world_width: width of the world
    - world_height: height of the world
    - world_right: right boundary of the world
    - world_left: left boundary of the world
    - world_top: top boundary of the world
    - world_bottom: bottom boundary of the world
    - world_offset_x: x-coordinate of the world offset
    - world_offset_y: y-coordinate of the world offset
    - mouseworld_y_before: y-coordinate of the mouse in world coordinates before a zoom event
    - mouseworld_x_before: x-coordinate of the mouse in world coordinates before a zoom event
    - mouseworld_y_after: y-coordinate of the mouse in world coordinates after a zoom event
    - mouseworld_x_after: x-coordinate of the mouse in world coordinates after a zoom event
    - scale_up: factor by which to scale up when zooming in
    - scale_down: factor by which to scale down when zooming out
    - tab: unused variable
    - zoom: current zoom level
    - zoom_max: maximum zoom level
    - zoom_min: minimum zoom level
    - update_screen: boolean indicating whether the screen needs to be updated
    - panning: boolean indicating whether the screen is currently being panned
    - pan_start_pos: starting position of the mouse during a pan event"""

    def __init__(self, screen, screen_width, screen_height, **kwargs):
        # self.parent = kwargs.get("parent")
        self.key_pressed = False
        self.ctrl_pressed = False
        self.zoomable = False
        self.zoomable_widgets = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen

        self.world_offset_x = 0
        self.world_offset_y = 0

        self.mouseworld_y_before = None
        self.mouseworld_x_before = None
        self.mouseworld_y_after = None
        self.mouseworld_x_after = None

        self.scale_up = 1.2
        self.scale_down = 0.8

        self.tab = 1
        self.zoom = 1
        self.zoom_max = settings["zoom_max"]
        self.zoom_min = settings["zoom_min"]

        self.update_screen = True
        self.panning = False
        self.pan_start_pos = None

    def __str__(self):
        return f"world_offset_x: {self.world_offset_x}, world_offset_y: {self.world_offset_y}, zoom: {self.zoom}"

    def setup__(self, level_width, level_height):
        # Set the world offsets to the center of the level
        self.world_offset_x = level_width / 2
        self.world_offset_y = level_height / 2

        # Calculate the zoom level needed to fit the entire level on the screen
        zoom_x = self.screen_width / level_width
        zoom_y = self.screen_height / level_height

        # Set the zoom level to the smaller of the two to ensure the entire level fits on the screen
        self.zoom = min(zoom_x, zoom_y)

    def setup__(self, level_width, level_height):
        # Set the world offsets to center the view on the level
        self.world_offset_x = level_width / 2 - (self.screen_width / 2) / self.zoom
        self.world_offset_y = level_height / 2 - (self.screen_height / 2) / self.zoom

        # Calculate the zoom level needed to fit the entire level on the screen
        zoom_x = self.screen_width / level_width
        zoom_y = self.screen_height / level_height

        # Set the zoom level to the smaller of the two to ensure the entire level fits on the screen
        self.zoom = min(zoom_x, zoom_y)

    def setup(self, level_width, level_height):
        # Calculate the zoom level needed to fit the entire level on the screen
        zoom_x = self.screen_width / (level_width * 2)
        zoom_y = self.screen_height / (level_height * 2)

        # Set the zoom level to the smaller of the two to ensure the entire level fits on the screen
        self.zoom = min(zoom_x, zoom_y)

        # Set the world offsets to center the view on the level
        self.world_offset_x = (self.screen_width / 2) / self.zoom - (level_width / 2)
        self.world_offset_y = (self.screen_height / 2) / self.zoom - (level_height / 2)

    def listen(self, events, pan_enabled):
        #print (f"pan_zoom_handler: offset(x,y): {self.world_offset_y}, {self.world_offset_y}, {self.zoom}")
        # Mouse screen coords
        mouse_x, mouse_y = pg.mouse.get_pos()
        # event handler
        for event in events:
            # ctrl_pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = True

            elif event.type == pygame.KEYUP:
                self.ctrl_pressed = False

            # mouse
            if event.type == pg.MOUSEBUTTONDOWN and self.ctrl_pressed:
                if event.button == 4 or event.button == 5:
                    # X and Y before the zoom
                    self.mouseworld_x_before, self.mouseworld_y_before = self.screen_2_world(mouse_x, mouse_y)

                    # ZOOM IN/OUT
                    if event.button == 4 and self.zoom < self.zoom_max:
                        self.zoom *= self.scale_up

                    elif event.button == 5 and self.zoom > self.zoom_min:
                        self.zoom *= self.scale_down

                    # X and Y after the zoom
                    self.mouseworld_x_after, self.mouseworld_y_after = self.screen_2_world(mouse_x, mouse_y)

                    # Do the difference between before and after, and add it to the offset
                    self.world_offset_x += self.mouseworld_x_before - self.mouseworld_x_after
                    self.world_offset_y += self.mouseworld_y_before - self.mouseworld_y_after

                    self.tab = 1

                elif event.button == 1:
                    # PAN START
                    self.panning = True
                    self.pan_start_pos = mouse_x, mouse_y
                    self.tab = 1

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and self.panning:
                    # PAN STOP
                    self.panning = False
                    self.tab = 2

                elif event.button == 4 or event.button == 5:
                    self.tab = 2

            if self.panning:
                if not pan_enabled:
                    return
                self.pan(mouse_x, mouse_y)

    def pan(self, mouse_x, mouse_y):
        # Pans the screen if the left mouse button is held
        self.world_offset_x -= (mouse_x - self.pan_start_pos[0]) / self.zoom
        self.world_offset_y -= (mouse_y - self.pan_start_pos[1]) / self.zoom
        self.pan_start_pos = mouse_x, mouse_y

    def world_2_screen(self, world_x, world_y):
        screen_x = (world_x - self.world_offset_x) * self.zoom
        screen_y = (world_y - self.world_offset_y) * self.zoom
        return [screen_x, screen_y]

    def screen_2_world(self, screen_x, screen_y):
        world_x = (screen_x / self.zoom) + self.world_offset_x
        world_y = (screen_y / self.zoom) + self.world_offset_y
        return [world_x, world_y]

    def get_mouse_world_position(self):
        x, y = pygame.mouse.get_pos()
        mx, my = self.screen_2_world(x, y)
        # pygame.draw.circle(win, pygame.color.THECOLORS["white"], (mx,my ), 10)
        return mx, my

    def set_offset(self, x, y):
        #self.world_offset_x, self.world_offset_y = self.world_2_screen(x,y)
        self.world_offset_x, self.world_offset_y = self.screen_2_world(x, y)

    def set_zoom(self, zoom):
        self.zoom = zoom

pan_zoom_handler = PanZoomHandler(
    win, WIDTH, HEIGHT)
