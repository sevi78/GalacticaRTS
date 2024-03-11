import pygame

from source.configuration.game_config import config

class ResizeHandler:
    def __init__(self):
        self.resize_side = "top"
        self.resize_border = 10
        self.resize_clicked = False

    # should be outside this class: only editors should use it
    def drag(self, events):
        """ drag the widget """
        if not self.drag_enabled:
            return

        # if self.resize_side:
        #     return

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

                if self.world_y < config.ui_top_limit: self.world_y = config.ui_top_limit

                # set rect
                self.rect.x = self.world_x
                self.rect.y = self.world_y

                # set drag cursor
                config.app.cursor.set_cursor("drag")

        self.reposition(old_x, old_y)

        #self.resize(events)

    def set_resize_side(self):
        # Calculate the rectangles for detecting cursor position
        left_rect = pygame.Rect(self.rect.x, self.rect.y, self.resize_border, self.rect.height)
        right_rect = pygame.Rect(self.rect.right - self.resize_border, self.rect.y, self.resize_border, self.rect.height)
        top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.resize_border)
        bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom - self.resize_border, self.rect.width, self.resize_border)
        # First, check for corners since they are more specific conditions
        mouse_pos = pygame.mouse.get_pos()
        if top_rect.collidepoint(mouse_pos) and left_rect.collidepoint(mouse_pos):
            self.resize_side = "top-left"
        elif top_rect.collidepoint(mouse_pos) and right_rect.collidepoint(mouse_pos):
            self.resize_side = "top-right"
        elif bottom_rect.collidepoint(mouse_pos) and left_rect.collidepoint(mouse_pos):
            self.resize_side = "bottom-left"
        elif bottom_rect.collidepoint(mouse_pos) and right_rect.collidepoint(mouse_pos):
            self.resize_side = "bottom-right"
        # After checking for corners, check for edges
        elif top_rect.collidepoint(mouse_pos):
            self.resize_side = "top"
        elif bottom_rect.collidepoint(mouse_pos):
            self.resize_side = "bottom"
        elif left_rect.collidepoint(mouse_pos):
            self.resize_side = "left"
        elif right_rect.collidepoint(mouse_pos):
            self.resize_side = "right"
        else:
            self.resize_side = None

    def set_resize_cursor(self):
        # set the resize cursor
        cursor = config.app.cursor
        orientation = cursor.get_resize_cursor_orientation(self.resize_side)
        new_cursor = cursor.get_resize_cursor(orientation)
        cursor.set_cursor(new_cursor)

    def resize(self, events):
        # Determine the resize side based on the mouse position relative to the widget
        self.set_resize_side()

        if self.resize_side:
            self.set_resize_cursor()

        for event in events:
            # set first click
            if event.type == pygame.MOUSEBUTTONDOWN and not self.resize_clicked:
                if self.resize_side:
                    self.resize_clicked = True

            # while clicking
            if event.type == pygame.MOUSEBUTTONDOWN and self.resize_clicked:
                pygame.draw.line(config.app.win, (255, 0, 0), self.rect.center, pygame.mouse.get_pos(), 2)

            # click release
            if event.type == pygame.MOUSEBUTTONUP and self.resize_clicked:
                self.resize_clicked = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    # self.rect.x -= 10
                    value = 10
                    self.world_x -= value
                    self.world_width += value
                    self.reposition(self.world_x, self.world_y)
                    # # self.reposition_widgets()
                    # self.surface.get_rect().width = self.world_width
                    # pygame.transform.scale(self.surface,(self.world_width, self.world_height))
                    #
                    # self.frame.update(self.world_x, self.world_y, self.world_width, self.world_height)

            elif event.type == pygame.MOUSEMOTION and self.resize_side is not None and self.resize_clicked:
                # Calculate the new dimensions and position based on the mouse movement
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 'left' in self.resize_side:
                    delta_x = mouse_x - self.rect.x
                    self.world_width -= delta_x
                    self.world_x += delta_x
                elif 'right' in self.resize_side:
                    self.world_width = mouse_x - self.world_x

                if 'top' in self.resize_side:
                    delta_y = mouse_y - self.rect.y
                    self.world_height -= delta_y
                    self.world_y += delta_y
                elif 'bottom' in self.resize_side:
                    self.world_height = mouse_y - self.world_y

                # Update the widget's rect to reflect the new size and position
                self.rect.x = self.world_x
                self.rect.y = self.world_y
                self.rect.width = self.world_width
                self.rect.height = self.world_height

            elif event.type == pygame.MOUSEBUTTONUP:
                # Reset the resize side after the mouse button is released
                self.resize_side = None
                self.resize_clicked = False
                self.reposition(self.world_x, self.world_y)

            self.set_resize_cursor()


# the resize handler should be outside
class InteractionHandler(ResizeHandler):
    def __init__(self):
        ResizeHandler.__init__(self)
        self._on_hover = False
        self.on_hover_release = False

    @property
    def on_hover(self):
        return self._on_hover

    @on_hover.setter
    def on_hover(self, value):
        self._on_hover = value
        if value:
            if not self._hidden:
                config.hover_object = self
        else:
            if config.hover_object == self:
                config.hover_object = None



