import pygame

from source.configuration.game_config import config
from source.editors.deal_select import DealSelect
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.checkbox import Checkbox
from source.gui.widgets.selector import Selector
from source.multimedia_library.images import get_image


class AddDealEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        #  widgets
        self.selectors_offer = []
        self.selectors_request = []
        self.checkboxes_offer = []
        self.checkboxes_request = []
        self.selectors = []
        self.widgets = []

        # lists
        self.resources = ["minerals", "food", "water", "technology", "energy"]
        self.trader_resources = dict.fromkeys(self.resources, 0)
        self.player_resources = dict.fromkeys(self.resources, 0)
        self.value_list_offer = list(range(0, 1000, 10))
        self.value_list_request = list(range(0, 1000, 10))

        # create widgets
        self.create_close_button()
        self.create_selectors()
        self.create_buttons()

        # hide initially
        self.hide()

    def create_selectors(self):
        x = self.world_x + 30
        y = 130
        selector_spacing = 100
        selector_gap = 40

        # offer
        for key, value in self.player_resources.items():
            setattr(self, f"selector_offer_{key}", Selector(self.win, x + selector_spacing + selector_gap, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
                selector_spacing, {"list_name": key + "_list", "list": self.value_list_offer}, self, FONT_SIZE, repeat_clicks=True))

            self.selectors_offer.append(getattr(self, f"selector_offer_{key}"))

            checkbox = Checkbox(
                self.win, x, self.world_y + y, 30, 30, isSubWidget=False,
                color=self.frame_color,
                key=key, tooltip=key, onClick=lambda: print("OKOKOK"), layer=9, parent=self)
            checkbox.checked = False

            self.checkboxes.append(checkbox)
            self.checkboxes_offer.append(checkbox)
            self.widgets.append(checkbox)
            y += self.spacing_y

        x = self.world_x + self.world_width * 0.5
        y = 130

        # request
        for key, value in self.player_resources.items():
            setattr(self, f"selector_request_{key}", Selector(self.win, x + selector_spacing + selector_gap, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
                selector_spacing, {"list_name": key + "_list", "list": self.value_list_request}, self, FONT_SIZE, repeat_clicks=True))

            self.selectors_request.append(getattr(self, f"selector_request_{key}"))

            checkbox = Checkbox(
                self.win, x, self.world_y + y, 30, 30, isSubWidget=False,
                color=self.frame_color,
                key=key, tooltip=key, onClick=lambda: print("OKOKOK"), layer=9, parent=self)
            checkbox.checked = False

            self.checkboxes.append(checkbox)
            self.checkboxes_request.append(checkbox)
            self.widgets.append(checkbox)
            y += self.spacing_y

        self.max_height = y

        # initialize checkbox selection
        self.checkboxes_offer[0].checked = True
        self.checkboxes_request[1].checked = True

        # initialize selectro values
        for i in self.selectors_offer:
            i.current_value = 100

        for i in self.selectors_request:
            i.current_value = 100

    def create_buttons(self):
        button_size = 32
        agree_button = ImageButton(win=self.win,
            x=self.get_screen_x() + self.get_screen_width() / 2 - button_size / 2,
            y=self.max_height + button_size,
            width=button_size,
            height=button_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("thumps_up.png"), (button_size, button_size)),
            tooltip="agree!",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=self.layer,
            onClick=lambda: self.agree(),
            name="agree_button"
            )

        agree_button.hide()

        self.buttons.append(agree_button)
        self.widgets.append(agree_button)

        self.max_height += button_size

    def get_checkbox_values(self, **kwargs):
        checkbox = kwargs.get("checkbox", None)
        value = kwargs.get("value", None)

        # ensure that only a single checkbox can be checked and always a checkbox is checked
        if checkbox:
            if checkbox in self.checkboxes_offer:
                for i in self.checkboxes_offer:
                    if not i == checkbox:
                        i.checked = False
                    elif not i.checked:
                        i.checked = True

            if checkbox in self.checkboxes_request:
                for i in self.checkboxes_request:
                    if not i == checkbox:
                        i.checked = False
                    elif not i.checked:
                        i.checked = True

    def selector_callback(self, key, value, selector):
        pass

    def create_deal(self):
        # get the keys and values for the deal
        offer_key = [i.key for i in self.checkboxes_offer if i.checked][0]
        request_key = [i.key for i in self.checkboxes_request if i.checked][0]
        offer_value = [i.current_value for i in self.selectors_offer if i.key == offer_key][0]
        request_value = [i.current_value for i in self.selectors_request if i.key == request_key][0]

        # create offer and request
        offer = {offer_key: offer_value}
        request = {request_key: request_value}

        # create deal
        config.app.deal_manager.set_deal(DealSelect(
            config.app.win,
            0,
            30,
            300,
            60,
            False,
            offer=offer,
            request=request,
            layer=9,
            parent=config.app,
            player_index=config.player,
            save=False))

    def agree(self):
        self.create_deal()

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Offer:")
            self.draw_text(self.world_x + self.world_width * 0.5, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Request:")
