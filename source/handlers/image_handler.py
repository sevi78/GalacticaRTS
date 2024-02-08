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