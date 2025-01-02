import copy

import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.factories.building_factory import building_factory
from source.weapons.weapon_factory import weapon_factory
from source.gui.event_text import event_text
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.checkbox import Checkbox
from source.multimedia_library.images import get_image, scale_image_cached

OBJECT_FONT_SIZE = 40
BUTTON_SIZE = 60
BUTTON_FONT_SIZE = 20
INFO_FONT_SIZE = 16
CHECKBOX_SIZE = 25


# class WeaponSelectHandler:
#     def __init__(self):
#         self.max_weapons_upgrade_level = 2
#
#     def upgrade(self):
#         if self.current_weapon["level"] < self.max_weapons_upgrade_level:
#             prices = building_factory.get_prices_from_weapons_dict(
#                     self.current_weapon["name"], self.current_weapon["level"])
#             building_factory.build(self.current_weapon["name"], self.obj, prices=prices)
#             self.update_obj()
#         else:
#             event_text.set_text(f"maximum upgrade level of {self.max_weapons_upgrade_level} reached !!!", sender=config.app.game_client.id)


class WeaponSelect_(EditorBase):  # original, upgrade issues
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)

        self.max_weapons_upgrade_level = 2
        self.current_weapon_icon = None
        self.all_weapons = copy.deepcopy(weapon_factory.get_all_weapons())

        # lists
        self.current_weapon = copy.deepcopy(self.all_weapons["laser"])
        self.current_weapon_selection = "laser"

        #  widgets
        self.auto_pilot_checkbox = None

        self.widgets = []

        # create widgets
        self.create_close_button()

        self.max_height = height
        self.image_zoom = 3

        self.create_buttons()

        # hide initially
        self.hide()

    def create_buttons(self):
        x = 0
        y = 0
        for key in self.all_weapons.keys():
            button_size = BUTTON_SIZE
            icon = ImageButton(win=self.win,
                    x=self.get_screen_x() + x + TOP_SPACING,
                    y=self.get_screen_y() + y + TOP_SPACING * 3,
                    width=button_size,
                    height=button_size,
                    is_sub_widget=False,
                    parent=self,
                    image=scale_image_cached(get_image(f"{key}.png"), (button_size, button_size)),
                    tooltip=key,
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    on_click=lambda weapon_=key: self.select_weapon(weapon_),
                    name=key,
                    text=key + " ",  # dirty hack to ensure its not building something
                    text_color=self.frame_color,
                    font_size=BUTTON_FONT_SIZE,
                    info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                    text_h_align="right_outside",
                    outline_thickness=0,
                    outline_threshold=1
                    )

            self.buttons.append(icon)
            self.widgets.append(icon)
            y += button_size

        self.current_weapon_icon = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 3 - button_size / 2,
                y=self.get_screen_y() + y + TOP_SPACING * 4,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image(f"{self.current_weapon['name']}.png"), (
                    button_size, button_size)),
                tooltip=key,
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                on_click=lambda: print("current weapon"),
                name=key + ":",
                text="current weapon:",
                text_color=self.frame_color,
                font_size=BUTTON_FONT_SIZE,
                info_text="not set yet",
                text_v_align="over_the_top",
                text_h_align="left",
                )
        self.current_weapon_icon.disable()
        self.buttons.append(self.current_weapon_icon)
        self.widgets.append(self.current_weapon_icon)
        y += button_size

        button_size = BUTTON_SIZE
        self.upgrade_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 2 - button_size / 2,
                y=self.get_screen_y() + y + TOP_SPACING * 5,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.rotate(scale_image_cached(get_image(f"arrow-left.png"), (
                    button_size, button_size)), -90),
                tooltip="upgrade",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                on_click=lambda: self.upgrade(),
                name="upgrade_button",
                text="upgrade",
                text_color=self.frame_color,
                font_size=BUTTON_FONT_SIZE,
                info_text="",
                text_v_align="below_the_bottom"
                )

        self.buttons.append(self.upgrade_button)
        self.widgets.append(self.upgrade_button)

        self.auto_pilot_checkbox = Checkbox(
                self.win,
                self.upgrade_button.get_screen_x() + button_size * 3,
                self.upgrade_button.get_screen_y(),
                CHECKBOX_SIZE,
                CHECKBOX_SIZE,
                is_sub_widget=False,
                color=self.frame_color,
                key="auto_pilot",
                image_name="autopilot.png",
                tooltip="auto_pilot",
                on_click=lambda: print("OKOKOK"),
                layer=9,
                parent=self,
                button_size=CHECKBOX_SIZE,
                text="auto pilot",
                text_h_align="left_outside",
                text_color=self.frame_color)
        self.auto_pilot_checkbox.checked = False
        self.checkboxes.append(self.auto_pilot_checkbox)
        self.widgets.append(self.auto_pilot_checkbox)

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, value):

        self._obj = value
        if self._obj:
            self.current_weapon_selection = self._obj.weapon_handler.current_weapon["name"]
            self.update_obj()
            self.update()

    def update_obj(self):
        self.obj.weapon_handler.current_weapon_select = self.current_weapon_selection

        # if obj has selected weapon already, upgrade it
        if self.obj.weapon_handler.current_weapon_select in self.obj.weapon_handler.weapons.keys():
            self.obj.weapon_handler.current_weapon = copy.deepcopy(
                    self.obj.weapon_handler.weapons[self.obj.weapon_handler.current_weapon_select])
            self.current_weapon = copy.deepcopy(self.all_weapons[self.current_weapon_selection])
            self.current_weapon["level"] = copy.deepcopy(
                    self.obj.weapon_handler.weapons[self.obj.weapon_handler.current_weapon_select]["level"])
            self.upgrade_button.set_text("upgrade")
            self.upgrade_button.tooltip = "upgrade"
        else:
            self.obj.weapon_handler.current_weapon = copy.deepcopy(self.all_weapons[self.current_weapon_selection])
            self.current_weapon = copy.deepcopy(self.all_weapons[self.current_weapon_selection])
            self.upgrade_button.set_text("buy")
            self.upgrade_button.tooltip = "buy"
        self.update()

    def select_weapon(self, weapon_name):
        self.current_weapon_selection = weapon_name
        self.update()
        self.update_obj()

    def upgrade(self):  # has some issues with building cue
        # already in building cue
        in_progress = len([_ for _ in config.app.building_widget_list if
                           _.receiver == self.obj and _.name == self.current_weapon["name"]])
        # print ("in_progress:", in_progress)

        # we need to add in progress to the upgrade level to make shure we don't exceed the max level
        if self.current_weapon["level"] <= self.max_weapons_upgrade_level - in_progress:
            prices = building_factory.get_prices_from_weapons_dict(
                    self.current_weapon["name"], self.current_weapon["level"])

            building_factory.build(self.current_weapon["name"], self.obj, prices=prices)
            self.update_obj()
        else:
            event_text.set_text(f"maximum upgrade level of {self.max_weapons_upgrade_level} reached !!!", sender=config.app.game_client.id)

    def update(self):
        size = self.obj.image_raw.get_size()
        self.image = scale_image_cached(self.obj.image_raw, (
            size[0] * self.image_zoom, size[1] * self.image_zoom))

        self.current_weapon_icon.set_text(f"current weapon: {self.current_weapon_selection}")
        self.current_weapon_icon.tooltip = f"{self.current_weapon_selection}:"
        self.current_weapon_icon.set_image(get_image(f"{self.current_weapon_selection}.png"))

    def draw_image(self):
        self.win.blit(self.image, (
            (self.world_x + self.world_width / 2) - self.image.get_width() / 2, self.world_y + self.world_height / 4))

    def draw_weapon_info(self):
        if not self.current_weapon:
            return
        c = 0
        for key, value in self.current_weapon["upgrade values"][f"level_{self.current_weapon['level']}"].items():
            self.draw_text(self.current_weapon_icon.screen_x + self.current_weapon_icon.screen_width + self.text_spacing,
                           self.current_weapon_icon.screen_y + self.text_spacing * c, 200, INFO_FONT_SIZE, f"{key}: {value}")
            c += 1

    def draw_weapon_prices(self):
        c = 0
        level = self.current_weapon['level']
        already_bought = False
        price_text = "prices "
        x = self.world_x + self.screen_width - self.screen_width / 3.3
        y = self.world_y + TOP_SPACING + self.text_spacing * 4

        if level == 0 and not self.current_weapon["name"] in self.obj.weapon_handler.weapons.keys():
            price_text += "to buy:"
        else:
            price_text += f"for upgrade to level {level + 1}:"
            already_bought = True

        if level + 1 > self.max_weapons_upgrade_level:
            price_text = f"maximum level {level} reached!"

        self.draw_text(x, y, 200, INFO_FONT_SIZE, price_text)

        if not price_text.startswith("maximum"):
            for key, value in self.current_weapon["upgrade cost"][f"level_{self.current_weapon['level']}"].items():
                self.draw_text(x, y + 40 + self.text_spacing * (
                    c), 200, INFO_FONT_SIZE, f"{key.split('price_')[1]}: {value}")
                c += 1
            c += 2
            if already_bought:
                self.draw_text(x, y + 40 + self.text_spacing * (
                    c), 200, INFO_FONT_SIZE, "next level values:")
                c += 2
                for key, value in self.current_weapon["upgrade values"][
                    f"level_{self.current_weapon['level'] + 1}"].items():
                    self.draw_text(x, y + 40 + self.text_spacing * (
                        c), 200, INFO_FONT_SIZE, f"{key}: {value}")
                    c += 1

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.update_obj()
            self.update()
            self.draw_image()
            self.draw_frame()

            if self.obj:
                # draw ship name
                text = f"{self.obj.name}({self.obj.id}):"
                x = (self.world_x + self.world_width / 2) - self.image.get_width() / 2
                y = self.world_y + TOP_SPACING + self.text_spacing * 2
                self.draw_text(x, y, 200, OBJECT_FONT_SIZE, text)

                # draw title
                self.draw_text(self.world_x + self.text_spacing * 3, self.world_y + TOP_SPACING + self.text_spacing * 4, 200, BUTTON_FONT_SIZE, f"weapons:")

                self.draw_weapon_info()
                self.draw_weapon_prices()


