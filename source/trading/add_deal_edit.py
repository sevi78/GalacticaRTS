from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.checkbox import Checkbox
from source.gui.widgets.selector import Selector
from source.multimedia_library.images import get_image, scale_image_cached
from source.trading.market import market
from source.trading.trade import Trade

ARROW_SIZE = 20
FONT_SIZE = int(ARROW_SIZE * .8)
SELECTOR_SPACING = 100
SELECTOR_GAP = 40


class AddDealEdit(EditorBase):
    """
    this is the interface to add deal to the deal_manager by the human player
    """

    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)

        #  widgets
        self.selectors_offer = []
        self.selectors_request = []
        self.checkboxes_offer = []
        self.checkboxes_request = []
        self.selectors = []
        self.widgets = []
        self.selector_offer_percent = None
        self.selector_request_percent = None

        # lists
        self.resources = ["minerals", "food", "water", "technology", "energy"]
        self.trader_resources = dict.fromkeys(self.resources, 0)
        self.player_resources = dict.fromkeys(self.resources, 0)
        self.value_list_offer = list(range(0, 1000, 10))
        self.value_list_request = list(range(0, 1000, 10))
        self.percent_list = list(range(1, 10, 1)) + list(range(10, 30, 5)) + list(range(30, 100, 10))

        # create widgets
        self.create_close_button()
        self.create_selectors()
        self.create_percent_selectors()

        self.create_buttons()
        self.create_technology_trade_widgets()

        # hide initially
        self.hide()

    def create_selectors(self) -> None:
        x = self.world_x + 30
        y = 130

        # offer
        for key, value in self.player_resources.items():
            setattr(self, f"selector_offer_{key}", Selector(
                    self.win, x + SELECTOR_SPACING + SELECTOR_GAP,
                              self.world_y + y,
                    ARROW_SIZE,
                    self.frame_color,
                    9,
                    SELECTOR_SPACING,
                    {"list_name": key + "_list", "list": self.value_list_offer},
                    self,
                    FONT_SIZE,
                    repeat_clicks=True))

            self.selectors_offer.append(getattr(self, f"selector_offer_{key}"))

            checkbox = Checkbox(
                    self.win,
                    x,
                    self.world_y + y,
                    30,
                    30,
                    is_sub_widget=False,
                    color=self.frame_color,
                    key=key,
                    tooltip=key,
                    on_click=lambda: print("OKOKOK"),
                    layer=9,
                    parent=self)
            checkbox.checked = False

            self.checkboxes.append(checkbox)
            self.checkboxes_offer.append(checkbox)
            self.widgets.append(checkbox)
            y += self.spacing_y

        x = self.world_x + self.world_width * 0.5
        y = 130

        # request
        for key, value in self.player_resources.items():
            setattr(self, f"selector_request_{key}", Selector(
                    self.win,
                    x + SELECTOR_SPACING + SELECTOR_GAP,
                    self.world_y + y,
                    ARROW_SIZE,
                    self.frame_color,
                    9,
                    SELECTOR_SPACING,
                    {"list_name": key + "_list", "list": self.value_list_request},
                    self, FONT_SIZE,
                    repeat_clicks=True))

            self.selectors_request.append(getattr(self, f"selector_request_{key}"))

            checkbox = Checkbox(
                    self.win,
                    x,
                    self.world_y + y,
                    30,
                    30,
                    is_sub_widget=False,
                    color=self.frame_color,
                    key=key,
                    tooltip=key,
                    on_click=lambda: print("OKOKOK"),
                    layer=9,
                    parent=self)
            checkbox.checked = False

            self.checkboxes.append(checkbox)
            self.checkboxes_request.append(checkbox)
            self.widgets.append(checkbox)
            y += self.spacing_y

        self.max_height = y

        # initialize checkbox selection
        self.checkboxes_offer[0].checked = True
        self.checkboxes_request[1].checked = True

        # initialize selector values
        for i in self.selectors_offer:
            i.current_value = 100

        for i in self.selectors_request:
            i.current_value = 100

    def create_percent_selectors(self) -> None:
        x = self.world_x + 30

        self.selector_offer_percent = Selector(
                self.win,
                x + SELECTOR_SPACING + SELECTOR_GAP,
                self.max_height + SELECTOR_GAP,
                ARROW_SIZE,
                self.frame_color,
                9,
                SELECTOR_SPACING,
                {"list_name": "% offer_list", "list": self.percent_list},
                self,
                FONT_SIZE,
                repeat_clicks=False,
                restrict_list_jump=True)
        self.selector_offer_percent.current_value = 20

        x = self.world_x + self.world_width * 0.5
        self.selector_request_percent = Selector(
                self.win,
                x + SELECTOR_SPACING + SELECTOR_GAP,
                self.max_height + SELECTOR_GAP,
                ARROW_SIZE,
                self.frame_color,
                9,
                SELECTOR_SPACING,
                {"list_name": "% request_list", "list": self.percent_list},
                self,
                FONT_SIZE,
                repeat_clicks=False,
                restrict_list_jump=True)
        self.selector_request_percent.current_value = 15

    def create_technology_trade_widgets(self):
        x = self.world_x + 30
        y = self.max_height

        # technology checkbox
        self.selector_offer_technology_to_bank = Selector(
                self.win,
                x + SELECTOR_SPACING + SELECTOR_GAP,
                self.world_y + y,
                ARROW_SIZE,
                self.frame_color,
                9,
                SELECTOR_SPACING,
                {"list_name": "technology_list", "list": self.value_list_offer},
                self,
                FONT_SIZE,
                repeat_clicks=True)

        # self.selectors_offer.append(getattr(self,"selector_offer_technology1"))

        checkbox = Checkbox(
                self.win, x, self.world_y + y, 30, 30, is_sub_widget=False,
                color=self.frame_color,
                key="technology", tooltip="technology", on_click=lambda: print("OKOKOK"), layer=9, parent=self)
        checkbox.checked = True

        self.checkboxes.append(checkbox)
        # self.checkboxes_offer.append(checkbox)
        self.widgets.append(checkbox)

        # button
        button_size = 32
        self.agree_button1 = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 2,
                y=self.world_y + y,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("2to1.png"), (button_size, button_size)),
                tooltip="trade technology for 2/1 with the bank!",
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                on_click=lambda: self.agree_bank_deal(),
                name="agree_button1"
                )

        self.agree_button1.hide()

        self.buttons.append(self.agree_button1)
        self.widgets.append(self.agree_button1)

        y += self.spacing_y

    def create_buttons(self) -> None:
        button_size = 32
        agree_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 2,
                y=self.max_height + button_size,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("thumps_up.png"), (button_size, button_size)),
                tooltip="agree!",
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                on_click=lambda: self.agree(),
                name="agree_button"
                )

        agree_button.hide()

        self.buttons.append(agree_button)
        self.widgets.append(agree_button)

        # calculate_button
        calculate_button = ImageButton(win=self.win,
                x=self.get_screen_x() + button_size,
                y=self.max_height + button_size,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("brain.png"), (button_size, button_size)),
                tooltip="calculate deal!",
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                on_click=lambda: self.calculate_deal(),
                name="calculate_button"
                )

        calculate_button.hide()

        self.buttons.append(calculate_button)
        self.widgets.append(calculate_button)

        self.max_height += button_size * 3

    def get_checkbox_values(self, **kwargs) -> None:
        """ called from the checkbox on click """
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

        # set_technology_bank_deal
        request_key = [i.key for i in self.checkboxes_request if i.checked][0]
        offer_value = self.selector_offer_technology_to_bank.current_value
        request_value = int(offer_value / 2)
        self.set_technology_bank_deal(offer_value, request_key, request_value)

    def set_checkboxes_from_deal(self, deal: dict) -> None:
        for i in self.checkboxes_offer:
            if i.key in deal["offer"]:
                i.checked = True
                i.current_value = deal["offer"][i.key]
            else:
                i.checked = False

        for i in self.checkboxes_request:
            if i.key in deal["request"]:
                i.checked = True
                i.current_value = deal["request"][i.key]
            else:
                i.checked = False

    def set_selectors_from_deal(self, deal: dict) -> None:
        offer_value = deal["offer"][list(deal["offer"].keys())[0]]
        request_resource = list(deal["request"].keys())[0]
        request_value = int(offer_value / 2)
        self.set_technology_bank_deal(offer_value, request_resource, request_value)

        for i in self.selectors_offer:
            if i.key in deal["offer"]:
                i.current_value = deal["offer"][i.key]

        for i in self.selectors_request:
            if i.key in deal["request"]:
                i.current_value = deal["request"][i.key]

    def set_technology_bank_deal(self, offer_value, request_resource, request_value) -> None:
        self.selector_offer_technology_to_bank.current_value = offer_value
        self.agree_button1.tooltip = f"trade technology for 2/1 with the bank! you will get {request_value} of {request_resource} for {offer_value} of technology"

    def selector_callback(self, key, value, selector) -> None:
        pass

    def create_deal(self) -> None:
        # get the keys and values for the deal
        offer_key = [i.key for i in self.checkboxes_offer if i.checked][0]
        request_key = [i.key for i in self.checkboxes_request if i.checked][0]
        offer_value = [i.current_value for i in self.selectors_offer if i.key == offer_key][0]
        request_value = [i.current_value for i in self.selectors_request if i.key == request_key][0]

        # create offer and request
        offer = {offer_key: offer_value}
        request = {request_key: request_value}

        market.add_deal(Trade(config.app.game_client.id, offer, request), from_server=False)

    def agree(self) -> None:
        self.create_deal()

    def agree_bank_deal(self) -> None:
        """
        accepts the technology bank deal
        """

        request_key = [i.key for i in self.checkboxes_request if i.checked][0]
        offer_value = self.selector_offer_technology_to_bank.current_value
        request_value = int(offer_value / 2)
        trade_assistant = config.app.players[config.player].trade_assistant
        player_index = config.player

        # call the trade_technology_to_the_bank function from the assistant
        trade_assistant.trade_technology_to_the_bank(offer_value, request_key, request_value, player_index)

    def listen(self, events) -> None:
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self) -> None:
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Offer:")
            self.draw_text(self.world_x + self.world_width * 0.5, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Request:")

    def calculate_deal(self) -> None:
        """ calculates a deal based on the current offer and request values """
        trade_assistant = config.app.players[config.player].trade_assistant
        percentage_offer = self.selector_offer_percent.current_value
        percentage_request = self.selector_request_percent.current_value
        deal = trade_assistant.generate_deal_based_resource_maximum_and_minimum(percentage_offer, percentage_request)

        # set deal values
        if deal:
            self.set_checkboxes_from_deal(deal)
            self.set_selectors_from_deal(deal)
