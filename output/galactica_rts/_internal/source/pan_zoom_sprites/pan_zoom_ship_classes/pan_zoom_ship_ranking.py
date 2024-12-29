from source.debug.function_disabler import auto_disable, disabler
from source.game_play.ranking import Ranking
from source.gui.event_text import event_text
from source.multimedia_library.sounds import sounds


# disabled_functions = ["set_experience", "set_rank"]
# for i in disabled_functions:
#     disabler.disable(i)
#
# @auto_disable

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
    - update_rank_image: draws the rank image on the screen.

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
        # experience
        self.experience = 0
        self.experience_factor = 3000

        # ranking
        self.ranking = Ranking()
        self.rank = "Cadet"

    def set_experience(self, value):
        self.experience += value
        self.set_rank()

    def set_rank(self):
        # check if experience is big enough to upgrade
        rank_value = int(self.experience / self.experience_factor)

        # limit experience to int >0<8
        if rank_value < 0:
            rank_value = 0
        elif rank_value > 8:
            rank_value = 8

        # get previous rank fot text generation
        prev_rank = self.rank
        self.rank = self.ranking.ranks[rank_value]

        # set rank
        prev_key = next((key for key, value in self.ranking.ranks.items() if value == prev_rank), None)
        curr_key = next((key for key, value in self.ranking.ranks.items() if value == self.rank), None)

        # generate feedback for player, set event_text and play sound
        if curr_key > prev_key:
            event_text.set_text("Congratulations !!! Rank increased from {} to {} !!!".format(prev_rank, self.rank), obj=self,sender=self.owner)
            sounds.play_sound(sounds.rank_up)
        elif curr_key < prev_key:
            event_text.set_text("Shame on you !!! Rank decreased from {} to {} !!!".format(prev_rank, self.rank), obj=self, sender=self.owner)
            sounds.play_sound(sounds.rank_down)
