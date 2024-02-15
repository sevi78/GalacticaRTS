import pygame

from source.multimedia_library.images import get_image


def overblit_button_image(button, image_name, value):
    if not button:
        return
    if not value:
        size = (button.image.get_rect().width, button.image.get_rect().height)
        button.image.blit(pygame.transform.scale(get_image(image_name), size), (0, 0))  # Scale and blit the image
    else:
        # Restore the original image before overblitting
        button.image.fill((0, 0, 0, 0))  # Fill with transparent black
        button.image.blit(button.image_raw, (0, 0))  # Blit the original image


def outline_image(image, color=(0, 0, 0), threshold=127, thickness=0):
    image.blit(get_outline(image, color, threshold, thickness), (0, 0))
    return image


def get_outline__(image, color=(0, 0, 0), threshold=127):
    """Returns an outlined image of the same size.  The image argument must
    either be a convert surface with a set colorkey, or a convert_alpha
    surface. The color argument is the color which the outline will be drawn.
    In surfaces with alpha, only pixels with an alpha higher than threshold will
    be drawn.  Colorkeyed surfaces will ignore threshold."""
    mask = pygame.mask.from_surface(image, threshold)
    outline_image = pygame.Surface(image.get_size()).convert_alpha()
    outline_image.fill((0, 0, 0, 0))
    for point in mask.outline():
        outline_image.set_at(point, color)
    return outline_image


def get_outline(image, color=(0, 0, 0), threshold=127, thickness=0):
    mask = pygame.mask.from_surface(image, threshold)
    outline_image = pygame.Surface(image.get_size()).convert_alpha()
    outline_image.fill((0, 0, 0, 0))
    if thickness > 0:
        for point in mask.outline():
            for x in range(-thickness, thickness + 1):
                for y in range(-thickness, thickness + 1):
                    outline_image.set_at((point[0] + x, point[1] + y), color)
    else:
        for point in mask.outline():
            outline_image.set_at(point, color)

    return outline_image
