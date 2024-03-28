import copy
import math
import os

import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_config import TOP_SPACING, TOP_LIMIT
from source.gui.container.container_config import WIDGET_SIZE
from source.gui.container.container_widget_item import ContainerWidgetItem
from source.gui.container.deal_item import DealItem
from source.gui.widgets.frame import Frame
from source.gui.widgets.scroll_bar import ScrollBar
from source.handlers.mouse_handler import mouse_handler
from source.handlers.widget_handler import WidgetHandler
from source.interaction.interaction_handler import InteractionHandler
from source.multimedia_library.images import get_image

SCROLL_STEP = 25

class ContainerWidget(InteractionHandler):
    def __init__(self, win, x, y, width, height, widgets, function, **kwargs):
        InteractionHandler.__init__(self)
        self.offset_index = 0
        self.offset_y = 0
        self.offset_x = 0
        self.moving = False
        self.drag_enabled = True

        # params
        self.win = win
        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.world_height = height
        self.widgets = widgets
        self.function = function

        assert len(self.widgets) > 0, f"widgets can not be len 0 !"

        # kwargs
        self.parent = kwargs.get("parent", None)
        self.group = kwargs.get("group", None)
        self.layer = kwargs.get("layer", 10)
        self.name = kwargs.get("name", "container")
        self.list_name = kwargs.get("list_name", None)
        self.filters = kwargs.get("filters", [])
        self.filter_widget = kwargs.get("filter_widget", None)
        if self.filter_widget:
            self.filter_widget.parent = self

        self.isSubWidget = True
        self._hidden = True

        # surface
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.set_x(x)
        self.set_y(y)

        # scrolling
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_factor = self.get_scroll_step()
        self.scroll_offset_x = 0
        self.scroll_offset_y = 0
        self.max_scroll_y = self.get_max_scroll_y()

        # frame
        self.frame_border = 10
        self.frame = Frame(self.win,
            0, 0,
            self.world_width + self.frame_border,
            self.world_height + self.frame_border)

        # scrollbar
        self.scrollbar = ScrollBar(win, 0, 0, 5, self.world_height, self)

        # initial positioning maybe not needed
        self.reposition_widgets()

        # register
        WidgetHandler.addWidget(self)

        # save
        self.save = kwargs.get("save", True)

    def set_widgets(self, widgets):
        if widgets:
            if not isinstance(widgets[0], ContainerWidgetItem):
                self.set_widgets([ContainerWidgetItem(self.win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE,
                    image=copy.copy(_.image_raw), index=index, obj=_, parent=self) for index, _ in enumerate(widgets)])
            else:
                self.widgets = widgets

        self.offset_index = 0
        # set offset_y to minus 1 !!!
        self.offset_y = -1
        self.scrollbar.value = 0.0
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_factor = self.get_scroll_step()
        self.scroll_offset_x = 0
        self.scroll_offset_y = 0
        self.max_scroll_y = self.get_max_scroll_y()
        self.reposition_widgets()

        # hahahah :) !!! this makes is stay visible --- grotesque :)
        self.set_visible()
        self.set_visible()

    def set_x(self, value):
        self.world_x = value
        self.rect.x = value

    def set_y(self, value):
        self.world_y = value
        self.rect.y = value

    def get_max_scroll_y(self) -> int:
        len_ = len(self.widgets)
        size = self.widgets[0].world_width
        max_scroll_y = len_ * size
        return max_scroll_y

    def get_scroll_step(self) -> int:
        return self.widgets[0].world_height


    def select(self):
        # call the function
        if hasattr(self, "function"):
            if callable(self.function):
                getattr(self, "function")(self)

    def reposition_widgets(self):  # original
        # Adjust the position of each widget relative to the container's current position
        if not self.scroll_offset_y in range(-len(self.widgets), len(self.widgets)):
            return

        for widget in self.widgets:
            widget.win = self.surface  # self.surface
            widget.x = self.surface.get_rect().x
            widget.y = self.world_y + widget.rect.y - self.rect.y
            widget.y = widget.y + self.scroll_y * self.scroll_factor

            widget.set_position((widget.x, widget.y))

    def draw_widgets(self):
        for widget in self.widgets:
            widget.draw()

    def set_visible(self):
        self._hidden = not self._hidden
        # self.world_x, self.world_y = pygame.mouse.get_pos()[0], TOP_SPACING

        if self.filter_widget:
            if self._hidden:
                self.filter_widget.hide()
            else:
                self.filter_widget.show()

    def reposition(self, x, y):
        # set rect position
        self.rect.x = self.world_x
        self.rect.y = self.world_y
        if self.parent:
            self.rect.x = self.parent.rect.x
            self.rect.y = self.parent.rect.y

        # set surface position
        self.surface.get_rect().x = self.rect.x
        self.surface.get_rect().y = self.rect.y

        # set frame position
        self.frame.update_position((self.world_x, self.world_y))

        # scrollbar
        self.scrollbar.update_position()

        # filter widget
        if self.filter_widget:
            self.filter_widget.world_x = self.rect.x + self.rect.width - self.filter_widget.screen_width - 10
            self.filter_widget.world_y = self.rect.y - TOP_SPACING

    def listen(self, events):
        if self._hidden:
            return

        # all widgets listen
        self.scrollbar.listen(events)

        # set hovering
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.on_hover = True
            if config.app:
                config.app.cursor.set_cursor("scroll")
        else:
            self.on_hover = False

        # drag
        self.drag(events)

        # resize does not work yet
        # self.resize(events)

        # handle events
        for event in events:
            if event.type == pygame.QUIT:
                exit()

            # scroll
            if event.type == pygame.MOUSEWHEEL:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = event.y
                    if self.scroll_offset_y + self.scroll_y in range(-(len(self.widgets) - 1), 1):
                        self.scroll_offset_y += self.scroll_y
                        self.scrollbar.value = abs(1 / len(self.widgets) * self.scroll_offset_y)
                        print(f"self.scroll_offset_y: {self.scroll_offset_y},self.scrollbar.value: {self.scrollbar.value}")

                        self.reposition_widgets()

                        # set cursor
                        if config.app:
                            if event.y > 0:
                                config.app.cursor.set_cursor("scroll_up")
                            else:
                                config.app.cursor.set_cursor("scroll_down")

            # select
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        offset_y = mouse_handler.get_mouse_pos()[1] - self.world_y
                        rel_offset_y = offset_y - (self.scroll_offset_y * WIDGET_SIZE)

                        self.offset_index = math.floor(rel_offset_y / WIDGET_SIZE)
                        self.select()

        # hover
        for i in self.widgets:
            if not i.parent:
                i.parent = self

    def draw(self):
        if self._hidden:
            return

        # fill surface
        self.surface.fill((0, 123, 0))  # Clear the container's surface

        # draw frame
        self.frame.draw()
        self.surface.blit(self.frame.surface, (0, 0))

        # draw widgets
        self.draw_widgets()  # Draw the widgets onto the container's surface
        self.win.blit(self.surface, self.rect)

        # draw scrollbar
        self.scrollbar.draw()

