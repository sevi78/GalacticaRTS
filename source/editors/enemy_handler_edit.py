from source.interfaces.interface import Interface
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class EnemyHandlerEdit(Interface):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        Interface.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.create_save_button(lambda: self.parent.save_objects("enemy_handler_config.json", [
            self.obj]), "save enemy handler")
        self.create_close_button()

    def update_enemies(self, key, value):
        for ufo in sprite_groups.ufos.sprites():
            setattr(ufo, key, value)

    def interface_callback(self):
        for key, value in self.get_slider_data().items():
            if key != "spawn_interval":
                self.update_enemies(key, value)
