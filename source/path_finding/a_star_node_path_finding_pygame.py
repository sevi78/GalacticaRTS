import random
import pygame
from a_star_node_path_finding import Node, astar


def setup_nodes(
        width: int,
        height: int,
        num_nodes: int
        ) -> [list, Node, Node]:
    """
    Sets up a list of random nodes within the given width and height, and selects random start and end nodes.

    Args:
        width (int): The width of the display.
        height (int): The height of the display.
        num_nodes (int): The number of nodes to create.

    Returns:
        list[Node], Node, Node: The list of nodes, the start node, and the end node.
    """
    nodes = [Node(random.randint(20, width), random.randint(20, height)) for _ in range(num_nodes)]
    start = random.choice(nodes)
    end = random.choice(nodes)
    while end == start:
        end = random.choice(nodes)

    return nodes, start, end


def display_max_distance(
        screen: pygame.surface.Surface,
        color: pygame.color,
        max_distance: float
        ) -> None:
    """
    Displays the current maximum distance on the screen as text.

    Args:
        screen (pygame.surface.Surface): The Pygame display surface.
        color (pygame.color): The color to use for the text.
        max_distance (float): The current maximum distance.
    """
    font = pygame.font.Font(None, 36)
    text = font.render(f"Maximum Distance: {max_distance:.2f}", True, color)
    screen.blit(text, (10, 10))


def main():
    """
    The main function that sets up the Pygame display, handles user input, and runs the A* algorithm to find the
    shortest path between the start and end nodes.
    """
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 1000, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Shortest Path Between Circles")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Set up the nodes
    num_nodes = 35
    nodes, start, end = setup_nodes(width, height, num_nodes)
    max_distance = 100

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    nodes, start, end = setup_nodes(width, height, num_nodes)
            elif event.type == pygame.MOUSEWHEEL:
                max_distance = max(20, min(500, max_distance + event.y * 20))

        screen.fill(WHITE)

        # Draw all nodes
        for node in nodes:
            pygame.draw.circle(screen, BLACK, (node.x, node.y), 20)

        # Highlight start and end nodes
        if start:
            pygame.draw.circle(screen, GREEN, (start.x, start.y), 22, 2)
        if end:
            pygame.draw.circle(screen, RED, (end.x, end.y), 22, 2)

        # Calculate and draw the shortest path
        if start and end:
            path = astar(start, end, nodes, max_distance)
            if path:
                for i in range(len(path) - 1):
                    pygame.draw.line(screen, RED, (path[i].x, path[i].y), (path[i + 1].x, path[i + 1].y), 2)
            else:
                print("No path found within the distance constraint.")

        display_max_distance(screen, BLACK, max_distance)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
