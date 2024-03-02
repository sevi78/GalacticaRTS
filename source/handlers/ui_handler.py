from source.handlers.file_handler import write_file, load_file
from source.handlers.widget_handler import WidgetHandler


class UIHandler:
    """
    writes the positions of all widgets with the attribute "save" into a json file
    reads the positions of all widgets with the attribute "save" from a json file and sets the positions of the widgets
    """
    def __init__(self):
        # all widgets
        self.ui_elements = {}

        # widgets x,y as dict, use this to store to the file
        self.ui_elements_dicts = {}

    def set_ui_elements(self):
        # reset dicts
        self.ui_elements = {}
        self.ui_elements_dicts = {}

        # for all objects that has "save" attribute, setup two dicts. first with obj second with x,y
        for index, i in enumerate([_ for _ in WidgetHandler.get_all_widgets() if hasattr(_, "save")]):
            self.ui_elements[str(index)] = i
            self.ui_elements_dicts[str(index)] = {"world_x": i.world_x, "world_y": i.world_y}

    def save_ui_elements(self):
        # setup objects to save
        self.set_ui_elements()

        # write to disk
        write_file("ui_config.json", "config", self.ui_elements_dicts)

    def restore_ui_elements(self):
        # set objects to restore
        self.set_ui_elements()

        # load config file
        self.ui_elements_dicts = load_file("ui_config.json", "config")

        # for all widgets
        for key, obj in self.ui_elements.items():

            # temp store x,y for repositioning of the children widgets
            old_x, old_y = obj.world_x, obj.world_y

            # check for stored values
            if key in self.ui_elements_dicts:

                # set the values
                for i in self.ui_elements_dicts[key]:
                    setattr(obj, i, self.ui_elements_dicts[key][i])
                    setattr(obj.rect, i.split("world_")[1], self.ui_elements_dicts[key][i])

                # reposition
                if hasattr(obj, "reposition"):
                    obj.reposition(old_x, old_y)


ui_handler = UIHandler()
