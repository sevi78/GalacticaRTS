from source.handlers.time_handler import time_handler

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
        self.start_time = time_handler.time
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

        current_time = time_handler.time
        self.remaining_time = self.end_time - current_time
        self.time_text = f"deal ends in: {int(self.remaining_time)} s"
