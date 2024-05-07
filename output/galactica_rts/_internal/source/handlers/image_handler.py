import pygame
from PIL import ImageFilter
from PIL.Image import Image

from source.multimedia_library.images import get_image


def change_non_transparent_pixels(image: pygame.surface, new_color) -> pygame.surface:
    """
    Changes all non-transparent pixels of the given image to the specified color,
    while preserving the transparency of each pixel.

    Args:
    - image (pygame.Surface): The source image.
    - new_color (tuple): The new color to apply (R, G, B). Alpha value is not needed as it's preserved.

    Returns:
    - pygame.Surface: The processed image with updated colors.
    """
    # Ensure the image supports per-pixel alpha transparency
    image = image.convert_alpha()

    # Lock the surface to allow direct pixel access
    image.lock()

    # Iterate over each pixel in the image
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            # Get the current color and alpha of the pixel
            current_color = image.get_at((x, y))
            # If the pixel is not completely transparent, change its color
            if current_color.a != 0:
                new_pixel_color = pygame.Color(new_color[0], new_color[1], new_color[2], current_color.a)
                image.set_at((x, y), new_pixel_color)

    # Unlock the surface
    image.unlock()

    return image


def blur_image(surf: pygame.surface, radius):  # unused
    pil_string_image = pygame.image.tostring(surf, "RGBA", False)
    pil_image = Image.frombuffer("RGBA", surf.get_size(), pil_string_image)
    pil_blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=radius))
    blurred_image = pygame.image.fromstring(pil_blurred.tobytes(), pil_blurred.size, pil_blurred.mode)
    return blurred_image.convert_alpha()


def overblit_button_image(button, image_name: str, value: bool, **kwargs) -> None:
    """
    Overblits an image on top of a button's image.

    :param button: The button to overblit the image on.
    :param image_name: The name of the image to overblit.
    :param value: The value of the button.
    :param kwargs: Additional keyword arguments for customizing the overblit.
    """
    if not button:
        return

    size = kwargs.get("size", (button.image.get_rect().width, button.image.get_rect().height))
    offset_x, offset_y = kwargs.get("offset_x", 0), kwargs.get("offset_y", 0)
    outline = kwargs.get("outline", False)
    color = kwargs.get("color", (100, 100, 100))

    # this is used to reset the image for checkbox behaviour
    if not value:
        # Scale and blit the image
        if outline:
            image = outline_image(pygame.transform.scale(get_image(image_name), size), color, 127, 0)
        else:
            image = pygame.transform.scale(get_image(image_name), size)

        button.image.blit(image, (offset_x, offset_y))
    else:
        # Restore the original image before overblitting
        button.image.fill((0, 0, 0, 0))  # Fill with transparent black
        button.image.blit(button.image_raw, (0, 0))  # Blit the original image


def outline_image(image, color=(0, 0, 0), threshold=127, thickness=0) -> pygame.surface:
    image.blit(get_outline(image, color, threshold, thickness), (0, 0))
    return image


def get_outline(image, color=(0, 0, 0), threshold=127, thickness=0) -> pygame.surface:
    """Returns an outlined image of the same size.  The image argument must
    either be a convert surface with a set colorkey, or a convert_alpha
    surface. The color argument is the color which the outline will be drawn.
    In surfaces with alpha, only pixels with an alpha higher than threshold will
    be drawn.  Colorkeyed surfaces will ignore threshold."""

    # Convert the image to a mask
    mask = pygame.mask.from_surface(image, threshold)
    outline_image = pygame.Surface(image.get_size()).convert_alpha()
    outline_image.fill((0, 0, 0, 0))

    # If the thickness is greater than 0, draw the outline with a thickness
    if thickness > 0:
        for point in mask.outline():
            for x in range(-thickness, thickness + 1):
                for y in range(-thickness, thickness + 1):
                    outline_image.set_at((point[0] + x, point[1] + y), color)
    else:
        for point in mask.outline():
            outline_image.set_at(point, color)

    return outline_image
