import random

import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, BUTTON_SIZE, TOP_SPACING
from source.factories.building_factory import building_factory
from source.game_play.navigation import navigate_to
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.checkbox import Checkbox
from source.gui.widgets.inputbox import InputBox
from source.gui.widgets.selector import Selector

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.physics.orbit import set_orbit_object_id
from source.utils import global_params
from source.multimedia_library.images import images, pictures_path, get_image

PLANET_MAX_SIZE = 200.0

PLANET_MIN_SIZE = 10.0


class PlanetEditBuilder:
    def create_randomize_button(self):
        button_size = 32
        randomize_button = ImageButton(win=self.win,
            x=self.get_screen_x() + button_size / 2,
            y=self.world_y + TOP_SPACING + button_size / 2,
            width=button_size,
            height=button_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("randomize_icon.png"), (button_size, button_size)),
            tooltip="randomize planet",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=self.layer,
            onClick=lambda: self.randomize(),
            )

        randomize_button.hide()

        self.buttons.append(randomize_button)
        self.widgets.append(randomize_button)

    def create_inputboxes(self):
        """"""
        self.inputbox = InputBox(self.win, self.world_x - self.spacing_x / 2 + self.world_width / 2, self.world_y + TOP_SPACING, self.spacing_x * 2, 32,
            text="", parent=self, key="name")
        self.widgets.append(self.inputbox)

    def create_selectors(self):
        """"""
        x = self.world_x + self.world_width / 2 - ARROW_SIZE / 2
        y = 140

        self.selector_planet = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9, self.spacing_x,
            {"list_name": "planets_list", "list": sprite_groups.planets.sprites()}, self, FONT_SIZE)
        y += self.spacing_y

        self.type_planet = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9, self.spacing_x,
            {"list_name": "type_list", "list": self.type_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_id = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9, self.spacing_x,
            {"list_name": "id_list", "list": self.id_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_level = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9, self.spacing_x,
            {"list_name": "level_list", "list": self.level_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_image_name_small = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "image_name_small_list", "list": self.image_name_small_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_has_atmosphere = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "has_atmosphere_list", "list": self.has_atmosphere_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_atmosphere = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "atmosphere_name_list", "list": self.atmosphere_name_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_orbit_object_id = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "orbit_object_id_list", "list": self.orbit_object_id_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_orbit_speed = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "orbit_speed_list", "list": self.orbit_speed_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_buildings_max = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "buildings_max_list", "list": self.buildings_max_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_building_slot_amount = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "building_slot_amount_list", "list": self.building_slot_amount_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_orbit_angle = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "orbit_angle_list", "list": self.orbit_angle_list}, self, FONT_SIZE)
        y += self.spacing_y

        self.selector_alien_population = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "alien_population", "list": self.alien_population_list}, self, FONT_SIZE)

        y += self.spacing_y
        self.max_height = y

    def create_checkboxes(self):
        """"""
        all_possible_resources = building_factory.get_resource_categories()
        y = self.world_y + 100
        x = self.world_width / 2 + BUTTON_SIZE

        for i in all_possible_resources:
            checkbox = Checkbox(
                self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
                color=self.frame_color,
                key=i, tooltip=i, onClick=lambda: print("OKOKOK"), layer=9, parent=self)
            x += BUTTON_SIZE * 1.5

            self.checkboxes.append(checkbox)
            self.widgets.append(checkbox)


