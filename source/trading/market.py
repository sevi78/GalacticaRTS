import copy

from source.configuration.game_config import config
from source.gui.container.container_config import WIDGET_SIZE
from source.gui.container.container_widget_item import ContainerWidgetItem
from source.gui.container.container_widget_item_button import ContainerWidgetItemButton
from source.gui.event_text import event_text
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image, get_gif_frames, overblit_button_image
from source.trading.trade import Trade

button_size = WIDGET_SIZE * .7
OFFER_DEAL_PERCENT = 25
MAX_DEALS_PER_PLAYERS = 3
MAX_DEALS_PER_LIST = 25


class Market:
    def __init__(self) -> None:
        self.deals = []
        self.accepted_deals = []
        self.declined_deals = []
        self.last_deals = {}
        self.overblit_image = None

    def __repr__(self):
        return f"deals: {self.deals}\n, accepted_deals: {self.accepted_deals}\n, declined_deals: {self.declined_deals}"

    def get_deals_from_player(self, player) -> list:
        return [i for i in self.deals if i.owner_index == player.owner]

    def deals_per_player_limit_reached(self, deal: Trade):
        player = config.app.players[deal.owner_index]
        player_deals = self.get_deals_from_player(player)
        if len(player_deals) >= MAX_DEALS_PER_PLAYERS:
            event_text.set_text(f"Sorry {player.name}, you can't make anymore deals at the moment, you have reached the maximum({MAX_DEALS_PER_PLAYERS}) of deals!")
            return True
        return False

    def add_deal(self, trade: Trade) -> None:
        if self.deals_per_player_limit_reached(trade):
            return
        self.deals.append(trade)
        self.last_deals[trade.owner_index] = trade
        self.update_container_widget(trade)

    def update_container_widget(self, trade: Trade):
        widgets = self.convert_deals_into_container_widget_item()
        config.app.deal_container.set_widgets(widgets)

    def convert_deals_into_container_widget_item(self, sort_by=None, reverse=True, **kwargs) -> list:  # orig
        widgets = []

        if sort_by != None:
            self.deals = self.sort_trades(self.deals, sort_by)

        for index_, deal in enumerate(self.deals):
            """
            example::
            deal.request: {'food':10}
            deal.offer: {'water':10}
            """

            widgets.append(ContainerWidgetItem(
                    config.app.win,
                    0,
                    WIDGET_SIZE,
                    WIDGET_SIZE,
                    WIDGET_SIZE,
                    image=get_image(config.app.players[0].image_name),
                    obj=deal,
                    index=index_ + 1,
                    item_buttons=[
                        ContainerWidgetItemButton(
                                config.app.win,
                                0,
                                0,
                                button_size,
                                button_size,
                                "decline",
                                "thumps_upred_flipped.png",
                                container_name="deal_container",
                                function=lambda index__=index_: self.decline_deal(index__, 0)),
                        ContainerWidgetItemButton(
                                config.app.win,
                                0,
                                0,
                                button_size,
                                button_size,
                                "agree",
                                "thumps_up.png",
                                container_name="deal_container",
                                function=lambda index__=index_: self.accept_deal(index__, 0)),
                        ],
                    parent=None,
                    container_name="deal_container"))
        return widgets

    def sort_trades(self, trades: list[Trade], sort_by: str) -> list[Trade]:
        """
        Sort a list of Trade objects based on the specified sort_by key in the offer dictionary.

        Args:
            trades (List[Trade]): A list of Trade objects.
            sort_by (str): The key in the offer dictionary to sort by.

        Returns:
            List[Trade]: A sorted list of Trade objects.
        """
        sorted_trades = sorted(trades, key=lambda trade: trade.obj.offer.get(sort_by, 0), reverse=True)

        return sorted_trades

    def convert_deals_into_container_widget_item__(self, sort_by=None, reverse=True, **kwargs) -> list:
        widgets = []

        # Extract the first key from deal.offer or deal.request for sorting

        print(self.deals)
        sorted = self.sort_trades(self.deals, sort_by)

        def get_first_key(deal):
            return next(iter(deal.offer.keys()))

        # Sort the deals if sort_by is provided
        if sort_by is not None:
            self.deals = sorted(self.deals, key=lambda deal: get_first_key(deal), reverse=reverse)

        for index_, deal in enumerate(self.deals):
            """
            example::
            deal.request: {'food':10}
            deal.offer: {'water':10}
            """
            widgets.append(ContainerWidgetItem(
                    config.app.win,
                    0,
                    WIDGET_SIZE,
                    WIDGET_SIZE,
                    WIDGET_SIZE,
                    image=get_image(config.app.players[0].image_name),
                    obj=deal,
                    index=index_ + 1,
                    item_buttons=[
                        ContainerWidgetItemButton(
                                config.app.win,
                                0,
                                0,
                                button_size,
                                button_size,
                                "decline",
                                "thumps_upred_flipped.png",
                                container_name="deal_container",
                                function=lambda index__=index_: self.decline_deal(index__, 0)),
                        ContainerWidgetItemButton(
                                config.app.win,
                                0,
                                0,
                                button_size,
                                button_size,
                                "agree",
                                "thumps_up.png",
                                container_name="deal_container",
                                function=lambda index__=index_: self.accept_deal(index__, 0)),
                        ],
                    parent=None,
                    container_name="deal_container"))
        return widgets

    def convert_sprite_groups_to_container_widget_items_list(
            self, sprite_group_name, sort_by=None, reverse=True, **kwargs
            ) -> list:
        # If a sort_by attribute is provided, sort the sprite_group by that attribute
        sprite_group = getattr(sprite_groups, sprite_group_name)

        if config.show_human_player_only:
            sprite_group = [i for i in sprite_group if i.owner == 0]

        if sort_by is not None:
            sprite_group = sorted(sprite_group, key=lambda x: getattr(x, sort_by), reverse=reverse)

        item_buttons = kwargs.get("item_buttons", {})
        parent = kwargs.get("parent", None)
        return [ContainerWidgetItem(
                config.app.win,
                0,
                WIDGET_SIZE * index,
                WIDGET_SIZE,
                WIDGET_SIZE,
                image=get_image(_.image_name) if not _.image_name.endswith(".gif") else get_gif_frames(_.image_name)[0],
                obj=_,
                index=index + 1,
                item_buttons=item_buttons,
                parent=parent)
            for index, _ in enumerate(sprite_group)]

    def accept_deal(self, deal_index, buyer_index):
        self.transfer_resources(self.deals[deal_index], buyer_index)

    def decline_deal(self, deal_index, buyer_index):
        if deal_index < len(self.deals):
            trade = self.deals.pop(deal_index)
            self.declined_deals.append(trade)
            self.update_container_widget(trade)
        else:
            print("Invalid deal_index: out of range")

    def transfer_resources(self, deal: Trade, buyer_index) -> None:
        provider = config.app.players[deal.owner_index]
        provider_resource = list(deal.offer.keys())[0]
        provider_value = list(deal.offer.values())[0]
        buyer = config.app.players[buyer_index]
        buyer_resource = list(deal.request.keys())[0]
        buyer_value = list(deal.request.values())[0]
        buyer_resource_amount = getattr(buyer, buyer_resource, 0)
        remaining_resources = buyer_resource_amount - buyer_value

        if remaining_resources < 0:
            event_text.set_text(f"You don't have enough resources to make this deal! you are missing: {remaining_resources} of {buyer_resource}")
            return

        setattr(provider, provider_resource, getattr(provider, provider_resource) - provider_value)
        setattr(buyer, provider_resource, getattr(buyer, provider_resource) + provider_value)
        setattr(buyer, buyer_resource, buyer_resource_amount - buyer_value)
        setattr(provider, buyer_resource, getattr(provider, buyer_resource) + buyer_value)

        event_text.text = f"{provider.name} gave {provider_value} {provider_resource} to {buyer.name}, received {buyer_value} {buyer_resource} from {buyer.name}"

        trade = self.deals.pop(self.deals.index(deal))
        self.accepted_deals.append(trade)
        self.update_container_widget(trade)

    def get_fitting_deal(self, player) -> None:
        resource_stock = player.get_resource_stock()
        for i in self.deals:
            if i.owner_index != player.owner:
                deal_key = list(i.offer.keys())[0]
                if deal_key == player.auto_economy_handler.get_lowest_value_key(resource_stock):
                    self.accept_deal(self.deals.index(i), player.owner)

    def overblit_deal_icon(self) -> None:
        if not self.overblit_image:
            self.overblit_image = copy.copy(config.app.settings_panel.deal_manager_icon.image)
        if self.deals:
            overblit_button_image(config.app.settings_panel.deal_manager_icon, "warning.png", False)
        else:
            config.app.settings_panel.deal_manager_icon.image = self.overblit_image

    def update(self):
        widgets = config.app.deal_container.widgets
        for i in widgets:
            i.obj.update()
            if i.obj.remaining_time < 0.0:
                self.decline_deal(widgets.index(i), 0)
        self.overblit_deal_icon()


market = Market()
