import time

import pygame
from pygame import MOUSEBUTTONDOWN, Rect

from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_model_config.qt_config import QT_RECT
from source.qt_universe.model.qt_quad_tree import get_nearest_object
from source.qt_universe.model.qt_time_handler import time_handler
from source.qt_universe.view import qt_draw
from source.qt_universe.view.qt_view_config import qt_draw_config
from source.qt_universe.view.shader_handler import shader_handler

NAVIGATOR_ANIM_TIME = 3.0
ZOOM_ANIM_TIME = 2.5


class Navigator__:
    def __init__(self, game):
        self.zoom_animating = False
        self.game = game
        self.navigation_animating = False
        self.target_obj = None
        self.start_time = time.time()
        self.zoom_start_time = time.time()
        self.end_x = None
        self.end_y = None
        self.current_zoom = None
        self.end_zoom = None

    def __str__(self):
        return f"self.animating: {self.animating}, self.target_obj: {self.target_obj}"  # , self.target_obj: {self.target_obj}, self.start_time: {self.start_time}, self.start_x: {self.start_x}, self.start_y: {self.start_y}"

    def navigate_to_world_position(self, x, y):
        """
        use obj.world_x, obj.world_y  as input for navigation:
        - sets the world offsets of the pan_zoom_handler = navigating
        """
        panzoom = pan_zoom_handler
        screen_x, screen_y = panzoom.world_2_screen(x, y)
        panzoom.set_world_offset(panzoom.screen_2_world(screen_x - panzoom.screen_width / 2, screen_y - panzoom.screen_height / 2))

    def navigate_to_obj(self, obj):
        """
        use obj as input for navigation
        -   gets the world position of the object
        -   sets the world offsets of the pan_zoom_handler using navigate_to_world_position
        """
        self.navigate_to_world_position(obj.x, obj.y)

    def navigate_to_obj_animated(self, obj):
        self.target_obj = obj

    def update_navigation_animation(self):  # no zooming
        # do nothing if no target obj is set
        obj = self.target_obj
        if not obj:
            return

        # start animation
        if not self.navigation_animating:
            self.start_time = time.time()

            # get the start position (center of the screen)
            self.end_x, self.end_y = pan_zoom_handler.screen_2_world(
                    self.game.qt_renderer.screen.get_width() / 2,
                    self.game.qt_renderer.screen.get_height() / 2)

            # set animating to true
            self.navigation_animating = True

        # animate
        if self.navigation_animating:
            print("navigate_to_obj_animated: animation in progress:", time.time() - self.start_time)
            current_time = time.time()
            elapsed_time = current_time - self.start_time

            # Calculate interpolation factor
            t = elapsed_time / NAVIGATOR_ANIM_TIME

            # Use easing function for smooth animation (optional)
            t = self.ease_out_cubic(t)

            # Interpolate between target position and end position
            new_x = self.end_x + (obj.x - self.end_x) * t
            new_y = self.end_y + (obj.y - self.end_y) * t

            # set panning to true to ensure the objects get updated
            pan_zoom_handler.panning = True
            # pan_zoom_handler.zooming = True

            # navigate to new position
            self.navigate_to_world_position(new_x, new_y)

            # reset animation, all variables
            if time.time() - self.start_time >= NAVIGATOR_ANIM_TIME:
                print("navigate_to_obj_animated: animation complete")
                self.navigation_animating = False
                self.end_x = None
                self.end_y = None
                # self.target_obj = None
                self.start_time = time.time()
                self.current_zoom = None
                self.end_zoom = None
                self.game.qt_renderer.debug_object = None
                pan_zoom_handler.panning = False
                # pan_zoom_handler.zooming = False

    def update_zoom_animation(self):
        obj = self.target_obj
        if not obj:
            return

        # start animation
        if not self.zoom_animating:
            self.zoom_start_time = time.time()

            # set the current_zoom
            self.current_zoom = pan_zoom_handler.zoom
            self.end_zoom = 1.0

            # set animating to true
            self.zoom_animating = True

        # animate
        if self.zoom_animating:
            print("navigate_to_obj_animated: zoom animation in progress:", time.time() - self.zoom_start_time)
            current_time = time.time()
            elapsed_time = current_time - self.zoom_start_time

            # Calculate interpolation factor
            t = elapsed_time / ZOOM_ANIM_TIME

            # Use easing function for smooth animation (optional)
            t = self.ease_out_cubic(t)

            # Interpolate between end_zoom and current_zoom
            pan_zoom_handler.set_zoom(self.current_zoom + (self.end_zoom - self.current_zoom) * t)

            # set zooming to true to ensure the objects get updated
            pan_zoom_handler.zooming = True

            # reset animation, all variables
            if time.time() - self.start_time >= ZOOM_ANIM_TIME:
                print("navigate_to_obj_animated: zoom animation complete")
                self.zoom_animating = False
                self.zoom_start_time = time.time()
                self.current_zoom = None
                self.end_zoom = None
                self.game.qt_renderer.debug_object = None
                self.target_obj = None
                pan_zoom_handler.zooming = False

    def ease_out_cubic(self, t):
        return 1 - (1 - t) ** 3

    def update(self):
        self.update_navigation_animation()
        self.update_zoom_animation()
        self.draw()

    def draw(self):
        if self.target_obj:
            self.game.qt_renderer.debug_object = self.target_obj



