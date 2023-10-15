import time

from source.pan_zoom_sprites.attack import attack, launch_missile
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.utils.positioning import get_distance

MISSILE_LAUNCH_INTERVALL = 2


class PanZoomPlanetDefence:
    def __init__(self, parent):
        self.parent = parent
        self.attack_distance_raw = 300
        self.attack_distance = self.attack_distance_raw
        self.defence_units_names = ["cannon", "missile"]
        self.last_missile_launch = time.time()
        self.missile_launch_interval = MISSILE_LAUNCH_INTERVALL

    def get_defence_units(self):
        return [i for i in self.parent.buildings if i in self.defence_units_names]

    def get_missiles(self):
        return len([i for i in self.parent.buildings if i == "missile"])

    def defend(self):
        defence_units = self.get_defence_units()

        if len(defence_units) == 0:
            return

        # for ufo in global_params.app.ufos:
        for ufo in sprite_groups.ufos:
            dist = get_distance(self.parent.rect.center, ufo.rect.center)
            # dist = get_distance(self.parent.get_position())
            self.attack_distance = self.attack_distance_raw * self.parent.get_zoom()

            if dist < self.attack_distance:
                # pygame.draw.circle(global_params.win,
                #     pygame.color.THECOLORS["red"], self.parent.get_position(), self.attack_distance, 1)
                # pygame.draw.circle(global_params.win, colors.frame_color, self.parent.get_position(), dist, 1)

                if "cannon" in defence_units:
                    attack(self.parent, ufo)
                if "missile" in defence_units:
                    missiles = self.get_missiles()
                    if time.time() - self.missile_launch_interval / missiles > self.last_missile_launch:
                        launch_missile(self.parent, ufo)
                        self.last_missile_launch = time.time()
            else:
                pass
                # pygame.draw.circle(global_params.win,
                #     pygame.color.THECOLORS["green"], self.parent.get_position(), self.attack_distance, 1)
