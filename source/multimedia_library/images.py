import math
from functools import lru_cache

import numpy as np
import pygame
from PIL.Image import Image

# remove this if posible, so far still neded to initialize pygame before loading images
pygame.init()
pygame.display.set_mode((1920, 1080), pygame.RESIZABLE, pygame.DOUBLEBUF)

from PIL import Image, ImageFilter
from source.handlers.file_handler import pictures_path

images = {}
all_image_names = []

filter_icons = {
    'buildings': 'buildings_icon.png',
    'energy': 'energy_icon.png',
    'experience': 'experience_icon.png',
    'explored': 'explored_icon.png',
    'food': 'food_icon.png',
    'minerals': 'minerals_icon.png',
    'name': 'name_icon.png',
    'owner': 'owner.png',
    'owner_index': 'owner.png',
    'population': 'population_icon.png',
    'population_limit': 'population_limit_icon.png',
    'speed': 'speed_icon.png',
    'state': 'state_icon.png',
    'technology': 'technology_icon.png',
    'water': 'water_icon.png',
    "players": "players_icon.png",
    "level": "level_icon.png",
    }

gifs = {}
gif_frames = {}
gif_fps = {}
gif_durations = {}
MAX_GIF_SIZE = 1000
LOAD_AT_GAME_START = False


@lru_cache(maxsize=None)
def load_folders(folder):
    """Objective:
    The objective of the "load_folders" function is to load all the PNG images from a given folder and its subfolders
    into a dictionary, where the keys are the folder names and the subfolder names, and the values are the loaded images.

    Inputs:
    - folder: a string representing the path of the folder to be searched for PNG images.
    - dict: a dictionary to store the loaded images.

    Flow:
    1. Get a list of subfolders in the given folder.
    2. Create a new dictionary entry for the given folder in the input dictionary.
    3. For each subfolder, create a new dictionary entry for it in the dictionary under the given folder.
    4. For each PNG image in the subfolder, load the image using Pygame and add it to the dictionary under the subfolder.

    Outputs:
    - None (the loaded images are stored in the input dictionary).

    Additional aspects:
    - The function uses the Pygame library to load the PNG images.
    - The function only loads PNG images and ignores other file types.
    - The function assumes that all PNG images have a ".png" file extension."""
    subfolders = [str(f.path).split(os.sep)[-1] for f in os.scandir(folder) if f.is_dir()]
    dict_ = {folder: {}}
    accepted_image_types = ['.png', ".svg"]

    for sub in subfolders:
        path = os.path.join(folder, sub)
        # files = [f for f in os.listdir(path) if isfile(join(path, f))]
        # print (files)
        dict_[folder][sub] = {}
        for image in os.listdir(path):
            filename, file_extension = os.path.splitext(image)
            if file_extension in accepted_image_types:
                img = load_image(folder, image, sub)
                img.convert_alpha()
                dict_[folder][sub][image] = img
                all_image_names.append(image)

            if file_extension == ".gif":
                load_gif(image)

    return dict_


@lru_cache(maxsize=None)
def load_image(folder, image, sub):
    img = pygame.image.load(os.path.join(folder, sub, image))
    return img


@lru_cache(maxsize=None)
def load_gif(gif_name):
    path = os.path.join(pictures_path + "gifs", gif_name)
    gif = Image.open(path)
    gifs[gif_name] = gif
    gif_frames[gif_name] = get_gif_frames(gif_name)
    gif_fps[gif_name] = load_gif_fps(gif)
    gif_durations[gif_name] = load_gif_durations(gif)
    return gif


def load_gif_durations(gif):
    durations = []
    for frame in range(0, gif.n_frames):
        gif.seek(frame)
        durations.append(gif.info['duration'])

    # Calculate the average duration
    avg_duration = sum(durations) / len(durations)
    if avg_duration == 0.0:
        avg_duration = 20.0

    return avg_duration


@lru_cache(maxsize=None)
def get_gif_duration(gif_name):
    return gif_durations[gif_name]