class Navigator:
    def __init__(self, game):
        self.game = game
        self.target_obj = None
        self.navigation_animating = False
        self.start_time = time.time()
        self.end_x = None
        self.end_y = None
        self.current_zoom = None
        self.end_zoom = None

    def __str__(self):
        return f"self.animating: {self.animating}, self.target_obj: {self.target_obj}"

    def navigate_to_world_position(self, x, y):
        """
        use obj.world_x, obj.world_y as input for navigation:
        - sets the world offsets of the pan_zoom_handler = navigating
        """
        panzoom = pan_zoom_handler
        screen_x, screen_y = panzoom.world_2_screen(x, y)
        panzoom.set_world_offset(panzoom.screen_2_world(screen_x - panzoom.screen_width / 2, screen_y - panzoom.screen_height / 2))

    def navigate_to_obj(self, obj):
        """
        use obj as input for navigation
        - gets the world position of the object
        - sets the world offsets of the pan_zoom_handler using navigate_to_world_position
        """
        self.navigate_to_world_position(obj.x, obj.y)

    def navigate_to_obj_animated(self, obj):
        self.target_obj = obj
        self.navigation_animating = True
        self.current_zoom = pan_zoom_handler.zoom
        self.end_zoom = 1.0
        self.start_time = time.time()
        self.end_x, self.end_y = pan_zoom_handler.screen_2_world(
            self.game.qt_renderer.screen.get_width() / 2,
            self.game.qt_renderer.screen.get_height() / 2)

    def update_navigation_animation(self):
        if not self.navigation_animating or not self.target_obj:
            return

        current_time = time.time()
        elapsed_time = current_time - self.start_time
        t = min(elapsed_time / NAVIGATOR_ANIM_TIME, 1)
        t = self.ease_out_cubic(t)

        new_x = self.end_x + (self.target_obj.x - self.end_x) * t
        new_y = self.end_y + (self.target_obj.y - self.end_y) * t

        pan_zoom_handler.panning = True

        # set the zoom, its hacky, but only works like this with ery slow values
        pan_zoom_handler.zoom = pan_zoom_handler.get_zoom() + 0.0003
        self.navigate_to_world_position(new_x, new_y)

        self.game.game_object_manager.update_objects()

        if t == 1:
            self.navigation_animating = False
            self.start_time = time.time()
            self.current_zoom = pan_zoom_handler.zoom
            self.end_zoom = 1.0
            self.reset_animation()



    def reset_animation(self):
        self.end_x = None
        self.end_y = None
        self.current_zoom = None
        self.end_zoom = None
        self.game.qt_renderer.debug_object = None
        self.target_obj = None
        pan_zoom_handler.panning = False
        pan_zoom_handler.zooming = False

    def ease_out_cubic(self, t):
        return 1 - (1 - t) ** 3

    def update(self):
        if self.navigation_animating:
            self.update_navigation_animation()
        self.draw()

    def draw(self):
        if self.target_obj:
            self.game.qt_renderer.debug_object = self.target_obj



