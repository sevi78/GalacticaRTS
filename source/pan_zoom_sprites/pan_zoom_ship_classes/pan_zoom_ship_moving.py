import math

from source.configuration.game_config import config
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_params import SHIP_ORBIT_SPEED, SHIP_ORBIT_SPEED_MAX

TRAVEL_EXPERIENCE_FACTOR = 0.1


class PanZoomShipMoving:
    def __init__(self, kwargs):
        self.desired_orbit_radius_raw = 100
        self.desired_orbit_radius = self.desired_orbit_radius_raw
        self.desired_orbit_radius_max = 200
        self.target = None
        self.enemy = None
        self.orbit_speed = SHIP_ORBIT_SPEED
        self.orbit_speed_max = SHIP_ORBIT_SPEED_MAX
        self.zoomable = True
        self.min_dist_to_other_ships = 80
        self.min_dist_to_other_ships_max = 200
        self.orbit_radius = 100 + self.id * 30
        self.orbit_radius_max = 300
        self.previous_position = (self.world_x, self.world_y)

    @property
    def orbiting(self):
        return self._orbiting

    @orbiting.setter
    def orbiting(self, value):
        self._orbiting = value
        if value:
            if self.target:
                self.set_orbit_object_id(self.target.id)

        self.state_engine.set_state()

    @property
    def moving(self):
        return self._moving

    @moving.setter
    def moving(self, value):
        self._moving = value
        if value == True:
            self.orbiting = False

        self.state_engine.set_state()

    @property
    def move_stop(self):
        return self._move_stop

    @move_stop.setter
    def move_stop(self, value):
        self._move_stop = value

        if not hasattr(self, "state_engine"):
            return
        self.state_engine.set_state()

    def set_speed(self):
        # adjust speed if no energy
        if self.move_stop > 0:
            speed = self.speed / 10
        else:
            speed = self.speed
        return speed

    def set_attack_distance(self):
        self.attack_distance = self.attack_distance_raw * self.get_zoom()

    def set_desired_orbit_radius(self):
        self.desired_orbit_radius = self.desired_orbit_radius_raw * self.get_zoom()

    def set_target_object_reset_distance(self):
        self.target_object_reset_distance = self.target_object_reset_distance_raw * self.get_zoom()

    def set_reload_max_distance(self):
        self.reload_max_distance = self.reload_max_distance_raw * self.get_zoom()

    def set_distances(self):
        self.set_attack_distance()
        self.set_desired_orbit_radius()
        self.set_target_object_reset_distance()
        self.set_reload_max_distance()

    def set_energy_reloader(self, obj):
        self.energy_reloader = obj

    def play_travel_sound(self):
        # plays sound
        if not self.hum_playing:
            sounds.play_sound(self.hum, channel=self.sound_channel, loops=1000, fade_ms=500)
            self.hum_playing = True

    def develop_planet(self):
        if self.target.explored:
            return

        self.set_experience(1000)
        self.parent.info_panel.set_planet_image(self.target.image_raw)
        self.target.get_explored(self.owner)

    def reach_enemy(self):
        self.target_reached = True
        self.orbit_object = self.target
        self.enemy = self.orbit_object
        self.moving = False

    def reach_planet(self):
        self.moving = False
        self.develop_planet()

        # unload_cargo goods
        if not self.target.type == "sun" and self.target.owner == self.owner or self.target.owner == -1:
            self.unload_cargo()

        self.set_energy_reloader(self.target)

        sounds.stop_sound(self.sound_channel)
        self.hum_playing = False

        if self.target.owner != self.owner:
            self.declare_war()


    def declare_war(self):
        config.app.declare_war_edit.set_enemy_and_player(self.target.owner, self.owner)
        config.app.declare_war_edit.set_visible()


    def consume_energy_if_traveling(self):
        # only subtract energy if some energy is left
        if self.energy <= 0.0 or self.orbiting:
            return

        # subtract the traveled distance from the ships energy
        traveled_distance = math.dist((self.world_x, self.world_y), self.previous_position)
        self.energy -= traveled_distance * self.energy_use
        self.set_experience(traveled_distance * TRAVEL_EXPERIENCE_FACTOR)

    def get_max_travel_range(self):
        return self.energy / self.energy_use
