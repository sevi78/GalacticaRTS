import pygame

from source.configuration.game_config import config
from source.draw.arrow import draw_arrows_on_line_from_start_to_end
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.path_finding.a_star_node_path_finding import Node, astar


class PathFindingManager:
    def __init__(self):
        self.nodes = None
        self.path = None
        self.start_node = None
        self.end_node = None
        self.max_distance = None
        self.update_nodes()

    def __repr__(self):
        return (f"PathFindingManager:\n"
                f"self.start_node:{self.start_node}\n"
                f"self.end_node:{self.end_node}\n"
                f"max_distance: {self.max_distance}\n"
                f"path:  {self.path}\n ")

    def update_nodes(self) -> None:
        """ sets the valid nodes to the pathfinding manager used to generate the path """
        self.nodes = [i.node for i in sprite_groups.planets.sprites()] + [i.node for i in sprite_groups.ships.sprites()]

    def set_start_node(self, node: Node) -> None:
        """sets the start node"""
        self.start_node = node

    def set_end_node(self, node: Node) -> None:
        """ sets the end node """
        self.end_node = node

    def set_max_distance(self, distance: float) -> None:
        """ sets the max distance to the pathfinding manager used to generate the path """
        self.max_distance = distance

    def generate_path(self, start_node, end_node, max_distance):
        """ generates the path using a* algorithm """
        self.set_start_node(start_node)
        self.set_end_node(end_node)
        self.set_max_distance(max_distance)
        self.path = astar(self.start_node, self.end_node, self.nodes, self.max_distance)

    def draw_path(self):
        """ draws the path """
        if self.path:
            for i in range(len(self.path) - 1):
                start_pos = pan_zoom_handler.world_2_screen(self.path[i].x, self.path[i].y)
                end_pos = pan_zoom_handler.world_2_screen(self.path[i + 1].x, self.path[i + 1].y)
                # pygame.draw.line(config.app.win, pygame.color.THECOLORS["pink"], start_pos, end_pos, 2)
                draw_arrows_on_line_from_start_to_end(
                        surf=config.app.win,
                        color=pygame.color.THECOLORS["green"],
                        start_pos=start_pos,
                        end_pos=end_pos,
                        width=1,
                        dash_length=30,
                        arrow_size=(0, 6),
                        )


pathfinding_manager = PathFindingManager()
