import heapq
import math


# Node class to represent a node in the graph
class Node:
    """
    A simple class to store the x and y coordinates of a node.

    Attributes:
        x (float or int): The x-coordinate of the node.
        y (float or int): The y-coordinate of the node.
    """

    def __init__(self, x: [float, int], y: [float, int], owner: object) -> None:
        self.x = x
        self.y = y
        self.owner = owner

    def __repr__(self):
        return f"x,y : {self.x},{self.y}, owner:{self.owner}"

    def update(self, x, y):
        """ updates the node x,y position """
        self.x = x
        self.y = y

    def get_position(self):
        return [self.x, self.y]


# Function to calculate the Euclidean distance between two nodes
def distance(
        node1: Node,
        node2: Node
        ) -> float:
    """
    Calculates the Euclidean distance between two nodes.

    Args:
        node1 (Node): The first node.
        node2 (Node): The second node.

    Returns:
        float: The Euclidean distance between the two nodes.
    """
    return math.dist((node1.x, node1.y), (node2.x, node2.y))


# Function to calculate the shortest path using A* algorithm
def astar(
        start: Node,
        end: Node,
        nodes: list[Node],
        max_distance: float
        ) -> [list[Node], None]:
    """
    Finds the shortest path between the start and end nodes using the A* algorithm.

    The 'A* algorithm' is a pathfinding algorithm that uses a heuristic function (in this case, the Euclidean distance)
    to estimate the cost of reaching the goal from a given node. It maintains two lists: an open list of nodes to be
    explored, and a closed list of nodes that have already been explored.

    At each step, the algorithm selects the node from the open list with the lowest estimated total cost (f-score),
    which is the sum of the actual cost to reach that node (g-score) and the estimated cost from that node to the
    goal (h-score). The algorithm then adds the selected node to the closed list and explores its neighbors,
    updating their g-scores and f-scores as necessary. The process continues until the goal node is reached or
    no path is found.

    Args:
        start (Node): The starting node.
        end (Node): The ending node.
        nodes (list[Node]): The list of nodes in the graph.
        max_distance (float): The maximum distance between two nodes.

    Returns:
        list[Node] or None: The list of nodes representing the shortest path, or None if no path is found.
    """
    open_list = []  # List of nodes to be explored, sorted by f-score
    closed_list = set()  # Set of nodes that have already been explored
    heapq.heappush(open_list, (0, start))  # Add the start node to the open list with an f-score of 0
    came_from = {}  # Dictionary to keep track of the path from the start node to each node
    g_score = {start: 0}  # Dictionary to store the actual cost to reach each node
    f_score = {start: distance(start, end)}  # Dictionary to store the estimated total cost to reach each node

    while open_list:
        try:
            # Select the node with the lowest f-score from the open list
            current = heapq.heappop(open_list)[1]

            # If the current node is the end node, reconstruct the path and return it
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            # Add the current node to the closed list
            closed_list.add(current)

            # Explore the neighbors of the current node
            for node in nodes:
                if node != current and distance(current, node) <= max_distance:
                    # Calculate the tentative g-score (actual cost to reach the neighbor)
                    tentative_g_score = g_score[current] + distance(current, node)

                    # If the tentative g-score is better than the current g-score for the neighbor,
                    # update the came_from dictionary, g-score, and f-score for the neighbor
                    if node not in g_score or tentative_g_score < g_score[node]:
                        came_from[node] = current
                        g_score[node] = tentative_g_score
                        f_score[node] = tentative_g_score + distance(node, end)
                        if node not in open_list:
                            heapq.heappush(open_list, (f_score[node], node))
        except TypeError as e:
            print("astar error: ", e)

    # If no path is found, return None
    return None
