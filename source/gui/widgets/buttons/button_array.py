import pygame

from source.gui.widgets.buttons.button import Button
from source.gui.widgets.widget_base_components.widget_base import WidgetBase


class ButtonArray(WidgetBase):
    def __init__(self, win, x, y, width, height, shape, **kwargs):
        """ A collection of buttons

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
        :param shape: The 2d shape of the array (columns, rows)
        :type shape: tuple of int
        :param kwargs: Optional parameters
        """
        super().__init__(win, x, y, width, height, **kwargs)
        self.layers = kwargs.get("layers")[0]
        self.layer = kwargs.get("layers")[0]
        self.shape = shape
        self.numButtons = shape[0] * shape[1]

        # Array
        self.colour = kwargs.get('colour', (210, 210, 180))
        self.border = kwargs.get('border', 10)
        self.topBorder = kwargs.get('topBorder', self.border)
        self.bottomBorder = kwargs.get('bottomBorder', self.border)
        self.leftBorder = kwargs.get('leftBorder', self.border)
        self.rightBorder = kwargs.get('rightBorder', self.border)
        self.borderRadius = kwargs.get('borderRadius', 0)
        self.separationThickness = kwargs.get('separationThickness', self.border)

        self.buttonAttributes = {
            # # Colour
            # 'inactiveColour': kwargs.get('inactiveColours', colors.ui_dark),
            # 'hoverColour': kwargs.get('hoverColours', colors.ui_white),
            # 'pressedColour': kwargs.get('pressedColours', self.frame_color),
            # 'shadowDistance': kwargs.get('shadowDistances', None),
            # 'shadowColour': kwargs.get('shadowColours', colors.shadow_color),
            # "borderColour":kwargs.get('borderColours', colors.border_color),
            # "inactiveBorderColour":kwargs.get('inactiveBorderColours', colors.inactive_color),
            # "hiddenColour": kwargs.get('hiddenColours', None),

            # Colour
            'inactiveColour': kwargs.get('inactiveColours', None),
            'hoverColour': kwargs.get('hoverColours', None),
            'pressedColour': kwargs.get('pressedColours', None),
            'shadowDistance': kwargs.get('shadowDistances', None),
            'shadowColour': kwargs.get('shadowColours', None),
            "borderColour": kwargs.get('borderColours', None),
            "inactiveBorderColour": kwargs.get('inactiveBorderColours', None),
            "hiddenColour": kwargs.get('hiddenColours', None),

            # Function
            'onClick': kwargs.get('onClicks', None),
            'onRelease': kwargs.get('onReleases', None),
            'onClickParams': kwargs.get('onClickParams', None),
            'onReleaseParams': kwargs.get('onReleaseParams', None),
            "property": kwargs.get('propertys', None),
            'layer': kwargs.get('layers', 4),

            # Text
            'textColour': kwargs.get('textColours', None),
            'font_size': kwargs.get('font_sizes', None),
            'text': kwargs.get('texts', None),
            'font': kwargs.get('fonts', None),
            'textHAlign': kwargs.get('textHAligns', None),
            'textVAlign': kwargs.get('textVAligns', None),
            'margin': kwargs.get('margins', None),
            'tooltip': kwargs.get('tooltips', None),
            'parent': kwargs.get('parents', None),
            "ui_parent": kwargs.get('ui_parents', None),
            "name": kwargs.get('names', None),
            "info_text": kwargs.get('info_texts', None),
            "array_parent": kwargs.get('array_parent', None),

            # Image
            'image': kwargs.get('images', None),
            'imageHAlign': kwargs.get('imageHAligns', None),
            'imageVAlign': kwargs.get('imageVAligns', None),
            'imageRotation': kwargs.get('imageRotations', None),
            'imageFill': kwargs.get('imageFills', None),
            'imageZoom': kwargs.get('imageZooms', None),
            'radius': kwargs.get('radii', None)
            }

        self.buttons = []
        self.createButtons()

    def createButtons(self):
        across, down = self.shape
        # error handling for empty shape
        if across == 0:
            return
        if down == 0:
            return

        width = (self.screen_width - self.separationThickness * (
                across - 1) - self.leftBorder - self.rightBorder) // across
        height = (self.screen_height - self.separationThickness * (
                down - 1) - self.topBorder - self.bottomBorder) // down

        count = 0
        for i in range(across):
            for j in range(down):
                x = self.screen_x + i * (width + self.separationThickness) + self.leftBorder
                y = self.screen_y + j * (height + self.separationThickness) + self.topBorder
                kwargs = {k: v[count] for k, v in self.buttonAttributes.items() if v is not None}
                self.buttons.append(Button(self.win, x, y, width, height, isSubWidget=True,
                    **kwargs)
                    )

                count += 1

    def listen_(self, events):
        pass

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            rects = [
                (self.screen_x + self.borderRadius, self.screen_y, self.screen_width - self.borderRadius * 2,
                 self.screen_height),
                (self.screen_x, self.screen_y + self.borderRadius, self.screen_width,
                 self.screen_height - self.borderRadius * 2)
                ]

            circles = [
                (self.screen_x + self.borderRadius, self.screen_y + self.borderRadius),
                (self.screen_x + self.borderRadius, self.screen_y + self.screen_height - self.borderRadius),
                (self.screen_x + self.screen_width - self.borderRadius, self.screen_y + self.borderRadius),
                (self.screen_x + self.screen_width - self.borderRadius,
                 self.screen_y + self.screen_height - self.borderRadius)
                ]

            for rect in rects:
                pass
                # pygame.draw.rect(self.win, self.colour, rect)
                # this draws the annoying background

            for circle in circles:
                pygame.draw.circle(self.win, self.colour, circle, self.borderRadius)

            # for button in self.buttons:
            #     button.draw()

    def getButtons(self):
        return self.buttons