# @lru_cache(maxsize=None)
def load_gif_fps(gif_file):
    # Get the durations of all frames
    durations = []
    for i in range(0, gif_file.n_frames):
        gif_file.seek(i)
        durations.append(gif_file.info['duration'])

    # Calculate the average FPS
    avg_duration = sum(durations) / len(durations)

    try:
        fps = 1000 / avg_duration  # Calculate the FPS (1000 ms = 1 second)
    except ZeroDivisionError:
        fps = 20
    return fps


@lru_cache(maxsize=None)
def get_image(image_name) -> pygame.surface.Surface:  # old, not performant at all!!
    start_time = time.perf_counter()
    # Initialize `no_icon` image
    no_icon_path = os.path.join(pictures_path, "icons", "no_icon.png")
    no_icon = images.get(pictures_path, {}).get("icons", {}).get("no_icon.png")

    if no_icon is None:
        no_icon = pygame.image.load(no_icon_path)
        images.setdefault(pictures_path, {}).setdefault("icons", {})[no_icon_path] = no_icon

    # Search in all subdirectories of `images` to find the image
    for category, sub_dict in images.items():
        for sub_category, items in sub_dict.items():
            if image_name in items:
                return items[image_name]

    # If image is not found in `images`, search in `pictures_path` subdirectories
    for root, dirs, files in os.walk(pictures_path):
        if image_name in files:
            img_path = os.path.join(root, image_name)
            img = pygame.image.load(img_path)
            img.convert_alpha()
            # Add the image to `images` dictionary
            images.setdefault(root, {}).setdefault(os.path.dirname(image_name), {})[image_name] = img
            return img

    # If no image is found, return `no_icon`
    end_time = time.perf_counter()
    print(f"No icon loaded in {(end_time - start_time) * 1000:.4f} ms")
    return no_icon


import os
import pygame
import time

# Use a flat dictionary for faster lookups
image_cache = {}


def get_image__(image_name) -> pygame.surface.Surface:
    start_time = time.perf_counter()

    # Check if the image is already in the cache
    if image_name in image_cache:
        end_time = time.perf_counter()
        # print(f"Image {image_name} loaded from cache in {(end_time - start_time) * 1000:.4f} ms")
        return image_cache[image_name]

    # Search for the image in pictures_path
    for root, _, files in os.walk(pictures_path):
        if image_name in files:
            img_path = os.path.join(root, image_name)
            img = pygame.image.load(img_path).convert_alpha()
            image_cache[image_name] = img
            end_time = time.perf_counter()
            # print(f"Image {image_name} loaded from disk in {(end_time - start_time) * 1000:.4f} ms")
            return img

    # If no image is found, load and return no_icon
    no_icon_path = os.path.join(pictures_path, "icons", "no_icon.png")
    if "no_icon.png" not in image_cache:
        no_icon = pygame.image.load(no_icon_path).convert_alpha()
        image_cache["no_icon.png"] = no_icon

    end_time = time.perf_counter()
    # print(f"No icon replaced: {image_name} because not found, loaded in {(end_time - start_time) * 1000:.4f} ms")
    return image_cache["no_icon.png"]


@lru_cache(maxsize=None)
def get_gif(gif_name):
    try:
        return gifs[gif_name]
    except KeyError:
        return load_gif(gif_name)


@lru_cache(maxsize=None)
def get_gif_fps(gif_name):
    return gif_fps[gif_name]


@lru_cache(maxsize=None)
def get_gif_frames(gif_name):
    """ Load explosion GIF and extract frames"""
    frames = []

    gif = get_gif(gif_name)
    ratio = 1.0
    rescale = False

    # Check if the size of the GIF is bigger than MAX_GIF_SIZE
    if max(gif.size) > MAX_GIF_SIZE:
        # Calculate the ratio to rescale the images
        ratio = MAX_GIF_SIZE / max(gif.size)
        rescale = True

    for frame in range(gif.n_frames):
        if not frame == 0:
            gif.seek(frame)
            frame_surface_raw = pygame.image.frombytes(gif.tobytes(), gif.size, gif.mode).convert_alpha()

            # Rescale the images if necessary
            if rescale:
                new_size = (int(gif.size[0] * ratio), int(gif.size[1] * ratio))
                frame_surface = scale_image_cached(frame_surface_raw, new_size)
            else:
                frame_surface = frame_surface_raw

            frames.append(frame_surface)
        # frames.pop(0)
    return frames


