import pygame.display

from source.configuration.game_config import config
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.text.text_formatter import format_number, get_reduced_number

FONT_SIZE = 10


class ZoomScale(WidgetBase):
    """
    shows the zoom factor and the world width in km as a line thing with edges
    """

    def __init__(self, win, x, y, width, height, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height)
        # set world_width_raw used for scaling
        self.world_width_raw = width

        # generate start and end position
        self.start_pos = (self.world_x, self.world_y + self.world_height)
        self.end_pos = (self.world_x + self.world_width, self.world_y + self.world_height)
        self.reduced_number = 1

        # set zoom factor
        self.zoom = 1

        # set text
        self.text = ""
        self.font_size = FONT_SIZE
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.text_spacing = self.font_size / 3
        self.dist_str = ""
        self.anchor_left = kwargs.get("anchor_left", None)
        self.update()

    def get_screen_dist(self) -> int:
        """ gets the distance recalculated from world_width_raw and zoom, used factor 1000 for correct size"""
        return self.world_width_raw / pan_zoom_handler.zoom * 1000

    def get_distance_string(self) -> str:
        """ generates a string with the distance in km"""
        dist = self.get_screen_dist()
        f_str = format_number(dist, 1)
        return f_str

    def set_zoom(self, value):
        self.zoom = value
        self.update()

    def update(self):
        # dirty hack to make sure its displayed correctly ;()
        # but still better than update every frame
        for i in range(2):
            # generate start and end position
            self.start_pos = (self.world_x, self.world_y + self.world_height)
            self.end_pos = (self.world_x + self.world_width, self.world_y + self.world_height)

            # calc reduced number
            self.reduced_number = get_reduced_number(self.get_screen_dist())

            # generate text
            self.dist_str = format_number(self.reduced_number, 1)
            self.text = self.font.render(f"{self.dist_str} km", True, self.frame_color)

            # set new width
            new_width = pan_zoom_handler.zoom * self.reduced_number / 1000
            self.world_width = new_width

    def set_positions(self):
        if self.anchor_left:
            if self.anchor_left.visible:
                self.world_x = self.anchor_left.world_x + self.anchor_left.world_width + 20
            else:
                self.world_x = 20

        self.start_pos = (self.world_x, self.world_y + self.world_height)
        self.end_pos = (self.world_x + self.world_width, self.world_y + self.world_height)

    def draw(self) -> None:
        self.set_positions()

        # draw horizontal line
        pygame.draw.line(self.win, self.frame_color, self.start_pos, self.end_pos, 1)

        # draw vertical lines
        pygame.draw.line(self.win, self.frame_color, self.start_pos, (
            self.start_pos[0], self.start_pos[1] - self.world_height), 1)
        pygame.draw.line(self.win, self.frame_color, self.end_pos, (
            self.end_pos[0], self.end_pos[1] - self.world_height), 1)

        # draw text
        self.win.blit(self.text, (
            self.world_x + self.world_width - 30 - (self.text_spacing * len(self.dist_str)), self.world_y - 5))


def main():
    win = pygame.display.set_mode((500, 500))
    zoom_scale = ZoomScale(win, 10, 10, 100, 5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        win.fill((0, 0, 0))
        zoom_scale.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
