from source.configuration.game_config import config
from source.draw.scope import scope
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship import PanZoomShip
from source.text.text_formatter import format_number


class PanZoomRescueDrone(PanZoomShip):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomShip.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.target_set = False
        del self.pathfinding_manager
        del self.progress_bar

    # def set_target(self, **kwargs):# original
    #     if self.target_set:
    #         return
    #
    #     target = kwargs.get("target", None)
    #     if not target:
    #         target = sprite_groups.get_hit_object(lists=["ships"])
    #     if target == self:
    #         return
    #
    #     if target:
    #         self.target = target
    #
    #     self.select(False)
    #     self.target_set = True

    def set_target(self, **kwargs):
        target = kwargs.get("target", sprite_groups.get_hit_object(lists=["ships"]))
        from_server = kwargs.get("from_server", None)

        if self.target_set:
            return

        if target == self:
            return

        if target:
            if hasattr(self, "pathfinding_manager"):
                if not self.pathfinding_manager.path:
                    self.target = target
                else:
                    self.pathfinding_manager.move_to_next_node()
                    self.enemy = None

            self.set_energy_reloader(target)
        else:
            self.target = self.target_object
            self.enemy = None
            self.orbit_object = None

            # set target object position
            self.target.world_x, self.target.world_y = self.pan_zoom.get_mouse_world_position()
            self.set_energy_reloader(None)

        self.select(False)
        self.target_set = True

        # fix the case if attacking and setting new target
        if self.target:
            if self.target != self.enemy:
                self.enemy = None
                self.orbit_object = None
                self.state_engine.set_state("moving")

            # send data to server, only if not called from server !!!
            if not from_server:
                config.app.game_client.send_message(self.get_network_data("set_target"))

    def reach_target(self, distance):
        if not self.target:
            return

        if self.target.property == "ship":
            if distance < self.desired_orbit_radius:
                # set the correct amount of energy
                if self.target.energy + self.energy > self.target.energy_max:
                    self.target.energy = self.target.energy_max
                else:
                    self.target.energy += self.energy

                self.target_reached = True
                self.moving = False
                self.__delete__(self)

    def update(self):
        # update state engine
        self.state_engine.update()

        # update game object
        self.update_pan_zoom_game_object()

        # return if game paused
        if config.game_paused:
            return

        self.listen()
        # if self.selected and self == config.app.ship:
        #     pre_calculated_energy_use = 0
        #     if config.app.weapon_select._hidden:
        #         pass
        #         # scope.draw_scope(
        #         #         start_pos= self.rect.center,
        #         #         range_= float('inf'),
        #         #         info={"energy use": format_number(pre_calculated_energy_use, 1)},
        #         #         lists="ships")

        self.set_distances()

        # set the info text/tooltip
        self.set_info_text()
        self.set_tooltip()

        # draw selection and connections
        if self.selected or self == config.app.ship:
            self.draw_selection()

        # travel
        if self.target and self.selected and self == config.app.ship:
            self.draw_connections(self.target)

        # autopilot
        self.handle_autopilot()