class InteractionHandler:
    def __init__(self, game):
        self.game = game
        self._qtree = self.game.game_object_manager._qtree
        self._qt_rect = self.game.qt_renderer.screen_rect
        self.show_qtree = False
        self.double_click = False
        self.last_click_time = time.time()

        self.navigator = Navigator(game)

    def handle_double_click(self):
        if self.double_click:
            self.navigator.navigate_to_obj_animated(get_nearest_object(self.game.game_object_manager._qtree,
                    pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], ["sun", "planet", "moon"], 100))
            self.double_click = False
            return True

    def handle_events(self, events):
        self.navigator.update()
        self.handle_mouse_events(events)
        self.handle_key_events(events)

    def handle_mouse_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    current_time = time.time()

                    elapsed_time = current_time - self.last_click_time
                    if elapsed_time < 0.5:  # 0.5 seconds for double-click
                        self.double_click = True
                        self.handle_double_click()
                    else:
                        self.double_click = False
                    self.last_click_time = current_time

            # if event.type == MOUSEMOTION:
            #     draw.circle(self.game.qt_renderer.screen, (255, 0, 0), event.pos, 5)

        # search_area_size = 100
        # search_area_rect = Rect(pygame.mouse.get_pos()[0]-search_area_size/2, pygame.mouse.get_pos()[1]-search_area_size/2, search_area_size, search_area_size)
        #
        # world_search_area = get_search_area(search_area_rect)
        # visible_objects = self.game.game_object_manager._qtree.query(world_search_area)
        #
        #
        # for obj in visible_objects:
        #     draw.rect(self.game.qt_renderer.screen, (255, 255, 0), (obj.rect.x, obj.rect.y, 20,20), 1)

        # draw.rect(self.game.qt_renderer.screen,RED, search_area_rect, 1)

        # nearest_sun = get_nearest_object(self.game.game_object_manager._qtree, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], "sun", 100)
        #
        # if nearest_sun:
        #     draw.circle(self.game.qt_renderer.screen, (255, 0, 0), (nearest_sun.rect.x, nearest_sun.rect.y), 5)

    def handle_key_events(self, events):
        # print(event.key)
        # if event.key == pygame.K_r:
        #     self._qtree = QuadTree(self._qt_rect, QT_CAPACITY)
        #     add_random_game_objects(self._qtree, POINTS_AMOUNT)
        # elif event.key == pygame.K_c:
        #     self._qtree = QuadTree(self._qt_rect, QT_CAPACITY)
        #     self._qtree.clear()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.show_qtree = not self.show_qtree

                elif event.key == 1073741911:
                    print("set_game_speed: ", time_handler.game_speed)  # plus
                    time_handler.set_game_speed(time_handler.game_speed + 1)

                elif event.key == 1073741910:  # pygame.K_MINUS:
                    print("set_game_speed: ", time_handler.game_speed)  # plus
                    time_handler.set_game_speed(time_handler.game_speed - 1)

                elif event.key == pygame.K_d and not event.mod & pygame.KMOD_SHIFT:
                    print("qt_draw.DEBUG", qt_draw.DEBUG)
                    qt_draw.DEBUG = not qt_draw.DEBUG

                elif event.key == pygame.K_d and event.mod & pygame.KMOD_SHIFT:
                    print("qt_draw_config.DRAW_SHADER", qt_draw_config.DRAW_SHADER)
                    qt_draw_config.DRAW_SHADER = not qt_draw_config.DRAW_SHADER
                    shader_handler.setup_shader_handler()

                elif event.key == pygame.K_s and event.mod & pygame.KMOD_SHIFT:
                    print("save")
                    self.game.game_object_manager.save_load.save(self.game.game_object_manager.all_objects)

                elif event.key == pygame.K_l and event.mod & pygame.KMOD_SHIFT:
                    print("load")
                    self.game.game_object_manager.save_load.load("test.json", "qt_database")

                elif event.key == pygame.K_c and event.mod & pygame.KMOD_SHIFT:
                    print("create universe")
                    self.game.universe_factory.delete_universe()
                    self.game.universe_factory.create_universe(QT_RECT)

                elif event.key == pygame.K_p:
                    print("selecting all planets")
                    self.game.game_object_manager.select_objects_by_type("planet")

                elif event.key == pygame.K_m:
                    print("selecting all moons")
                    self.game.game_object_manager.select_objects_by_type("moon")

                elif event.key == pygame.K_i and not event.mod & pygame.KMOD_SHIFT:
                    print("selecting all collectable_items")
                    self.game.game_object_manager.select_objects_by_type("collectable_item")

                elif event.key == pygame.K_i and event.mod & pygame.KMOD_SHIFT:
                    print (f"qt_draw_config.DRAW_IMAGES: {qt_draw_config.DRAW_IMAGES}")
                    qt_draw_config.DRAW_IMAGES = not qt_draw_config.DRAW_IMAGES

                elif event.key == pygame.K_s and not event.mod & pygame.KMOD_SHIFT:
                    print("selecting all suns")
                    self.game.game_object_manager.select_objects_by_type("sun")

                elif event.key == pygame.K_h:
                    print (f"qt_draw_config.DRAW_SHADER: {qt_draw_config.DRAW_SHADER}")
                    qt_draw_config.DRAW_SHADER = not qt_draw_config.DRAW_SHADER
                    shader_handler.setup_shader_handler()
                    self.game.qt_renderer.setup_qt_renderer()

    def get_visible_rect(self):
        return Rect(pan_zoom_handler.world_offset_x, pan_zoom_handler.world_offset_y,
                pygame.display.get_surface().get_width() / pan_zoom_handler.get_zoom(),
                pygame.display.get_surface().get_height() / pan_zoom_handler.get_zoom())

    def get_object_screen_rect(self, obj):
        screen_x, screen_y = pan_zoom_handler.world_2_screen(obj.x, obj.y)
        return Rect(
                screen_x - obj.width * pan_zoom_handler.get_zoom() / 2,
                screen_y - obj.height * pan_zoom_handler.get_zoom() / 2,
                obj.width * pan_zoom_handler.get_zoom(),
                obj.height * pan_zoom_handler.get_zoom()
                )
