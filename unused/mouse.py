import time
from enum import Enum

import pygame

from source.handlers.pan_zoom_sprite_handler import sprite_groups



class MouseState(Enum):
    HOVER = 0
    CLICK = 1
    MIDDLE_CLICK = 2  # New state for middle click
    RIGHT_CLICK = 3
    DRAG = 4
    RIGHT_DRAG = 5
    RELEASE = 6
    RIGHT_RELEASE = 7
    MIDDLE_RELEASE = 8  # New state for middle release


class Mouse:
    _refreshTime = 0.01

    # Redundant currently, may use for double click handling
    lastLeftClick = 0
    lastRightClick = 0
    leftClickElapsedTime = 0
    rightClickElapsedTime = 0

    _mouseState = MouseState.HOVER

    @staticmethod
    def listen():
        listening = True
        while listening:
            try:
                Mouse.updateMouseState()
            except pygame.error:
                listening = False
            time.sleep(Mouse._refreshTime)

    @staticmethod
    def updateMouseState():
        leftPressed, middlePressed, rightPressed = pygame.mouse.get_pressed()

        if leftPressed:
            if Mouse._mouseState == MouseState.CLICK or Mouse._mouseState == MouseState.DRAG:
                Mouse._mouseState = MouseState.DRAG
            else:
                Mouse._mouseState = MouseState.CLICK
        elif middlePressed:  # New condition for middle click
            if Mouse._mouseState == MouseState.MIDDLE_CLICK:
                Mouse._mouseState = MouseState.MIDDLE_CLICK
            else:
                Mouse._mouseState = MouseState.MIDDLE_CLICK
        elif rightPressed:
            if Mouse._mouseState == MouseState.RIGHT_CLICK or Mouse._mouseState == MouseState.RIGHT_DRAG:
                Mouse._mouseState = MouseState.RIGHT_DRAG
            else:
                Mouse._mouseState = MouseState.RIGHT_CLICK
        else:
            if Mouse._mouseState == MouseState.CLICK or Mouse._mouseState == MouseState.DRAG:
                Mouse._mouseState = MouseState.RELEASE
            elif Mouse._mouseState == MouseState.MIDDLE_CLICK:  # New condition for middle release
                Mouse._mouseState = MouseState.MIDDLE_RELEASE
            elif Mouse._mouseState == MouseState.RIGHT_CLICK or Mouse._mouseState == MouseState.RIGHT_DRAG:
                Mouse._mouseState = MouseState.RIGHT_RELEASE
            else:
                Mouse._mouseState = MouseState.HOVER

    @staticmethod
    def updateElapsedTime():
        """Also redundant until double click functionality implemented"""
        if Mouse._mouseState == MouseState.CLICK or Mouse._mouseState == MouseState.DRAG:
            Mouse.leftClickElapsedTime = time.time() - Mouse.lastLeftClick
        elif Mouse._mouseState == MouseState.RIGHT_CLICK or Mouse._mouseState == MouseState.RIGHT_DRAG:
            Mouse.rightClickElapsedTime = time.time() - Mouse.lastRightClick

    @staticmethod
    def getMouseState() -> MouseState:
        return Mouse._mouseState

    @staticmethod
    def getMousePos() -> (int, int):
        return pygame.mouse.get_pos()

    @staticmethod
    def setRefreshRatePerSec(refreshRate):
        Mouse._refreshTime = 1 / refreshRate if refreshRate != 0 else 0

    @staticmethod
    def get_hit_object(**kwargs: {list}) -> object or None:
        filter = kwargs.get("filter", [])
        # lists = ["planets", "ships", "ufos", "collectable_items", "celestial_objects"]
        lists = ["planets", "ships", "ufos", "collectable_items", "celestial_objects"]
        if filter:
            lists -= filter

        for list_name in lists:
            if hasattr(sprite_groups, list_name):
                for obj in getattr(sprite_groups, list_name):
                    if obj.rect.collidepoint(pygame.mouse.get_pos()):
                        return obj
            # else:
            #     hitables = [i for i in [_ for _ in WidgetHandler.get_all_widgets() if hasattr(_, "type")] if i.type == "asteroid"]
            #     for obj in hitables:
            #         if obj.rect.collidepoint(pygame.mouse.get_pos()):
            #             return obj
        return None


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((600, 600))

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        Mouse.updateMouseState()

        pygame.display.update()
        time.sleep(0.1)
