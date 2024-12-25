import pygame
import numpy as np

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Image on Rounded Surface")

# Load and scale the image
image = pygame.image.load(r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\assets\pictures\buildings\agriculture complex_125x125.png").convert_alpha()
image = pygame.transform.scale(image, (400, 300))

# Create a surface with per-pixel alpha
rounded_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

# Copy the image onto the new surface
rounded_surface.blit(image, (0, 0))

# Create a rounded corner mask
def create_rounded_mask(size, radius):
    mask = pygame.Surface(size, pygame.SRCALPHA)
    mask.fill((255, 255, 255, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)
    return pygame.surfarray.array_alpha(mask)

# Apply the mask to the surface
mask = create_rounded_mask(image.get_size(), radius=40)
surface_alpha = pygame.surfarray.pixels_alpha(rounded_surface)
surface_alpha[:] = np.minimum(surface_alpha, mask)
del surface_alpha

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(rounded_surface, (200, 150))
    pygame.display.flip()

pygame.quit()
