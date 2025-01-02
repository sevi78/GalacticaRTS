import pygame as pg
import pygame.transform
from pygame.math import clamp

from source.configuration.game_config import config


class PanZoomHandler__:  # limited
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

    def __init__(self, screen, screen_width, screen_height):
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

        self.zoom_max = 2.0
        self.zoom_min = 0.01
        self.zoom = 1

        self.update_screen = True
        self.panning = False
        self.pan_start_pos = None

    def set_zoom(self, zoom: float):
        self.zoom = clamp(round(zoom, 4), self.zoom_min, self.zoom_max)  # Clamp the zoom
        if hasattr(config.app, "zoom_scale"):
            config.app.zoom_scale.set_zoom(self.zoom)
        # print("Zoom set to: ", self.zoom)

    def get_zoom(self):
        return self.zoom

    def get_world_position(self) -> list:
        return [-self.world_offset_x, -self.world_offset_y]

    def __str__(self):
        return f"world_offset_x: {self.world_offset_x}, world_offset_y: {self.world_offset_y}, zoom: {self.zoom}"

    def pan(self, mouse_x, mouse_y):
        # Pans the screen if the left mouse button is held
        self.world_offset_x -= int((mouse_x - self.pan_start_pos[0]) / self.zoom)
        self.world_offset_y -= int((mouse_y - self.pan_start_pos[1]) / self.zoom)
        self.pan_start_pos = mouse_x, mouse_y
        try:
            config.app.cursor.set_cursor("navigate")
        except:
            pass

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
        return mx, my

    def listen(self, events):
        # Mouse screen coords, or map coordinates if mouse on map
        mouse_x, mouse_y = self.get_relative_mouse_position()

        # event handler
        for event in events:
            # mouse
            if event.type == pg.MOUSEBUTTONDOWN:  # and self.ctrl_pressed:
                if event.button in [4, 5]:
                    # check if containers at mouse position to avoid strange double behaviour
                    if not config.hover_object.__class__.__name__ == "ContainerWidget":
                        # X and Y before the zoom

                        self._set_mouse_world_before(mouse_x, mouse_y)

                        # ZOOM IN/OUT
                        self._zoom_in_out(event)

                        # X and Y after the zoom
                        self._set_mouse_world_after(mouse_x, mouse_y)

                        # Do the difference between before and after, and add it to the offset
                        self._update_world_offset()

                elif event.button == 2:
                    # PAN START
                    self.panning = True
                    self.pan_start_pos = mouse_x, mouse_y


            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 2 and self.panning:
                    # PAN STOP
                    self.panning = False

            if self.panning:
                self.pan(mouse_x, mouse_y)

    def _zoom_in_out(self, event):
        if event.button == 4 and self.zoom:
            self.set_zoom(self.zoom * self.scale_up)
            try:
                config.app.cursor.set_cursor("zoom_in")
            except:
                pass

            # config.app.cursor.set_cursor("zoom_in")
        elif event.button == 5 and self.zoom:
            self.set_zoom(self.zoom * self.scale_down)
            try:
                config.app.cursor.set_cursor("zoom_out")
            except:
                pass

    def _update_world_offset(self):
        """
        this is used by the pan_zoom_handler itself, only for internal use
        """
        self.world_offset_x += int(self.mouseworld_x_before - self.mouseworld_x_after)
        self.world_offset_y += int(self.mouseworld_y_before - self.mouseworld_y_after)

    def set_world_offset(self, world_offset: (float, float)):
        """
        this is used by navigation, the interface for the user
        """
        self.world_offset_x, self.world_offset_y = int(world_offset[0]), int(world_offset[1])

    def _set_mouse_world_after(self, mouse_x, mouse_y):
        self.mouseworld_x_after, self.mouseworld_y_after = self.screen_2_world(mouse_x, mouse_y)

    def _set_mouse_world_before(self, mouse_x, mouse_y):
        self.mouseworld_x_before, self.mouseworld_y_before = self.screen_2_world(mouse_x, mouse_y)

    def get_relative_mouse_position(self) -> (int, int):
        if hasattr(config.hover_object, "relative_mouse_x"):
            # Use relative position from the map
            screen_width, screen_height = config.win.get_width(), config.win.get_height()
            world_width = config.app.level_handler.data["globals"]["width"]
            world_height = config.app.level_handler.data["globals"]["height"]
            mouse_x = screen_width / world_width * config.app.map_panel.relative_mouse_x
            mouse_y = screen_height / world_height * config.app.map_panel.relative_mouse_y
        else:
            # Use real mouse position
            mouse_x, mouse_y = self.get_mouse_position()

        return mouse_x, mouse_y

    def get_mouse_position(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return mouse_x, mouse_y


# pan_zoom_handler = PanZoomHandler(config.win, config.width, config.height)

#
# import pygame as pg
# from pygame.math import clamp
#
#
class PanZoomHandler:
    def __init__(self, screen, screen_width, screen_height, zoom_changed_callback=None, cursor_change_callback=None):
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
        self.zoom_max = 1.4
        self.zoom_min = 0.01
        self._zoom = 1
        self.update_screen = True
        self.panning = False
        self.pan_start_pos = None
        self.zoom_changed_callback = zoom_changed_callback
        self.cursor_change_callback = cursor_change_callback

    @property
    def zoom(self):
        return self._zoom

    # @zoom.setter
    # def zoom(self, value):
    #     self._zoom = clamp(round(value, 4), self.zoom_min, self.zoom_max)
    #     if self.zoom_changed_callback:
    #         self.zoom_changed_callback(self._zoom)

    @zoom.setter
    def zoom(self, value):
        if value > self.zoom_max:
            self._zoom = self.zoom_max
        elif value < self.zoom_min:
            self._zoom = self.zoom_min
        else:
            self._zoom = value

        if self.zoom_changed_callback:
            self.zoom_changed_callback(self._zoom)

    def set_zoom(self, zoom: float):
        self.zoom = zoom

    def get_zoom(self):
        return self.zoom

    def get_world_position(self) -> list:
        return [-self.world_offset_x, -self.world_offset_y]

    def __str__(self):
        return f"world_offset_x: {self.world_offset_x}, world_offset_y: {self.world_offset_y}, zoom: {self.zoom}"

    def pan(self, mouse_x, mouse_y):
        self.world_offset_x -= int((mouse_x - self.pan_start_pos[0]) / self.zoom)
        self.world_offset_y -= int((mouse_y - self.pan_start_pos[1]) / self.zoom)
        self.pan_start_pos = mouse_x, mouse_y
        if self.cursor_change_callback:
            self.cursor_change_callback("navigate")

    def world_2_screen(self, world_x, world_y):
        screen_x = (world_x - self.world_offset_x) * self.zoom
        screen_y = (world_y - self.world_offset_y) * self.zoom
        return [screen_x, screen_y]

    def screen_2_world(self, screen_x, screen_y):
        world_x = (screen_x / self.zoom) + self.world_offset_x
        world_y = (screen_y / self.zoom) + self.world_offset_y
        return [world_x, world_y]

    def get_mouse_world_position(self):
        x, y = pg.mouse.get_pos()
        mx, my = self.screen_2_world(x, y)
        return mx, my

    def listen(self, events):
        mouse_x, mouse_y = self.get_mouse_position()
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button in [4, 5]:
                    self._set_mouse_world_before(mouse_x, mouse_y)
                    self._zoom_in_out(event)
                    self._set_mouse_world_after(mouse_x, mouse_y)
                    self._update_world_offset()
                elif event.button == 2:
                    self.panning = True
                    self.pan_start_pos = mouse_x, mouse_y
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 2 and self.panning:
                    self.panning = False
        if self.panning:
            self.pan(mouse_x, mouse_y)

    def _zoom_in_out(self, event):
        if event.button == 4 and self.zoom:
            self.set_zoom(self.zoom * self.scale_up)
            if self.cursor_change_callback:
                self.cursor_change_callback("zoom_in")
        elif event.button == 5 and self.zoom:
            self.set_zoom(self.zoom * self.scale_down)
            if self.cursor_change_callback:
                self.cursor_change_callback("zoom_out")

    def _update_world_offset(self):
        self.world_offset_x += int(self.mouseworld_x_before - self.mouseworld_x_after)
        self.world_offset_y += int(self.mouseworld_y_before - self.mouseworld_y_after)

    def set_world_offset(self, world_offset: (float, float)):
        self.world_offset_x, self.world_offset_y = int(world_offset[0]), int(world_offset[1])

    def _set_mouse_world_after(self, mouse_x, mouse_y):
        self.mouseworld_x_after, self.mouseworld_y_after = self.screen_2_world(mouse_x, mouse_y)

    def _set_mouse_world_before(self, mouse_x, mouse_y):
        self.mouseworld_x_before, self.mouseworld_y_before = self.screen_2_world(mouse_x, mouse_y)

    def get_mouse_position(self):
        return pg.mouse.get_pos()


def zoom_changed_callback(zoom) -> None:
    if hasattr(config.app, "zoom_scale"):
        config.app.zoom_scale.set_zoom(zoom)


def cursor_change_callback(cursor_name: str) -> None:
    if hasattr(config.app, "set_cursor"):
        config.app.cursor.set_cursor(cursor_name)


pan_zoom_handler = PanZoomHandler(config.win, config.width, config.height, zoom_changed_callback, cursor_change_callback)
