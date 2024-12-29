from source.configuration.game_config import config
from source.handlers.mouse_handler import MouseState, mouse_handler

from source.interaction.interaction_handler import InteractionHandler
from source.multimedia_library.images import scale_image_cached
from source.multimedia_library.sounds import sounds


class PanZoomShipInteraction(InteractionHandler):
    def __init__(self, kwargs):
        InteractionHandler.__init__(self)
        # functionality
        # self.orbiting = False
        self._selected = False
        self.target = None
        self.autopilot = kwargs.get("autopilot", False)

    # @property
    # def autopilot(self):
    #     return self._autopilot
    #
    # @autopilot.setter
    # def autopilot(self, value):
    #     self._autopilot = value
    #     self.state_engine.set_state()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        # print (f"owner: {self.owner}, config.player: {config.player}, config.app.game_client.id: {config.app.game_client.id}")
        # make sure only own ships can be selected
        if self.owner == config.app.game_client.id:
            self._selected = value

    @property
    def orbit_object(self):
        return self._orbit_object

    @orbit_object.setter
    def orbit_object(self, value):
        self._orbit_object = value

        if value:
            self.target = None
            self.orbiting = True
            self.orbit_direction = 1  # random.choice([-1, 1])
            self.orbit_object_id = value.id
            self.orbit_object_name = value.name
        else:
            self.orbiting = False
            self.orbit_angle = None
            self.orbit_object_id = -1
            self.orbit_object_name = ""

    @property
    def enemy(self):
        return self._enemy

    @enemy.setter
    def enemy(self, value):
        self._enemy = value
        if not value:
            self.orbit_angle = None
            self.orbit_object = None
            self.target_reached = False

    def select(self, value):
        if not self.owner == config.app.game_client.id:
            return

        self.selected = value

        if value:
            sounds.play_sound("click", channel=7)
            config.app.ship = self

    def deselect(self):
        if config.app.ship == self:
            config.app.ship = None

    def listen(self):
        if not self.owner == config.app.game_client.id:
            return
        # if not config.player == config.app.player.owner:
        #     return

        config.app.tooltip_instance.reset_tooltip(self)
        if not config.app.weapon_select._hidden:
            return

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()

            if self.collide_rect.collidepoint(x, y):
                if mouse_handler.double_clicks == 1:
                    self.open_weapon_select()

                if mouse_state == MouseState.RIGHT_CLICK:
                    if config.app.ship == self:
                        self.select(True)

                if mouse_state == MouseState.LEFT_RELEASE and self.clicked:
                    self.clicked = False

                elif mouse_state == MouseState.LEFT_CLICK:
                    self.clicked = True
                    self.select(True)
                    config.app.ship = self

                elif mouse_state == MouseState.LEFT_DRAG and self.clicked:
                    pass

                elif mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                    self.submit_tooltip()

                    # dirty hack because the outline image is not rotated
                    if self.state_engine.state == "sleeping":
                        self.win.blit(scale_image_cached(self.image_outline, self.rect.size), self.rect)
                    self.weapon_handler.draw_attack_distance()

                    # set cursor
                    config.app.cursor.set_cursor("ship")
            else:
                # not mouse over object
                self.clicked = False
                if mouse_state == MouseState.LEFT_CLICK:
                    self.reset_target()

                if mouse_state == MouseState.RIGHT_CLICK:
                    self.activate_traveling()
