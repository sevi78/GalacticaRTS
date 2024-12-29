# from pil import ImageFilter
# from pil.Image import Image
from PIL import Image, ImageFilter


from source.draw.arc_with_dashes import draw_arc_with_dashes
from source.handlers.color_handler import gradient_color
from source.handlers.pan_zoom_handler import pan_zoom_handler


def draw_electromagnetic_impulse(win, center, min_radius, max_radius, width, pulse_time, circles):
    # Define the colors for the gradient
    colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (0, 0, 255)]

    # Calculate the current size and brightness based on time
    time = pygame.time.get_ticks()  # Get the current time in milliseconds
    pulse_progress = (time % pulse_time) / pulse_time  # Calculate the progress of the pulse (0 to 1)

    # Create a surface for the pulse circles
    pulse_surface = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)

    # Draw each pulse circle on the surface
    for i in range(circles):
        radius = min_radius + (max_radius - min_radius) * i / (circles - 1)
        current_radius = int(radius + pulse_progress * (max_radius - radius))
        color = gradient_color(colors, i / (circles - 1))
        dim_color = (color[0], color[1], color[2], int(pulse_progress * 255))
        pygame.draw.circle(pulse_surface, dim_color, (max_radius, max_radius), current_radius, width)

    # Blit the pulse surface onto the window
    win.blit(pulse_surface, (center[0] - max_radius, center[1] - max_radius))


def draw_zoomable_circle(surface, color, world_x, world_y, radius):
    screen_x, screen_y = pan_zoom_handler.world_2_screen(world_x, world_y)
    pygame.draw.circle(surface, color, (screen_x, screen_y), radius * pan_zoom_handler.zoom, 1)


def draw_transparent_circle(surface, color, position, radius, alpha, **kwargs):
    special_flags = kwargs.get('special_flags', 0)

    if len(color) == 4:
        color = color[:3]  # Ignore the original alpha value

    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, color + (alpha,), (radius, radius), radius)

    surface.blit(circle_surface, (position[0] - radius, position[1] - radius), special_flags=special_flags)


def draw_dashed_circle(surf, color, center, radius, dash_length=10, width=1):
    # Create a rectangle that bounds the circle, centered on the provided center point
    circle_rect = (center[0] - radius, center[1] - radius, 2 * radius, 2 * radius)

    # Draw a dashed circle by drawing a dashed arc with a 360-degree sweep
    draw_arc_with_dashes(surf, color, circle_rect, 0, 360, radius, dash_length, width)


# class BlurredCircleCache:# original
#     def __init__(self):
#         self.cache = {}
#
#     def get_blurred_circle(self, color, radius, alpha, blur_radius):
#         key = (color, radius, alpha, blur_radius)
#         blur_radius = max(1, blur_radius)
#         if key not in self.cache:
#             blurred_image = self.create_blurred_image(color, radius, alpha, blur_radius)
#             self.cache[key] = blurred_image
#         return self.cache[key]
#
#     def create_blurred_image(self, color, radius, alpha, blur_radius):
#         # Create a surface for the circle with full opacity
#         circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
#         pygame.draw.circle(circle_surface, color + (255,), (radius, radius), radius)
#
#         # Convert the circle surface to a PIL image, ensuring correct color order
#         pil_image = Image.frombytes("RGBA", circle_surface.get_size(),
#                 pygame.image.tostring(circle_surface, "RGBA", False))
#
#         # Add a border around the image to help with edge blurring
#         border = int(blur_radius)
#         new_size = (pil_image.size[0] + 2 * border, pil_image.size[1] + 2 * border)
#         new_image = Image.new("RGBA", new_size, (0, 0, 0, 0))
#         new_image.paste(pil_image, (border, border))
#
#         # Apply Gaussian blur using PIL
#         pil_blurred = new_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
#
#         # Remove the border from the blurred image
#         pil_blurred = pil_blurred.crop((border, border, pil_blurred.size[0] - border, pil_blurred.size[1] - border))
#
#         # Apply the alpha value
#         pil_blurred.putalpha(Image.eval(pil_blurred.split()[3], lambda a: int(a * alpha / 255)))
#
#         # Convert the blurred PIL image back to a Pygame surface, ensuring correct color order
#         blurred_image = pygame.image.fromstring(
#                 pil_blurred.tobytes(), pil_blurred.size, pil_blurred.mode).convert_alpha()
#
#         return blurred_image
#
#
# blurred_circle_cache = BlurredCircleCache()

import pygame
# from PIL import Image, ImageFilter