class WeaponSelect(EditorBase):  # upgrade fixed
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)

        self.max_weapons_upgrade_level = 2
        self.current_weapon_icon = None
        self.all_weapons = copy.deepcopy(weapon_factory.get_all_weapons())

        # lists
        self.current_weapon = copy.deepcopy(self.all_weapons["laser"])
        self.current_weapon_selection = "laser"

        #  widgets
        self.auto_pilot_checkbox = None

        self.widgets = []

        # create widgets
        self.create_close_button()

        self.max_height = height
        self.image_zoom = 3

        self.create_buttons()

        # hide initially
        self.hide()

    def create_buttons(self):
        x = 0
        y = 0
        for key in self.all_weapons.keys():
            button_size = BUTTON_SIZE
            icon = ImageButton(win=self.win,
                    x=self.get_screen_x() + x + TOP_SPACING,
                    y=self.get_screen_y() + y + TOP_SPACING * 3,
                    width=button_size,
                    height=button_size,
                    is_sub_widget=False,
                    parent=self,
                    image=scale_image_cached(get_image(f"{key}.png"), (button_size, button_size)),
                    tooltip=key,
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    on_click=lambda weapon_=key: self.select_weapon(weapon_),
                    name=key,
                    text=key + " ",  # dirty hack to ensure its not building something
                    text_color=self.frame_color,
                    font_size=BUTTON_FONT_SIZE,
                    info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                    text_h_align="right_outside",
                    outline_thickness=0,
                    outline_threshold=1
                    )

            self.buttons.append(icon)
            self.widgets.append(icon)
            y += button_size

        self.current_weapon_icon = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 3 - button_size / 2,
                y=self.get_screen_y() + y + TOP_SPACING * 4,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image(f"{self.current_weapon['name']}.png"), (
                    button_size, button_size)),
                tooltip=key,
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                on_click=lambda: print("current weapon"),
                name=key + ":",
                text="current weapon:",
                text_color=self.frame_color,
                font_size=BUTTON_FONT_SIZE,
                info_text="not set yet",
                text_v_align="over_the_top",
                text_h_align="left",
                )
        self.current_weapon_icon.disable()
        self.buttons.append(self.current_weapon_icon)
        self.widgets.append(self.current_weapon_icon)
        y += button_size

        button_size = BUTTON_SIZE
        self.upgrade_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 2 - button_size / 2,
                y=self.get_screen_y() + y + TOP_SPACING * 5,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.rotate(scale_image_cached(get_image(f"arrow-left.png"), (
                    button_size, button_size)), -90),
                tooltip="upgrade",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                on_click=lambda: self.upgrade(),
                name="upgrade_button",
                text="upgrade",
                text_color=self.frame_color,
                font_size=BUTTON_FONT_SIZE,
                info_text="",
                text_v_align="below_the_bottom"
                )

        self.buttons.append(self.upgrade_button)
        self.widgets.append(self.upgrade_button)

        self.auto_pilot_checkbox = Checkbox(
                self.win,
                self.upgrade_button.get_screen_x() + button_size * 3,
                self.upgrade_button.get_screen_y(),
                CHECKBOX_SIZE,
                CHECKBOX_SIZE,
                is_sub_widget=False,
                color=self.frame_color,
                key="auto_pilot",
                image_name="autopilot.png",
                tooltip="auto_pilot",
                on_click=lambda: print("OKOKOK"),
                layer=9,
                parent=self,
                button_size=CHECKBOX_SIZE,
                text="auto pilot",
                text_h_align="left_outside",
                text_color=self.frame_color)
        self.auto_pilot_checkbox.checked = False
        self.checkboxes.append(self.auto_pilot_checkbox)
        self.widgets.append(self.auto_pilot_checkbox)

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, value):

        self._obj = value
        if self._obj:
            self.current_weapon_selection = self._obj.weapon_handler.current_weapon["name"]
            self.update_obj()
            self.update()

    def update_obj(self):
        # action = the string that will be printed in the upgrade button: either 'buy' or 'upgrade'
        action = self.obj.weapon_handler.update_weapon_state(self.current_weapon_selection)
        self.current_weapon = copy.deepcopy(self.obj.weapon_handler.current_weapon)
        self.upgrade_button.set_text(action)
        self.upgrade_button.tooltip = action
        self.update()

    def select_weapon(self, weapon_name):
        self.current_weapon_selection = weapon_name
        self.update()
        self.update_obj()

    def upgrade(self):
        self.obj.weapon_handler.upgrade_weapon()
        self.update_obj()

    def update(self):
        size = self.obj.image_raw.get_size()
        self.image = scale_image_cached(self.obj.image_raw, (
            size[0] * self.image_zoom, size[1] * self.image_zoom))

        self.current_weapon_icon.set_text(f"current weapon: {self.current_weapon_selection}")
        self.current_weapon_icon.tooltip = f"{self.current_weapon_selection}:"
        self.current_weapon_icon.set_image(get_image(f"{self.current_weapon_selection}.png"))

    def draw_image(self):
        self.win.blit(self.image, (
            (self.world_x + self.world_width / 2) - self.image.get_width() / 2, self.world_y + self.world_height / 4))

    def draw_weapon_info(self):
        if not self.current_weapon:
            return
        c = 0
        for key, value in self.current_weapon["upgrade values"][f"level_{self.current_weapon['level']}"].items():
            self.draw_text(self.current_weapon_icon.screen_x + self.current_weapon_icon.screen_width + self.text_spacing,
                           self.current_weapon_icon.screen_y + self.text_spacing * c, 200, INFO_FONT_SIZE, f"{key}: {value}")
            c += 1

    def draw_weapon_prices(self):
        c = 0
        level = self.current_weapon['level']
        already_bought = False
        price_text = "prices "
        x = self.world_x + self.screen_width - self.screen_width / 3.3
        y = self.world_y + TOP_SPACING + self.text_spacing * 4

        if level == 0 and not self.current_weapon["name"] in self.obj.weapon_handler.weapons.keys():
            price_text += "to buy:"
        else:
            price_text += f"for upgrade to level {level + 1}:"
            already_bought = True

        if level + 1 > self.max_weapons_upgrade_level:
            price_text = f"maximum level {level} reached!"

        self.draw_text(x, y, 200, INFO_FONT_SIZE, price_text)

        if not price_text.startswith("maximum"):
            for key, value in self.current_weapon["upgrade cost"][f"level_{self.current_weapon['level']}"].items():
                self.draw_text(x, y + 40 + self.text_spacing * (
                    c), 200, INFO_FONT_SIZE, f"{key.split('price_')[1]}: {value}")
                c += 1
            c += 2
            if already_bought:
                self.draw_text(x, y + 40 + self.text_spacing * (
                    c), 200, INFO_FONT_SIZE, "next level values:")
                c += 2
                for key, value in self.current_weapon["upgrade values"][
                    f"level_{self.current_weapon['level'] + 1}"].items():
                    self.draw_text(x, y + 40 + self.text_spacing * (
                        c), 200, INFO_FONT_SIZE, f"{key}: {value}")
                    c += 1

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.update_obj()
            self.update()
            self.draw_image()
            self.draw_frame()

            if self.obj:
                # draw ship name
                text = f"{self.obj.name}({self.obj.id}):"
                x = (self.world_x + self.world_width / 2) - self.image.get_width() / 2
                y = self.world_y + TOP_SPACING + self.text_spacing * 2
                self.draw_text(x, y, 200, OBJECT_FONT_SIZE, text)

                # draw title
                self.draw_text(self.world_x + self.text_spacing * 3, self.world_y + TOP_SPACING + self.text_spacing * 4, 200, BUTTON_FONT_SIZE, f"weapons:")

                self.draw_weapon_info()
                self.draw_weapon_prices()
