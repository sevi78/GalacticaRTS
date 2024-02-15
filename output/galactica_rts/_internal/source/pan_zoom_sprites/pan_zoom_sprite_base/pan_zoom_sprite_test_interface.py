import pygame
from pygame import K_s, K_a, K_w, K_d


class PanZoomSpriteTestInterace:
    def __init__(self, parent):
        self.parent = parent

    def keyboard_input(self, obj):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            obj.world_y -= obj.speed
        if keys[K_s]:
            obj.world_y += obj.speed
        if keys[K_a]:
            obj.world_x -= obj.speed
        if keys[K_d]:
            obj.world_x += obj.speed

        obj.world_position = (obj.world_x, obj.world_y)
