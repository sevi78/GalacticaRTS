from typing import Optional

from source.configuration.game_config import config
from source.editors.deal_select import DealSelect


class TradeAssistant:
    def __init__(self):
        pass

    def __repr__(self):
        return (f"TradeAssistant:\n"
                f" last_deal={self.get_last_deal_from_player(config.player)}\n,"
                f" deals={self.get_active_deals_from_player(config.player)}\n,"
                f" accepted_deals={self.get_accepted_deals_from_player(config.player)}\n,"
                f" declined_deals={self.get_declined_deals_from_player(config.player)}\n"
                f" last_deal_is_accepted={self.last_deal_is_accepted(config.player)}\n,"
                f" last_deal_is_declined={self.last_deal_is_declined(config.player)}\n,"
                f" last_deal_is_active={self.last_deal_is_active(config.player)}\n"
                f" get_last_deal_from_player_and_offer_key={self.get_last_deal_from_player_and_offer_key(config.player, 'energy')}\n"
                f" get_last_deal_from_player_and_request_key={self.get_last_deal_from_player_and_request_key(config.player, 'minerals')}\n"
                f" adjust_last_deal_amount={self.adjust_deal_offer_and_request_based_on_reference_deal(config.player, 'energy', 'minerals', self.get_last_deal_from_player(config.player))}\n"
                f" generate_deal_based_resource_maximum_and_minimum="
                f"{self.generate_deal_based_resource_maximum_and_minimum(config.player, 15.0, 10.0)}\n"
                )

    def last_deal_is_accepted(self, player_index: int) -> bool:
        last_deal = self.get_last_deal_from_player(player_index)
        if last_deal:
            return last_deal in self.get_accepted_deals_from_player(player_index)
        return False

    def last_deal_is_declined(self, player_index: int) -> bool:
        last_deal = self.get_last_deal_from_player(player_index)
        if last_deal:
            return last_deal in self.get_declined_deals_from_player(player_index)
        return False

    def last_deal_is_active(self, player_index: int) -> bool:
        last_deal = self.get_last_deal_from_player(player_index)
        if last_deal:
            return last_deal in self.get_active_deals_from_player(player_index)
        return False

    def get_active_deals_from_player(self, player_index: int) -> list:
        deal_manager = config.app.deal_manager
        deals = [i for i in deal_manager.deals if i.provider_index == player_index]
        return deals

    def get_accepted_deals_from_player(self, player_index: int) -> list:
        deal_manager = config.app.deal_manager
        deals = [i for i in deal_manager.accepted_deals if i.provider_index == player_index]
        return deals

    def get_declined_deals_from_player(self, player_index: int) -> list:
        deal_manager = config.app.deal_manager
        deals = [i for i in deal_manager.declined_deals if i.provider_index == player_index]
        return deals

    def get_last_deal_from_player(self, player_index: int) -> Optional[DealSelect]:
        deal_manager = config.app.deal_manager
        if player_index in deal_manager.last_deals.keys():
            return deal_manager.last_deals[player_index]
        return None

    def get_last_deal_from_player_and_offer_key(self, player_index: int, offer_key: str) -> Optional[DealSelect]:
        deal_manager = config.app.deal_manager
        if player_index in deal_manager.last_deals.keys():
            if offer_key in deal_manager.last_deals[player_index].offer.keys():
                return deal_manager.last_deals[player_index]
        return None

    def get_last_deal_from_player_and_request_key(self, player_index: int, request_key: str) -> Optional[DealSelect]:
        deal_manager = config.app.deal_manager
        if player_index in deal_manager.last_deals.keys():
            if request_key in deal_manager.last_deals[player_index].request.keys():
                return deal_manager.last_deals[player_index]
        return None

    def adjust_deal_offer_and_request_based_on_reference_deal(self, player_index: int, offer_key: str, request_key: str,
                                                              last_deal: DealSelect) -> dict:
        # create a new deal dict
        new_deal_dict = {"offer": {}, "request": {}}

        # if has a last deal, go on
        if last_deal:
            # check if the offer and request keys are in the last deal
            if offer_key in last_deal.offer.keys() and request_key in last_deal.request.keys():
                # if last deal was accepted
                if last_deal in self.get_accepted_deals_from_player(player_index):
                    new_deal_dict["offer"][offer_key] = last_deal.offer[offer_key] * .85
                    new_deal_dict["request"][request_key] = last_deal.request[request_key] * .9

                # if last deal was declined
                if last_deal in self.get_declined_deals_from_player(player_index):
                    new_deal_dict["offer"][offer_key] = last_deal.offer[offer_key] * .9
                    new_deal_dict["request"][request_key] = last_deal.request[request_key] * .85
            else:
                new_deal_dict["offer"] = last_deal.offer
                new_deal_dict["request"] = last_deal.request

        return new_deal_dict

    def generate_deal_based_resource_maximum_and_minimum(self, player_index: int, percentage_offer: float,
                                                         percentage_request: float) -> dict:
        # create a new deal dict
        player = config.app.players[player_index]
        new_deal_dict = {"offer": {}, "request": {}}

        # get player resource stock
        resource_stock = player.get_resource_stock()

        # get the lowest and highest resource values
        min_key = player.auto_economy_handler.get_lowest_value_key(resource_stock)
        max_key = player.auto_economy_handler.get_highest_value_key(resource_stock)
        min_value = resource_stock[min_key]
        max_value = resource_stock[max_key]

        new_deal_dict["offer"][max_key] = int(max_value / 100 * percentage_offer)
        new_deal_dict["request"][min_key] = int(max_value / 100 * percentage_request)

        return new_deal_dict


trade_assistant = TradeAssistant()
