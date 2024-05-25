import pygame


def draw_bar_chart(win, color, rect):
    pygame.draw.rect(win, color, rect)

    pygame.draw.rect(self.win, get_average_color(i.image, consider_alpha=True), pygame.Rect(i.world_x, i.world_y, i.world_width / 2, 100))