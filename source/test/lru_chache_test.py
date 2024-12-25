import pygame
from functools import lru_cache
import time

from source.multimedia_library.images import get_image

# Function to scale images with LRU caching
@lru_cache(maxsize=None)  # Adjust maxsize based on your needs
def cached_scale_image(surface, width, height):
    return pygame.transform.scale(surface, (width, height))

# Function to scale images without caching
def uncached_scale_image(surface, width, height):
    return pygame.transform.scale(surface, (width, height))

class YourClass:
    def __init__(self, image_raw):
        self.image_raw = image_raw  # This should be a pygame.Surface
        self.image = None

    def scale_and_measure(self, width, height, iterations=10000):
        # Measure cached scaling
        start_time = time.perf_counter()  # Use high-resolution timer
        for _ in range(iterations):
            self.image = cached_scale_image(self.image_raw, width, height)  # Store cached result
        cached_time = time.perf_counter() - start_time

        # Measure uncached scaling
        clear_image_cache()  # Clear cache to ensure no cached values are used
        start_time = time.perf_counter()  # Start timing again
        for _ in range(iterations):
            self.image = uncached_scale_image(self.image_raw, width, height)  # Store uncached result
        uncached_time = time.perf_counter() - start_time

        # Calculate percentage benefit
        if uncached_time > 0:  # Prevent division by zero
            percentage_benefit = ((uncached_time - cached_time) / uncached_time) * 100
        else:
            percentage_benefit = float('inf')  # Handle edge case where uncached time is zero

        # Compare times and print results
        if cached_time < uncached_time:
            faster_method = "Cached"
            faster_time = cached_time
            slower_time = uncached_time
        else:
            faster_method = "Uncached"
            faster_time = uncached_time
            slower_time = cached_time

        print(f"Scaling to {width}x{height}:")
        print(f"  Cached time: {cached_time:.6f} seconds.")
        print(f"  Uncached time: {uncached_time:.6f} seconds.")
        print(f"  Faster method: {faster_method} ({faster_time:.6f} seconds)")
        print(f"  Performance benefit: {percentage_benefit:.2f}%\n")

# Function to clear the cache if needed
def clear_image_cache():
    cached_scale_image.cache_clear()

# Example usage of YourClass in a Pygame application
def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Load an image as a pygame.Surface
    original_image = get_image("nebulae_300x300.png")  # Use convert_alpha for transparency

    # Create an instance of YourClass with the loaded image
    your_instance = YourClass(original_image)

    running = True

    # Define target sizes for scaling
    sizes = [(30, 30), (50, 50), (100, 100), (200, 200), (400, 400), (800, 800), (1600, 1200)]

    index = 0  # To track which size to scale next

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the current target size for scaling
        target_width, target_height = sizes[index]

        # Measure and compare both scaling methods for the current size
        your_instance.scale_and_measure(target_width, target_height)

        # Clear the screen and draw the last scaled image (for demonstration purposes)
        screen.fill((0, 0, 0))  # Fill with black or any background color

        if your_instance.image:
            your_instance.rect = your_instance.image.get_rect(center=(400, 300))  # Center the image on screen
            screen.blit(your_instance.image, your_instance.rect.topleft)

        pygame.display.flip()

        index += 1
        if index >= len(sizes):  # Loop through sizes
            index = 0

        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
