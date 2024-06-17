import time

from source.configuration.game_config import config

DEAL_LIFETIME = 120  # seconds


class Trade:
    def __init__(self, owner_index: int, offer: dict, request: dict) -> None:
        """
        example usage:
        request: {'food':10}
        offer: {'water':10}
        """

        """ 
        ?????????' why is it opposite ?? nedds to be checked :) 
        """
        self.request = offer
        self.offer = request
        self.owner_index = owner_index

        # timing
        self.life_time = DEAL_LIFETIME
        self.start_time = time.time()
        self.end_time = self.start_time + self.life_time
        self.remaining_time = DEAL_LIFETIME
        self.time_text = f"deal ends in: {int(self.remaining_time)} s"

    def generate_time_text(self) -> None:
        # remaining time text
        self.life_time = DEAL_LIFETIME / config.game_speed
        self.end_time = self.start_time + self.life_time

        current_time = time.time()
        self.remaining_time = self.end_time - current_time
        self.time_text = f"deal ends in: {int(self.remaining_time)} s"

    def __str__(self):
        name = config.app.players[self.owner_index].name
        text = f"{name} offers: "

        for key, value in self.offer.items():
            text += f"{key}: {value}"

        text += f" for "
        for key, value in self.request.items():
            text += f"{key}: {value}"

        text += f", {self.time_text}"

        return text

    def __repr__(self):
        return f"Trade: {self.__str__()}"

    def update(self):
        self.generate_time_text()
