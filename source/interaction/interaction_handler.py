from source.configuration.game_config import config


class InteractionHandler:
    def __init__(self):
        self._on_hover = False
        self.on_hover_release = False

    @property
    def on_hover(self):
        return self._on_hover

    @on_hover.setter
    def on_hover(self, value):
        self._on_hover = value
        if value:
            config.hover_object = self
        else:
            if config.hover_object == self:
                config.hover_object = None
