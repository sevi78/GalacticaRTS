from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_params import SHIP_ORBIT_SPEED, SHIP_ORBIT_SPEED_MAX
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.configuration import global_params
from source.handlers.position_handler import get_distance
from source.multimedia_library.sounds import sounds


class PanZoomShipMoving:
    """

    """

    def __init__(self, kwargs):

        self.desired_orbit_radius_raw = 100
        self.desired_orbit_radius = self.desired_orbit_radius_raw
        self.desired_orbit_radius_max = 200
        self.target = None
        self.enemy = None
        self._moving = False
        self._orbiting = False
        self.orbit_speed = SHIP_ORBIT_SPEED
        #self.orbit_speed_raw = SHIP_ORBIT_SPEED
        self.orbit_speed_max = SHIP_ORBIT_SPEED_MAX
        self.zoomable = True
        self.min_dist_to_other_ships = 80
        self.min_dist_to_other_ships_max = 200
        self.orbit_radius = 100 + self.id * 30
        self.orbit_radius_max = 300

    @property
    def orbiting(self):
        return self._orbiting

    @orbiting.setter
    def orbiting(self, value):
        self._orbiting = value
        if value:
            if self.target:
                self.set_orbit_object_id(self.target.id)

    @property
    def moving(self):
        return self._moving

    @moving.setter
    def moving(self, value):
        self._moving = value
        if value == True:
            self.orbiting = False

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

    def move_to_connection(self):
        self.moving = True
        # if stopped for any reason, no travel
        if self.move_stop > 0:
            self.moving = False
            self.set_experience(-1)
            return

        # low energy warning
        # self.low_energy_warning()

        # if everyting fine, undock and travel!(reset energy loader)
        # if not self.energy <= 1:
        #     self.set_energy_reloader(None)

        self.play_travel_sound()
        self.things_to_be_done_while_traveling()

        self.set_info_text()

    def get_target_position(self):
        if not self.target:
            return
        zoom = pan_zoom_handler.zoom
        if type(self.target) == tuple:
            x, y = self.target
        else:
            if self.target.rect:
                x, y = self.target.rect.center[0], self.target.rect.center[1]
            else:
                x, y = self.target.get_screen_x(), self.target.get_screen_y()
        return x, y

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
        self.target.get_explored()

    def reach_enemy(self):
        self.target_reached = True
        self.orbit_object = self.target
        self.enemy = self.orbit_object
        self.moving = False

    def reach_planet(self):
        self.moving = False
        self.develop_planet()

        # unload_cargo goods
        if not self.target.type == "sun":
            self.unload_cargo()
        self.set_energy_reloader(self.target)

        sounds.stop_sound(self.sound_channel)
        self.hum_playing = False

    def things_to_be_done_while_traveling(self):
        # set progress bar position
        self.progress_bar.set_progressbar_position()

        # draw fog of war
        # self.parent.fog_of_war.draw_fog_of_war(self)

        # get experience
        if self.moving:
            self.set_experience(1)
            if self.target:
                self.calculate_travel_cost(get_distance((self.get_screen_x(), self.get_screen_y()), (
                    self.get_target_position())))

    def calculate_travel_cost(self, distance):
        # calculate travelcosts
        self.energy -= distance * self.energy_use * global_params.time_factor  # * global_params.game_speed
        self.energy = int(self.energy)

    def set_energy_reloader(self, obj):
        self.energy_reloader = obj

    def low_energy_warning(self):
        return
        """
        bloody chatbot fuction, if energy is running out
        :return:
        """
        # low energy warning
        if self.energy < self.energy_warning_level:
            event_text.text = "LOW ENERGY WARNING!!! your ship is running out of energy! find a planet to land soon!!"

        if self.energy <= 0:
            event_text.text = "DAMMIT!!! your ship has run out of energy! you all gonna die !!!"
            self.move_stop += 1

        # if ship energy is empty
        if self.energy <= 0 and self.move_stop > 1000:
            event_text.text = "NO ENERGY DUDE! you cant move with this ship! "
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 2000:
            event_text.text = "..mhhh--- there might be a solution -- let me think about it a few seconds.."
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 3000:
            event_text.text = "the board engineer and i, have worked hard on a solution to this problem:"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 4000:
            event_text.text = "how about this: we sacrifice john the cook, i mean do we really need him?" \
                              " put him into the plasma reactor of our spaceship and get some energy out of him !"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 5000:
            event_text.text = "type 'yes' or 'no' if you want to burn the last cook from earth for surviving"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 6000:
            event_text.text = "haha!! that was just a joke! funny istn it ??"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 7000:
            event_text.text = "i mean, we will definitely cook the cook in the plasma engine, but I will decide for you :)"
            self.crew -= 1
            self.energy = 500
            self.move_stop = 0

        if self.energy > 0:
            self.move_stop = 0
