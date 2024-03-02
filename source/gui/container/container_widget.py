import copy
import math

import pygame
from source.editors.editor_base.editor_config import TOP_SPACING, TOP_LIMIT
from source.gui.container.container_config import WIDGET_SIZE
from source.gui.container.container_widget_item import ContainerWidgetItem
from source.gui.widgets.frame import Frame
from source.gui.widgets.scroll_bar import ScrollBar
from source.handlers.mouse_handler import mouse_handler
from source.handlers.widget_handler import WidgetHandler
from source.interaction.interaction_handler import InteractionHandler


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

                if self.world_y < TOP_LIMIT: self.world_y = TOP_LIMIT

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
        # self.world_x, self.world_y = pygame.mouse.get_pos()[0], TOP_SPACING

        if self.filter_widget:
            if self._hidden:
                self.filter_widget.hide()
            else:
                self.filter_widget.show()

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

                        self.offset_index = math.floor(rel_offset_y / WIDGET_SIZE)
                        self.select()


        # hover
        for i in self.widgets:
            if not i.parent:
                i.parent = self

    def draw(self):
        if self._hidden:
            return

        # set rect position
        self.rect.x = self.world_x
        self.rect.y = self.world_y
        if self.parent:
            self.rect.x = self.parent.rect.x
            self.rect.y = self.parent.rect.y

        # set surface position
        self.surface.get_rect().x = self.rect.x
        self.surface.get_rect().y = self.rect.y

        # fill surface
        self.surface.fill((0, 123, 0))  # Clear the container's surface

        # draw frame
        self.frame.update_position((self.world_x, self.world_y))
        self.frame.draw()
        self.surface.blit(self.frame.surface, (0, 0))

        # draw widgets
        self.draw_widgets()  # Draw the widgets onto the container's surface
        self.win.blit(self.surface, self.rect)

        # draw scrollbar
        self.scrollbar.update_position()
        self.scrollbar.draw()

        # filter wiget
        self.filter_widget.world_x = self.rect.x + self.rect.width - self.filter_widget.screen_width - 10
        self.filter_widget.world_y = self.rect.y - TOP_SPACING

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
