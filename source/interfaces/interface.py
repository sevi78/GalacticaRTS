import pygame
from pygame_widgets.util import drawText
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING, SLIDER_HEIGHT, ROUND_PRECISION
from source.gui.widgets.slider import Slider
from source.configuration import global_params
from source.handlers.color_handler import colors


class InterfaceVariable:
    def __init__(self, name, value, value_min, value_max):
        self.name = name
        self.value_min = value_min
        self.value_max = value_max
        self._value = 0
        self.value = value

    def __repr__(self):
        return (f"value: {self.value} type: {type(self.value)},"
                f" value_min: {self.value_min} type: {type(self.value_min)}"
                f" value_max: {self.value_max} type: {type(self.value_max)}")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value < self.value_min:
            self._value = self.value_min
        elif value > self.value_max:
            self._value = self.value_max
        else:
            self._value = value

    def get_value(self):
        return self.value


class InterfaceData:
    def __init__(self, interface_variable_names):
        self.interface_variable_names = interface_variable_names
        self.interface_variables = {}
        self.interface_variables = self.get_interface_variables()

    def set_variables(self, obj):
        for i in self.interface_variable_names:
            value = getattr(obj, i)

            if hasattr(obj, i + "_min"):
                min = getattr(obj, i + "_min")
            else:
                if type(value) == int:
                    min = 0
                elif type(value) == float:
                    min = 0.0

            if hasattr(obj, i + "_max"):
                max = getattr(obj, i + "_max")
            else:
                max = getattr(obj, i)

            self.interface_variables[i] = InterfaceVariable(i, value, min, max)

    def get_interface_variables(self):
        self.set_variables(self)
        return self.interface_variables

    def get_dict(self):
        data = {}
        for i in self.interface_variable_names:
            data[i] = getattr(self, i)
            if hasattr(self, i + "_max"):
                data[i + "_max"] = getattr(self, i + "_max")

            if hasattr(self, i + "_min"):
                data[i + "_min"] = getattr(self, i + "_min")

        return data


class Interface(EditorBase):
    """to create an interface, you must inherit InterfaceData to the object that should be edited:
    then you must overgive the interface_variable_names to the constructor. these are the variables that
    gonna be edited then.

    create a config file, 'object_name' .json.

    add this to the class you want to edit:

    # interface
    def __init__(self, ...):
        self.interface_variable_names = []

        for dict_name, dict in interface_variables.items():
            for key, value in dict.items():
                setattr(self, key, value)
                setattr(self, key + "_max", value)
                if not key.endswith("_max"):
                    self.interface_variable_names.append(key)

        InterfaceData.__init__(self, self.interface_variable_names)
        self.setup()

    def setup(self):
        data = load_file("event_panel.json")
        for name, dict in data.items():
            if name == self.name:
                for key, value in dict.items():
                    if key in self.__dict__:
                        setattr(self, key, value)

    this ensures that the data from the .json is loaded by contructing the object.
    looks comlicated...







    The code defines a class named Interface that represents a graphical user interface.
    It provides methods for creating sliders, hiding and showing the interface, and updating the values of the sliders
    based on user input.
    Example Usage:
    ```python # Create an instance of the Interface class interface = Interface(win, x, y, width, height)

    # Show the interface
    interface.show()

    # Hide the interface
    interface.hide()

    # Update the values of the sliders based on user input
    interface.listen(events)

    # Get the current values of the sliders
    slider_data = interface.get_slider_data()

    # Set the values of the sliders to the corresponding attributes of an object
    interface.set_obj_values()
    ```
    Main functionalities:

    The Interface class represents a graphical user interface that allows the user to interact
    with sliders to change the values of certain attributes. It provides methods for creating sliders,
    hiding and showing the interface, and updating the values of the sliders based on user input.

    Methods:
    - __init__: Initializes the Interface with the given parameters and sets default values for optional parameters.
    - create_sliders: Creates sliders based on the attributes of the associated object.
    - get_slider_data: Returns the current values of the sliders.
    - set_slider_data: Updates the values of the sliders based on the attributes of the associated object.
    - set_obj_values: Sets the values of the attributes of the associated object based on the values of the sliders.
    - draw_slider_texts: Draws the text labels for the sliders. - draw: Draws the interface on the screen.

    Fields:
    - sliders: A dictionary that stores the sliders created by the interface.
    - obj: The object associated with the interface.
    - win: The window surface on which the interface is drawn.
    - x, y: The coordinates of the top-left corner of the interface.
    - _width, _height: The width and height of the interface.
    - arrow_size, spacing_x, spacing_y: Constants used for positioning the widgets.
    - parent: The parent widget of the interface. - layer: The layer of the interface.
    - font: The font used for drawing text on the interface.
    - frame_color: The color of the frame of the interface.
    - frame: A surface used for drawing the frame of the interface.
    - widgets: A list that stores the widgets created by the interface.

    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.slider_height = SLIDER_HEIGHT
        self.max_height = 0
        self.sliders = {}

        self.slider_text_font_size = 20
        self.slider_font = pygame.font.SysFont(global_params.font_name, self.slider_text_font_size - 1)

        # create widgets
        self.create_sliders()

        # hide initially
        self.hide()

    def create_sliders(self):
        width = self.get_screen_width() / 2 - self.text_spacing
        x = self.world_x + self.world_width / 2
        y = self.world_y + 200

        for key, var in self.obj.interface_variables.items():
            value = var.value

            if type(value) == int:
                step = 1
            if type(value) == float:
                step = 0.001

            slider = Slider(win=self.win,
                x=x,
                y=y,
                width=width,
                height=self.slider_height,
                min=var.value_min,
                max=var.value_max,
                step=step,
                initial=value,
                handleColour=colors.ui_dark,
                layer=self.layer,
                parent=self)

            slider.colour = colors.ui_darker

            y += self.spacing_y

            self.sliders[key] = slider
            self.widgets.append(slider)

        self.max_height += y

    def get_slider_data(self):
        data = {}
        for name, slider in self.sliders.items():
            data[name] = slider.getValue()

        return data

    def set_slider_data(self):
        if not hasattr(self, "sliders"):
            return

        for key, value in self.sliders.items():
            self.sliders[key].setValue(getattr(self.obj, key))

    def set_obj_values(self):
        if self._hidden:
            return

        data = self.get_slider_data()

        for key, value in data.items():
            if type(value) == float:
                value = round(value, ROUND_PRECISION)
            setattr(self.obj, key, value)
            if hasattr(self.obj, "set_info_text"):
                self.obj.set_info_text()

    def draw_slider_texts(self):
        for name, slider in self.sliders.items():
            rect = pygame.Rect(self.world_x + self.text_spacing, slider.world_y - 2, self.world_width, self.slider_text_font_size)
            text = f"{name} : {round(slider.getValue(), ROUND_PRECISION)} / {slider.max}"
            drawText(self.win, text, self.frame_color, rect, self.slider_font, align="left")

    def draw(self):
        if self._hidden:
            return
        self.draw_frame()
        self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.world_width / 20, 200, 30, self.obj.name)

        self.set_slider_data()
        self.set_obj_values()

        self.draw_slider_texts()

        if hasattr(self, "interface_callback"):
            self.interface_callback()
