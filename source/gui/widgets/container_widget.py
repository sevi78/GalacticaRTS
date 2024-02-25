import copy
import math

import pygame
from source.gui.widgets.frame import Frame
from source.gui.widgets.scroll_bar import ScrollBar
from source.handlers.mouse_handler import mouse_handler
from source.handlers.widget_handler import WidgetHandler
from source.interaction.interaction_handler import InteractionHandler

WIDGET_SIZE = 30
config = {
    "ui_panel_alpha": 220,
    "ui_rounded_corner_big_thickness": 3,
    "ui_rounded_corner_radius_big": 30,
    "ui_rounded_corner_radius_small": 9,
    "ui_rounded_corner_small_thickness": 1
    }


class ContainerWidgetItem:
    def __init__(self, win, x, y, width, height, image, **kwargs):
        self.win = win
        self.world_x = x
        self.world_y = y
        self.image_raw = image
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.world_width = width
        self.world_height = height
        self._hidden = False
        self.obj = kwargs.get("obj", None)

    def set_position(self, pos):
        self.world_x, self.world_y = pos
        self.rect.topleft = pos

    def hide(self):
        self._hidden = True

    def show(self):
        self._hidden = False

    def draw(self):
        self.rect.topleft = (self.world_x, self.world_y)
        if not self._hidden:
            self.win.blit(self.image, self.rect)


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

        # kwargs
        self.parent = kwargs.get("parent", None)
        self.group = kwargs.get("group", None)
        self.layer = kwargs.get("layer", 10)
        self.isSubWidget = True
        self._hidden = True

        # surface
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))

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

        # initial position ing maybe not needed
        self.reposition_widgets()

        # register
        WidgetHandler.addWidget(self)

    def set_widgets(self, widgets):
        if widgets:
            if not isinstance(widgets[0], ContainerWidgetItem):
                self.set_widgets([ContainerWidgetItem(self.win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE,
                    image=copy.copy(_.image_raw), obj=_) for index, _ in enumerate(widgets)])
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

    def select(self, rel_offset_y):
        # set index
        self.offset_index = math.floor(rel_offset_y / WIDGET_SIZE)
        # print(f"self.offset_index: {self.offset_index}")
        # print(f"self.function: {self.function}")

        # call the function
        getattr(self, "function")(self)

    def drag(self, events):
        """ drag the widget """
        if not self.drag_enabled:
            return

        old_x, old_y = self.world_x, self.world_y  # store old position
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.moving = True
                    self.offset_x = self.world_x - event.pos[0]  # calculate the offset x
                    self.offset_y = self.world_y - event.pos[1]  # calculate the offset y

            elif event.type == pygame.MOUSEBUTTONUP:
                self.moving = False

            elif event.type == pygame.MOUSEMOTION and self.moving:
                self.world_x = event.pos[0] + self.offset_x  # apply the offset x
                self.world_y = event.pos[1] + self.offset_y  # apply the offset y

                # limit y to avoid strange behaviour if close button is at the same spot as the editor open button

                # if self.world_y < TOP_LIMIT: self.world_y = TOP_LIMIT

                # set rect
                self.rect.x = self.world_x
                self.rect.y = self.world_y

    def reposition_widgets(self):
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
        self.world_x, self.world_y = pygame.mouse.get_pos()

    def listen(self, events):
        if self._hidden:
            return
        # all widgets listen
        self.scrollbar.listen(events)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.on_hover = True
        else:
            self.on_hover = False

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            # drag
            self.drag(events)

            # scroll
            if event.type == pygame.MOUSEWHEEL:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = event.y
                    if self.scroll_offset_y + self.scroll_y in range(-(len(self.widgets) - 1), 1):
                        self.scroll_offset_y += self.scroll_y
                        self.scrollbar.value = abs(1 / len(self.widgets) * self.scroll_offset_y)

                        self.reposition_widgets()

            # select
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        offset_y = mouse_handler.get_mouse_pos()[1] - self.world_y
                        rel_offset_y = offset_y - (self.scroll_offset_y * WIDGET_SIZE)
                        self.select(rel_offset_y)

    def draw(self):
        if self._hidden:
            return

        self.rect.x = self.world_x
        self.rect.y = self.world_y
        if self.parent:
            self.rect.x = self.parent.rect.x
            self.rect.y = self.parent.rect.y
        self.surface.get_rect().x = self.rect.x
        self.surface.get_rect().y = self.rect.y
        self.surface.fill((0, 123, 0))  # Clear the container's surface
        self.frame.update_position((self.world_x, self.world_y))
        self.frame.draw()
        self.surface.blit(self.frame.surface, (0, 0))
        self.draw_widgets()  # Draw the widgets onto the container's surface
        self.win.blit(self.surface, self.rect)

        self.scrollbar.update_position()
        self.scrollbar.draw()

# def main():
#     pygame.init()
#     win = pygame.display.set_mode((800, 600))
#     image = pygame.image.load(r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\icons\alien_face_green.png")
#
#     # widgets = []
#     #
#     # for index , _ in enumerate(os.listdir(r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\icons")):
#     #     path = r'C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\icons' + os.sep + _
#     #
#     #     print (f"path: {path}")
#     #     image = pygame.image.load(path)
#     #     print (f"image:{image}, _:{_}")
#     #
#     #     widget = ImageWidget(win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE, image)
#     #     widgets.append(widget)
#     path = r'C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\icons'
#     widgets = [
#         ImageWidget(win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE, pygame.image.load(path + os.sep + _))
#         for index, _ in enumerate(os.listdir(path))]
#
#     # widgets = [ImageWidget(win, 0, WIDGET_SIZE * _, WIDGET_SIZE, WIDGET_SIZE, image) for _ in range(17)]
#     container = ContainerWidget(win, 280, 0, 200, 300, widgets, print)
#     container.set_x(50)
#     container.set_y(130)
#
#     path = r'C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\planets'
#     container.set_widgets([
#         ImageWidget(win, 0, WIDGET_SIZE * index, WIDGET_SIZE, WIDGET_SIZE, pygame.image.load(path + os.sep + _))
#         for index, _ in enumerate(os.listdir(path))])
#
#     while True:
#         events = pygame.event.get()
#         container.listen(events)
#         mouse_handler.update_mouse_state()
#
#         win.fill((0, 120, 0))
#
#         container.draw()
#
#         pygame.display.update()
#
#
# if __name__ == "__main__":
#     main()
