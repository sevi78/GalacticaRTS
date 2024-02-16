import pygame
from pygame_widgets.util import drawText

from source.configuration import global_params
from source.gui.lod import level_of_detail
from source.handlers.color_handler import colors


class GameObjectDebug:
    def __init__(self):
        pass

    def debug_object(self):
        color = colors.frame_color
        if not level_of_detail.inside_screen(self.rect.center):
            color = colors.outside_screen_color

        # center
        pygame.draw.circle(global_params.win, pygame.color.THECOLORS["white"], self.rect.center, 5, 1)
        # rect
        pygame.draw.rect(global_params.win, color, self.rect, 1)

        # attack_distance
        if hasattr(self, "attack_distance"):
            pygame.draw.circle(global_params.win, color, self.rect.center, self.attack_distance, 1)

        # target
        if hasattr(self, "target"):
            if self.target:
                pygame.draw.line(global_params.win,
                    pygame.color.THECOLORS["red"], self.rect.center, self.target.rect.center, 1)

                # pygame.draw.line(global_params.win, colors.select_color, self.rect.center, self.target_position, 1)

        # orbit_obj
        if hasattr(self, "orbit_obj"):
            if self.orbit_obj:
                pygame.draw.line(global_params.win,
                    pygame.color.THECOLORS["red"], self.rect.center, self.orbit_obj.rect.center, 1)

        if hasattr(self, "world_x"):
            if hasattr(self, "property"):
                if self.property == "planet":
                    pygame.draw.circle(global_params.win,
                        pygame.color.THECOLORS["red"], (self.world_x, self.world_y), 20, 1)
                    pygame.draw.line(global_params.win,
                        pygame.color.THECOLORS["red"], self.rect.center, (self.world_x, self.world_y), 1)

                    pos = (self.screen_x + self.get_screen_width() / 2, self.screen_y + self.get_screen_height() / 2)
                    pos = self.center
                    pygame.draw.line(global_params.win,
                        pygame.color.THECOLORS["blue"], self.rect.center, pos, 1)


        # text
        font = pygame.font.SysFont(global_params.font_name, 18)
        text = self.type
        drawText(global_params.app.win, text, color, (
            self.rect.x, self.rect.y, 400, 30), font, "left")