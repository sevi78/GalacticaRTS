from source.interfaces.interface import Interface

class EventPanelEdit(Interface):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        Interface.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.create_save_button(lambda: self.parent.save_objects("event_panel.json",[self.obj]),"save event panel settings")
        self.create_close_button()


