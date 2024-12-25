import sys

import pygame
from pygame import Vector2

from source.draw.arrow import ArrowCrossAnimatedArray
from source.gui.lod import level_of_detail
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomSpriteBase, PanZoomMovingRotatingImage


class ShipLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()
        self.events = []

    def update(self, *args):
        for sprite in self.sprites():
            sprite.update(*args)
            for event in self.events:
                if hasattr(sprite, 'listen'):
                    sprite.listen(event)
        self.events.clear()

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if spr.inside_screen:
                if spr.image:
                    self.spritedict[spr] = surface_blit(spr.image, spr.rect)
                else:
                    spr.draw()
            if spr.debug:
                spr.debug_object()
        self.lostsprites = []

    def handle_events(self, events):
        self.events.extend(events)


# class PanZoomShip(PanZoomMovingRotatingImage):
#     __slots__ = PanZoomMovingRotatingImage.__slots__ + ('selected', 'target_object')
#
#     def __init__(
#             self,
#             win: pygame.Surface,
#             world_x: int,
#             world_y: int,
#             world_width: int,
#             world_height: int,
#             layer: int = 0,
#             group: ShipLayeredUpdates = None,
#             image_name: str = "spaceship.png",
#             id=None
#             ):
#         super().__init__(
#                 win, world_x, world_y, world_width, world_height,
#                 layer, group, image_name
#                 )
#         self.selected = True
#         self.id = id
#         self.target = None
#         self.target_object = PanZoomTargetObject(
#                 win=win,
#                 world_x=world_x,
#                 world_y=world_y,
#                 world_width=20,
#                 world_height=20,
#                 group=group,
#                 parent=self
#                 )
#
#     def update(self):
#         super().update()
#
#         if self.selected:
#             self.rotate_to_mouse()
#
#         if self.target_object.active:
#             self.rotate_to_target()
#             self.move_to_target()
#
#     def rotate_to_mouse(self):
#         mouse_pos = Vector2(pygame.mouse.get_pos())
#         self.rotate_towards(mouse_pos)
#
#     def rotate_to_target(self):
#         target_pos = Vector2(self.target_object.rect.center)
#         self.rotate_towards(target_pos)
#
#     def rotate_towards(self, target_pos):
#         direction = target_pos - Vector2(self.rect.center)
#         angle = direction.angle_to(Vector2(1, 0))
#         self.rotation_angle = -angle
#
#     def move_to_target(self):
#         target_pos = Vector2(self.target_object.rect.center)
#         direction = target_pos - Vector2(self.rect.center)
#         if direction.length() > 1:
#             self.direction = direction.normalize()
#         else:
#             self.direction = Vector2(0, 0)
#             self.target_object.active = False
#
#     def listen(self, event):
#
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 3:  # Right mouse button
#                 mouse_pos = pygame.mouse.get_pos()
#                 self.set_target(mouse_pos)
#
#     def set_target(self, pos):
#         self.target_object.set_position(*pos)
#         self.target_object.active = True
#
class PanZoomShip_1(PanZoomMovingRotatingImage):
    __slots__ = PanZoomMovingRotatingImage.__slots__ + ('selected', 'target_object')

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group: ShipLayeredUpdates = None,
            image_name: str = "spaceship.png",
            id=None
            ):
        super().__init__(
                win, world_x, world_y, world_width, world_height,
                layer, group, image_name
                )
        self.selected = True
        self.id = id
        self.target = None
        self.target_object = PanZoomTargetObject(
                win=win,
                world_x=world_x,
                world_y=world_y,
                world_width=20,
                world_height=20,
                group=group,
                parent=self
                )

    def update(self):
        super().update()
        if self.selected:
            self.rotate_to_mouse()

        if self.target_object.active:
            self.rotate_to_target()
            self.move_to_target()

    def rotate_to_mouse(self):
        mouse_pos = Vector2(pygame.mouse.get_pos())
        self.rotate_towards(mouse_pos)

    def rotate_to_target(self):
        target_pos = Vector2(self.target_object.rect.center)
        self.rotate_towards(target_pos)

    def rotate_towards(self, target_pos):
        direction = target_pos - Vector2(self.rect.center)
        angle = direction.angle_to(Vector2(1, 0))
        self.rotation_angle = -angle
        self.rotate(self.rotation_angle)

    def move_to_target(self):
        target_pos = Vector2(self.target_object.rect.center)
        direction = target_pos - Vector2(self.rect.center)
        if direction.length() > 1:
            self.direction = direction.normalize()
        else:
            self.direction = Vector2(0, 0)
            self.target_object.active = False

    def listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                mouse_pos = pygame.mouse.get_pos()
                self.set_target(mouse_pos)

    def set_target(self, pos):
        self.target_object.set_position(*pos)
        self.target_object.active = True


