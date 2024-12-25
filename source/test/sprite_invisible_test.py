import pygame
from pygame import Vector2
from pygame.sprite import Sprite, Group, LayeredDirty, LayeredUpdates

from source.factories.universe_factory import universe_factory

from source.multimedia_library.images import get_image
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomMovingRotatingGif


class ToggleSprite(Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = get_image(image_path)
        self.rect = self.image.get_rect()
        self.visible = True

    def toggle_visibility(self):
        self.visible = not self.visible

    def update(self):
        if not self.visible:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)




pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

sprite_group = Group()
# toggle_sprite = ToggleSprite("spaceship.png")

toggle_sprite = PanZoomMovingRotatingGif(
                win=screen,  # type: ignore
                world_x=100,
                world_y=100,
                world_width=114,
                world_height=64,
                layer=0,  # type: ignore
                group=sprite_group,
                gif_name="electro_discharge_croped.gif",
                gif_index=0,
                gif_animation_time=None,
                loop_gif=True,
                kill_after_gif_loop=False,
                image_alpha=None,
                rotation_angle=0,
                movement_speed=0,
                direction=Vector2(0, 0),
                world_rect=universe_factory.world_rect,
                align_image="center"
                )
toggle_sprite.set_position(100, 100)
sprite_group.add(toggle_sprite)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_sprite.visieble = not toggle_sprite.visible

    sprite_group.update()
    screen.fill((0,0,0))

    # sprite_groups.universe.update()
    # sprite_groups.universe.draw(screen)
    sprite_group.draw(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