@lru_cache(maxsize=None)
def get_image_names_from_folder(folder, **kwargs):
    startswith_string = kwargs.get("startswith_string", "")
    image_names = os.listdir(pictures_path + folder)

    if startswith_string:
        image_names = [i for i in image_names if i.startswith(startswith_string)]

    return image_names


#
# @lru_cache(maxsize=None)
# def resize_image(image, new_size):
#     # Calculate the aspect ratio of the original image
#     aspect_ratio = image.get_width() / image.get_height()
#
#     # Adjust the width and height to fit within the new size while maintaining the aspect ratio
#     if new_size[0] / aspect_ratio < new_size[1]:
#         new_height = int(new_size[0] / aspect_ratio)
#         new_image = scale_image_cached(image, (new_size[0], new_height))
#     else:
#         new_width = int(new_size[1] * aspect_ratio)
#         new_image = scale_image_cached(image, (new_width, new_size[1]))
#
#     return new_image


@lru_cache(maxsize=None)
def find_unused_images_gifs(image_dir, gif_dir, images_dict, gifs_dict):
    unused_files = []

    # Check for unused images
    for folder, subfolders in images_dict.items():
        for subfolder, image_files in subfolders.items():
            actual_files = os.listdir(os.path.join(image_dir, folder, subfolder))
            for file in actual_files:
                if file not in image_files:
                    unused_files.append(os.path.join(image_dir, folder, subfolder, file))

    # Check for unused gifs
    actual_gif_files = os.listdir(gif_dir)
    for file in actual_gif_files:
        if file not in gifs_dict:
            unused_files.append(os.path.join(gif_dir, file))

    return unused_files


# @lru_cache(maxsize=None)  # Adjust maxsize based on your needs
# def scale_image_cached(surface, width, height):
#     # Print cache info each time the function is called
#     cache_stats = scale_image_cached.cache_info()
#     print(f"Cache Info - Hits: {cache_stats.hits}, Misses: {cache_stats.misses}, "
#           f"Current Size: {cache_stats.currsize}, Max Size: {cache_stats.maxsize}")
#     return pygame.transform.scale(surface, (width, height))

@lru_cache(maxsize=1000)  # Adjust maxsize based on your needs
def scale_image_cached(surface, size):
    # Print cache info each time the function is called
    # cache_stats = scale_image_cached.cache_info()
    # print(f"Cache Info - Hits: {cache_stats.hits}, Misses: {cache_stats.misses}, "
    #       f"Current Size: {cache_stats.currsize}, Max Size: {cache_stats.maxsize}")

    return pygame.transform.scale(surface, size)


@lru_cache(maxsize=1000)  # Adjust maxsize based on your needs
def rotate_image_cached(surface, rotation_angle):
    return pygame.transform.rotate(surface, rotation_angle)


def rotate_image_to(obj, position: tuple, rotate_correction_angle: int):
    """
    Rotate the image to face a given position.

    # 0 - image is looking to the right
    # 90 - image is looking up
    # 180 - image is looking to the left
    # 270 - image is looking down
    :param obj: The image object to rotate.
    :param position: A tuple (x, y) representing the target position.
    :param rotate_correction_angle: Angle correction for rotation.
    """
    old_rect = obj.rect

    # Unpack the target position
    target_x, target_y = position

    # Calculate relative position
    rel_x = target_x - obj.rect.centerx
    rel_y = target_y - obj.rect.centery

    # Calculate target angle
    target_angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - rotate_correction_angle

    # Normalize target_angle to [0, 360)
    target_angle = target_angle % 360

    # Smoothing algorithm
    if obj.prev_angle is not None:
        # Calculate the shortest rotation
        diff = (target_angle - obj.prev_angle + 180) % 360 - 180

        if abs(diff) > obj.rotation_smoothing:
            angle = (obj.prev_angle + obj.rotation_smoothing * (diff / abs(diff))) % 360
        else:
            angle = target_angle
    else:
        angle = target_angle

    # if angle == obj.prev_angle:
    #     # print ("same angle")
    #     return angle

    obj.prev_angle = angle
    new_image = rotate_image_cached(obj.image, angle)
    obj.image = new_image
    obj.image_rotated = new_image

    # Reset the rect
    obj.rect = obj.image.get_rect(center=old_rect.center)

    return angle


