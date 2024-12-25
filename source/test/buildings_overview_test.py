import pygame
import math

from source.handlers.file_handler import load_file

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Building Layout")

# Colors
BACKGROUND = (240, 240, 240)
TEXT_COLOR = (0, 0, 0)
BUILDING_COLOR = (100, 100, 200)

# Font
font = pygame.font.Font(None, 24)
#
#
# def calculate_position(building, max_price, max_production, category_width, category_height):
#     # Normalize price and production
#     price = sum(building[f"price_{resource}"] for resource in
#                 ["energy", "food", "minerals", "water", "technology", "population"])
#     production = sum(building[f"production_{resource}"] for resource in
#                      ["energy", "food", "minerals", "water", "technology", "population"])
#
#     # Calculate x position based on price
#     x = (price / max_price) * (category_width - 60) + 30
#
#     # Handle case where max_production is zero
#     if max_production > 0:
#         y = (1 - production / max_production) * (category_height - 60) + 30
#     else:
#         # Set a default y position or handle it as needed
#         y = category_height - 30  # Place at the bottom if no production
#
#     return x, y
#
#
# def draw_buildings(buildings_dict):
#     categories = list(buildings_dict.keys())
#     category_width = WIDTH // len(categories)
#
#     for i, category in enumerate(categories):
#         category_buildings = buildings_dict[category]
#
#         # Calculate max price and production for this category
#         max_price = max(sum(building[f"price_{resource}"] for resource in
#                             ["energy", "food", "minerals", "water", "technology", "population"])
#                         for building in category_buildings.values())
#         max_production = max(sum(building[f"production_{resource}"] for resource in
#                                  ["energy", "food", "minerals", "water", "technology", "population"])
#                              for building in category_buildings.values())
#
#         # Draw category name
#         category_text = font.render(category.capitalize(), True, TEXT_COLOR)
#         screen.blit(category_text, (i * category_width + 10, 10))
#
#         for building_name, building_data in category_buildings.items():
#             x, y = calculate_position(building_data, max_price, max_production, category_width, HEIGHT)
#             x += i * category_width  # Offset x by category
#
#             # Draw building
#             pygame.draw.circle(screen, BUILDING_COLOR, (int(x), int(y)), 5)
#
#             # Draw building name
#             name_text = font.render(building_name, True, TEXT_COLOR)
#             screen.blit(name_text, (int(x) + 10, int(y) - 10))
#
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# WIDTH, HEIGHT = 1200, 800
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Building Layout")
#
# # Colors
# BACKGROUND = (240, 240, 240)
# TEXT_COLOR = (0, 0, 0)
# BUILDING_COLOR = (100, 100, 200)
#
# # Font
# font = pygame.font.Font(None, 24)
#
#
# def calculate_position(building, max_price, max_production, category_width, category_height):
#     # Normalize price and production
#     price = sum(building[f"price_{resource}"] for resource in
#                 ["energy", "food", "minerals", "water", "technology", "population"])
#     production = sum(building[f"production_{resource}"] for resource in
#                      ["energy", "food", "minerals", "water", "technology", "population"])
#
#     # Calculate x position based on price
#     x = (price / max_price) * (category_width - 60) + 30
#
#     # Handle case where max_production is zero
#     if max_production > 0:
#         y = (1 - production / max_production) * (category_height - 60) + 30
#     else:
#         # Set a default y position or handle it as needed
#         y = category_height - 30  # Place at the bottom if no production
#
#     return x, y
#
#
# def draw_buildings(buildings_dict):
#     categories = list(buildings_dict.keys())
#     category_width = WIDTH // len(categories)
#
#     building_positions = []  # To keep track of building positions to prevent overlaps
#
#     for i, category in enumerate(categories):
#         category_buildings = buildings_dict[category]
#
#         # Calculate max price and production for this category
#         max_price = max(sum(building[f"price_{resource}"] for resource in
#                             ["energy", "food", "minerals", "water", "technology", "population"])
#                         for building in category_buildings.values())
#         max_production = max(sum(building[f"production_{resource}"] for resource in
#                                  ["energy", "food", "minerals", "water", "technology", "population"])
#                              for building in category_buildings.values())
#
#         # Draw category name
#         # category_text = font.render(category.capitalize(), True, TEXT_COLOR)
#         # screen.blit(category_text, (i * category_width + 10, 10))
#
#         for building_name, building_data in category_buildings.items():
#             # Attempt to calculate position
#             x, y = calculate_position(building_data, max_price or 1, max_production or 1, category_width, HEIGHT)
#             x += i * category_width  # Offset x by category
#
#             # Prevent overlapping by adjusting position if necessary
#             overlap_found = True
#             while overlap_found:
#                 overlap_found = False
#                 for pos in building_positions:
#                     if math.dist((x, y), pos) < 20:  # Adjust threshold as needed (20 pixels here)
#                         overlap_found = True
#                         y += 20  # Move down if overlapping; adjust as necessary
#                         break
#
#             # Store the position of this building to check against future buildings
#             building_positions.append((x, y))
#
#             # Draw building
#             pygame.draw.circle(screen, BUILDING_COLOR, (int(x), int(y)), 5)
#
#             # Draw building name
#             name_text = font.render(building_name.capitalize(), True, TEXT_COLOR)
#             screen.blit(name_text, (int(x) + 10, int(y) - 10))
#