class BlurredCircleCache:
    def __init__(self):
        self.cache = {}

    def get_blurred_circle(self, color, radius, alpha, blur_radius):
        key = (color, radius, alpha, blur_radius)
        blur_radius = max(1, blur_radius)
        if key not in self.cache:
            blurred_image = self.create_blurred_image(color, radius, alpha, blur_radius)
            self.cache[key] = blurred_image
        return self.cache[key]

    def create_blurred_image(self, color, radius, alpha, blur_radius):
        try:
            # Create a surface for the circle with full opacity
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, color + (255,), (radius, radius), radius)

            # Convert the circle surface to a PIL image
            pil_image_data = pygame.image.tostring(circle_surface, "RGBA", False)
            pil_image = Image.frombytes("RGBA", circle_surface.get_size(), pil_image_data)

            # Add a border around the image to help with edge blurring
            border = int(blur_radius)
            new_size = (pil_image.size[0] + 2 * border, pil_image.size[1] + 2 * border)
            new_image = Image.new("RGBA", new_size, (0, 0, 0, 0))
            new_image.paste(pil_image, (border, border))

            # Apply Gaussian blur using PIL
            pil_blurred = new_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

            # Remove the border from the blurred image
            pil_blurred = pil_blurred.crop((border, border,
                                            pil_blurred.size[0] - border,
                                            pil_blurred.size[1] - border))

            # Apply the alpha value
            alpha_channel = pil_blurred.split()[3]
            pil_blurred.putalpha(Image.eval(alpha_channel, lambda a: int(a * alpha / 255)))

            # Convert the blurred PIL image back to a Pygame surface
            blurred_image = pygame.image.fromstring(
                    pil_blurred.tobytes(), pil_blurred.size, pil_blurred.mode).convert_alpha()

            return blurred_image

        except Exception as e:
            print(f"Error creating blurred image: {e}")
            return None  # Return None or handle it as needed


# Usage example
blurred_circle_cache = BlurredCircleCache()


def draw_transparent_circle_blurred(
        surface: pygame.Surface,
        color: [int, int, int, int],
        position: [int, int],
        radius: int,
        alpha: int,
        special_flags: int,
        blur_radius: int
        ) -> None:
    if len(color) == 4:
        color = color[:3]  # Ignore the original alpha value

    blurred_image = blurred_circle_cache.get_blurred_circle(color, radius, alpha, blur_radius)
    if blurred_image:
        surface.blit(blurred_image, (
            position[0] - blurred_image.get_width() // 2,
            position[1] - blurred_image.get_height() // 2), special_flags=special_flags)


# strange perplexity version :) looks like mandelbrot but it's not
# import pygame
# import numpy as np
# from scipy.ndimage import gaussian_filter
#
# class BlurredCircleCache:
#     def __init__(self):
#         self.cache = {}
#
#     def get_blurred_circle(self, color, radius, alpha, blur_radius):
#         key = (tuple(color), radius, alpha, blur_radius)
#         if key not in self.cache:
#             blurred_image = self.create_blurred_image(color, radius, alpha, blur_radius)
#             self.cache[key] = blurred_image
#         return self.cache[key]
#
#     def create_blurred_image(self, color, radius, alpha, blur_radius):
#         # Create a square numpy array for the circle
#         size = int(radius * 2)
#         circle = np.zeros((size, size, 4), dtype=np.float32)
#
#         # Create a meshgrid for circle creation
#         y, x = np.ogrid[-radius:radius, -radius:radius]
#         mask = x*x + y*y <= radius*radius  # Create a circular mask
#
#         # Assign color with full opacity to the masked area
#         circle[mask] = np.array(color, dtype=np.float32)  # Use RGBA directly
#
#         # Apply Gaussian blur
#         blurred = gaussian_filter(circle, sigma=[blur_radius, blur_radius, 0])
#
#         # Normalize alpha channel and apply desired alpha
#         max_alpha = np.max(blurred[:,:,3])
#         if max_alpha > 0:  # Avoid division by zero
#             blurred[:,:,3] = (blurred[:,:,3] / max_alpha) * (alpha / 255.0)
#
#         # Multiply color channels by the alpha channel
#         blurred[:,:,:3] *= blurred[:,:,3:4]
#
#         # Convert to Pygame surface
#         surf = pygame.Surface((size, size), pygame.SRCALPHA)
#         pygame.surfarray.pixels_alpha(surf)[:] = (blurred[:,:,3] * 255).astype(np.uint8)
#         pygame.surfarray.pixels3d(surf)[:] = (blurred[:,:,:3] * 255).astype(np.uint8)
#
#         return surf
#
# blurred_circle_cache = BlurredCircleCache()
#
# def draw_transparent_circle_blurred(
#         surface: pygame.Surface,
#         color: tuple[int, int, int, int],  # Expecting an RGBA tuple
#         position: tuple[int, int],
#         radius: int,
#         alpha: int,
#         special_flags: int,
#         blur_radius: float
# ) -> None:
#     blurred_image = blurred_circle_cache.get_blurred_circle(color, radius, alpha, blur_radius)
#     surface.blit(blurred_image, (
#         position[0] - blurred_image.get_width() // 2,
#         position[1] - blurred_image.get_height() // 2), special_flags=special_flags)


def main():
    pygame.init()
    win = pygame.display.set_mode((900, 600))

    run = True
    while run:
        win.fill((0, 0, 0))
        x = 100
        size = 60
        for i in range(10):
            draw_transparent_circle(win, (255, 255, 255), (x, 300), size, 20, special_flags=6)
            # draw_transparent_circle(win, (255, 255, 255), (x, 300), size, 20)
            x += size
        pygame.display.update()


if __name__ == "__main__":
    main()
