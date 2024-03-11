import pygame

from source.game_play.navigation import navigate_to, navigate_to_position
from source.handlers.pan_zoom_sprite_handler import sprite_groups

""" cant move back to event_text; big mess with imports"""


def listen(self, events):
    """ called from event_text """
    # dirty hack to gez the planets
    self.planet_names = [i.name for i in sprite_groups.planets.sprites()]

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for click_surf in self.click_surfaces_list:
                if click_surf[1].collidepoint(event.pos):
                    follow_link(self)


def follow_link(self):
    if self.obj:
        if self.obj.__class__.__name__ == "PanZoomShip":
            navigate_to_position(self.obj.screen_x, self.obj.screen_y)
        if self.obj.__class__.__name__ == "PanZoomPlanet":
            navigate_to(self.obj)
