# import pygame
#
#
# def create_360_degree_rotating_gif_from_image(image_path: str, steps: int):
#     image = pygame.image.load(image_path).convert_alpha()
#     frames = []
#
#     # Rotate the image 360 degrees
#     for i in range(int(360 / steps)):
#         # Rotate the image
#         rotated_image = pygame.transform.rotate(image, i * steps)
#
#         # Get the new rectangle for the rotated image
#         rotated_rect = rotated_image.get_rect(center=(image.get_width() // 2, image.get_height() // 2))
#
#         # Adjust the position to keep it centered
#         frames.append(rotated_image)
#
#     return frames
#
#
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     clock = pygame.time.Clock()
#
#     frames = create_360_degree_rotating_gif_from_image(
#             r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\celestial objects\galaxy_2.png",
#             1)
#     frame_index = 0
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return
#
#         screen.fill((0, 0, 0))
#
#         # Display the current frame centered on the screen
#         frame_rect = frames[frame_index].get_rect(center=(400, 300))  # Centering the image on screen
#         screen.blit(frames[frame_index], frame_rect.topleft)
#
#         # Update frame index to loop through frames
#         frame_index = (frame_index + 1) % len(frames)
#
#         pygame.display.flip()
#         clock.tick(60)  # Limit to 10 FPS for smoother rotation
#
#
# if __name__ == "__main__":
#     main()
# import os
#
# import imageio
# import pygame
#
# def create_360_degree_rotating_gif_from_image(image_path: str, steps: int):
#     image = pygame.image.load(image_path).convert_alpha()
#     frames = []
#
#     # Calculate the number of frames based on steps
#     num_frames = 360 // steps  # This determines how many frames to create
#
#     # Rotate the image 360 degrees
#     for i in range(num_frames):
#         # Rotate the image by (i * steps) degrees
#         rotated_image = pygame.transform.rotate(image, i * steps)
#
#         # Get the new rectangle for the rotated image
#         rotated_rect = rotated_image.get_rect(center=(image.get_width() // 2, image.get_height() // 2))
#
#         # Append the rotated image to frames
#         frames.append(rotated_image)
#
#
#
#
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     clock = pygame.time.Clock()
#
#     frames = create_360_degree_rotating_gif_from_image(
#             r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\celestial objects\galaxy_2.png",
#             1)  # Change step value here
#     # frame_index = 0
#     #
#     # while True:
#     #     for event in pygame.event.get():
#     #         if event.type == pygame.QUIT:
#     #             pygame.quit()
#     #             return
#     #
#     #     screen.fill((0, 0, 0))
#     #
#     #     # Display the current frame centered on the screen
#     #     frame_rect = frames[frame_index].get_rect(center=(400, 300))  # Centering the image on screen
#     #     screen.blit(frames[frame_index], frame_rect.topleft)
#     #
#     #     # Update frame index to loop through frames
#     #     frame_index = (frame_index + 1) % len(frames)
#     #
#     #     pygame.display.flip()
#     #     clock.tick(60)  # Limit to 10 FPS for smoother rotation
#
# if __name__ == "__main__":
#     main()
import pygame
import imageio
import os


def create_360_degree_rotating_gif_from_image(image_path: str, steps: int):
    # Load the image with alpha channel support
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

    # Save frames as a GIF
    gif_path = os.path.splitext(image_path)[0] + '.gif'  # Create a path for the GIF file
    with imageio.get_writer(gif_path, mode='I', duration=0.1) as writer:  # Adjust duration for frame speed
        for frame in frames:
            # Convert Pygame surface to a format suitable for imageio
            frame_surface = pygame.surfarray.array3d(frame)
            frame_surface = frame_surface.transpose([1, 0, 2])  # Transpose to match (width, height, color)

            # Handle alpha channel if present
            alpha_surface = pygame.surfarray.array2d(frame.convert_alpha())
            if alpha_surface is not None:
                # Create a mask for transparency
                mask = (alpha_surface == 0)  # Create a mask where alpha is zero (transparent)

                # Set transparent pixels to black or any desired background color
                frame_surface[mask] = [0, 0, 0]  # Change this color if needed

            writer.append_data(frame_surface)

    return frames


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    frames = create_360_degree_rotating_gif_from_image(r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\celestial objects\galaxy_2.png", 1)  # Change step value here
    frame_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))

        # Display the current frame centered on the screen
        frame_rect = frames[frame_index].get_rect(center=(400, 300))  # Centering the image on screen
        screen.blit(frames[frame_index], frame_rect.topleft)

        # Update frame index to loop through frames
        frame_index = (frame_index + 1) % len(frames)

        pygame.display.flip()
        clock.tick(10)  # Limit to 10 FPS for smoother rotation


if __name__ == "__main__":
    main()


