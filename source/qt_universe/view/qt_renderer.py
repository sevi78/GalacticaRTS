import pygame
from pygame import Rect

from source.math.math_handler import ndigits
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_time_handler import time_handler
from source.qt_universe.view.qt_debugger import draw_debug_text
from source.qt_universe.view.qt_draw import draw_objects
from source.qt_universe.view.qt_draw_methods import draw_quadtree_boundary, draw_quadtree


class QTRenderer__:  # original
    def __init__(self, game) -> None:
        self.game = game

    def draw(self) -> None:
        # Clear the screen
        self.game.screen.fill((0, 0, 0))

        # Clear the universe surface
        self.game.universe_surface.fill((0, 0, 0))

        # Draw the points onto the universe surface
        self.draw_objects()

        # Draw the universe surface onto the main screen
        self.game.screen.blit(self.game.universe_surface, (0, 0))

        # Draw box selection
        self.game.box_selection.draw()

        # Draw the quadtree boundary
        self.draw_quadtree_boundary()

        # Draw debug text directly on the screen
        self.draw_debug_text()

        # Finally, update the screen
        pygame.display.update()

    def draw_objects(self) -> None:
        draw_objects(self.game.universe_surface, self.game.game_object_manager._qtree,
                self.game.get_screen_search_area())

    def draw_quadtree_boundary(self) -> None:
        draw_quadtree_boundary(self.game.game_object_manager._qtree,
                self.game.screen, pan_zoom_handler)
        if self.game.interaction_handler.show_qtree:
            draw_quadtree(self.game.game_object_manager._qtree,
                    self.game.screen, pan_zoom_handler)

    def draw_debug_text(self) -> None:
        draw_debug_text(self.game.screen, {
            "fps": self.game._clock.get_fps(),
            "game_speed": time_handler.game_speed,
            "point_count": self.game.game_object_manager._qtree.count(),
            "dynamic_object_count": len(self.game.game_object_manager.dynamic_objects),
            "zoom:": pan_zoom_handler.get_zoom(),
            "lod:": ndigits(pan_zoom_handler.get_zoom(), 4)
            })


class QTRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.screen_rect = Rect(0, 0, 1920, 1080)
        self.screen = pygame.display.set_mode([self.screen_rect.w, self.screen_rect.h], pygame.RESIZABLE)
        # self.screen = pygame.display.set_mode([self.screen_rect.w, self.screen_rect.h], pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE, display=0)

        # the surface where the univers objects are drawn
        self.universe_surface = pygame.Surface(self.screen.get_size())

        # define the screen_shader
        # self.screen_shader = pygame_shaders.DefaultScreenShader(self.universe_surface) # <- Here we supply our default display, it's this display which will be displayed onto the opengl context via the screen_shader

    def draw(self) -> None:
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Clear the universe surface
        self.universe_surface.fill((0, 0, 0))

        # Draw the points onto the universe surface
        self.draw_objects()

        # Draw the universe surface onto the main screen
        self.screen.blit(self.universe_surface, (0, 0))

        # Draw box selection
        self.game.box_selection.draw()

        # Draw the quadtree boundary
        self.draw_quadtree_boundary()

        # Draw debug text directly on the screen
        self.draw_debug_text()

        # this renders the shader to the display
        # self.screen_shader.render()

        pygame.display.flip()

        # Finally, update the screen
        pygame.display.update()

    def draw_objects(self) -> None:
        draw_objects(self.game.qt_renderer.universe_surface, self.game.game_object_manager._qtree,
                self.game.get_screen_search_area())

    def draw_quadtree_boundary(self) -> None:
        draw_quadtree_boundary(self.game.game_object_manager._qtree,
                self.game.qt_renderer.screen, pan_zoom_handler)
        if self.game.interaction_handler.show_qtree:
            draw_quadtree(self.game.game_object_manager._qtree,
                    self.game.qt_renderer.screen, pan_zoom_handler)

    def draw_debug_text(self) -> None:
        draw_debug_text(self.game.qt_renderer.screen, {
            "fps": self.game._clock.get_fps(),
            "game_speed": time_handler.game_speed,
            "point_count": self.game.game_object_manager._qtree.count(),
            "dynamic_object_count": len(self.game.game_object_manager.dynamic_objects),
            "zoom:": pan_zoom_handler.get_zoom(),
            "lod:": ndigits(pan_zoom_handler.get_zoom(), 4)
            })