class PanZoomShip(PanZoomMovingRotatingImage):
    __slots__ = PanZoomMovingRotatingImage.__slots__ + ('selected', 'target_object')

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group: ShipLayeredUpdates = None,
            image_name: str = "spaceship.png",
            id=None
            ):
        super().__init__(
                win, world_x, world_y, world_width, world_height,
                layer, group, image_name
                )
        self.selected = True
        self.id = id

        self.target_object = PanZoomTargetObject(
                win=win,
                world_x=world_x,
                world_y=world_y,
                world_width=20,
                world_height=20,
                group=group,
                parent=self
                )
        self.target = self.target_object

        self.debug = True

    def update(self):
        super().update()
        if self.selected:
            self.rotate_to(pygame.mouse.get_pos())

    def rotate_to(self, pos: tuple):
        direction = pos - Vector2(self.rect.center)
        correction_angle = 270
        angle = direction.angle_to(Vector2(1, 0))
        self.rotation_angle = angle + correction_angle

    # def move_to_target(self):
    #     target_pos = Vector2(self.target_object.rect.center)
    #     direction = target_pos - Vector2(self.rect.center)
    #     if direction.length() > 1:
    #         self.direction = direction.normalize()
    #     else:
    #         self.direction = Vector2(0, 0)
    #         self.target_object.active = False

    def listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_RIGHT:  # Right mouse button
                mouse_pos = pygame.mouse.get_pos()
                self.set_target(mouse_pos)

    def set_target(self, pos):
        x,y = pan_zoom_handler.screen_2_world(pos[0], pos[1])
        self.target_object.set_position(x,y)
        self.target_object.active = True


class PanZoomTargetObject(PanZoomSpriteBase):
    def __init__(
            self,
            win,
            world_x,
            world_y,
            world_width,
            world_height,
            layer=0,
            group=None,
            parent=None,
            ):
        super().__init__(win, world_x, world_y, world_width, world_height, layer, group)
        self.active = False

        self.property = "target_object"
        self.type = "target object"
        self.parent = parent
        self.id = self.parent.id

        self.target_cross = ArrowCrossAnimatedArray(
                self.win,
                colors.frame_color,
                (400, 300),
                40,
                0,
                8,
                1,
                3,
                5,
                0.8,
                -1)


    def update(self):
        if self.screen_position_changed or self._pan_zoom_changed():
            self._update_screen_position()
            self.screen_position_changed = False

            self.inside_screen = level_of_detail.inside_screen(self.rect.center)

        self.target_cross.update(self.rect.center)

    def draw(self):
        pygame.draw.rect(self.win, colors.frame_color, self.rect)
        self.target_cross.draw()

    # def update(self):
    #
    #     # only draw if the player is the client
    #     # if not config.app.game_client.id == self.parent.owner:
    #     #     return
    #
    #     # only draw if the target is set
    #     # if self.parent.target and self.parent.selected:
    #     if self.parent.target:
    #         self.target_cross.set_center_distance(self.parent.target.rect.width)
    #         self.target_cross.update(self.parent.target.rect.center)
    #         self.target_cross.draw()
    #
    #     # if config.game_paused:
    #     #     return
    #
    #     # self.update_pan_zoom_sprite()
    #
    #     if not self.parent:
    #         self.kill()
    #         return
    #
    #     super().update()


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display dimensions and create a window
    WIDTH, HEIGHT = 1820, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("PanZoomSprite Demo")

    # Create sprite group for managing all sprites together
    world_width, world_height = 500, 500
    ship_sprites = ShipLayeredUpdates()

    # Initialize font for displaying FPS
    font = pygame.font.Font(None, 36)  # Default font with size 36

    # Main game loop to run until quit event occurs
    clock = pygame.time.Clock()

    ship = PanZoomShip(
            win=screen,
            world_x=300,
            world_y=300,
            world_width=100,
            world_height=100,
            layer=1,
            group=ship_sprites,
            image_name="spaceship.png",
            id=0
            )

    running = True

    while running:
        events = pygame.event.get()
        pan_zoom_handler.listen(events)

        # Update all sprites in the group based on their logic defined in update method
        ship_sprites.handle_events(events)
        ship_sprites.update()
        # sprite_groups.update()

        # Clear screen with black background before drawing new frame
        screen.fill((0, 0, 0))

        # Draw each sprite onto the screen using their draw method
        ship_sprites.draw(screen)
        # sprite_groups.draw(screen)

        # Draw debugging rect for level of detail if needed
        level_of_detail.draw_debug_rect()

        # Calculate and display FPS in upper left corner of screen
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))  # Positioning text at top-left corner

        for event in events:
            # box_selection.listen(events)
            if event.type == pygame.QUIT:
                running = False
        # Update display with drawn content for this frame
        pygame.display.update()

        # Cap frame rate to control game speed and performance consistency
        clock.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
