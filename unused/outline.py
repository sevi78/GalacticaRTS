import pygame



from source.multimedia_library.images import get_image
from source.utils.colors import colors


def add_alpha_channel(image):
    # Load the image
    img = image
    img = img.convert()  # Convert the image to a format suitable for drawing

    # Create a new surface with per-pixel alpha transparency
    img_with_alpha = pygame.Surface(img.get_size(), pygame.SRCALPHA)

    # Copy the original image onto the new surface
    img_with_alpha.blit(img, (0, 0))

    # Return the image with an added alpha channel
    return img_with_alpha


# Function to outline darkest pixels in a certain range
def outline_darkest_pixels(image, start_range, end_range, outline_color):
    # Load the image
    img = image
    img = img.convert_alpha()  # Convert the image to a format suitable for drawing

    # Get the dimensions of the image
    width, height = img.get_size()

    # Create a new surface to draw the outlined pixels
    outlined_img = pygame.Surface((width, height), pygame.SRCALPHA)

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the color of the current pixel
            pixel_color = img.get_at((x, y))

            # Check if the pixel color falls within the specified range
            if start_range <= pixel_color[0] <= end_range:
                # Outline the pixel by drawing a line around it
                pygame.draw.line(outlined_img, outline_color, (x, y), (x, y))
            else:
                # Make the pixel transparent
                pixel_color = pixel_color[:3] + (0,)  # Set alpha value to 0
                outlined_img.set_at((x, y), pixel_color)
    # Return the outlined image
    return outlined_img


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Image Outline Test")

# Load the image and get the outlined image
image = pygame.transform.scale(get_image("spacehunter_25x25.png"), (200, 200))
img_with_alpha = add_alpha_channel(image)
outlined_image = outline_darkest_pixels(img_with_alpha, 150, 250, colors.frame_color)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the original image
    screen.blit(image, (0, 0))

    # Draw the outlined image
    screen.blit(outlined_image, (200, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
