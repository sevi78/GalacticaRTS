import os

import pygame
from PIL import Image

from source.utils import global_params

pygame.init()

WIDTH = global_params.WIDTH
HEIGHT = global_params.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
images = {}
dirpath = os.path.dirname(os.path.realpath(__file__))
pictures_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "pictures" + os.sep
gifs_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "gifs" + os.sep

gifs = {}


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


def get_image__(image_name):
    no_icon = images[pictures_path]["icons"]["no_icon.pmg"]
    for category, sub_dict in images.items():
        for sub_category, items in sub_dict.items():
            if image_name in items:
                return items[image_name]

    print (f"image_name not found,no such image in any directory: {image_name}")
    return None

def get_image(image_name):
    no_icon = images[pictures_path]["icons"]["no_icon.png"]
    for category, sub_dict in images.items():
        for sub_category, items in sub_dict.items():
            if image_name in items:
                return items[image_name]
    return no_icon



def load_gif_frames(gif_name):
    """ Load explosion GIF and extract frames"""
    frames = []
    path = os.path.join(gifs_path, gif_name)
    gif = Image.open(path)
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_surface = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
        frames.append(frame_surface)
    return frames


def load_gif(gif_name):
    path = os.path.join(gifs_path, gif_name)
    gif = Image.open(path)
    return gif


def get_gif_frames(gif):
    """ Load explosion GIF and extract frames"""
    frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_surface = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode).convert_alpha()
        frames.append(frame_surface)
    return frames


load_folders(os.path.join(pictures_path), images)

# images.get_image(
#     cur.execute(f"select image_name_small from planets where id = {self.id}").fetchone()[0]],
