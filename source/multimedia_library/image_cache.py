import os
import pygame
from PIL import Image
import psutil  # For memory usage
from source.handlers.file_handler import pictures_path


class ImageCache:
    def __init__(self):
        self.image_cache = {}
        self.pictures_path = pictures_path  # Replace with actual path

    def get_image(self, image_name: str, rotation: int) -> pygame.surface.Surface:
        cache_key = (image_name, rotation)

        # Check if the image is already in the cache
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Search for the image in the specified directory
        for root, _, files in os.walk(self.pictures_path):
            if image_name in files:
                img_path = os.path.join(root, image_name)
                img = pygame.image.load(img_path).convert_alpha()

                print(f"Image '{image_name}' loaded from disk.")

                # Rotate the image as needed
                if rotation != 0:
                    img = pygame.transform.rotate(img, rotation)
                    print(f"Image '{image_name}' rotated by {rotation}°.")

                # Cache the processed image (only rotated)
                self.image_cache[cache_key] = img
                return img

        # Load a default "no icon" image if not found
        no_icon_path = os.path.join(self.pictures_path, "icons", "no_icon.png")
        no_icon = pygame.image.load(no_icon_path).convert_alpha()
        self.image_cache[cache_key] = no_icon
        print(f"No icon found for '{image_name}', loaded default icon.")
        return no_icon

    def get_image_names_from_folder(self, folder: str) -> list:
        """Get all PNG image names from a specified folder."""
        return [f for f in os.listdir(folder) if f.endswith('.png')]


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    image_cache_instance = ImageCache()

    # Load image names from the "celestial objects" folder
    image_names = image_cache_instance.get_image_names_from_folder(image_cache_instance.pictures_path)

    # Initialize variables for rotating
    rotation_angle = 0  # Start at 0°

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear screen with white background

        # Display images on the screen at different positions
        for index, image_name in enumerate(image_names):
            img_surface = image_cache_instance.get_image(image_name, rotation_angle)

            x_pos = (index % 5) * (img_surface.get_width() + 10) + 50
            y_pos = (index // 5) * (img_surface.get_height() + 10) + 50

            screen.blit(img_surface, (x_pos, y_pos))

        # Update rotation angle
        rotation_angle += 1 % 360  # Rotate by 1 degree each frame

        # Display memory usage in MB and FPS on the screen
        memory_info = psutil.virtual_memory()
        memory_usage_mb = memory_info.used / (1024 ** 2)  # Convert bytes to MB

        font = pygame.font.Font(None, 36)

        text_surface = font.render(f'Memory Usage: {memory_usage_mb:.2f} MB | FPS: {clock.get_fps():.2f}', True, (
        0, 0, 0))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