#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# WIDTH, HEIGHT = 1200, 800
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Building Layout")
#
# # Colors
# BACKGROUND = (240, 240, 240)
# TEXT_COLOR = (0, 0, 0)
# BUILDING_COLOR = (100, 100, 200)
# ARROW_COLOR = (0, 0, 0)
#
# # Font
# font = pygame.font.Font(None, 24)
#
#
# def calculate_position(building, max_price, max_production, category_width, category_height):
#     # Normalize price and production
#     price = sum(building[f"price_{resource}"] for resource in
#                 ["energy", "food", "minerals", "water", "technology", "population"])
#     production = sum(building[f"production_{resource}"] for resource in
#                      ["energy", "food", "minerals", "water", "technology", "population"])
#
#     # Calculate x position based on price
#     x = (price / max_price) * (category_width - 60) + 30
#
#     # Handle case where max_production is zero
#     if max_production > 0:
#         y = (1 - production / max_production) * (category_height - 60) + 30
#     else:
#         # Set a default y position or handle it as needed
#         y = category_height - 30  # Place at the bottom if no production
#
#     return x, y
#
#
# def draw_arrows():
#     # Draw Price Arrow
#     pygame.draw.line(screen, ARROW_COLOR, (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50), 3)  # Horizontal arrow
#     pygame.draw.polygon(screen, ARROW_COLOR, [(WIDTH - 50, HEIGHT - 50), (WIDTH - 40, HEIGHT - 55),
#                                               (WIDTH - 40, HEIGHT - 45)])  # Arrowhead right
#     price_text = font.render("Price:", True, TEXT_COLOR)
#     screen.blit(price_text, (WIDTH // 2 - price_text.get_width() // 2, HEIGHT - 70))
#
#     # Draw Production Arrow
#     pygame.draw.line(screen, ARROW_COLOR, (100, HEIGHT - 100), (100, HEIGHT - 500), 3)  # Vertical arrow
#     pygame.draw.polygon(screen, ARROW_COLOR, [(100, HEIGHT - 500), (95, HEIGHT - 490),
#                                               (105, HEIGHT - 490)])  # Arrowhead up
#     production_text = font.render("Production:", True, TEXT_COLOR)
#     screen.blit(production_text, (110, HEIGHT // 2))
#
#
# def draw_buildings(buildings_dict):
#     categories = list(buildings_dict.keys())
#     category_width = WIDTH // len(categories)
#
#     building_positions = []  # To keep track of building positions to prevent overlaps
#
#     for i, category in enumerate(categories):
#         category_buildings = buildings_dict[category]
#
#         # Calculate max price and production for this category
#         max_price = max(sum(building[f"price_{resource}"] for resource in
#                             ["energy", "food", "minerals", "water", "technology", "population"])
#                         for building in category_buildings.values())
#         max_production = max(sum(building[f"production_{resource}"] for resource in
#                                  ["energy", "food", "minerals", "water", "technology", "population"])
#                              for building in category_buildings.values())
#
#         for building_name, building_data in category_buildings.items():
#             # Attempt to calculate position
#             x, y = calculate_position(building_data, max_price or 1, max_production or 1, category_width, HEIGHT)
#             x += i * category_width  # Offset x by category
#
#             # Prevent overlapping by adjusting position if necessary
#             overlap_found = True
#             while overlap_found:
#                 overlap_found = False
#                 for pos in building_positions:
#                     if math.dist((x, y), pos) < 20:  # Adjust threshold as needed (20 pixels here)
#                         overlap_found = True
#                         y += 20  # Move down if overlapping; adjust as necessary
#                         break
#
#             # Store the position of this building to check against future buildings
#             building_positions.append((x, y))
#
#             # Draw building
#             pygame.draw.circle(screen, BUILDING_COLOR, (int(x), int(y)), 5)
#
#             # Draw building name
#             name_text = font.render(building_name.capitalize(), True, TEXT_COLOR)
#             screen.blit(name_text, (int(x) + 10, int(y) - 10))
#
#
# # Main loop
# running = True
# # Draw buildings (replace with your actual buildings dictionary)
# buildings_dict = load_file("buildings.json", "config")
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     screen.fill(BACKGROUND)
#
#
#
#     draw_buildings(buildings_dict)
#
#     pygame.display.flip()
#
# pygame.quit()
#
# import pygame
# import math
# import json
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# WIDTH, HEIGHT = 1200, 800
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Building Layout")
#
# # Colors
# BACKGROUND = (240, 240, 240)
# TEXT_COLOR = (0, 0, 0)
# BUILDING_COLOR = (100, 100, 200)
# ARROW_COLOR = (0, 0, 0)
#
# # Font
# font = pygame.font.Font(None, 24)
#
#
#
#
#
# def calculate_position(building, max_price, max_production, category_width, category_height):
#     # Normalize price and production
#     price = sum(building[f"price_{resource}"] for resource in
#                 ["energy", "food", "minerals", "water", "technology", "population"])
#     production = sum(building[f"production_{resource}"] for resource in
#                      ["energy", "food", "minerals", "water", "technology", "population"])
#
#     # Calculate x position based on price
#     x = (price / max_price) * (category_width - 60) + 30
#
#     # Handle case where max_production is zero
#     if max_production > 0:
#         y = (1 - production / max_production) * (category_height - 60) + 30
#     else:
#         # Set a default y position or handle it as needed
#         y = category_height - 30  # Place at the bottom if no production
#
#     return x, y
#
#
# def draw_arrows():
#     # Draw Price Arrow
#     pygame.draw.line(screen, ARROW_COLOR, (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50), 3)  # Horizontal arrow
#     pygame.draw.polygon(screen, ARROW_COLOR, [(WIDTH - 50, HEIGHT - 50), (WIDTH - 40, HEIGHT - 55),
#                                               (WIDTH - 40, HEIGHT - 45)])  # Arrowhead right
#     price_text = font.render("Price:", True, TEXT_COLOR)
#     screen.blit(price_text, (WIDTH // 2 - price_text.get_width() // 2, HEIGHT - 70))
#
#     # Draw Production Arrow
#     pygame.draw.line(screen, ARROW_COLOR, (100, HEIGHT - 100), (100, HEIGHT - 500), 3)  # Vertical arrow
#     pygame.draw.polygon(screen, ARROW_COLOR, [(100, HEIGHT - 500), (95, HEIGHT - 490),
#                                               (105, HEIGHT - 490)])  # Arrowhead up
#     production_text = font.render("Production:", True, TEXT_COLOR)
#     screen.blit(production_text, (110, HEIGHT // 2))
#
#
# def draw_buildings(buildings_dict):
#     categories = list(buildings_dict.keys())
#     category_width = WIDTH // len(categories)
#
#     building_positions = []  # To keep track of building positions to prevent overlaps
#
#     for i, category in enumerate(categories):
#         category_buildings = buildings_dict[category]
#
#         # Calculate max price and production for this category
#         max_price = max(sum(building[f"price_{resource}"] for resource in
#                             ["energy", "food", "minerals", "water", "technology", "population"])
#                         for building in category_buildings.values())
#         max_production = max(sum(building[f"production_{resource}"] for resource in
#                                  ["energy", "food", "minerals", "water", "technology", "population"])
#                              for building in category_buildings.values())
#
#         for building_name, building_data in category_buildings.items():
#             # Attempt to calculate position
#             x, y = calculate_position(building_data, max_price or 1, max_production or 1, category_width, HEIGHT)
#             x += i * category_width  # Offset x by category
#
#             # Ensure x and y are within screen bounds
#             x = min(max(x, 30), WIDTH - 30)  # Keep x within bounds with padding
#             y = min(max(y, 30), HEIGHT - 60)  # Keep y within bounds with padding
#
#             # Prevent overlapping by adjusting position if necessary
#             overlap_found = True
#             while overlap_found:
#                 overlap_found = False
#                 for pos in building_positions:
#                     if math.dist((x, y), pos) < 20:  # Adjust threshold as needed (20 pixels here)
#                         overlap_found = True
#                         y += 20  # Move down if overlapping; adjust as necessary
#                         break
#
#             # Store the position of this building to check against future buildings
#             building_positions.append((x, y))
#
#             # Draw building
#             pygame.draw.circle(screen, BUILDING_COLOR, (int(x), int(y)), 5)
#
#             # Draw building name
#             name_text = font.render(building_name.capitalize(), True, TEXT_COLOR)
#             screen.blit(name_text, (int(x) + 10, int(y) - 10))
#
#
# # Main loop
# running = True
#
# # Load buildings dictionary from JSON file
# buildings_dict = load_file("buildings.json", "config")
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     screen.fill(BACKGROUND)
#
#     draw_arrows()  # Draw arrows and labels
#
#     draw_buildings(buildings_dict)
#
#     pygame.display.flip()
#
# pygame.quit()
#
# import pygame
# import math
# import json
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# WIDTH, HEIGHT = 1200, 800
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Building Layout")
#
# # Colors
# BACKGROUND = (240, 240, 240)
# TEXT_COLOR = (0, 0, 0)
# BUILDING_COLOR = (100, 100, 200)
# ARROW_COLOR = (0, 0, 0)
#
# # Font
# font = pygame.font.Font(None, 24)
#
#
#
#
#
# def calculate_position(building, max_price, max_production, category_width, category_height):
#     # Normalize price and production
#     price = sum(building[f"price_{resource}"] for resource in
#                 ["energy", "food", "minerals", "water", "technology", "population"])
#     production = sum(building[f"production_{resource}"] for resource in
#                      ["energy", "food", "minerals", "water", "technology", "population"])
#
#     # Calculate x position based on price
#     x = (price / max_price) * (category_width - 60) + 30
#
#     # Handle case where max_production is zero
#     if max_production > 0:
#         y = (1 - production / max_production) * (category_height - 60) + 30
#     else:
#         # Set a default y position or handle it as needed
#         y = category_height - 30  # Place at the bottom if no production
#
#     return x, y
#
#
# def draw_arrows():
#     # Draw Price Arrow
#     pygame.draw.line(screen, ARROW_COLOR, (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50), 3)  # Horizontal arrow
#     pygame.draw.polygon(screen, ARROW_COLOR, [(WIDTH - 50, HEIGHT - 50), (WIDTH - 40, HEIGHT - 55),
#                                               (WIDTH - 40, HEIGHT - 45)])  # Arrowhead right
#     price_text = font.render("Price:", True, TEXT_COLOR)
#     screen.blit(price_text, (WIDTH // 2 - price_text.get_width() // 2, HEIGHT - 70))
#
#     # Draw Production Arrow further to the left
#     pygame.draw.line(screen, ARROW_COLOR, (80, HEIGHT - 100), (80, HEIGHT - 500), 3)  # Vertical arrow
#     pygame.draw.polygon(screen, ARROW_COLOR, [(80, HEIGHT - 500), (75, HEIGHT - 490),
#                                               (85, HEIGHT - 490)])  # Arrowhead up
#
#     # Rotate Production text by creating a new surface with rotation
#     production_text = font.render("Production:", True, TEXT_COLOR)
#     rotated_text = pygame.transform.rotate(production_text, 90)  # Rotate text by 90 degrees
#
#     # Blit rotated text at the appropriate position
#     screen.blit(rotated_text, (60, HEIGHT // 2 - rotated_text.get_height() // 2))  # Center vertically around the arrow
#
#
# def draw_buildings(buildings_dict):
#     categories = list(buildings_dict.keys())
#     category_width = WIDTH // len(categories)
#
#     building_positions = []  # To keep track of building positions to prevent overlaps
#
#     for i, category in enumerate(categories):
#         category_buildings = buildings_dict[category]
#
#         # Calculate max price and production for this category
#         max_price = max(sum(building[f"price_{resource}"] for resource in
#                             ["energy", "food", "minerals", "water", "technology", "population"])
#                         for building in category_buildings.values())
#         max_production = max(sum(building[f"production_{resource}"] for resource in
#                                  ["energy", "food", "minerals", "water", "technology", "population"])
#                              for building in category_buildings.values())
#
#         for building_name, building_data in category_buildings.items():
#             # Attempt to calculate position
#             x, y = calculate_position(building_data, max_price or 1, max_production or 1, category_width, HEIGHT)
#             x += i * category_width  # Offset x by category
#
#             # Ensure x and y are within screen bounds
#             x = min(max(x, 30), WIDTH - 30)  # Keep x within bounds with padding
#             y = min(max(y, 30), HEIGHT - 60)  # Keep y within bounds with padding
#
#             # Prevent overlapping by adjusting position if necessary
#             overlap_found = True
#             while overlap_found:
#                 overlap_found = False
#                 for pos in building_positions:
#                     if math.dist((x, y), pos) < 20:  # Adjust threshold as needed (20 pixels here)
#                         overlap_found = True
#                         y += 20  # Move down if overlapping; adjust as necessary
#                         break
#
#             # Store the position of this building to check against future buildings
#             building_positions.append((x, y))
#
#             # Draw building
#             pygame.draw.circle(screen, BUILDING_COLOR, (int(x), int(y)), 5)
#
#             # Draw building name
#             name_text = font.render(building_name.capitalize(), True, TEXT_COLOR)
#             screen.blit(name_text, (int(x) + 10, int(y) - 10))
#
#
# # Main loop
# running = True
#
# # Load buildings dictionary from JSON file using specified parameters
# buildings_dict = load_file("buildings.json", "config")
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     screen.fill(BACKGROUND)
#
#     draw_arrows()  # Draw arrows and labels
#
#     draw_buildings(buildings_dict)
#
#     pygame.display.flip()
#
# pygame.quit()
#
# import pygame
# import math
# import json
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# WIDTH, HEIGHT = 1200, 800
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Building Layout")
#
# # Colors
# BACKGROUND = (240, 240, 240)
# TEXT_COLOR = (0, 0, 0)
# BUILDING_COLOR = (100, 100, 200)
# ARROW_COLOR = (0, 0, 0)
# SCALE_COLOR = (150, 150, 150)
#
# # Font
# font = pygame.font.Font(None, 24)
#
#
#
#
#
# def calculate_position(building, max_price, max_production, category_width, category_height):
#     # Normalize price and production
#     price = sum(building[f"price_{resource}"] for resource in
#                 ["energy", "food", "minerals", "water", "technology", "population"])
#     production = sum(building[f"production_{resource}"] for resource in
#                      ["energy", "food", "minerals", "water", "technology", "population"])
#
#     # Calculate x position based on price
#     x = (price / max_price) * (category_width - 60) + 30
#
#     # Handle case where max_production is zero
#     if max_production > 0:
#         y = (1 - production / max_production) * (category_height - 60) + 30
#     else:
#         # Set a default y position or handle it as needed
#         y = category_height - 30  # Place at the bottom if no production
#
#     return x, y
#
#
# def draw_arrows():
#     # Draw Price Arrow at bottom left
#     pygame.draw.line(screen, ARROW_COLOR, (50, HEIGHT - 50), (150, HEIGHT - 50), 3)  # Horizontal arrow
#     pygame.draw.polygon(screen, ARROW_COLOR, [(150, HEIGHT - 50), (140, HEIGHT - 55),
#                                               (140, HEIGHT - 45)])  # Arrowhead right
#     price_text = font.render("Price:", True, TEXT_COLOR)
#     screen.blit(price_text, (100 - price_text.get_width() // 2, HEIGHT - 70))
#
#     # Draw Production Arrow at bottom left
#     pygame.draw.line(screen, ARROW_COLOR, (50, HEIGHT - 100), (50, HEIGHT - 500), 3)  # Vertical arrow
#     pygame.draw.polygon(screen, ARROW_COLOR, [(50, HEIGHT - 500), (45, HEIGHT - 490),
#                                               (55, HEIGHT - 490)])  # Arrowhead up
#
#     # Rotate Production text by creating a new surface with rotation
#     production_text = font.render("Production:", True, TEXT_COLOR)
#     rotated_text = pygame.transform.rotate(production_text, 90)  # Rotate text by 90 degrees
#
#     # Blit rotated text at the appropriate position
#     screen.blit(rotated_text, (20 - rotated_text.get_width() // 2,
#                                HEIGHT // 2 - rotated_text.get_height() // 2))  # Center vertically around the arrow
#
#
# def draw_background():
#     """Draw a background rectangle indicating where buildings are displayed."""
#     pygame.draw.rect(screen, SCALE_COLOR, (200 + 30, 30, WIDTH - 260 - 30 * 2, HEIGHT - 100), border_radius=10)
#
#
# def draw_scale(max_price=None, max_production=None):
#     """Draw scales for price and production."""
#
#     # Draw Price Scale
#     if max_price is not None:
#         for i in range(6):
#             scale_x = int(200 + i * ((WIDTH - 260) / 5))
#             pygame.draw.line(screen, (0, 0, 0), (scale_x, HEIGHT - 50), (scale_x, HEIGHT - 40), 2)
#             scale_text = font.render(f"{int(i * (max_price / 5))}", True, TEXT_COLOR)
#             screen.blit(scale_text, (scale_x - 10, HEIGHT - 35))
#
#     # Draw Production Scale
#     if max_production is not None:
#         for i in range(6):
#             scale_y = int(HEIGHT - 100 + i * ((HEIGHT - 500) / 5))
#             pygame.draw.line(screen, (0, 0, 0), (40, scale_y), (50, scale_y), 2)
#             scale_text = font.render(f"{int(i * (max_production / 5))}", True, TEXT_COLOR)
#             screen.blit(scale_text, (10, scale_y - 10))
#
#
# def draw_buildings(buildings_dict):
#     categories = list(buildings_dict.keys())
#     category_width = WIDTH // len(categories)
#
#     building_positions = []  # To keep track of building positions to prevent overlaps
#
#     for i, category in enumerate(categories):
#         category_buildings = buildings_dict[category]
#
#         # Calculate max price and production for this category
#         max_price = max(sum(building[f"price_{resource}"] for resource in
#                             ["energy", "food", "minerals", "water", "technology", "population"])
#                         for building in category_buildings.values())
#         max_production = max(sum(building[f"production_{resource}"] for resource in
#                                  ["energy", "food", "minerals", "water", "technology", "population"])
#                              for building in category_buildings.values())
#
#         for building_name, building_data in category_buildings.items():
#             # Attempt to calculate position
#             x, y = calculate_position(building_data, max_price or 1, max_production or 1, category_width - 60, HEIGHT - 100)
#             x += i * category_width + 30  # Offset x by category and add padding
#
#             # Ensure x and y are within screen bounds with padding of at least 30 pixels to avoid overlap with arrows
#             x = min(max(x, 200 + 30), WIDTH - 30)  # Keep x within bounds with padding on right side
#             y = min(max(y, 30), HEIGHT - 130)  # Keep y within bounds with padding on top
#
#             # Prevent overlapping by adjusting position if necessary
#             overlap_found = True
#             while overlap_found:
#                 overlap_found = False
#                 for pos in building_positions:
#                     if math.dist((x, y), pos) < 20:
#                         overlap_found = True
#                         y += 20  # Move down if overlapping; adjust as necessary
#                         break
#
#             # Store the position of this building to check against future buildings
#             building_positions.append((x, y))
#
#             # Draw building
#             pygame.draw.circle(screen, BUILDING_COLOR, (int(x), int(y)), 5)
#
#             # Draw building name
#             name_text = font.render(building_name.capitalize(), True, TEXT_COLOR)
#             screen.blit(name_text, (int(x) + 10, int(y) - 10))
#
#
# # Main loop
# running = True
#
# # Load buildings dictionary from JSON file using specified parameters
# buildings_dict = load_file("buildings.json", "config")
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     screen.fill(BACKGROUND)
#
#     draw_background()  # Draw background rectangle
#
#     draw_arrows()  # Draw arrows and labels
#
#     draw_buildings(buildings_dict)
#
#     # Get maximum values for scaling purposes after drawing buildings.
#     max_price = max(sum(building[f"price_{resource}"] for resource in
#                         ["energy", "food", "minerals", "water", "technology", "population"])
#                     for category in buildings_dict.values() for building in category.values())
#     max_production = max(sum(building[f"production_{resource}"] for resource in
#                              ["energy", "food", "minerals", "water", "technology", "population"])
#                          for category in buildings_dict.values() for building in category.values())
#
#     draw_scale(max_price, max_production)
#
#     pygame.display.flip()
#
# pygame.quit()


