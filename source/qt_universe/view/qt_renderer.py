import pygame
from pygame import Rect, draw

from source.math.math_handler import ndigits
from source.pygame_shaders import pygame_shaders
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_time_handler import time_handler
from source.qt_universe.view.qt_debugger import draw_debug_text
from source.qt_universe.view.qt_draw import draw_objects
from source.qt_universe.view.qt_draw_methods import draw_quadtree_boundary, draw_quadtree
from source.qt_universe.view.qt_view_config import qt_draw_config
from source.qt_universe.view.qt_view_config.qt_draw_config import  RED

WIDTH, HEIGHT = 1920, 1080


# class QTRenderer__:  # original
#     def __init__(self, game) -> None:
#         self.game = game
#
#     def draw(self) -> None:
#         # Clear the screen
#         self.game.screen.fill((0, 0, 0))
#
#         # Clear the universe surface
#         self.game.universe_surface.fill((0, 0, 0))
#
#         # Draw the points onto the universe surface
#         self.draw_objects()
#
#         # Draw the universe surface onto the main screen
#         self.game.screen.blit(self.game.universe_surface, (0, 0))
#
#         # Draw box selection
#         self.game.box_selection.draw()
#
#         # Draw the quadtree boundary
#         self.draw_quadtree_boundary()
#
#         # Draw debug text directly on the screen
#         self.draw_debug_text()
#
#         # Finally, update the screen
#         pygame.display.update()
#
#     def draw_objects(self) -> None:
#         draw_objects(self.game.universe_surface, self.game.game_object_manager._qtree,
#                 self.game.get_screen_search_area())
#
#     def draw_quadtree_boundary(self) -> None:
#         draw_quadtree_boundary(self.game.game_object_manager._qtree,
#                 self.game.screen, pan_zoom_handler)
#         if self.game.interaction_handler.show_qtree:
#             draw_quadtree(self.game.game_object_manager._qtree,
#                     self.game.screen, pan_zoom_handler)
#
#     def draw_debug_text(self) -> None:
#         draw_debug_text(self.game.screen, {
#             "fps": self.game._clock.get_fps(),
#             "game_speed": time_handler.game_speed,
#             "point_count": self.game.game_object_manager._qtree.count(),
#             "dynamic_object_count": len(self.game.game_object_manager.dynamic_objects),
#             "zoom:": pan_zoom_handler.get_zoom(),
#             "lod:": ndigits(pan_zoom_handler.get_zoom(), 4)
#             })


class QTRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.screen_rect = Rect(0, 0, WIDTH, HEIGHT)
        self.screen_shader = None
        self.screen = None
        # the surface where the univers objects are drawn
        self.universe_surface = pygame.Surface((WIDTH, HEIGHT))

        # dirty hack for debugging
        self.debug_object = None

        self.setup_qt_renderer()
    def setup_qt_renderer(self):
        if qt_draw_config.DRAW_SHADER:
            self.screen = pygame.display.set_mode((
                1920, 1080), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE, display=0)
            # define the screen_shader
            self.screen_shader = pygame_shaders.DefaultScreenShader(self.universe_surface)  # <- Here we supply our default display, it's this display which will be displayed onto the opengl context via the screen_shader
        else:
            self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE, display=0)
        # self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE, display=0)




    def draw_objects(self) -> None:
        draw_objects(self.game.qt_renderer.universe_surface, self.game.game_object_manager._qtree,
                self.game.get_screen_search_area())

    def draw_quadtree_boundary(self) -> None:
        draw_quadtree_boundary(self.game.game_object_manager._qtree,
                self.game.qt_renderer.universe_surface, pan_zoom_handler)

    def draw_debug_text(self, screen) -> None:
        # print (self.game._clock.get_fps())

        draw_debug_text(screen, {
            "fps": self.game._clock.get_fps(),
            "game_speed": time_handler.game_speed,
            "point_count": self.game.game_object_manager._qtree.count(),
            "dynamic_object_count": len(self.game.game_object_manager.dynamic_objects),
            "zoom:": pan_zoom_handler.get_zoom(),
            "lod:": ndigits(pan_zoom_handler.get_zoom(), 4)
            })

    def draw_debug_rect(self):
        if self.debug_object:
            rect = Rect(0,0, 100, 100)
            rect.center = self.debug_object.rect.center
            draw.rect(self.screen, RED, rect, 1)

    def draw(self) -> None:
        # Clear the screen
        # self.screen.fill((0, 0, 0))

        # Clear the universe surface
        self.universe_surface.fill((0, 0, 0))

        # Draw the points onto the universe surface
        self.draw_objects()

        # Draw the quadtree boundary
        self.draw_quadtree_boundary()

        # draw quadtree
        if self.game.interaction_handler.show_qtree:
            draw_quadtree(self.game.game_object_manager._qtree, self.universe_surface, pan_zoom_handler)

        if qt_draw_config.DRAW_SHADER:
            # Draw debug text  on the universe_surface
            # self.draw_debug_text(self.universe_surface)
            # this renders the shader to the display

            # rendered_shader = self.shader.render()
            #
            # # then render the shader onto the display
            # screen.blit(rendered_shader, (0, 0), special_flags=pygame.BLEND_MAX)

            self.screen_shader.render()
            # pygame.display.flip()

        else:

            # Draw the universe surface onto the main screen
            self.screen.blit(self.universe_surface, (0, 0))

        # Draw debug text  on the universe_surface
        self.draw_debug_text(self.screen)

        # Draw box selection
        self.game.box_selection.draw()

        # draw debug rect
        self.draw_debug_rect()

        # pygame.display.flip()
        # pygame.display.update()
