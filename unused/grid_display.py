"""
write a pygame app(800,600). draw a rectangle: display_surface of 300x300 inside the app somewhere. ensure the rect is
visible. now draw other rectangles: "items" (=item_amount) inside the   display_surface. ensure that the area of
display_surface is optimal used. means the sizes and arrangement of the items and item_size must be adjusted to the optimal display:
the items are arranged in rows and colums like an excel sheat. for example: if display_surface is (300x300) and the
item_amont of items is 9, then they should be arranged as : 3x3 items (3 columns,3 rows) with an items_size of (100x100).
make the code readable, use useful comments. seperate drawing from logic. dont explain the code in the chat, only return the code.

"""
import math

import pygame


# def calculate_grid(item_amount, width, height):
#     """Calculate the optimal grid size and item size based on the number of items and display surface dimensions."""
#     columns = math.ceil(math.sqrt(item_amount))
#     rows = math.ceil(item_amount / columns)
#
#     # Adjust rows and columns to fit the items optimally
#     while columns * rows < item_amount:
#         if columns <= rows:
#             columns += 1
#         else:
#             rows += 1
#
#     # Ensure items fill the display surface as much as possible
#     item_width = width // columns
#     item_height = height // rows
#
#     return rows, columns, item_width, item_height


# rows, columns, item_width, item_height = calculate_grid(item_amount, display_surface_rect.width, display_surface_rect.height)

#
# def draw_display_surface(surface):
#     """Draw the main display surface."""
#     pygame.draw.rect(screen, BLACK, surface, 2)
#
#
# def draw_items(surface, rows, columns, item_width, item_height):
#     """Draw items inside the display surface."""
#     for row in range(rows):
#         for col in range(columns):
#             item_index = row * columns + col
#             if item_index >= item_amount:
#                 break
#             item_rect = pygame.Rect(
#                 surface.x + col * item_width,
#                 surface.y + row * item_height,
#                 item_width,
#                 item_height
#             )
#             pygame.draw.rect(screen, RED, item_rect, 2)
#
#
# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 item_amount += 1
#             if event.key == pygame.K_LEFT:
#                 item_amount -= 1
#                 if item_amount == 0:
#                     item_amount = 1
#
#     # Recalculate grid
#     rows, columns, item_width, item_height = calculate_grid(item_amount, display_surface_rect.width, display_surface_rect.height)
#
#     # Fill the screen with white
#     screen.fill(WHITE)
#
#     # Draw the display surface and items
#     draw_display_surface(display_surface_rect)
#     draw_items(display_surface_rect, rows, columns, item_width, item_height)
#
#     # Update the display
#     pygame.display.flip()
#
# # Quit Pygame
# pygame.quit()
# sys.exit()

#
# import math
# import sys
#
# import pygame
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Pygame Rectangle Grid")
#
# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
#
# # Display surface dimensions
# display_surface_rect = pygame.Rect(250, 150, 300, 400)
#
# # Number of items and their arrangement
# item_amount = 10
#
#
# def calculate_grid(item_amount, width, height):
#     """Calculate the optimal grid size and item size based on the number of items and display surface dimensions."""
#     columns = math.ceil(math.sqrt(item_amount))
#     rows = math.ceil(item_amount / columns)
#
#     # Adjust rows and columns to fit the items optimally
#     while columns * rows < item_amount:
#         if columns <= rows:
#             columns += 1
#         else:
#             rows += 1
#
#     # Ensure items are square and maintain the aspect ratio of the display surface
#     item_size = min(width // columns, height // rows)
#     item_width = item_size * width // height
#     item_height = item_size
#
#     return rows, columns, item_width, item_height
#
#
# rows, columns, item_width, item_height = calculate_grid(item_amount, display_surface_rect.width, display_surface_rect.height)
#
#
# def draw_display_surface(surface):
#     """Draw the main display surface."""
#     pygame.draw.rect(screen, BLACK, surface, 2)
#
#
# def draw_items(surface, rows, columns, item_width, item_height):
#     """Draw items inside the display surface."""
#     for row in range(rows):
#         for col in range(columns):
#             item_index = row * columns + col
#             if item_index >= item_amount:
#                 break
#             item_rect = pygame.Rect(
#                 surface.x + col * item_width,
#                 surface.y + row * item_height,
#                 item_width,
#                 item_height
#             )
#             pygame.draw.rect(screen, RED, item_rect, 2)
#
#
# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 item_amount += 1
#             if event.key == pygame.K_LEFT:
#                 item_amount -= 1
#                 if item_amount == 0:
#                     item_amount = 1
#
#     # Recalculate grid
#     rows, columns, item_width, item_height = calculate_grid(item_amount, display_surface_rect.width, display_surface_rect.height)
#
#     # Fill the screen with white
#     screen.fill(WHITE)
#
#     # Draw the display surface and items
#     draw_display_surface(display_surface_rect)
#     draw_items(display_surface_rect, rows, columns, item_width, item_height)
#
#     # Update the display
#     pygame.display.flip()
#
# # Quit Pygame
# pygame.quit()
# sys.exit()
# import math
# import sys
#
# import pygame
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Pygame Rectangle Grid")
#
# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
#
# # Display surface dimensions
# display_surface_rect = pygame.Rect(250, 150, 300, 400)
#
# # Number of items and their arrangement
# item_amount = 10


def calculate_grid(item_amount, width, height):
    """Calculate the optimal grid size and item size based on the number of items and display surface dimensions."""
    columns = math.ceil(math.sqrt(item_amount))
    rows = math.ceil(item_amount / columns)

    # Adjust rows and columns to fit the items optimally
    while columns * rows < item_amount:
        if columns <= rows:
            columns += 1
        else:
            rows += 1

    # Ensure items are square and maintain the aspect ratio of the display surface
    item_size = min(width // columns, height // rows)
    item_width = item_size
    item_height = item_size

    return rows, columns, item_width, item_height


# rows, columns, item_width, item_height = calculate_grid(item_amount, display_surface_rect.width, display_surface_rect.height)


def draw_display_surface(surface):
    """Draw the main display surface."""
    pygame.draw.rect(screen, BLACK, surface, 2)


def draw_items(surface, rows, columns, item_width, item_height):
    """Draw items inside the display surface."""
    for row in range(rows):
        for col in range(columns):
            item_index = row * columns + col
            if item_index >= item_amount:
                break
            item_rect = pygame.Rect(
                surface.x + col * item_width,
                surface.y + row * item_height,
                item_width,
                item_height
            )
            pygame.draw.rect(screen, RED, item_rect, 2)

#
# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 item_amount += 1
#             if event.key == pygame.K_LEFT:
#                 item_amount -= 1
#                 if item_amount == 0:
#                     item_amount = 1
#
#     # Recalculate grid
#     rows, columns, item_width, item_height = calculate_grid(item_amount, display_surface_rect.width, display_surface_rect.height)
#
#     # Fill the screen with white
#     screen.fill(WHITE)
#
#     # Draw the display surface and items
#     draw_display_surface(display_surface_rect)
#     draw_items(display_surface_rect, rows, columns, item_width, item_height)
#
#     # Update the display
#     pygame.display.flip()
#
# # Quit Pygame
# pygame.quit()
# sys.exit()


