import math

from pygame import Vector2

from source.configuration.game_config import config
from source.handlers.diplomacy_handler import diplomacy_handler
from source.handlers.orbit_handler import set_orbit_object_id, orbit_ship
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import rotate_image_to
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_params import SHIP_ORBIT_SPEED, SHIP_ORBIT_SPEED_MAX
from source.path_finding.a_star_node_path_finding import Node
from source.path_finding.pathfinding_manager import PathFindingManager

TRAVEL_EXPERIENCE_FACTOR = 0.1

# disabled_functions = ["play_travel_sound", "consume_energy_if_traveling"]
# for i in disabled_functions:
#     disabler.disable(i)
#
# @auto_disable
class PanZoomShipMoving:
    def __init__(self, kwargs):
        self.following_path = False
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

        # pathfinding
        self.node = Node(self.world_x, self.world_y, self)
        self.pathfinding_manager = PathFindingManager(self)

    @property
    def orbiting(self):
        return self._orbiting

    @orbiting.setter
    def orbiting(self, value):
        self._orbiting = value
        if value:
            if self.target:
                if hasattr(self.target, "id"):
                    if not self.target.id == self.id:
                        set_orbit_object_id(self, self.target.id)
                    else:

                        print("@orbiting.setter error: target.id == self.id!")
                else:
                    print("@orbiting.setter error: target has no attr 'id'!")

        # self.state_engine.set_state()

    @property
    def moving(self):
        return self._moving

    @moving.setter
    def moving(self, value):
        self._moving = value
        if value == True:
            self.orbiting = False
            self.state_engine.set_state("moving")

        # self.state_engine.set_state()

    @property
    def move_stop(self):
        return self._move_stop

    @move_stop.setter
    def move_stop(self, value):
        self._move_stop = value

        if not hasattr(self, "state_engine"):
            return
        if value:
            self.state_engine.set_state("move_stop")

    def set_speed(self):
        # adjust speed if no energy
        if self.move_stop > 0:
            speed = self.speed / 10
        else:
            speed = self.speed
        return speed

    def set_attack_distance(self):
        self.attack_distance = self.attack_distance_raw  # * pan_zoom_handler.get_zoom()

    def set_desired_orbit_radius(self):
        self.desired_orbit_radius = self.desired_orbit_radius_raw  # * pan_zoom_handler.get_zoom()

    def set_target_object_reset_distance(self):
        self.target_object_reset_distance = self.target_object_reset_distance_raw  # * pan_zoom_handler.get_zoom()

    def set_reload_max_distance(self):
        self.reload_max_distance = self.reload_max_distance_raw * pan_zoom_handler.get_zoom()
        # pygame.draw.circle(self.win, pygame.color.THECOLORS["green"], self.rect.center, self.reload_max_distance, 1)

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
        if self.owner == config.app.game_client.id:
            self.parent.info_panel.set_planet_image(self.target.image_raw)

        self.target.get_explored(self.owner)

    def reach_target(self, distance):
        if not self.target:
            return

        if self.target.property == "ufo":
            if distance <= self.attack_distance:
                self.moving = False
                self.reach_enemy()
                self.pathfinding_manager.reset()
                return

        elif self.target.property == "planet":
            if distance < self.desired_orbit_radius:
                self.reach_planet()

                # self.pathfinding_manager.reset()
                return

        elif self.target.property == "ship":
            if distance < self.desired_orbit_radius:
                if not diplomacy_handler.is_in_peace(self.target.owner, self.owner):
                    self.reach_enemy()
                    return
                self.target_reached = True
                self.moving = False
                self.orbit_object = self.target
                self.pathfinding_manager.reset()
                return

        elif self.target.property == "item":
            if distance < self.item_collect_distance:
                self.moving = False
                self.economy_agent.load_cargo(self)
                self.target.end_object()
                self.target = None
                self.target_reached = True
                self.pathfinding_manager.reset()
                return

        elif self.target.property == "target_object":
            if distance < self.target_object_reset_distance:
                self.moving = False
                self.target = None
                self.target_reached = True
                self.pathfinding_manager.reset()

    def reach_enemy(self):
        self.target_reached = True
        self.orbit_object = self.target
        self.enemy = self.orbit_object
        self.moving = False

    def reach_planet(self):
        """ if a planet is reached, then depending on diplomacy and path_following, several scenarios will happen:

            if the planet is hostile:
                attack the planet

            if planet is inhabited:
                develop the planet
        """

        # develop planet
        self.develop_planet()

        # follow path: check if any waypoints left
        if self.pathfinding_manager.path:
            self.target_reached = False
            self.pathfinding_manager.move_to_next_node()
        else:
            self.target_reached = True

        # if no waypoints, target is reached
        if self.target_reached:
            # unload_cargo goods
            if not self.target.type == "sun" and self.target.owner == self.owner or self.target.owner == -1:
                self.economy_agent.unload_cargo(self)

            self.set_energy_reloader(self.target)

            # sound stop
            sounds.stop_sound(self.sound_channel)
            self.hum_playing = False

            # # open diplomacy edit to make war or peace
            # if self.target.owner != self.owner:
            #     config.app.diplomacy_edit.open(self.target.owner, self.owner)

            # attack if hostile planet
            if not diplomacy_handler.is_in_peace(self.target.owner, self.owner):
                self.reach_enemy()

            # set orbit object ( also resets target)
            self.orbit_object = self.target
            self.moving = False

    def follow_target(self, obj):
        self.state_engine.set_state("attacking")
        target_position = Vector2(obj.world_x, obj.world_y)
        current_position = Vector2(self.world_x, self.world_y)

        direction = target_position - current_position
        distance = direction.length() * pan_zoom_handler.get_zoom()
        speed_ = self.set_speed()

        if distance > self.attack_distance:
            direction.normalize()

            # Get the speed of the obj
            speed = 0.1
            if obj.property in ["ship", "ufo"]:
                speed = (speed_ + obj.speed)
            if obj.property == "planet":
                speed = obj.orbit_speed

            if speed > self.set_speed():
                speed = self.set_speed()

            # Calculate the displacement vector for each time step
            displacement = direction * speed * time_handler.game_speed / config.fps
            # print(f"displacement: {displacement}")

            # Move the obj towards the target position with a constant speed
            if config.app.game_client.is_host:
                self.world_x += displacement.x
                self.world_y += displacement.y

            self.set_world_position((self.world_x, self.world_y))

            self.angle = rotate_image_to(self, target_position, 180)

    def follow_target_(self, obj):
        self.state_engine.set_state("attacking")
        target_position = Vector2(obj.world_x, obj.world_y)
        current_position = Vector2(self.world_x, self.world_y)



        direction = target_position - current_position
        distance = direction.length() * pan_zoom_handler.get_zoom()
        speed_ = self.set_speed()

        speed = 0.1
        if distance > self.attack_distance:
            direction.normalize()

            # Get the speed of the obj

            if obj.property in ["ship", "ufo"]:
                speed = (speed_ + obj.speed)
            if obj.property == "planet":
                speed = obj.orbit_speed

            if speed > self.set_speed():
                speed = self.set_speed()

            # # Calculate the displacement vector for each time step
            # displacement = direction * speed * time_handler.game_speed / config.fps
            # # print(f"displacement: {displacement}")
            #
            # # Move the obj towards the target position with a constant speed
            # if config.app.game_client.is_host:
            #     self.world_x += displacement.x
            #     self.world_y += displacement.y
            #
            # self.set_world_position((self.world_x, self.world_y))
            #
            # rotate_image_to(self, target_position, 180)

        orbit_ship(self, obj, speed, -1)



    def consume_energy_if_traveling(self):
        # only subtract energy if some energy is left
        if self.energy <= 0.0 or self.orbiting:
            return

        # subtract the traveled distance from the ships energy
        traveled_distance = math.dist((self.world_x, self.world_y), self.previous_position)
        self.energy -= traveled_distance * self.energy_use
        self.set_experience(traveled_distance * TRAVEL_EXPERIENCE_FACTOR)

    def get_max_travel_range(self) -> float:
        """ returns the max distance in world coordinates the ship can move based on its energy """
        return self.energy / self.energy_use


