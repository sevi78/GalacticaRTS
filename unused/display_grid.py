import math

import pygame.event
from source.handlers.color_handler import colors


class DisplayGrid:
    def __init__(self, button_display_rect):
        self.item_amount = 10
        self.button_display_rect = button_display_rect
        self.item_size = 30
        self.rows = 0
        self.columns = 0

    def calc_rows_and_columns(self, items_amount: int) -> tuple:
        # Calculate the display range for x and y
        button_display_range_x = self.button_display_rect.width
        button_display_range_y = self.button_display_rect.height

        # Find the factors of items_amount
        factors = [(i, items_amount // i) for i in range(1, int(math.sqrt(items_amount)) + 1) if items_amount % i == 0]

        # Select the pair of factors that are closest to forming a square
        num_rows, num_columns = min(factors, key=lambda x: abs(x[0] - x[1]))

        # Adjust the item size to fit the grid perfectly
        item_size = min(button_display_range_x / num_columns, button_display_range_y / num_rows)

        # Return the number of rows, columns, and the adjusted item size
        return num_rows, num_columns, item_size, item_size


def draw_grid__(win, grid, items):
    # frame
    pygame.draw.rect(win, colors.frame_color, grid.button_display_rect, 1)

    x, y = 0, 0
    grid.rows = 0
    grid.columns = 0
    item_size = grid.item_size
    for i in range(items):
        x, y = grid.button_display_rect.x + x, grid.button_display_rect.y + y

        x += grid.item_size

        if x > grid.button_display_rect.width:

            grid.rows += 1
            x = 0
            y += item_size
        else:
            grid.columns += 1

        optimal_size = math.floor(grid.button_display_rect.width / grid.columns)
        item_size = optimal_size
        pygame.draw.rect(win, colors.outside_screen_color, (x - item_size, y, item_size, item_size), 1)


def draw_grid(win, grid, items):
    # frame
    pygame.draw.rect(win, colors.frame_color, grid.button_display_rect, 1)

    x, y = grid.button_display_rect.x, grid.button_display_rect.y
    grid.rows = 1
    grid.columns = 0
    item_size = grid.item_size
    for i in range(items):
        # Draw the item
        pygame.draw.rect(win, colors.outside_screen_color, (x, y, item_size, item_size), 1)

        # Move to the next position
        x += item_size
        grid.columns += 1

        # If we reach the end of the row, move to the next line
        if x >= grid.button_display_rect.right:
            grid.rows += 1
            x = grid.button_display_rect.x
            y += item_size

    # Calculate the optimal item size based on the number of columns
    if grid.columns > 0:
        optimal_size = grid.button_display_rect.width // grid.columns / grid.rows
        grid.item_size = optimal_size


def main():
    # Example usage:
    # Assuming 'button_display_rect' is an object with width and height attributes
    win = pygame.display.set_mode((800, 800))
    button_display_rect = pygame.Rect(0, 0, 400, 400)  # Initialize your button display rect object here
    grid = DisplayGrid(button_display_rect)
    # rows, columns, item_size_x, item_size_y = grid.calc_rows_and_columns(12)
    # print(f"Rows: {rows}, Columns: {columns}, Item Size: {item_size_x}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    grid.item_size += 10

                if event.key == pygame.K_DOWN:
                    grid.item_size -= 10

                if event.key == pygame.K_LEFT:
                    grid.item_amount += 10

                if event.key == pygame.K_RIGHT:
                    grid.item_amount -= 10

        pygame.display.get_surface().fill((0, 0, 0))
        draw_grid(win, grid, grid.item_amount)
        pygame.display.update()


if __name__ == "__main__":
    main()