def rounded_surface(surface: pygame.Surface, corner_radius: int) -> pygame.Surface:
    """
    Create a rounded version of the given surface.

    Args:
    surface (pygame.Surface): The original surface to round.
    corner_radius (int): The radius of the rounded corners.

    Returns:
    pygame.Surface: A new surface with rounded corners.
    """
    # Create a new surface with per-pixel alpha
    size = surface.get_size()
    rounded = pygame.Surface(size, pygame.SRCALPHA)

    # Create a rounded corner mask
    mask = pygame.Surface(size, pygame.SRCALPHA)
    mask.fill((255, 255, 255, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=corner_radius)

    # Apply the mask to the original surface
    rounded.blit(surface, (0, 0))
    mask_alpha = pygame.surfarray.array_alpha(mask)
    surface_alpha = pygame.surfarray.pixels_alpha(rounded)
    surface_alpha[:] = np.minimum(surface_alpha, mask_alpha)
    del surface_alpha  # Release the surface lock

    return rounded


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



def underblit_image(
        image: pygame.surface, sub_image: pygame.surface, offset_x: int, offset_y: int
        ) -> pygame.surface.Surface:
    surf = pygame.surface.Surface(image.get_size(), pygame.SRCALPHA)
    surf.blit(sub_image, (offset_x, offset_y))
    surf.blit(image, (0, 0))
    return surf

def overblit_button_image(button, image_name: str, value: bool, **kwargs) -> None:
    """
    Overblits an image on top of a button's image.

    :param button: The button to overblit the image on.
    :param image_name: The name of the image to overblit.
    :param value: The value of the button.
    :param kwargs: Additional keyword arguments for customizing the overblit.

    kwargs:

    size (tuple): The size of the overblit image. Default is (button.image.get_rect().width, button.image.get_rect().height).

    offset_x (int): The x-offset of the overblit image. Default is 0.

    offset_y (int): The y-offset of the overblit image. Default is 0.

    outline (bool): Whether to apply an outline to the overblit image. Default is False.

    color (tuple): The color of the outline. Default is (100, 100, 100).
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
            image = outline_image(scale_image_cached(get_image(image_name), size), color, 127, 0)
        else:
            image = scale_image_cached(get_image(image_name), size)

        button.image.blit(image, (offset_x, offset_y))
    else:
        # Restore the original image before overblitting
        button.image.fill((0, 0, 0, 0))  # Fill with transparent black
        button.image.blit(button.image_raw, (0, 0))  # Blit the original image


def outline_image(image, color=(0, 0, 0), threshold=127, thickness=0) -> pygame.surface:
    """
    this blits an outline to the image and returns it

    """
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
    outline_image_ = pygame.Surface(image.get_size()).convert_alpha()
    outline_image_.fill((0, 0, 0, 0))

    # If the thickness is greater than 0, draw the outline with a thickness
    if thickness > 0:
        for point in mask.outline():
            for x in range(-thickness, thickness + 1):
                for y in range(-thickness, thickness + 1):
                    outline_image_.set_at((point[0] + x, point[1] + y), color)
    else:
        for point in mask.outline():
            outline_image_.set_at(point, color)

    return outline_image_


if LOAD_AT_GAME_START:
    start = time.time()
    images = load_folders(os.path.join(pictures_path))
    end = time.time()
    print(f"Loaded images in {end - start} seconds")
    # pprint(find_unused_images_gifs(pictures_path, os.path.join(pictures_path, 'gifs'), images, gifs))

if __name__ == "__main__":
    pass
