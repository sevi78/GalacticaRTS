"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).
"""

__all__ = ['main']

import os

import pygame_menu

from source.database.database_access import create_connection, get_database_file_path, \
    get_dict_from_database
from source.utils import global_params
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups

# Constants and global variables
FPS = 60
WINDOW_SIZE = (840, 1200)
global settings_run
settings_run = True


def quit_menu():
    print("quitting main_menu")
    settings_run = False


# Define the selector_callback function for the selector
def on_selector_change(value):
    # Update the ID based on the selected value
    planet_id = value  # Replace this with your logic to update the ID

    # Do something with the updated ID
    print(f"Selected planet ID: {planet_id}")
    return planet_id


def main(test: bool = False, **kwargs) -> None:
    surface = global_params.win

    # -------------------------------------------------------------------------
    # Create menus: Settings
    # -------------------------------------------------------------------------
    settings_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    settings_menu_theme.title_offset = (5, -2)
    settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    settings_menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    settings_menu_theme.widget_font_size = 20

    if global_params.app.selected_planet:
        planet = global_params.app.selected_planet
    else:
        planet = sprite_groups.planets.sprites()[0]

    planet_name = planet.name

    # create menu
    settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        theme=settings_menu_theme,
        title=planet_name,
        width=WINDOW_SIZE[0] * 0.9,
        onclose=pygame_menu.events.BACK,  # User press ESC button
        )

    dirpath = os.path.dirname(os.path.realpath(__file__))
    pictures_path = os.path.split(dirpath)[0].split("source")[0] + "assets" + os.sep + "pictures" + os.sep
    settings = get_dict_from_database(planet.id)

    # Add the selector to the menu
    planet_name_list = [(name, str(id)) for id, name in settings.items()]
    print("planet_name_list:", planet_name_list)
    # settings_menu.add.selector('Select a planet: ', planet_name_list, onchange=on_selector_change)

    print("settings", settings)

    # set images
    image_name_small = settings["image_name_small"]
    image_name_big = settings["image_name_big"]

    # add images
    settings_menu.add.image(os.path.join(pictures_path + "planets" + os.sep + image_name_small))
    settings_menu.add.image(os.path.join(pictures_path + "planets" + os.sep + image_name_big))

    # iterate over settings, so we can add new fields to planet
    for key, value in settings.items():
        # check for type to make shure input is correct format
        if "int" in str(type(value)):
            input_type = pygame_menu.locals.INPUT_INT

        if "str" in str(type(value)):
            input_type = pygame_menu.locals.INPUT_TEXT

        if "float" in str(type(value)):
            input_type = pygame_menu.locals.INPUT_FLOAT

        if "None" in str(type(value)):
            input_type = pygame_menu.locals.INPUT_TEXT

        if "[" in str(value):
            value = str(value)
            input_type = pygame_menu.locals.INPUT_TEXT

        # ckeck if value exists and take value from file,  otherwise take default from planet_config
        if key in settings.keys():
            default = settings[key]
        else:
            default = str(value)
            print(f"PlanetEditor error: could not find {key} in {planet_name}.json!")

        # construct text_input
        settings_menu.add.text_input(
            str(key) + ': ',
            default=default,
            maxwidth=0,
            textinput_id=key,
            input_underline='',
            align=pygame_menu.locals.ALIGN_LEFT,
            input_type=input_type,
            wordwrap=True)

    def data_fun() -> None:
        """
        Update data of the menu in SQLite database. written by perplexity ai
        """
        data = settings_menu.get_input_data()
        print('Settings data:', data)

        # create a connection to the database
        conn = create_connection(get_database_file_path())
        cur = conn.cursor()

        # update data in the "planets" table
        update_sql = "UPDATE planets SET "
        update_values = []
        for key, value in data.items():
            if key in [col[1] for col in cur.execute("PRAGMA table_info(planets)").fetchall()]:
                update_sql += f"{key} = ?, "
                update_values.append(value)

        update_sql = update_sql.rstrip(", ")
        update_sql += f" WHERE id = '{planet.id}'"
        cur.execute(update_sql, tuple(update_values))

        # commit the changes and close the cursor and connection
        conn.commit()
        cur.close()
        conn.close()

        # finally set new values to planet for realtime edit
        planet.load_from_db()

    # Add final buttons
    settings_menu.add.vertical_fill(30, "vf")
    settings_menu.add.button('Store data', data_fun, button_id='store')  # Call function
    settings_menu.add.button('Restore original values', settings_menu.reset_value)

    if settings_run:
        # Main menu
        settings_menu.mainloop(surface, None, disable_loop=test, fps_limit=FPS, clear_surface=False)
