import pygame as pg
from pygame import Rect

from source.configuration.game_config import config
from source.game_play.navigation import navigate_to_position


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
        # self.update_screen = True
        self.panning = False
        self.zooming = False
        self.pan_start_pos = None
        self.zoom_changed_callback = zoom_changed_callback
        self.cursor_change_callback = cursor_change_callback

        # self.game_object_manager = GameObjectManager(QT_RECT)

    @property
    def zoom(self):
        return self._zoom

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
        # return f"world_offset_x: {self.world_offset_x}, world_offset_y: {self.world_offset_y}, zoom: {self.zoom}, self.panning: {self.panning}, self.zoooming: {self.zoooming}"
        return f" self.panning: {self.panning}, self.zoooming: {self.zooming}"

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
        self.zooming = False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button in [4, 5]:
                    self.zooming = True
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

    def center_pan_zoom_handler(self, rect_: Rect) -> None:
        """
        centers the pan zoom handler to the center of the level
        """
        # calculate the min zoom factor
        pan_zoom_handler.zoom_min = 1000 / rect_.width

        # set zoom
        pan_zoom_handler.set_zoom(pan_zoom_handler.zoom_min)

        # navigate zo center of the level
        navigate_to_position(rect_.width, rect_.height)


def zoom_changed_callback(zoom) -> None:
    # print("Zoom changed to: ", zoom)
    pass
    # if hasattr(config.app, "zoom_scale"):
    #     config.app.zoom_scale.set_zoom(zoom)

    # game_object_manager.update()


def cursor_change_callback(cursor_name: str) -> None:
    # print("Cursor changed to: ", cursor_name)
    pass
    # if hasattr(config.app, "set_cursor"):
    #     config.app.cursor.set_cursor(cursor_name)

    # game_object_manager.update()


pan_zoom_handler = PanZoomHandler(config.win, config.width, config.height, zoom_changed_callback, cursor_change_callback)
