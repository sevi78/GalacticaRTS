"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).
"""

__all__ = ['main']

import pygame_menu

from source.utils import global_params
from source.database.saveload import load_file, write_file

# Constants and global variables
FPS = 60
WINDOW_SIZE = (1400, 1000)

global settings_run
settings_run = True


def main(test: bool = False, **kwargs) -> None:
    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = global_params.win  # create_example_window('Galactica - Settings', WINDOW_SIZE,init_pygame=False)#kwargs.get("surface") #
    # clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Settings
    # -------------------------------------------------------------------------
    settings_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    settings_menu_theme.title_offset = (5, -2)
    settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    settings_menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    settings_menu_theme.widget_font_size = 20

    # gets values from save_load file(settings.json)
    settings = load_file("settings.json")

    # create menu
    settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        theme=settings_menu_theme,
        title='Settings',
        width=WINDOW_SIZE[0] * 0.9,
        onclose=pygame_menu.events.BACK, )  # User press ESC button)

    settings_menu.add.text_input(
        'TODO: ',
        default=settings["todo"],
        maxwidth=0,
        textinput_id='todo',
        input_underline='_',
        align=pygame_menu.locals.ALIGN_RIGHT,
        textwrap=True)

    settings_menu.add.text_input(
        'FPS: ',
        maxchar=3,
        default=int(settings["fps"]),
        textinput_id='fps',
        input_underline='_',
        align=pygame_menu.locals.ALIGN_RIGHT)

    settings_menu.add.text_input(
        'font_name: ',
        maxchar=20,
        default=str(settings["font_name"]),
        textinput_id='font_name',
        input_underline='_',
        align=pygame_menu.locals.ALIGN_RIGHT)

    # Selectable items
    widths = [("1920",),
              ("1400",),
              ("800",)]

    # Create selector with 3 options
    settings_menu.add.selector(
        'WIDTH:\t',
        widths,
        selector_id='WIDTH',
        default=settings["WIDTH"][1],
        align=pygame_menu.locals.ALIGN_RIGHT)

    heights = [("1080",),
               ("800",),
               ("600",)]

    # Create selector with 3 options
    settings_menu.add.selector(
        'HEIGHT:\t',
        heights,
        selector_id='HEIGHT',
        default=settings["HEIGHT"][1],
        align=pygame_menu.locals.ALIGN_RIGHT)

    # scene size
    settings_menu.add.text_input(
        'scene width: ',
        maxchar=5,
        default=int(settings["scene_width"]),
        textinput_id='scene_width',
        input_underline='_',
        input_type=pygame_menu.locals.INPUT_INT,
        align=pygame_menu.locals.ALIGN_RIGHT)

    settings_menu.add.text_input(
        'scene height: ',
        maxchar=5,
        default=int(settings["scene_height"]),
        textinput_id='scene_height',
        input_underline='_',
        input_type=pygame_menu.locals.INPUT_INT,
        align=pygame_menu.locals.ALIGN_RIGHT)

    settings_menu.add.range_slider('Universe Density:(lower value = less stars)',
        settings["universe_density"], (1, 100), 10,
        rangeslider_id='universe_density',
        value_format=lambda x: str(int(x)),
        align=pygame_menu.locals.ALIGN_RIGHT)

    # layers =[('0',[0] ),
    #            ('1'[1],),
    #            ('2',[2]),
    #            ('3',[3]),
    #            ('4',[4]),
    #            ('5',[5]),
    #            ('6',[6]),
    #            ('7',[7]),
    #            ('8', [8]),
    #            ('9',[9])]
    layers = [("0", 1), ("1", 0)]
    default = settings["visible_layers"][1]
    settings_menu.add.dropselect_multiple(
        title='visible layers: not working yet',
        items=layers,
        default=settings["visible_layers"][1],
        dropselect_multiple_id='visible_layers',
        max_selected=2,
        open_middle=True,
        selection_box_height=2,
        align=pygame_menu.locals.ALIGN_RIGHT)

    # Create switch
    settings_menu.add.toggle_switch('draw Background Image: ', settings["draw_background_image"],
        toggleswitch_id='draw_background_image', align=pygame_menu.locals.ALIGN_RIGHT)

    settings_menu.add.toggle_switch('Moveable', settings["moveable"],
        toggleswitch_id='moveable', align=pygame_menu.locals.ALIGN_RIGHT,
        )

    settings_menu.add.toggle_switch('Zoom', settings["enable_zoom"],
        toggleswitch_id='enable_zoom', align=pygame_menu.locals.ALIGN_RIGHT,
        )

    settings_menu.add.toggle_switch('pan', settings["enable_pan"],
        toggleswitch_id='enable_pan', align=pygame_menu.locals.ALIGN_RIGHT,
        )

    settings_menu.add.toggle_switch('enable_orbit', settings["enable_orbit"],
        toggleswitch_id='enable_orbit', align=pygame_menu.locals.ALIGN_RIGHT,
        )

    settings_menu.add.toggle_switch('enable_game_events', settings["enable_game_events"],
        toggleswitch_id='enable_game_events', align=pygame_menu.locals.ALIGN_RIGHT,
        )

    settings_menu.add.toggle_switch('debug', settings["debug"],
        toggleswitch_id='debug', align=pygame_menu.locals.ALIGN_RIGHT,
        )

    settings_menu.add.range_slider('Game Speed:', settings["game_speed"], (1, 25), 1,
        rangeslider_id='game_speed',
        value_format=lambda x: str(int(x)), align=pygame_menu.locals.ALIGN_RIGHT)

    settings_menu.add.range_slider('Time Factor:', settings["time_factor"], (1, 10), 1,
        rangeslider_id='time_factor',
        value_format=lambda x: str(int(x)), align=pygame_menu.locals.ALIGN_RIGHT)

    def data_fun() -> None:
        """
        Print data of the menu.
        """

        data = settings_menu.get_input_data()
        print('Settings data:', data)
        for k in data.keys():
            print(f'setting.data_fun: \t{k}\t=>\t{data[k]}')

        global_params.settings = data
        write_file("settings.json", data)

        # set new values to game
        for key, value in data.items():
            """
            False todo
            False universe_density, because needs to be restarted to build th euniverse
            False visible_layers, bad anyway
            """

            if hasattr(global_params, key):
                setattr(global_params, key, value)

    # Add final buttons

    settings_menu.add.vertical_fill(30, "vf")
    settings_menu.add.button('Store data', data_fun, button_id='store')  # Call function
    settings_menu.add.button('Restore original values', settings_menu.reset_value, align=pygame_menu.locals.ALIGN_LEFT)

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    main_menu_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font_size = 30

    # main_menu = pygame_menu.Menu(
    #     height=WINDOW_SIZE[1],
    #     onclose=pygame_menu.events.BACK,  # User press ESC button
    #     theme=main_menu_theme,
    #     title='Main menu',
    #     width=WINDOW_SIZE[0]
    #     )

    # main_menu.add.button('Settings', settings_menu)

    if settings_run:
        # Main menu
        settings_menu.mainloop(surface, None, disable_loop=test, fps_limit=FPS, clear_surface=False)
