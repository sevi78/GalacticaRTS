from source.multimedia_library.images import get_image, scale_image_cached


class Ranking:
    def __init__(self):
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
        self.resize_rank_images()

    def resize_rank_images(self):
        for key, image in self.rank_images.items():
            self.rank_images[key] = scale_image_cached(image, (image.get_width() / 2.5, image.get_height() / 2.5))

    def set_rank_from_population(self, obj, population_list):
        # get a list of all possible population ranges: [0, 1000, 2500, 5000, 10000]
        population_list = sorted(set(population_list))

        # check if objs population bigger than any item in population ranges and set its image based on the index
        for i in range(len(population_list)):
            if obj.economy_agent.population >= population_list[i]:
                obj.rank = self.ranks[i]
