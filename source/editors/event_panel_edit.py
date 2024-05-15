from source.gui.interfaces.interface import Interface


class EventPanelEdit(Interface):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        Interface.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.create_save_button(lambda: self.parent.save_objects("event_panel.json", [
            self.obj]), "save event panel settings")
        self.create_close_button()

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)
