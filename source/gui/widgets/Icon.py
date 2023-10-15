import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame_widgets.mouse import Mouse, MouseState
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.utils import global_params


class Icon(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget, **kwargs):
        # image, key, tooltip, frame_color, moveable, include_text, parent):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 4)
        self.parent = kwargs.get("parent")
        self.value = 0
        self.key = kwargs.get("key")
        self.win = win
        self.frame_color = kwargs.get("frame_color")

        self.image = kwargs.get("image")
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.name = str(self.image).split("_")[0]

        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.height = height
        self.rect.x, self.rect.y = x, y

        # text
        self.include_text = kwargs.get("include_text")
        self.display_value_only = False
        self.text_spacing = 8
        self.text = self.key
        self.font = pygame.font.SysFont(global_params.font_name, 18)
        self.text_img = self.font.render(self.text, True, self.frame_color)

        self.width_all = 0
        self.rect_all = pygame.rect.Rect(self.world_x, self.world_y, self.world_width, self.height)

        # moving
        self.moveable = kwargs.get("moveable")
        self.moving = False

        # clicking
        self.clickable = False
        self.function = None

        # tooltip
        self.tooltip = kwargs.get("tooltip")

        # register
        self.parent.icons.append(self)

    def move(self, events):
        if not self.moveable:   return

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.moving = True

            elif event.type == MOUSEBUTTONUP:
                self.moving = False

            elif event.type == MOUSEMOTION and self.moving:
                self.rect.move_ip(event.rel)

    def on_click(self, events):
        if not self.clickable:  return
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.function:
                        print("executing:", self.function)
                        exec(self.function)

            elif event.type == MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    pass
                    # print ("hovering")
                    # hr = pygame.draw.rect(self.image,self.rect,pygame.color.THECOLORS["red"])
                    # self.win.blit(self.win, hr)

    def set_text(self):
        if self.display_value_only:
            self.text = str(self.value)

        if self.key != "":
            if self.key == "city":
                self.text = str(int(getattr(self.parent.player, "population"))) + "/" + str(int(self.parent.player.population_limit))
            else:
                self.text = str(int(self.value)) + "/" + str(int(getattr(self.parent, "production_" + self.key)))

        self.text_img = self.font.render(self.text, True, self.frame_color)

    def listen(self, events):
        self.update(events)
        mouseState = Mouse.getMouseState()
        x, y = Mouse.getMousePos()
        global_params.app.tooltip_instance.reset_tooltip(self)
        if self.rect.collidepoint(x, y):
            if mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                self.draw_hover_rect()
                if self.tooltip != "":
                    global_params.tooltip_text = self.tooltip

    def update(self, events):
        if self.key != "":
            self.value = getattr(self.parent.player, self.key)

        self.on_click(events)

        for i in self.__dict__.items():
            if hasattr(i, "update()"):
                i.update()

    def draw(self):
        if self._hidden:
            return

        self.win.blit(self.image, self.rect)
        self.set_text()
        self.win.blit(self.text_img, (self.rect.x + self.world_width + self.text_spacing, self.rect.y + 6))

        if self.include_text:
            self.width_all = self.text_img.get_width() + self.rect.width
            self.rect_all.width = self.width_all
            self.rect_all.x = self.rect.x + self.text_spacing
            self.rect_all.y = self.rect.y + 6
            self.rect_all.height = self.text_img.get_height()
