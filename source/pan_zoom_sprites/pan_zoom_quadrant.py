import pygame.display
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

from source.gui.lod import inside_screen
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.universe.universe_background import Universe
from source.utils.global_params import global_params
from source.utils.mouse import Mouse

WIDTH, HEIGHT = 800, 800


class Quadrant(PanZoomSprite):
    """this holds the universe of the space in the rect of (x,y,width,height)"""

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)

        # we need to overload this, otherwise it will get the image size of PanZoomSprite, wich is no_image size
        self.world_width = width
        self.world_height = height
        # self.update_pan_zoom_sprite()
        self.universe = Universe(self.win, x, y, width, height)

    def hide_universe(self):
        for key, value in self.universe.celestial_objects.items():
            for obj in value:
                obj.hide()

    def show_universe(self):
        for key, value in self.universe.celestial_objects.items():
            for obj in value:
                obj.show()

    def update(self):
        self.update_pan_zoom_sprite()
        # self.set_world_position((self.world_x, self.world_y))
        if inside_screen(self.rect.center):
            # self.show_universe()
            # self.show()

            pass
            # print ("Quadrant.update")

        else:
            pass
            # self.hide_universe()
            # self.hide()


def main(win):
    running = True
    while running:

        win.fill((0, 0, 0))
        events = pygame.event.get()
        pan_zoom_handler.listen(events, True)
        max_w = win.get_width() / pan_zoom_handler.zoom_min
        print(max_w, pan_zoom.zoom, pan_zoom_handler.zoom)

        Mouse.updateMouseState()

        # Event handling
        for event in events:
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        events = pygame.event.get()

        # print("pan_zoom_handler", pan_zoom_handler)
        sprite_groups.update()
        # sprite_groups.listen(events)
        # sprite_groups.draw(win)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    global_params.show_grid = True
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    x, y = 200, 300
    width, height = 100, 100
    pan_zoom = pan_zoom_handler
    image_name = "no_icon.png"

    # quadrant = Quadrant(win, x, y, width, height, pan_zoom, image_name, group="quadrants")

    main(win)