class PlanetEdit(EditorBase, PlanetEditBuilder):
    """Main functionalities:
    The PlanetEdit class is responsible for creating a GUI interface for editing planet properties. It allows the user
    to select a planet from a list, change its name, image, atmosphere, orbit object ID, and resources.
    It also provides a checkbox for each possible resource, allowing the user to select which resources are available
    on the planet. The class communicates with the parent class to update the selected planet and navigate to it on the
    screen.

    Methods:
    - create_inputboxes(): creates an input box for the planet name
    - create_selectors(): creates selectors for the planet image, atmosphere, and orbit object ID
    - create_checkboxes(): creates a checkbox for each possible resource
    - set_checkbox_values(): sets the value of each checkbox based on the selected planet's possible resources
    - get_checkbox_values(): gets the values of all checkboxes and updates the selected planet's resources accordingly
    - get_selected_planet(): gets the selected planet from the parent class and updates the GUI accordingly
    - selector_callback(): updates the selected planet's properties based on user input
    - set_new_value_to_planet(): sets a new value for a selected planet's property and updates the GUI accordingly
    - listen(): listens for user input and updates the GUI accordingly
    - draw(): draws the GUI elements on the screen
    - hide(): hides the GUI elements
    - show(): shows the GUI elements

    Fields:
    - orbit_object_id_list: a list of possible orbit object IDs
    - widgets: a list of all GUI elements
    - spacing: the spacing between GUI elements
    - plus_arrow_button: a button for increasing a value
    - minus_arrow_button: a button for decreasing a value
    - conn: a connection to the database
    - dict: a dictionary of planet properties from the database
    - parent: the parent class
    - layer: the layer of the GUI elements
    - font: the font used for text
    - frame_color: the color of the GUI frames
    - atmosphere_name_list: a list of possible atmosphere names
    - atmosphere_current: the current atmosphere name
    - image_name_small_list: a list of possible planet image names
    - image_name_small_current: the current planet image name
    - _selected_planet: the currently selected planet
    - checkboxes: a list of all resource checkboxes
    - checkbox_values: a list of selected resource checkboxes

    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        self.scale = 1.0
        self.s_pressed = False

        # lists
        self.type_list = ["sun", "planet", "moon"]
        self.level_list = [_ for _ in range(10)]
        self.id_list = [_ for _ in range(len(sprite_groups.planets) + 1)]
        self.building_slot_amount_list = [_ for _ in range(10)]
        self.buildings_max_list = [_ for _ in range(25)]
        self.orbit_object_id_list = [_ for _ in range(len(sprite_groups.planets) + 1)]
        self.orbit_speed_list = [round(0.001 + _ * 0.001, 3) for _ in range(20)]
        self.atmosphere_name_list = list(images[pictures_path]["atmospheres"].keys())
        self.atmosphere_name_list.append("")
        self.has_atmosphere_list = [_ for _ in range(0, 2)]
        self.image_name_small_list = list(images[pictures_path]["planets"].keys())
        self.orbit_angle_list = [_ for _ in range(0, 360)]
        self.alien_population_list = [_ for _ in range(0, 10000000, 100000)]

        #  widgets
        self.selector_image_name_small = None
        self.selector_orbit_object_id = None
        self.selector_atmosphere = None
        self.selector_planet = None
        self.inputbox = None

        # current values
        self.atmosphere_current = None
        self.image_name_small_current = None
        self._selected_planet = None

        # create widgets
        self.create_checkboxes()
        self.create_selectors()
        self.create_inputboxes()
        self.create_save_button(lambda: self.parent.save_planets(), "save planet")
        self.create_close_button()
        self.create_randomize_button()

        # hide initially
        self.hide()

    @property
    def selected_planet(self):
        """"""
        return self._selected_planet

    @selected_planet.setter
    def selected_planet(self, value):
        self._selected_planet = value
        self.set_selector_current_value()
        navigate_to(self.parent.selected_planet, y_offset=-200)

    def set_selector_current_value(self):
        """updates the selectors values"""
        for i in self.selectors:
            if i.key == "planets":
                i.set_current_value(self.parent.selected_planet)
            else:
                i.set_current_value(getattr(self.selected_planet, i.key))

    def set_checkbox_values(self):
        """this sets the values to the checkboxes when selected planet changes"""
        if not self.selected_planet:
            return

        possible_resources = self.selected_planet.possible_resources

        for i in self.checkboxes:
            if i.key in possible_resources:
                i.update(True)
            else:
                i.update(False)

    def get_checkbox_values(self):
        """gets the values from the checkboxes and calls update_planet_resources()"""
        self.checkbox_values = [i.key for i in self.checkboxes if i.checked]
        self.update_planet_resources()

    def update_planet_resources(self):
        """updates the planets resources"""
        self.selected_planet.update_planet_resources(self.checkbox_values)

    def get_selected_planet(self):
        """gets the selected planet"""
        # error handling if no planet selected
        if not self.parent.selected_planet:
            return None

        # only set checkbox values if selected planet changes
        selected_planet = self.selected_planet
        self.selected_planet = self.parent.selected_planet

        if selected_planet != self.parent.selected_planet:
            self.set_selector_current_value()
            self.set_checkbox_values()

        self.image_name_small_current = self.selected_planet.image_name_small
        self.atmosphere_current = self.selected_planet.atmosphere_name

        text = self.selected_planet.name  # + ", id: " + str(self.selected_planet.id)
        self.inputbox.set_text(text)

    def get_input_box_values(self, obj, key, value):
        # self.parent.get_input_box_values("name", self.text)
        # self.parent.get_input_box_values("string", self.text)
        if key == "name":
            self.set_new_value_to_planet("name", value)
            self.set_new_value_to_planet("string", value)

    def set_new_value_to_planet(self, key, value):
        """sets the new values to the planet, called from outside
        """
        if not self.selected_planet:
            return

        setattr(self.selected_planet, key, value)
        self.selected_planet.image_raw = get_image(self.selected_planet.image_name_small)

        if self.selected_planet.atmosphere_name != "":
            self.selected_planet.atmosphere = images[pictures_path]["atmospheres"][self.selected_planet.atmosphere_name]
            self.selected_planet.atmosphere_raw = images[pictures_path]["atmospheres"][
                self.selected_planet.atmosphere_name]
        else:
            self.selected_planet.atmosphere = None
            self.selected_planet.atmosphere_raw = None

    def selector_callback(self, key, value):
        """this is the selector_callback function called from the selector to return the values to the editor"""
        has_atmosphere_set = False

        if key == "planets":
            self.parent.set_selected_planet(value)

        if key == "has_atmosphere":
            if value == 0 and self.selector_atmosphere.current_value != "":
                self.selector_atmosphere.current_value = ""
                has_atmosphere_set = True

        if key == "atmosphere_name":
            if not has_atmosphere_set:
                setattr(self.selected_planet, key, value)

        if key == "orbit_object_id":
            set_orbit_object_id(self.selected_planet, value)
        else:
            setattr(self.selected_planet, key, value)

    def scale_planet__(self, events):
        if self._hidden:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.s_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    self.s_pressed = False

            if event.type == pygame.MOUSEWHEEL and self.s_pressed:
                min_size = 10.0
                max_size = 200.0
                self.scale = event.y
                planet = self.parent.selected_planet

                # Check if resulting value is less than min_size
                if planet.world_width + self.scale < min_size:
                    planet.world_width = min_size

                # Check if resulting value is greater than max_size
                elif planet.world_width + self.scale > max_size:
                    planet.world_width = max_size
                else:
                    planet.world_width += self.scale

                # Check if resulting value is less than min_size
                if planet.world_height + self.scale < min_size:
                    planet.world_height = min_size

                # Check if resulting value is greater than max_size
                elif planet.world_height + self.scale > max_size:
                    planet.world_height = max_size
                else:
                    planet.world_height += self.scale

    def scale_planet(self, events):
        if self._hidden:
            return
        planet = self.parent.selected_planet

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.s_pressed = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_s:
                self.s_pressed = False
            elif event.type == pygame.MOUSEWHEEL and self.s_pressed:
                self.scale = event.y

                # Check if resulting value is less than min_size or greater than max_size
                planet.world_width = max(PLANET_MIN_SIZE, min(PLANET_MAX_SIZE, planet.world_width + self.scale))
                planet.world_height = max(PLANET_MIN_SIZE, min(PLANET_MAX_SIZE, planet.world_height + self.scale))

    def randomize(self):
        ignorables = ["planets", "id", "level", "orbit_object_id", "orbit_angle"]
        for selector in self.selectors:
            if not selector.key in ignorables:
                selector.current_value = random.choice(selector.list)

            self.selector_callback(selector.key, selector.current_value)

        for checkbox in self.checkboxes:
            checkbox.update(random.choice([0, 1]))
            self.get_checkbox_values()

    def listen(self, events):
        """show or hide, navigate to planet on selection"""
        self.inputbox.handle_events(events)
        self.scale_planet(events)
        for event in events:
            # ignore all inputs while any text input is active
            if global_params.text_input_active:
                return

        if not self.parent.selected_planet:
            if len(sprite_groups.planets.sprites()) > 0:
                self.parent.set_selected_planet(sprite_groups.planets.sprites()[0])

        if not self._hidden or self._disabled:
            self.orbit_object_id_list = [_ for _ in range(len(sprite_groups.planets.sprites()))]
            self.id_list = [_ for _ in range(len(sprite_groups.planets.sprites()))]

    def draw(self):
        """"""
        if not self._hidden or self._disabled:
            self.draw_frame()
            self.get_selected_planet()
            self.inputbox.update()
