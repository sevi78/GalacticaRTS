import pygame
from pygame import Surface, Rect, draw, gfxdraw

from source.handlers.pan_zoom_handler import pan_zoom_handler

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = pygame.color.THECOLORS["yellow"]


def draw_quadtree(quadtree, surface: Surface, pan_zoom_handler):
    screen_rect = Rect(0, 0, surface.get_width(), surface.get_height())
    boundary_screen = pan_zoom_handler.world_2_screen(quadtree.boundary.x, quadtree.boundary.y)
    boundary_screen_width = quadtree.boundary.width * pan_zoom_handler.get_zoom()
    boundary_screen_height = quadtree.boundary.height * pan_zoom_handler.get_zoom()
    boundary_screen_rect = Rect(
            boundary_screen[0], boundary_screen[1], boundary_screen_width, boundary_screen_height)

    if screen_rect.colliderect(boundary_screen_rect):
        draw_rect_border(surface, boundary_screen_rect, (255, 255, 255))
        if quadtree.divided:
            draw_quadtree(quadtree.northEast, surface, pan_zoom_handler)
            draw_quadtree(quadtree.northWest, surface, pan_zoom_handler)
            draw_quadtree(quadtree.southEast, surface, pan_zoom_handler)
            draw_quadtree(quadtree.southWest, surface, pan_zoom_handler)


def draw_quadtree_boundary(quadtree, surface: Surface, pan_zoom_handler):
    screen_rect = Rect(0, 0, surface.get_width(), surface.get_height())
    boundary_screen = pan_zoom_handler.world_2_screen(quadtree.boundary.x, quadtree.boundary.y)
    boundary_screen_width = quadtree.boundary.width * pan_zoom_handler.get_zoom()
    boundary_screen_height = quadtree.boundary.height * pan_zoom_handler.get_zoom()
    boundary_screen_rect = Rect(
            boundary_screen[0], boundary_screen[1], boundary_screen_width, boundary_screen_height)

    if screen_rect.colliderect(boundary_screen_rect):
        draw_rect_border(surface, boundary_screen_rect, BLUE)


def draw_rect_border(screen: Surface, r: Rect, color) -> None:
    draw.line(screen, color, (r.x, r.y), (r.x + r.w, r.y))
    draw.line(screen, color, (r.x, r.y), (r.x, r.y + r.h))
    draw.line(screen, color, (r.x + r.w, r.y), (r.x + r.w, r.y + r.h))
    draw.line(screen, color, (r.x, r.y + r.h), (r.x + r.w, r.y + r.h))


def draw_points_inside_visible_rect(screen, qtree, visible_rect):
    for p in qtree.points:
        if visible_rect.collidepoint(p.x, p.y):
            screen_position_x, screen_position_y = pan_zoom_handler.world_2_screen(p.x, p.y)
            gfxdraw.pixel(screen, int(screen_position_x), int(screen_position_y), RED)


def draw_points_selection(screen, qtree):
    mX, mY = pygame.mouse.get_pos()
    world_x, world_y = pan_zoom_handler.screen_2_world(mX, mY)
    search_size = 200 / pan_zoom_handler.get_zoom()
    search_area = Rect(world_x - search_size / 2, world_y - search_size / 2, search_size, search_size)
    found = qtree.query(search_area)
    screen_search_area = Rect(mX - 100, mY - 100, 200, 200)
    draw_rect_border(screen, screen_search_area, GREEN)
    for point in found:
        screen_x, screen_y = pan_zoom_handler.world_2_screen(point.x, point.y)
        r = point.width / 2 * pan_zoom_handler.get_zoom()
        if r < 1: r = 1
        draw.circle(screen, point.color, (int(screen_x), int(screen_y)), r)


def draw_points_inside_screen_rect(screen, qtree):
    border = 50
    screen_search_area = Rect(border, border, screen.get_width() - (border * 2), screen.get_height() - (border * 2))
    draw_rect_border(screen, screen_search_area, YELLOW)

    # Convert screen coordinates to world coordinates
    world_x1, world_y1 = pan_zoom_handler.screen_2_world(screen_search_area.left, screen_search_area.top)
    world_x2, world_y2 = pan_zoom_handler.screen_2_world(screen_search_area.right, screen_search_area.bottom)

    # Create a world coordinate search area
    world_search_area = Rect(world_x1, world_y1, world_x2 - world_x1, world_y2 - world_y1)

    found = qtree.query(world_search_area)
    for point in found:
        screen_x, screen_y = pan_zoom_handler.world_2_screen(point.x, point.y)
        screen_width, screen_height = point.width * pan_zoom_handler.get_zoom(), point.height * pan_zoom_handler.get_zoom()
        r = point.width / 2 * pan_zoom_handler.get_zoom()

        if r < 1:
            r = 1
            lod = 0
        elif r < 10:
            lod = 1

        else:
            lod = 2

        if lod == 0:
            gfxdraw.pixel(screen, int(screen_x), int(screen_y), BLUE)

        else:
            draw.circle(screen, BLUE, (int(screen_x), int(screen_y)), int(r))
