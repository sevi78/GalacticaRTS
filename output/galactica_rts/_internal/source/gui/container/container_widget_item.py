import pygame

from source.draw.rect import draw_transparent_rounded_rect
from source.gui.container.container_config import FONT_SIZE, WIDGET_SIZE, TEXT_SPACING
from source.handlers.color_handler import colors


class ContainerWidgetItem:
    def __init__(self, win, x, y, width, height, image, index, **kwargs):
        self.win = win
        self.world_x = x
        self.world_y = y
        self.image_raw = image
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.index = index
        self.world_width = width
        self.world_height = height
        self._hidden = False
        self.obj = kwargs.get("obj", None)
        self.parent = kwargs.get("parent", None)
        self.widgets = []

        # text
        self.text = self.set_text()
        self.font_size = FONT_SIZE
        self.font = pygame.sysfont.SysFont(None, 15)

    def set_text(self):
        text = ""
        if self.obj:
            if self.obj.__class__.__name__ == "PanZoomPlanet":
                if not self.obj.explored:
                    text = "unknown planet"
                else:
                    text = self.obj.name

            text += f", index: {self.index}, obj.id: {self.obj.id}"
        else:
            text += f", index: {self.index}"
        return text

    def set_position(self, pos):
        self.world_x, self.world_y = pos
        self.rect.topleft = pos

        for widget in self.widgets:
            widget.win = self.win
            widget.set_position(pos)
            # print (widget.world_x, widget.world_y, widget.win)

    def hide(self):
        self._hidden = True

    def show(self):
        self._hidden = False

    def draw_text(self):
        self.win.blit(self.font.render(
                self.text,
                True,
                colors.frame_color),
                (self.world_x + WIDGET_SIZE + TEXT_SPACING, self.world_y + WIDGET_SIZE / 2))

    def draw_hover_rect(self):
        if self.parent:
            self.rect.width = self.parent.world_width
            if self.parent.rect.collidepoint(pygame.mouse.get_pos()):
                # set start x: the position for the rect to start. no way to explain the logic ---... :()
                start_y = ((self.parent.rect.y + (self.index + self.parent.scroll_offset_y) * self.parent.scroll_factor)
                           - self.parent.scroll_factor)

                end_y = start_y + self.parent.scroll_factor

                if pygame.mouse.get_pos()[1] in range(start_y, end_y):
                    draw_transparent_rounded_rect(self.win, colors.ui_dark, self.rect, 0, 75)

    def draw(self):
        self.rect.topleft = (self.world_x, self.world_y)
        if not self._hidden:
            self.win.blit(self.image, self.rect)
            self.draw_text()
            self.draw_hover_rect()
