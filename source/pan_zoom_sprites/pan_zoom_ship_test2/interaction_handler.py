import pygame

from source.configuration.game_config import config
from source.handlers.pan_zoom_sprite_handler import sprite_groups

#
# class InteractionHandler2:
#     def __init__(self, win):
#         self.win = win
#         self.interactable_objects = []
#
#     def add(self, obj):
#         self.interactable_objects.append(obj)
#
#     def remove(self, obj):
#         self.interactable_objects.remove(obj)
#
#     def handle_mouse(self):
#         mouse_pos = pygame.mouse.get_pos()
#
#         # on left click ( only one click)
#         if pygame.mouse.get_just_pressed()[0]:
#             for obj in self.interactable_objects:
#                 # on obj
#                 if obj.collide_rect.collidepoint(mouse_pos):
#                     obj.selected = not obj.selected
#                 # somewhere else than the obj
#                 # else:
#                 #     obj.logic.selected = False
#
#         # # on right click ( only one click)
#         if pygame.mouse.get_just_pressed()[2]:
#             for obj in self.interactable_objects:
#                 if obj.state_engine.state == "waiting for order":
#                     obj.movement_handler.set_target( mouse_pos)
#
#
#         # if pygame.mouse.get_just_released()[0]:
#         # self.rotate_to(mouse_pos)
#
#
#         print (self.get_hit_object(mouse_pos))
#
#     def get_hit_object(self, mouse_pos, **kwargs):
#         filter_ = kwargs.get("filter", [])
#         lists = kwargs.get("lists", ["planets", "ships", "ufos", "collectable_items", "celestial_objects"])
#         lists = [l for l in lists if l not in filter_]
#
#         for list_name in lists:
#             sprite_list = getattr(sprite_groups, list_name, None)
#             if sprite_list is not None:
#                 for sprite in sprite_list:
#                     if sprite.rect.collidepoint(mouse_pos):
#                         return sprite
#
#         return None
#
#     def debug_object(self):
#
#         fontsize = 15
#         font = pygame.font.Font(None, fontsize)  # You might want to store this as a class attribute for efficiency
#         y_offset = 0
#
#         text = f"Interaction:\n"
#         for attr in self.__dict__:
#             if not hasattr(self, attr):
#                 continue
#             value = getattr(self, attr)
#             text += f"{attr}: {value}\n"
#
#         text_surface = font.render(text, True, (255, 255, 255))  # White text
#         self.win.blit(text_surface, (10, 400 + y_offset))
#         y_offset += fontsize  # Move down for next line of text
#
#
# interaction_handler2 = InteractionHandler2(config.win)

class InteractionHandler2:
    def __init__(self, win):
        self.win = win
        self.interactable_objects = []
        self.mouse_pos = (0, 0)
        self.hit_object = None
        self.hit_object_list = []

    def add(self, obj):
        self.interactable_objects.append(obj)

    def remove(self, obj):
        self.interactable_objects.remove(obj)

    def update_mouse_position(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def update_hit_objects(self, **kwargs):
        self.hit_object_list = self.get_hit_objects(**kwargs)
        self.hit_object = self.hit_object_list[0] if self.hit_object_list else None

    def handle_mouse(self):
        self.update_mouse_position()
        self.update_hit_objects()

        # on left click (only one click)
        if pygame.mouse.get_just_pressed()[0]:
            for obj in self.interactable_objects:
                if obj.collide_rect.collidepoint(self.mouse_pos):
                    obj.selected = not obj.selected

        # on right click (only one click)
        if pygame.mouse.get_just_pressed()[2]:
            for obj in self.interactable_objects:
                if obj.state_engine.state == "waiting for order":
                    obj.set_target(self.mouse_pos)



    def get_hit_objects(self, **kwargs):
        filter_ = kwargs.get("filter", [])
        lists = kwargs.get("lists", ["planets", "ships", "ufos", "collectable_items", "celestial_objects"])
        lists = [l for l in lists if l not in filter_]

        hit_objects = []
        for list_name in lists:
            sprite_list = getattr(sprite_groups, list_name, None)
            if sprite_list is not None:
                for sprite in sprite_list:
                    if sprite.rect.collidepoint(self.mouse_pos):
                        hit_objects.append(sprite)

        return hit_objects

    def debug_object(self):
        fontsize = 15
        font = pygame.font.Font(None, fontsize)
        y_offset = 0

        text = f"Interaction:\n"
        for attr in self.__dict__:
            if not hasattr(self, attr):
                continue
            value = getattr(self, attr)
            text += f"{attr}: {value}\n"

        text_surface = font.render(text, True, (255, 255, 255))
        self.win.blit(text_surface, (10, 400 + y_offset))
        y_offset += fontsize

# Usage
interaction_handler2 = InteractionHandler2(config.win)

# # In your main game loop:
# interaction_handler2.handle_mouse()