def main():
    pygame.init()
    win = pygame.display.set_mode((800, 600))

    widgets = [DealItem(
            win,
            0,
            0,
            WIDGET_SIZE,
            WIDGET_SIZE,
            image=get_image(""),
            obj=None,
            index=0,
            player_index = 0,
            offer = {"energy":50},
            request={"food":100})
            ]

    container = ContainerWidget(win, 280, 0, 200, 300, widgets, print)
    container.set_visible()

    while True:
        events = pygame.event.get()
        container.listen(events)
        mouse_handler.update_mouse_state()
        win.fill((0, 0, 0))

        container.draw()

        pygame.display.update()

def main__():
    pygame.init()
    win = pygame.display.set_mode((800, 600))
    image = pygame.image.load(r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\icons\alien_face_green.png")

    # widgets = []
    #
    # for index , _ in enumerate(os.listdir(r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\icons")):
    #     path = r'C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\icons' + os.sep + _
    #
    #     print (f"path: {path}")
    #     image = pygame.image.load(path)
    #     print (f"image:{image}, _:{_}")
    #
    #     widget = ImageWidget(win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE, image)
    #     widgets.append(widget)
    # path = r'C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\icons'
    # widgets = [
    #     ContainerWidgetItem(win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE, pygame.image.load(path + os.sep + _), index)
    #     for index, _ in enumerate(os.listdir(path))]

    widgets = []
    # widgets = [ImageWidget(win, 0, WIDGET_SIZE * _, WIDGET_SIZE, WIDGET_SIZE, image) for _ in range(17)]
    container = ContainerWidget(win, 280, 0, 200, 300, widgets, print)

    container.set_visible()

    # path = r'C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\planets'
    # container.set_widgets([
    #     ImageWidget(win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE, pygame.image.load(path + os.sep + _))
    #     for index, _ in enumerate(os.listdir(path))])

    while True:
        events = pygame.event.get()
        container.listen(events)
        mouse_handler.update_mouse_state()

        win.fill((0, 0, 0))

        container.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
