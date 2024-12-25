import pygame
import imageio
import os
from datetime import datetime


def create_360_degree_rotating_gif_from_image(image_path: str, steps: int):
    image = pygame.image.load(image_path).convert_alpha()
    frames = []

    # Calculate the number of frames based on steps
    num_frames = 360 // steps  # This determines how many frames to create

    # Rotate the image 360 degrees
    for i in range(num_frames):
        # Rotate the image by (i * steps) degrees
        rotated_image = pygame.transform.rotate(image, i * steps)

        # Append the rotated image to frames
        frames.append(rotated_image)

    return frames


def make_gif(frames: list, frames_per_second: float):
    """ Makes a .gif from a list of Pygame surfaces at a given frame rate. """

    # Create a timestamp for the GIF filename
    timestampStr = datetime.now().strftime("%y%m%d_%H%M%S")
    gif_path = f"rotating_gif_{timestampStr}.gif"  # Save in current directory with timestamp

    print('Started making GIF')
    print('Please wait...')

    with imageio.get_writer(gif_path, mode='I', duration=1 / frames_per_second) as writer:
        for frame in frames:
            # Convert Pygame surface to a format suitable for imageio
            frame_surface = pygame.surfarray.array3d(frame)
            frame_surface = frame_surface.transpose([1, 0, 2])  # Transpose to match (width, height, color)

            writer.append_data(frame_surface)

    print('Finished making GIF!')
    print('GIF can be found at:', gif_path)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    frames = create_360_degree_rotating_gif_from_image(r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\celestial objects\galaxy_2.png", 1)  # Change step value here
    fps = 60
    make_gif(frames, fps)


if __name__ == "__main__":
    main()
