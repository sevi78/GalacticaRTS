import os

import pygame

from source.handlers.color_handler import get_average_color
from source.handlers.file_handler import pictures_path
from source.multimedia_library.images import get_gif_frames, load_gif_fps, load_gif, load_gif_durations


def load_image_attributes():
    # setup variables
    image_sizes = {}
    average_colors = {}
    average_colors_alpha = {}
    max_gif_frames = {}
    gif_fps = {}
    gif_durations = {}

    # loop through all images in all subdirectories
    for root, dirs, files in os.walk(pictures_path):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                img_path = os.path.join(root, file)
                try:
                    # try to load the image
                    img = pygame.image.load(img_path)

                    # add the image size to the dictionary: image_sizes
                    image_sizes[file] = img.get_size()

                    # add the average color to the dictionary: average_colors, average_colors_alpha (consider_alpha)
                    average_colors[file] = get_average_color(img, consider_alpha=False)
                    average_colors_alpha[file] = get_average_color(img, consider_alpha=True)

                    # add the max gif frames to the dictionary: max_gif_frames
                    if file.lower().endswith(".gif"):
                        # gif frames
                        gif = load_gif(img_path)
                        gif_frames = get_gif_frames(img_path)
                        max_gif_frames[file] = len(gif_frames) - 1

                        # gif fps
                        gif_fps_ = load_gif_fps(gif)
                        gif_fps[file] = gif_fps_

                        # gif_duration
                        gif_duration = load_gif_durations(gif)
                        gif_durations[file] = gif_duration

                        # add the average color to the dictionary: average_colors, average_colors_alpha (consider_alpha)
                        average_colors[file] = get_average_color(gif_frames[0], consider_alpha=False)
                        average_colors_alpha[file] = get_average_color(gif_frames[0], consider_alpha=True)

                except pygame.error as e:
                    print(f"Error loading image {img_path}: {e}")

    return image_sizes, average_colors, average_colors_alpha, max_gif_frames, gif_fps, gif_durations


def write_image_attributes():
    """
    Write the image attributes to a file
    """
    image_sizes, average_colors, average_colors_alpha, max_gif_frames, gif_fps, gif_durations = load_image_attributes()

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the file path
    file_path = os.path.join(current_dir, "image_attributes.py")

    # Write the attributes to the file
    with open(file_path, "w") as file:
        file.write("# This file contains image attributes\n\n")
        file.write(f"image_sizes_dict = {image_sizes}\n\n")
        file.write(f"average_colors_dict = {average_colors}\n\n")
        file.write(f"average_colors_alpha_dict = {average_colors_alpha}\n\n")
        file.write(f"max_gif_frames_dict = {max_gif_frames}\n")
        file.write(f"gif_fps_dict = {gif_fps}\n")
        file.write(f"gif_durations_dict = {gif_durations}\n")

    print(f"Image attributes have been written to {file_path}")

write_image_attributes()
# pprint(max_gif_frames)
# for key, value in average_colors.items():
#     print(f"{key}: {value}, alpha: {average_colors_alpha[key]}")
