import pygame
from pygame_widgets.mouse import MouseState, Mouse

from source.gui.lod import inside_screen
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.buttons.moveable import Moveable
from source.utils import global_params


class Button(WidgetBase, Moveable):
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

        to make button execute:
        overgive:  self.onClick = lambda: self.execute(kwargs)  to the class that inherits from Button,
        then implement: def execute(self, kwargs): in this class
        """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)
        self.kwargs = kwargs
        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 3)

        # self.selected = False
        self.center = (
        self.get_screen_x() + self.get_screen_width() / 2, self.get_screen_y() + self.get_screen_height() / 2)
        self.name = kwargs.get("name")
        self.info_text = kwargs.get("info_text")
        self.target = None

        # Colour
        self.inactiveColour = kwargs.get('inactiveColour', (150, 150, 150))
        self.hoverColour = kwargs.get('hoverColour', (125, 125, 125))
        self.pressedColour = kwargs.get('pressedColour', (100, 100, 100))
        self.colour = kwargs.get('colour', self.inactiveColour)  # Allows colour to override inactiveColour
        self.inactiveColour = self.colour
        self.shadowDistance = kwargs.get('shadowDistance', 0)
        self.shadowColour = kwargs.get('shadowColour', (210, 210, 180))
        self.hiddenColour = kwargs.get('hiddenColour', self.inactiveColour)

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
        self.radius_extension = kwargs.get('radius_extension', 0)
        self.transparent = kwargs.get('transparent', False)
        self.image_hover_surface = pygame.surface.Surface((
            width + self.radius_extension, height + self.radius_extension), 0, self.win)
        self.image_hover_surface.set_alpha(kwargs.get("image_hover_surface_alpha", 0))
        self.image = kwargs.get('image', None)
        self.imageHAlign = kwargs.get('imageHAlign', 'centre')
        self.imageVAlign = kwargs.get('imageVAlign', 'centre')

        if self.image:
            self.rect = self.image.get_rect()
            self.alignImageRect()

        # Border
        self.borderThickness = kwargs.get('borderThickness', 0)
        self.inactiveBorderColour = kwargs.get('inactiveBorderColour', (0, 0, 0))
        self.hoverBorderColour = kwargs.get('hoverBorderColour', (80, 80, 80))
        self.pressedBorderColour = kwargs.get('pressedBorderColour', (100, 100, 100))
        self.borderColour = kwargs.get('borderColour', self.inactiveBorderColour)
        self.inactiveBorderColour = self.borderColour
        self.radius = kwargs.get('radius', 0)

        # ToolTip
        self.tooltip = kwargs.get("tooltip", "")

        # info_panel
        self.infopanel = kwargs.get("infopanel", "")

    def drawCircle(self, color, alpha):
        if self.transparent:
            self.circle = pygame.surface.Surface((self.get_screen_width(), self.get_screen_height()), 0, self.win)
            self.circle.set_alpha(0)
            circle = pygame.draw.circle(surface=self.circle, color=color,
                center=self.rect.center,
                radius=(self.get_screen_width() * 1.5))

            self.win.blit(self.circle, self.rect)

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not inside_screen(self.get_position(), border=0):
            return

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
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                    self.drawCircle(self.pressedColour, 128)

                    # set planet on click of the building slot buttons
                    if self.parent:
                        if hasattr(self.parent, "property"):
                            if self.parent.property == "planet":
                                global_params.app.set_selected_planet(self.parent)
                                # self.parent.set_info_text()
                    if self.string:
                        global_params.app.build(self.string)

                elif mouseState == MouseState.DRAG and self.clicked:
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                    self.drawCircle(self.pressedColour, 128)

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.colour = self.hoverColour
                    self.borderColour = self.hoverBorderColour

                    self.drawCircle(self.hoverColour, 128)

                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            global_params.tooltip_text = self.tooltip

                    # set info_panel
                    if self.info_text:
                        if self.info_text != "":
                            # global_params.app.info_panel.text = self.info_text
                            global_params.app.info_panel.set_text(self.info_text)
                            global_params.app.info_panel.set_planet_image(self.image, size=(
                                85, 85), align="topright")
            else:
                self.clicked = False
                self.colour = self.inactiveColour
                self.borderColour = self.inactiveBorderColour

                self.drawCircle(self.inactiveColour, 0)

    def execute(self, code):
        exec(code)

    def draw(self):
        """ Display to surface """
        self.update_position()
        if not inside_screen(self.get_position(), border=0):
            return
        if not self._hidden:
            if not self.transparent:
                pygame.draw.rect(
                    self.win, self.shadowColour,
                    (self.screen_x + self.shadowDistance, self.screen_y + self.shadowDistance, self.screen_width,
                     self.screen_height),
                    border_radius=self.radius
                    )

                pygame.draw.rect(
                    self.win, self.borderColour, (self.screen_x, self.screen_y, self.screen_width, self.screen_height),
                    border_radius=self.radius
                    )

                pygame.draw.rect(
                    self.win, self.colour, (self.screen_x + self.borderThickness, self.screen_y + self.borderThickness,
                                            self.screen_width - self.borderThickness * 2,
                                            self.screen_height - self.borderThickness * 2),
                    border_radius=self.radius
                    )

            if self.image:
                self.rect = self.image.get_rect()
                self.alignImageRect()
                self.win.blit(self.image, self.rect)

            # if self.atmosphere:
            #     rect = self.atmosphere.get_rect()
            #     rect.center = self.rect.center
            #     rect.width, rect.height = self.rect.width * 1.1, self.rect.height * 1.1
            #
            #     self.win.blit(self.atmosphere, self.rect)

            self.text = self.font.render(self.string, True, self.textColour)
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
