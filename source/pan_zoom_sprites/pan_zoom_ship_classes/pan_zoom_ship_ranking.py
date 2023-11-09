import pygame

from source.gui.event_text import event_text
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds


class PanZoomShipRanking:
    """
    Main functionalities:
    The PanZoomShipRanking class is responsible for ranking the ship based on the experience gained by the player.
    It contains a dictionary of possible ranks and their corresponding images, as well as methods to set the experience
    and rank, and to draw the rank image on the screen.

    Methods:
    - __init__: initializes the class with default values for experience, rank, ranks, and rank_images.
    - set_experience: updates the experience value and calls set_rank to update the rank accordingly.
    - set_rank: calculates the rank based on the experience value and updates it. It also displays a message and plays
      a sound if the rank has increased or decreased.
    - draw_rank_image: draws the rank image on the screen.

    Fields:
    - property: a string indicating the type of property being ranked (in this case, "ship").
    - experience: an integer representing the amount of experience gained by the player.
    - experience_factor: a constant used to calculate the rank based on the experience value.
    - rank: a string representing the current rank of the ship.
    - ranks: a dictionary mapping rank values to their corresponding strings.
    - rank_images: a dictionary mapping rank strings to their corresponding images.

    possible ranks:
            0: "Cadet",
            1: "Ensign",
            2: "Lieutenant",
            3: "Commander",
            4: "Commodore",
            5: "Captain",
            6: "Vice Admiral",
            7: "Admiral",
            8: "Fleet Admiral"
    """

    def __init__(self):
        # ranking
        self.experience = 0
        self.experience_factor = 3000
        self.rank = "Cadet"
        self.ranks = {0: "Cadet", 1: "Ensign", 2: "Lieutenant", 3: "Commander", 4: "Commodore", 5: "Captain", 6: "Vice Admiral", 7: "Admiral", 8: "Fleet Admiral"}

        # rank image
        self.rank_images = {
            "Cadet": get_image("badge1_30x30.png"),
            "Ensign": get_image("badge2_30x30.png"),
            "Lieutenant": get_image("badge3_30x30.png"),
            "Commander": get_image("badge4_48x30.png"),
            "Commodore": get_image("badge5_48x30.png"),
            "Captain": get_image("badge6_48x30.png"),
            "Vice Admiral": get_image("badge7_43x30.png"),
            "Admiral": get_image("badge8_43x30.png"),
            "Fleet Admiral": get_image("badge9_44x30.png")
            }

        # resize rank images
        for key, image in self.rank_images.items():
            self.rank_images[key] = pygame.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))

    def set_experience(self, value):
        self.experience += value
        self.set_rank()

    def set_rank(self):
        rank_value = int(self.experience / self.experience_factor)
        if rank_value < 0:
            rank_value = 0
        elif rank_value > 8:
            rank_value = 8
        prev_rank = self.rank
        self.rank = self.ranks[rank_value]
        prev_key = next((key for key, value in self.ranks.items() if value == prev_rank), None)
        curr_key = next((key for key, value in self.ranks.items() if value == self.rank), None)
        if curr_key > prev_key:
            event_text.text = "Congratulations !!! Rank increased from {} to {} !!!".format(prev_rank, self.rank)
            sounds.play_sound(sounds.rank_up)
        elif curr_key < prev_key:
            event_text.text = "Shame on you !!! Rank decreased from {} to {} !!!".format(prev_rank, self.rank)
            sounds.play_sound(sounds.rank_down)
