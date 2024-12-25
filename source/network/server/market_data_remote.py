import time

DEAL_LIFETIME = 120  # seconds


class Trade:
    def __init__(self, owner_index: int, offer: dict, request: dict) -> None:
        """
        example usage:
        owner_index: 0
        request: {'food':10}
        offer: {'water':10}
        """
        self.request = request
        self.offer = offer
        self.owner_index = owner_index

        # timing
        self.life_time = DEAL_LIFETIME
        self.start_time = time.time()
        self.end_time = self.start_time + self.life_time
        self.remaining_time = DEAL_LIFETIME
        self.time_text = f"deal ends in: {int(self.remaining_time)} s"

    def __repr__(self):
        return {"owner_index": self.owner_index, "offer": self.offer, "request": self.request}

    def __str__(self, name: str):
        text = f"{name} offers: "

        for key, value in self.offer.items():
            text += f"{key}: {value}"

        text += f" for "
        for key, value in self.request.items():
            text += f"{key}: {value}"

        text += f", {self.time_text}"

        return text

    def generate_time_text(self, game_speed: int) -> None:
        # remaining time text
        self.life_time = DEAL_LIFETIME / game_speed
        self.end_time = self.start_time + self.life_time

        current_time = time.time()
        self.remaining_time = self.end_time - current_time
        self.time_text = f"deal ends in: {int(self.remaining_time)} s"


class MarketDataRemote:
    def __init__(self):
        self.deals = []
        self.accepted_deals = []
        self.declined_deals = []
        self.last_deals = {}

    def __repr__(self):
        return f"deals: {self.deals}\n, accepted_deals: {self.accepted_deals}\n, declined_deals: {self.declined_deals}"

    def handle_message(self, message: dict) -> None:
        """
        {'function': 'add_deal', 'trade': {'owner_index': 3, 'offer': {'technology': 2000}, 'request': {'minerals': 1500}}}
        {'function': 'accept_deal', 'deal_index': 1, 'buyer_index': 4}
        {'function': 'decline_deal', 'deal_index': 1}
        """
        # print(f"handle_message: {message}")
        match message["f"]:
            case "add_deal":
                trade_dict = message["trade"]
                self.add_deal(Trade(trade_dict["owner_index"], trade_dict["offer"], trade_dict["request"]))
            case "accept_deal":
                self.accept_deal(message["deal_index"], message["buyer_index"])
            case "decline_deal":
                self.decline_deal(message["deal_index"])

    def add_deal(self, trade: Trade) -> None:
        self.deals.append(trade)
        self.last_deals[trade.owner_index] = trade

    def accept_deal(self, deal_index, buyer_index):
        if 0 <= deal_index < len(self.deals):
            trade = self.deals.pop(deal_index)
            self.accepted_deals.append(trade)
            return trade
        return None

    def decline_deal(self, deal_index):
        if 0 <= deal_index < len(self.deals):
            trade = self.deals.pop(deal_index)
            self.declined_deals.append(trade)
            return trade
        return None
