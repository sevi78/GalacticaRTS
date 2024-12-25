import math

import pygame
from pygame import Rect, Vector2

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import UniverseLayeredUpdates, sprite_groups
from source.math.math_handler import degrees_to_vector2
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomMovingRotatingGif, PanZoomGif, \
    PanZoomSpriteBase
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite

pygame.init()

WIDTH = 800
HEIGHT = 600
EXPLOSION_RELATIVE_GIF_SIZE = 0.3
SHRINK_FACTOR = 0.005


class CurveMoveSprite(PanZoomSpriteBase):
    def __init__(
            self,
            win,
            world_x,
            world_y,
            world_width,
            world_height,
            layer=0,
            group=sprite_groups.universe,
            target=None
            ):
        super().__init__(win=win, world_x=world_x, world_y=world_y, world_width=world_width, world_height=world_height, layer=layer, group=group)

        self.pos = pygame.math.Vector2(world_x, world_y)
        self.color = pygame.color.THECOLORS["red"]
        self.speed = pygame.math.Vector2(1.5, 0)
        self.gravity = 0.05
        self.friction = 0.99
        self.target = target

    def move_towards_target(self):
        dir_vec = pygame.math.Vector2(self.target.rect.center) - self.rect.center
        v_len_sq = dir_vec.length_squared()
        if v_len_sq > 0:
            dir_vec.scale_to_length(self.gravity)
            self.speed = (self.speed + dir_vec) * self.friction
            self.pos += self.speed

            self.set_position(self.pos.x, self.pos.y)

    def additional_update_tasks(self):
        self.move_towards_target()

    # def draw(self):
    #     pygame.draw.circle(window, self.color, (self.rect.centerx, self.rect.centery), self.rect.width // 2)


class CurveMove:
    def __init__(self, world_x, world_y, direction):
        self.pos = pygame.math.Vector2(world_x, world_y)
        self.direction = direction
        self.gravity = 0.05
        self.friction = 0.99
        self.debug = True

    def get_curve_position(self, obj, target):
        dir_vec = pygame.math.Vector2(target.rect.center) - obj.rect.center
        v_len_sq = dir_vec.length_squared()
        if v_len_sq > 0:
            dir_vec.scale_to_length(self.gravity)
            self.direction = (self.direction + dir_vec) * self.friction
            self.pos += self.direction

        return self.pos


class Missile(PanZoomMovingRotatingGif):
    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group: UniverseLayeredUpdates = None,
            gif_name: str = None,
            gif_index: int = 0,
            gif_animation_time: float = None,
            loop_gif: bool = True,
            kill_after_gif_loop: bool = False,
            image_alpha: int = None,
            rotation_angle: int = 0,
            movement_speed: float = 0,
            direction: Vector2 = (0, 0),
            world_rect: Rect = Rect(0, 0, 0, 0),
            target: any = None,
            get_rotate_correction_anglerotation_angle=None, **kwargs
            ):
        super().__init__(win, world_x, world_y, world_width, world_height, layer, group, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop, image_alpha, rotation_angle, movement_speed, direction, world_rect)
        self.target_reached = None
        self.target = target
        self.debug = True
        self.enable_wrap_around = False

        direction = degrees_to_vector2(-self.rotation_angle + 270, self.movement_speed)
        self.curve_move = CurveMove(world_x, world_y, direction)

        self.exploded = False
        self.explosion_relative_gif_size = kwargs.get("explosion_relative_gif_size", 1.0)
        self.explosion_name = kwargs.get("explosion_name", "explosion.gif")
        self.explode_if_target_reached = kwargs.get("explode_if_target_reached", True)

    def explode(self, **kwargs):
        return
        # self.explode_calls += 1
        sound = kwargs.get("sound", None)
        size = kwargs.get("size", (40, 40))

        x, y = self.world_x, self.world_y
        if not self.exploded:
            explosion = PanZoomSprite(
                    self.win, x, y, size[0], size[1], pan_zoom_handler, self.explosion_name,
                    loop_gif=False, kill_after_gif_loop=True, align_image="center",
                    relative_gif_size=self.explosion_relative_gif_size,
                    layer=10, sound=sound, group="universe", name="explosion")

            self.exploded = True

        if hasattr(self, "__delete__"):
            self.__delete__(self)
        self.kill()

    def reach_target(self):
        self.target_reached = math.dist(self.rect.center, self.target.rect.center) < 10

        if self.target_reached:
            if self.explode_if_target_reached:
                self.explode()
            if hasattr(self, "damage"):
                self.damage()

    def update(self):
        x, y = self.curve_move.get_curve_position(self, self.target)
        self.set_position(x, y)
        self.rotation_angle = -math.degrees(math.atan2(self.curve_move.direction.y, self.curve_move.direction.x))
        super().update()

        self.reach_target()


def main():
    window = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
    pygame.display.set_caption("test map")
    clock = pygame.time.Clock()
    white = 255, 255, 255
    red = 205, 0, 10

    touched = PanZoomGif(
            win=window,
            world_x=250,
            world_y=200,
            world_width=200,
            world_height=200,
            layer=0,
            group=sprite_groups.universe,
            gif_name="sun.gif",
            gif_index=0,
            gif_animation_time=None,
            loop_gif=True,
            kill_after_gif_loop=True,
            image_alpha=None,
            rotation_angle=0)

    touched.debug = True

    missile = Missile(
            win=window,
            world_x=550,
            world_y=600,
            world_width=42,
            world_height=17,
            layer=0,
            group=sprite_groups.universe,
            gif_name="missile_42x17.gif",
            gif_index=0,
            gif_animation_time=None,
            loop_gif=True,
            kill_after_gif_loop=True,
            image_alpha=None,
            rotation_angle=45,
            movement_speed=10.5,
            world_rect=Rect(0, 0, 1000, 1000),
            target=touched)

    #
    # missile  = CurveMove(
    #         win=window,
    #         world_x=250,
    #         world_y=400,
    #         world_width=20,
    #         world_height=20,
    #         layer=0,
    #         group=sprite_groups.universe,
    #         target=touched
    #         # gif_name="missile_42x17.gif",
    #         # gif_index=0,
    #         # gif_animation_time=None,
    #         # loop_gif=True,
    #         # kill_after_gif_loop=True,
    #         # image_alpha=None,
    #         # rotation_angle=0,
    #         # movement_speed=0,
    #         # direction=Vector2(0, 0),
    # )

    fps = 60
    move = False

    run = True
    while run:
        events = pygame.event.get()
        pan_zoom_handler.listen(events)
        for event in events:

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    move = True
                if event.key == pygame.K_r:
                    move = False
                    missile = Missile(
                            win=window,
                            world_x=250,
                            world_y=400,
                            world_width=20,
                            world_height=20,
                            layer=0,
                            group=sprite_groups.universe,
                            gif_name="missile_42x17.gif",
                            gif_index=0,
                            gif_animation_time=None,
                            loop_gif=True,
                            kill_after_gif_loop=True,
                            image_alpha=None,
                            rotation_angle=0,
                            movement_speed=0,
                            direction=Vector2(0, 0),
                            world_rect=Rect(0, 0, 1000, 1000),
                            target=touched)

        window.fill((0, 0, 0))

        sprite_groups.universe.update()
        sprite_groups.universe.draw(window)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    exit()


if __name__ == "__main__": main()

