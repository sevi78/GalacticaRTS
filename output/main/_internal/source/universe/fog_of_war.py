import pygame
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.utils import global_params


class FogOfWar(WidgetBase):
    """Main functionalities:
    The FogOfWar class is a subclass of WidgetBase and Moveable classes. It represents a surface that is used to draw a
    fog of war effect on the game screen. The fog of war is drawn as a circle around a given object,
    with a radius determined by the object's fog_of_war_radius attribute. The class has methods for drawing the fog of
    war circle, listening to events, and drawing the fog of war surface on the game screen.

    Methods:
    - __init__: initializes the FogOfWar object, setting its position, size, and layer, and creating a surface to draw
      the fog of war effect on.
    - draw: draws the fog of war surface on the game screen.
    - listen: listens to events, but does nothing.
    - draw_fog_of_war: draws the fog of war circle on the fog of war surface, centered around a given object and with a
      radius determined by the object's fog_of_war_radius attribute.

    Fields:
    - layer: an integer representing the layer of the fog of war surface.
    - surface: a pygame.Surface object representing the surface to draw the fog of war effect on."""

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 2)
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey((60, 60, 60))

    def draw(self):
        self.win.blit(self.surface, (self.screen_x, self.screen_y))

    def draw_fog_of_war(self, obj, **kwargs):
        """
        draws the fog of war circle based on the fog of war raduis of the obj
        :param obj:
        :param kwargs:
        :return:
        """
        if not global_params.app:  # bullshit here, bad initializing
            return
        x, y = kwargs.get("x", obj.get_screen_x() + obj.get_screen_width() / 2), kwargs.get("y", obj.get_screen_y() + obj.get_screen_height() / 2)

        # recalculate position because fog of war surface is moved too
        x = x - global_params.app.fog_of_war.get_screen_x()
        y = y - global_params.app.fog_of_war.get_screen_y()
        radius = kwargs.get("radius", obj.fog_of_war_radius)
        pygame.draw.circle(surface=self.surface, color=(60, 60, 60), center=(
            x, y), radius=radius, width=0)
