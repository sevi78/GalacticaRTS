import copy

from source.configuration.game_config import config
from source.editors.deal_select import DealSelect
from source.editors.editor_base.editor_base import EditorBase
from source.handlers.image_handler import overblit_button_image

OFFER_DEAL_PERCENT = 25
MAX_DEALS_PER_PLAYERS = 3


class DealManager(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        #  widgets
        self.overblit_image = None
        self.widgets = []
        self.deals = []

        # hide initially
        self.hide()

    def set_deal(self, deal):
        deal.world_x = self.world_x
        self.deals.append(deal)
        self.widgets.append(deal)
        self.reposition_deals()

    def get_deals(self):
        return self.deals

    def get_deals_from_player(self, player):
        player_deals = []
        for i in self.deals:
            if i.provider_index == player.owner:
                player_deals.append(i)

        return player_deals

    def add_fitting_deal(self, player, lowest_value_key, highest_value_key):
        # limit deals per player
        player_deals = self.get_deals_from_player(player)
        deal_amount = len(player_deals)
        if deal_amount > MAX_DEALS_PER_PLAYERS:
            return
        # calculate the value to offer, this case 25 percent
        offer_value = int(player.get_stock()[highest_value_key] / 100 * OFFER_DEAL_PERCENT)

        offer = {highest_value_key: offer_value}
        request = {lowest_value_key: offer_value}

        self.set_deal(DealSelect(
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
            player_index=player.owner,
            save=False))

    def get_fitting_deal(self, player):
        # pprint (f"self.player.index:{self.player.owner}, {self.player.name}")
        # get all deals
        deals = config.app.deal_manager.get_deals()
        resource_stock = player.get_resource_stock()

        for i in deals:
            # ensure that player cant buy its own deals
            if not i.provider_index == player.owner:
                # compare keys, get fitting deal
                deal_key = list(i.offer.keys())[0]
                if deal_key == player.auto_economy_handler.get_lowest_value_key(resource_stock):
                    # print(f"{player.name} is buying {deal_key}")
                    i.agree(player.owner)

    def overblit_deal_icon(self):
        # store the image for overblitting
        if not self.overblit_image:
            self.overblit_image = copy.copy(config.app.resource_panel.deal_manager_icon.image)

        # check if there are any deals
        if len(self.deals) > 0:
            overblit_button_image(config.app.resource_panel.deal_manager_icon, "warning.png", False)
        else:
            # reset the image
            config.app.resource_panel.deal_manager_icon.image = self.overblit_image

    def reposition_deals(self):
        for i in self.deals:
            i._hidden = self._hidden
            i.screen_width = self.rect.width
            i.screen_x = self.world_x
            i.world_y = self.world_y + i.world_height / 2 * self.deals.index(i)

        self.max_height = len(self.deals) * 30

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.drag(events)

    def draw(self):
        self.overblit_deal_icon()
        if not self._hidden and not self._disabled:
            self.reposition_deals()