import pygame
import math
import json

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Building Layout")

# Colors
BACKGROUND = (240, 240, 240)
TEXT_COLOR = (0, 0, 0)
BUILDING_COLOR = (100, 100, 200)
ARROW_COLOR = (0, 0, 0)
SCALE_COLOR = (150, 150, 150)

# Font
font = pygame.font.Font(None, 24)


def calculate_position(building, max_price, max_production, category_width, category_height):
    # Normalize price and production
    price = sum(building[f"price_{resource}"] for resource in
                ["energy", "food", "minerals", "water", "technology", "population"])
    production = sum(building[f"production_{resource}"] for resource in
                     ["energy", "food", "minerals", "water", "technology", "population"])

    # Calculate x position based on price
    x = (price / max_price) * (category_width - 60) + 30

    # Handle case where max_production is zero
    if max_production > 0:
        y = (1 - production / max_production) * (category_height - 60) + 30
    else:
        # Set a default y position or handle it as needed
        y = category_height - 30  # Place at the bottom if no production

    return x, y


def draw_arrows():
    # Draw Price Arrow at bottom left
    pygame.draw.line(screen, ARROW_COLOR, (50, HEIGHT - 50), (150, HEIGHT - 50), 3)  # Horizontal arrow
    pygame.draw.polygon(screen, ARROW_COLOR, [(150, HEIGHT - 50), (140, HEIGHT - 55),
                                              (140, HEIGHT - 45)])  # Arrowhead right
    price_text = font.render("Price:", True, TEXT_COLOR)
    screen.blit(price_text, (100 - price_text.get_width() // 2, HEIGHT - 70))

    # Draw Production Arrow at bottom left
    pygame.draw.line(screen, ARROW_COLOR, (50, HEIGHT - 100), (50, HEIGHT - 500), 3)  # Vertical arrow
    pygame.draw.polygon(screen, ARROW_COLOR, [(50, HEIGHT - 500), (45, HEIGHT - 490),
                                              (55, HEIGHT - 490)])  # Arrowhead up

    # Rotate Production text by creating a new surface with rotation
    production_text = font.render("Production:", True, TEXT_COLOR)
    rotated_text = pygame.transform.rotate(production_text, 90)  # Rotate text by 90 degrees

    # Blit rotated text at the appropriate position
    screen.blit(rotated_text, (20 - rotated_text.get_width() // 2,
                               HEIGHT // 2 - rotated_text.get_height() // 2))  # Center vertically around the arrow


def draw_background():
    """Draw a background rectangle indicating where buildings are displayed."""
    pygame.draw.rect(screen, SCALE_COLOR, (200 + 30, 30, WIDTH - 260 - 30 * 2, HEIGHT - 100), border_radius=10)


def draw_scale(max_price=None, max_production=None):
    """Draw scales for price and production."""

    # Draw Price Scale
    if max_price is not None:
        for i in range(6):
            scale_x = int(200 + i * ((WIDTH - 260) / 5))
            pygame.draw.line(screen, (0, 0, 0), (scale_x, HEIGHT - 50), (scale_x, HEIGHT - 40), 2)
            scale_text = font.render(f"{int(i * (max_price / 5))}", True, TEXT_COLOR)
            screen.blit(scale_text, (scale_x - 10, HEIGHT - 35))

    # Draw Production Scale
    if max_production is not None:
        for i in range(6):
            scale_y = int(HEIGHT - 100 + i * ((HEIGHT - 500) / 5))
            pygame.draw.line(screen, (0, 0, 0), (40, scale_y), (50, scale_y), 2)
            scale_text = font.render(f"{int(i * (max_production / 5))}", True, TEXT_COLOR)
            screen.blit(scale_text, (10, scale_y - 10))


def draw_buildings(buildings_dict):
    categories = list(buildings_dict.keys())
    category_width = WIDTH // len(categories)

    building_positions = []  # To keep track of building positions to prevent overlaps

    for i, category in enumerate(categories):
        category_buildings = buildings_dict[category]

        # Calculate max price and production for this category
        max_price = max(sum(building[f"price_{resource}"] for resource in
                            ["energy", "food", "minerals", "water", "technology", "population"])
                        for building in category_buildings.values())
        max_production = max(sum(building[f"production_{resource}"] for resource in
                                 ["energy", "food", "minerals", "water", "technology", "population"])
                             for building in category_buildings.values())

        for building_name, building_data in category_buildings.items():
            # Attempt to calculate position
            x, y = calculate_position(building_data, max_price or 1, max_production or 1, category_width - 60, HEIGHT - 100)
            x += i * category_width + 30  # Offset x by category and add padding

            # Ensure x and y are within screen bounds with padding of at least 30 pixels to avoid overlap with arrows
            x = min(max(x, 200 + 30), WIDTH - 30)  # Keep x within bounds with padding on right side
            y = min(max(y, 30), HEIGHT - 130)  # Keep y within bounds with padding on top

            # Prevent overlapping by adjusting position if necessary
            overlap_found = True
            while overlap_found:
                overlap_found = False
                for pos in building_positions:
                    if math.dist((x, y), pos) < 20:
                        overlap_found = True
                        y += 20  # Move down if overlapping; adjust as necessary
                        break

            # Store the position of this building to check against future buildings
            building_positions.append((x, y))

            # Draw building
            pygame.draw.circle(screen, BUILDING_COLOR, (int(x), int(y)), 5)

            # Draw building name
            name_text = font.render(building_name.capitalize(), True, TEXT_COLOR)
            screen.blit(name_text, (int(x) + 10, int(y) - 10))


# Main loop
running = True

# Load buildings dictionary from JSON file using specified parameters
buildings_dict = load_file("buildings.json", "config")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND)

    draw_background()  # Draw background rectangle

    draw_arrows()  # Draw arrows and labels

    draw_buildings(buildings_dict)

    # Get maximum values for scaling purposes after drawing buildings.
    max_price = max(sum(building[f"price_{resource}"] for resource in
                        ["energy", "food", "minerals", "water", "technology", "population"])
                    for category in buildings_dict.values() for building in category.values())
    max_production = max(sum(building[f"production_{resource}"] for resource in
                             ["energy", "food", "minerals", "water", "technology", "population"])
                         for category in buildings_dict.values() for building in category.values())

    draw_scale(max_price, max_production)

    pygame.display.flip()

pygame.quit()
