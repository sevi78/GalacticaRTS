from datetime import datetime

import pygame
import os


def capture_screenshot(screen: pygame.Surface, filename: str, area: tuple, target_size: tuple, **kwargs):
    """
    Capture a screenshot of a specific area of the screen and resize it to the target size.

    Parameters:
    screen (pygame.Surface): The screen surface.
    filename (str): The filename to save the screenshot as.
    area (tuple): A tuple of four integers representing the area to capture.
                  The tuple should be in the format (x, y, width, height).
    target_size (tuple): A tuple of two integers representing the target size (width, height) for the captured image.
    """

    event_text = kwargs.get("event_text", None)
    try:
        # Create a new surface representing the area of the screen to capture
        subsurface = screen.subsurface(pygame.Rect(*area))

        # Ensure the directory exists
        directory = os.path.join("assets", "pictures", "levels")
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Resize the subsurface to the target size
        resized_subsurface = pygame.transform.scale(subsurface, target_size)

        # Save the resized subsurface to an image file
        pygame.image.save(resized_subsurface, os.path.join(directory, filename))
    except ValueError as e:
        print("ValueError: subsurface rectangle outside surface area: ", e)
        if event_text:
            event_text.text = f"error, cannot make screenshot: {e}"
    except Exception as e:
        print("An error occurred: ", e)
        if event_text:
            event_text.text = f"error, cannot make screenshot: {e}"

    if event_text:
        print(f"screenshot created: {filename}")
        event_text.text = f"screenshot created: {filename}"
