from pygame import Rect, draw


from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.view.game_objects.qt_game_objects import QTImage, QTFlickeringStar, QTPulsatingStar, QTGif, \
    QTMovingImage
from source.qt_universe.view.qt_debugger import debug_object
from source.qt_universe.view.qt_draw_methods import draw_qt_image, draw_flickering_star, draw_pulsating_star, \
    draw_qt_gif, draw_orbit_circle
from source.qt_universe.view.qt_view_config.qt_draw_config import *



def get_world_search_area() -> Rect:
    screen_rect = pygame.display.get_surface().get_rect()
    screen_search_area = screen_rect.inflate(-200, -200)  # Inflate by 200 pixels on each side
    world_x1, world_y1 = pan_zoom_handler.screen_2_world(screen_search_area.left, screen_search_area.top)
    world_x2, world_y2 = pan_zoom_handler.screen_2_world(screen_search_area.right, screen_search_area.bottom)
    return pygame.Rect(world_x1, world_y1, world_x2 - world_x1, world_y2 - world_y1)


def draw_objects(screen, qtree, screen_search_area) -> None:
    """
    draw objects from the quadtree in the visible area
    """
    # draw the screen search area
    draw.rect(screen, (0, 50, 1), screen_search_area, 1)

    # Convert screen coordinates to world coordinates
    world_search_area = get_world_search_area()

    # Query the quadtree for objects in the visible area
    found = qtree.query(world_search_area)

    for point in found:
        # draw.rect(screen, pygame.color.THECOLORS["white"], point.rect, 1)

        if DRAW_ORBIT:
            if hasattr(point, 'orbit_object'):
                draw_orbit_circle(screen, point)

        if isinstance(point, QTImage) or isinstance(point, QTMovingImage):
            draw_qt_image(screen, point)

        elif isinstance(point, QTFlickeringStar):
            draw_flickering_star(screen, point)

        elif isinstance(point, QTPulsatingStar):
            draw_pulsating_star(screen, point)

        elif isinstance(point, QTGif):
            draw_qt_gif(screen, point)

        if point.selected:
            # Define your size limits
            limit_width = 2  # Set your desired minimum width limit
            limit_height = 2  # Set your desired minimum height limit

            # Limit the rectangle size using max() to ensure it doesn't go below the limits
            point.rect.width = max(point.rect.width, limit_width)
            point.rect.height = max(point.rect.height, limit_height)

            # Draw the rectangle
            draw.rect(screen, MINT_TURQUOISE, point.rect, 1)

        if DEBUG and point.selected:
            debug_object(screen, point)

        if point.selected:
            color = MINT_TURQUOISE
            if not point.visible:
                color = RED

            draw.rect(screen, color, point.rect, 1)
