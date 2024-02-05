import sys

import pygame

# Initialize Pygame
pygame.init()

# Set up the game screen
gameScreen = pygame.display.set_mode((800, 600))

# Main loop
running = True
mouse_pressed = False  # Track the mouse button state
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True  # Set the mouse button state to pressed
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False  # Set the mouse button state to released

    if mouse_pressed:  # Check if the mouse is pressed and moving
        print("Mouse button pressed at", pygame.mouse.get_pos())

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
