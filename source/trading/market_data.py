class MarketData:
    def __init__(self):
        self.deals = []
        self.accepted_deals = []
        self.declined_deals = []
        self.last_deals = {}

    def __repr__(self):
        return f"deals: {self.deals}\n, accepted_deals: {self.accepted_deals}\n, declined_deals: {self.declined_deals}"

    def add_deal(self, trade):
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


market_data = MarketData()
