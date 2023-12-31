import os
import pygame
from PIL import Image

from source.handlers.file_handler import pictures_path

images = {}
all_image_names = []


gifs = {}
gif_frames = {}
MAX_GIF_SIZE = 150


def load_folders(folder, dict):
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
    dict[folder] = {}

    for sub in subfolders:
        path = os.path.join(folder, sub)
        # files = [f for f in os.listdir(path) if isfile(join(path, f))]
        # print (files)
        dict[folder][sub] = {}
        for image in os.listdir(path):
            filename, file_extension = os.path.splitext(image)
            if file_extension == ".png":
                img = pygame.image.load(os.path.join(folder, sub, image))
                img.convert_alpha()
                dict[folder][sub][image] = img
                all_image_names.append(image)

            if file_extension == ".gif":
                load_gif(image)


def get_image(image_name):
    no_icon = images[pictures_path]["icons"]["no_icon.png"]
    for category, sub_dict in images.items():
        for sub_category, items in sub_dict.items():
            if image_name in items:
                return items[image_name]
    return no_icon


def load_gif(gif_name):
    path = os.path.join(pictures_path + "gifs", gif_name)
    gif = Image.open(path)
    gifs[gif_name] = gif
    gif_frames[gif_name] = get_gif_frames(gif_name)


def get_gif(gif_name):
    return gifs[gif_name]


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
        gif.seek(frame)
        frame_surface_raw = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode).convert_alpha()

        # Rescale the images if necessary
        if rescale:
            new_size = (int(gif.size[0] * ratio), int(gif.size[1] * ratio))
            frame_surface = pygame.transform.scale(frame_surface_raw, new_size)
        else:
            frame_surface = frame_surface_raw

        frames.append(frame_surface)
    return frames


def get_image_names_from_folder(folder):
    image_names = os.listdir(pictures_path + folder)
    return image_names


def resize_image(image, new_size):
    # Calculate the aspect ratio of the original image
    aspect_ratio = image.get_width() / image.get_height()

    # Adjust the width and height to fit within the new size while maintaining the aspect ratio
    if new_size[0] / aspect_ratio < new_size[1]:
        new_height = int(new_size[0] / aspect_ratio)
        new_image = pygame.transform.scale(image, (new_size[0], new_height))
    else:
        new_width = int(new_size[1] * aspect_ratio)
        new_image = pygame.transform.scale(image, (new_width, new_size[1]))

    return new_image


load_folders(os.path.join(pictures_path), images)

# images.get_image(
#     cur.execute(f"select image_name_small from planets where id = {self.id}").fetchone()[0]],
