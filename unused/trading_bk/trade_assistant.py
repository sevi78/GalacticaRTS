from typing import Optional

from source.configuration.game_config import config
from source.gui.event_text import event_text
from source.trading.deal_select import DealSelect


class TradeAssistant:
    def __init__(self, player):
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
        deal_manager = config.app.deal_manager
        deals = [i for i in deal_manager.accepted_deals if i.provider_index == self.player_index]
        return deals

    def get_declined_deals_from_player(self) -> list:
        deal_manager = config.app.deal_manager
        deals = [i for i in deal_manager.declined_deals if i.provider_index == self.player_index]
        return deals

    def get_last_deal_from_player(self) -> Optional[DealSelect]:
        deal_manager = config.app.deal_manager
        if self.player_index in deal_manager.last_deals.keys():
            return deal_manager.last_deals[self.player_index]
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

    def generate_fitting_deal(self) -> dict:
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
        data = {"player_index": self.player_index, "offer": offer, "request": request}
        return data

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
            self.offer_percentage = max(self.offer_percentage * 1.1, 0.1)
            self.request_percentage = max(self.request_percentage * 1.15, 0.1)
        elif last_deal in self.get_declined_deals_from_player():
            self.offer_percentage = max(self.offer_percentage * 0.9, 0.1)
            self.request_percentage = max(self.request_percentage * 0.85, 0.1)

        # print (f"adjust_percentages:\n self.offer_percentage:{self.offer_percentage}\nself.request_percentage:{self.request_percentage}")

    def trade_technology_to_the_bank(
            self, offer_value: int, request_resource: str, request_value: int, player_index: int
            ):
        player = config.app.players[player_index]

        if player.technology - offer_value > 0:
            setattr(player, request_resource, getattr(player, request_resource) + request_value)
            player.technology -= offer_value

            # print (f"trade_technology_to_the_bank: player: {player.name}, request:{request_resource}/{request_value}, for {offer_value} of technologyy")
        else:
            event_text.text = f"not enough technology for the deal!"
