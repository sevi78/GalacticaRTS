# import pygame
#
# from source.draw.arrow import ArrowCrossAnimatedArray
# from source.gui.lod import level_of_detail
# from source.handlers.color_handler import colors
# from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomSpriteBase
#
#
# class PanZoomTargetObject(PanZoomSpriteBase):
#     def __init__(
#             self,
#             win,
#             world_x,
#             world_y,
#             world_width,
#             world_height,
#             layer=0,
#             group=None,
#             parent=None,
#             ):
#         super().__init__(win, world_x, world_y, world_width, world_height, layer, group)
#         self.active = False
#
#         self.property = "target_object"
#         self.type = "target object"
#         self.parent = parent
#         self.id = self.parent.id
#         self.image = pygame.surface.Surface((10, 10))
#
#         self.target_cross = ArrowCrossAnimatedArray(
#                 self.win,
#                 colors.frame_color,
#                 (400, 300),
#                 40,
#                 0,
#                 8,
#                 1,
#                 3,
#                 5,
#                 0.8,
#                 -1)
#
#     def update(self):
#         if self.screen_position_changed or self._pan_zoom_changed():
#             self._update_screen_position()
#             self.screen_position_changed = False
#
#             self.inside_screen = level_of_detail.inside_screen(self.rect.center)
#
#         self.target_cross.update(self.rect.center)
#
#     def draw(self):
#         pygame.draw.rect(self.win, colors.frame_color, self.rect)
#         self.target_cross.draw()
