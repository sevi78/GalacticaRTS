from typing import Optional

from source.configuration.game_config import config
from source.gui.event_text import event_text
from source.trading.market_data import market_data
from source.trading.trade import Trade


class TradeAssistant:
    def __init__(self, player):
        """ this class is injected to the player object."""
        self.player = player
        self.player_index = self.player.owner
        self.offer_percentage = 20
        self.request_percentage = 15

    def __repr__(self):
        return (f"TradeAssistant:\n"
                f" last_deal={self.get_last_deal_from_player()}\n,"
                f" accepted_deals={self.get_accepted_deals_from_player()}\n,"
                f" declined_deals={self.get_declined_deals_from_player()}\n"
                f"{self.generate_deal_based_resource_maximum_and_minimum(15.0, 10.0)}\n"
                )

    def get_accepted_deals_from_player(self) -> list:
        deals = [i for i in market_data.accepted_deals if i.owner_index == self.player_index]
        return deals

    def get_declined_deals_from_player(self) -> list:
        deals = [i for i in market_data.declined_deals if i.owner_index == self.player_index]
        return deals

    def get_last_deal_from_player(self) -> Optional[Trade]:
        if self.player_index in market_data.last_deals.keys():
            return market_data.last_deals[self.player_index]
        return None

    def generate_deal_based_resource_maximum_and_minimum(
            self,
            percentage_offer: float,
            percentage_request: float,
            ) -> dict:

        """
        this is called from the add_deal_edit to make the best deal based on the percentage values
        """

        # create a new deal dict
        new_deal_dict = {"offer": {}, "request": {}}

        # get player resource stock
        resource_stock = self.player.get_resource_stock()

        # get the lowest and highest resource values
        min_key = self.player.auto_economy_handler.get_lowest_value_key(resource_stock)
        max_key = self.player.auto_economy_handler.get_highest_value_key(resource_stock)
        min_value = resource_stock[min_key]
        max_value = resource_stock[max_key]

        new_deal_dict["offer"][max_key] = int(max_value / 100 * percentage_offer)
        new_deal_dict["request"][min_key] = (int(max_value / 100 * percentage_request))

        return new_deal_dict

    def generate_fitting_deal(self) -> Trade:
        """
        Generates a fitting deal for the player.
        it is called from:

        config.app.deal_manager.add_fitting_deal(self.player.trade_assistant.generate_fitting_deal())


        gets the lowest and highest resource values, calculates the offer and request values based on the percentages
        and returns a dictionary containing the player index, offer, and request.

        Returns:
            dict: A dictionary containing the player index, offer, and request.
        """
        auto_economy_handler = self.player.auto_economy_handler
        lowest_value_key = auto_economy_handler.get_lowest_value_key(self.player.get_resource_stock())
        highest_value_key = auto_economy_handler.get_highest_value_key(self.player.get_resource_stock())

        # adjust_percentages
        self.adjust_percentages()

        # calculate the value to offer
        offer_value = int(self.player.get_stock()[highest_value_key] / 100 * self.offer_percentage)
        request_value = int(self.player.get_stock()[highest_value_key] / 100 * self.request_percentage)

        # create offer and request
        offer = {highest_value_key: offer_value}
        request = {lowest_value_key: request_value}
        trade = Trade(self.player.owner, offer, request)
        return trade

    def adjust_percentages(self):
        """
        Analyzes the player's past deals and adjusts the offer and request percentages accordingly.

        The function makes the following adjustments:
        - If the last deal was accepted, decrease the offer percentage by 15% and the request percentage by 10%.
        - If the last deal was declined, decrease the offer percentage by 10% and the request percentage by 15%.
        - If the last deal was active (neither accepted nor declined), do not adjust the percentages.

        The adjusted percentages are capped at a minimum of 5% to avoid going below 0.
        """

        # Get the last deal
        last_deal = self.get_last_deal_from_player()

        # If there is no last deal, return without making any adjustments
        if not last_deal:
            return

        # Adjust the percentages based on the status of the last deal
        if last_deal in self.get_accepted_deals_from_player():
            self.offer_percentage = self.limit_percentage(max(self.offer_percentage * 1.1, 0.1))
            self.request_percentage = self.limit_percentage(max(self.request_percentage * 1.15, 0.1))
        elif last_deal in self.get_declined_deals_from_player():
            self.offer_percentage = self.limit_percentage(max(self.offer_percentage * 0.9, 0.1))
            self.request_percentage = self.limit_percentage(max(self.request_percentage * 0.85, 0.1))

    def limit_percentage(self, percentage: float) -> float:
        if percentage >= 100.0:
            percentage = 100.0

        if percentage <= 0.0:
            percentage = 0.0

        return percentage

    def trade_technology_to_the_bank(
            self, offer_value: int, request_resource: str, request_value: int, player_index: int, **kwargs
            ):
        from_server = kwargs.get("from_server", False)
        player = config.app.players[player_index]

        if player.stock["technology"] - offer_value > 0:
            # setattr(player, request_resource, getattr(player, request_resource) + request_value)
            player.stock[request_resource] = player.stock[request_resource] + request_value
            player.stock["technology"] -= offer_value

            # print (f"trade_technology_to_the_bank: player: {player.name}, request:{request_resource}/{request_value}, for {offer_value} of technologyy")
        else:
            event_text.set_text(f"not enough technology for the deal!", sender=player_index)

        if not from_server:
            config.app.game_client.send_message({
                "f": "trade_technology_to_the_bank",
                "offer_value": offer_value,
                "request_resource": request_resource,
                "request_value": request_value,
                "player_index": player_index
                })
