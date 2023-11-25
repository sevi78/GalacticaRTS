import pygame
from pygame_widgets import Mouse
from pygame_widgets.mouse import MouseState

from source.gui.lod import inside_screen
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.utils import global_params
from source.factories.building_factory import building_factory


class ImageButton(WidgetBase):
    """ A customisable button for Pygame

        :param win: Surface on which to draw
        :type win: pygame.Surface
        :param x: X-coordinate of top left
        :type x: int
        :param y: Y-coordinate of top left
        :type y: int
        :param width: Width of button
        :type width: int
        :param height: Height of button
        :type height: int
        :param kwargs: Optional parameters:
        """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.function = kwargs.get("function", None)
        self.layer = kwargs.get("layer", 3)
        self.parent = kwargs.get("parent")
        self.center = (
            self.get_screen_x() + self.get_screen_width() / 2, self.get_screen_y() + self.get_screen_height() / 2)
        self.name = kwargs.get("name")
        self.info_text = kwargs.get("info_text")

        # Function
        self.onClick = kwargs.get('onClick', lambda *args: None)
        self.onRelease = kwargs.get('onRelease', lambda *args: None)
        self.onClickParams = kwargs.get('onClickParams', ())
        self.onReleaseParams = kwargs.get('onReleaseParams', ())
        self.clicked = False
        self.moveable = kwargs.get("moveable", False)
        self.moving = False
        self.property = kwargs.get("property")

        # Text (Remove if using PyInstaller)
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.font_size = kwargs.get('font_size', 20)
        self.string = kwargs.get('text', '')
        self.font = kwargs.get('font', pygame.font.SysFont(global_params.font_name, self.font_size))
        self.text = self.font.render(self.string, True, self.textColour)
        self.textHAlign = kwargs.get('textHAlign', 'centre')
        self.textVAlign = kwargs.get('textVAlign', 'centre')
        self.margin = kwargs.get('margin', 20)
        self.textRect = self.text.get_rect()
        self.alignTextRect()

        # Image
        self.transparent = kwargs.get('transparent', False)
        self.image = kwargs.get('image', None)
        self.imageHAlign = kwargs.get('imageHAlign', 'centre')
        self.imageVAlign = kwargs.get('imageVAlign', 'centre')

        if self.image:
            self.rect = self.image.get_rect()
            self.alignImageRect()

        # ToolTip
        self.tooltip = kwargs.get("tooltip", "")

        # info_panel
        self.infopanel = kwargs.get("infopanel", "")

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if global_params.app:
            global_params.app.tooltip_instance.reset_tooltip(self)
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.rect.collidepoint(x, y):
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.onClick(*self.onClickParams)

                    # this is used for build .... dirty hack, but leave it !
                    if self.string:
                        building_factory.build(self.string)

                    # another dirty hack
                    if hasattr(self.parent, "on_resource_click"):
                        self.parent.on_resource_click(self)

                elif mouseState == MouseState.DRAG and self.clicked:
                    pass

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.draw_hover_rect()

                    # set info_panel
                    if self.info_text:
                        if self.info_text != "":
                            global_params.app.info_panel.set_text(self.info_text)
                            global_params.app.info_panel.set_planet_image(self.image_raw, align="topright")

                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            global_params.tooltip_text = self.tooltip
            else:
                self.clicked = False

    def execute(self, code):
        exec(code)

    def draw(self):
        """ Display to surface """
        # self.update_position()

        if not inside_screen(self.get_position(), border=0):
            return

        if not self._hidden:
            if self.image:
                self.rect = self.image.get_rect()
                self.alignImageRect()
                self.win.blit(self.image, self.rect)

            self.textRect = self.text.get_rect()
            self.alignTextRect()
            self.win.blit(self.text, self.textRect)

    def setOnClick(self, onClick, params=()):
        self.onClick = onClick
        self.onClickParams = params

    def setOnRelease(self, onRelease, params=()):
        self.onRelease = onRelease
        self.onReleaseParams = params

    def setInactiveColour(self, colour):
        self.inactiveColour = colour

    def setPressedColour(self, colour):
        self.pressedColour = colour

    def setHoverColour(self, colour):
        self.hoverColour = colour

    def get(self, attr):
        parent = super().get(attr)
        if parent is not None:
            return parent

        if attr == 'colour':
            return self.colour

    def set(self, attr, value):
        super().set(attr, value)

        if attr == 'colour':
            self.inactiveColour = value
