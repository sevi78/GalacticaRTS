import copy

import pygame

from source.configuration.game_config import config
from source.gui.container.container_config import WIDGET_SIZE
from source.gui.container.container_widget_item import ContainerWidgetItem
from source.gui.container.container_widget_item_button import ContainerWidgetItemButton
from source.gui.event_text import event_text
from source.gui.widgets.moving_image import MovingImage
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image, overblit_button_image
from source.trading.market_data import market_data
from source.trading.trade import Trade

button_size = WIDGET_SIZE * .7
OFFER_DEAL_PERCENT = 25
MAX_DEALS_PER_PLAYERS = 3
MAX_DEALS_PER_LIST = 25


class Market:  # server
    def __init__(self) -> None:
        self.overblit_image = None

    def __repr__(self):
        return f"deals: {self.deals}\n, accepted_deals: {self.accepted_deals}\n, declined_deals: {self.declined_deals}"

    def get_deals_from_player(self, player) -> list:
        return [i for i in market_data.deals if i.owner_index == player.owner]

    def deals_per_player_limit_reached(self, deal: Trade):
        player = config.app.players[deal.owner_index]
        player_deals = self.get_deals_from_player(player)
        if len(player_deals) >= MAX_DEALS_PER_PLAYERS:
            event_text.set_text(f"Sorry {player.name}, you can't make anymore deals at the moment, you have reached the maximum({MAX_DEALS_PER_PLAYERS}) of deals!", sender=deal.owner_index)
            return True
        return False

    def update_container_widget(self, trade: Trade):
        widgets = self.convert_deals_into_container_widget_item()
        config.app.deal_container.set_widgets(widgets)

    def convert_deals_into_container_widget_item(self, sort_by=None, reverse=True, **kwargs) -> list:
        widgets = []

        if sort_by != None:
            market_data.deals = self.sort_trades(market_data.deals, sort_by)

        for index_, deal in enumerate(market_data.deals):
            """
            example::
            deal.request: {'food':10}
            deal.offer: {'water':10}
            """

            item_buttons = [
                ContainerWidgetItemButton(
                        config.app.win,
                        0,
                        0,
                        button_size,
                        button_size,
                        "decline",
                        "thumps_upred_flipped.png",
                        container_name="deal_container",
                        function=lambda index__=index_: self.decline_deal(index__)),
                ]

            if deal.owner_index != config.app.game_client.id:  # Check if the deal belongs to the current player
                item_buttons.append(
                        ContainerWidgetItemButton(
                                config.app.win,
                                0,
                                0,
                                button_size,
                                button_size,
                                "agree",
                                "thumps_up.png",
                                container_name="deal_container",
                                function=lambda index__=index_: self.accept_deal(index__, config.app.game_client.id)),
                        )

            widgets.append(ContainerWidgetItem(
                    config.app.win,
                    0,
                    WIDGET_SIZE,
                    WIDGET_SIZE,
                    WIDGET_SIZE,
                    image=get_image(config.app.players[0].image_name),
                    obj=deal,
                    index=index_ + 1,
                    item_buttons=item_buttons,
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

    def get_fitting_deal(self, player) -> None:
        resource_stock = player.get_resource_stock()
        for i in market_data.deals:
            if i.owner_index != player.owner:
                deal_key = list(i.offer.keys())[0]
                if deal_key == player.auto_economy_handler.get_lowest_value_key(resource_stock):
                    self.accept_deal(market_data.deals.index(i), player.owner)

    def overblit_deal_icon(self) -> None:
        if not self.overblit_image:
            self.overblit_image = copy.copy(config.app.settings_panel.deal_manager_icon.image)
        if market_data.deals:
            overblit_button_image(config.app.settings_panel.deal_manager_icon, "warning.png", False)
        else:
            config.app.settings_panel.deal_manager_icon.image = self.overblit_image

    def transfer_resources(self, deal: Trade, buyer_index) -> None:
        """
            Execute a resource transfer between two players based on a trade deal.

            Args:
                deal (Trade): The trade deal containing offer and request details.
                buyer_index (int): The index of the buyer in the players list.

            Side effects:
                - Updates player inventories
                - Displays transaction messages
                - Updates market data
                - Shows resource transfer animations
        """
        # get the provider and buyer
        provider = config.app.players[deal.owner_index]
        provider_resource = list(deal.offer.keys())[0]
        provider_value = list(deal.offer.values())[0]
        buyer = config.app.players[buyer_index]
        buyer_resource = list(deal.request.keys())[0]
        buyer_value = list(deal.request.values())[0]
        buyer_resource_amount = buyer.stock[buyer_resource]  # getattr(buyer, buyer_resource, 0)
        remaining_resources = buyer_resource_amount - buyer_value

        # Check if the buyer has enough resources
        if remaining_resources < 0:
            event_text.set_text(f"You don't have enough resources to make this deal! you are missing: {remaining_resources} of {buyer_resource}", sender=buyer_index)
            return

        # Transfer resources
        provider.stock[provider_resource] -= provider_value
        buyer.stock[provider_resource] += provider_value

        buyer.stock[buyer_resource] = buyer_resource_amount - buyer_value
        provider.stock[buyer_resource] += buyer_value

        # set event text
        event_text.set_text(f"{provider.name} gave {provider_value} {provider_resource} to {buyer.name}, received {buyer_value} {buyer_resource} from {buyer.name}")

        # Display animated resource transfers
        self.show_transfer_resources(buyer_resource, buyer_value, provider_resource, provider_value, buyer_index, deal.owner_index)

        # Remove the deal from the list
        if deal in market_data.deals:
            trade = market_data.deals.pop(market_data.deals.index(deal))
            market_data.accepted_deals.append(trade)
            self.update_container_widget(trade)

    def show_transfer_resources(
            self,
            buyer_resource: str,
            buyer_value: int,
            provider_resource: str,
            provider_value: int,
            buyer_index: int,
            provider_index: int
            ):
        """
        Display animated resource transfers between buyer and provider.

        This function creates moving images to visualize resource transfers. It only
        displays animations for the client involved in the transaction (either buyer or provider).

        Args:
            buyer_resource (str): Type of resource the buyer is receiving.
            buyer_value (int): Amount of resource the buyer is receiving.
            provider_resource (str): Type of resource the provider is giving.
            provider_value (int): Amount of resource the provider is giving.
            buyer_index (int): Identifier for the buyer.
            provider_index (int): Identifier for the provider.

        Returns:
            None
        """
        client_id = config.app.game_client.id
        # Only proceed if the current client is involved in the transaction
        if client_id not in (buyer_index, provider_index):
            return

        # determine if the current client is the buyer or provider
        is_provider = client_id == provider_index

        # List of tuples containing data for both resources involved in the transfer
        resources = [
            (provider_resource, provider_value, is_provider),
            (buyer_resource, buyer_value, not is_provider)
            ]

        for resource, value, is_outgoing in resources:
            # Get the icon object for the current resource
            icon = getattr(config.app.resource_panel, f"{resource}_icon")

            # Determine starting y-position and movement direction
            start_y = icon.rect.y if is_outgoing else icon.rect.y + 60
            velocity = (0, 0.5) if is_outgoing else (0, -0.5)

            # Set operand and color based on whether resource is outgoing or incoming
            operand = "-" if is_outgoing else "+"
            color = pygame.color.THECOLORS["red" if is_outgoing else "green"]

            # Create and display the moving image for the resource transfer
            MovingImage(
                    config.app.win,
                    icon.rect.x, start_y, 30, 30,
                    get_image(f"{resource}_icon.png"),
                    3.0, velocity,
                    f" {value}{operand}", color,
                    "georgiaproblack", 1,
                    pygame.Rect(icon.rect.x, start_y, 30, 30)
                    )

    def add_deal(self, trade: Trade, **kwargs) -> None:
        from_server = kwargs.get("from_server", False)
        if not from_server:
            config.app.game_client.send_message({"f": "add_deal", "trade": trade.__repr__()})
        else:
            if self.deals_per_player_limit_reached(trade):
                return
            market_data.add_deal(trade)
            self.update_container_widget(trade)

    def accept_deal(self, deal_index, buyer_index, **kwargs):
        from_server = kwargs.get("from_server", False)
        if not from_server:
            config.app.game_client.send_message({"f": "accept_deal", "deal_index": deal_index, "buyer_index": buyer_index})
        else:
            trade = market_data.accept_deal(deal_index, buyer_index)
            if trade:
                self.transfer_resources(trade, buyer_index)
                self.update_container_widget(trade)

    def decline_deal(self, deal_index, **kwargs):
        from_server = kwargs.get("from_server", False)
        if not from_server:
            config.app.game_client.send_message({"f": "decline_deal", "deal_index": deal_index})
        else:
            trade = market_data.decline_deal(deal_index)
            if trade:
                self.update_container_widget(trade)

    def update(self):
        widgets = config.app.deal_container.widgets
        for i in widgets:
            i.set_text_and_state_image()

            i.obj.generate_time_text(time_handler.game_speed)
            if i.obj.remaining_time < 0.0:
                self.decline_deal(widgets.index(i))
        self.overblit_deal_icon()


market = Market()
