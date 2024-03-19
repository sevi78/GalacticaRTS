import random

from source.configuration.game_config import config
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.position_handler import get_random_pos
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image, get_gif
from source.pan_zoom_sprites.pan_zoom_collectable_item import PanZoomCollectableItem
from source.text.info_panel_text_generator import info_panel_text_generator
from source.universe.celestial_objects.asteroid import Asteroid
from source.universe.celestial_objects.celestial_object import CelestialObject
from source.universe.celestial_objects.celestial_object_static import CelestialObjectStatic
from source.universe.celestial_objects.comet import Comet
from source.universe.celestial_objects.stars import FlickeringStar, PulsatingStar

COMET_DIVIDE_FACTOR = 500
ASTEROID_GIF_DIVIDE_FACTOR = 300
ASTEROID_DIVIDE_FACTOR = 150
NEBULAE_DIVIDE_FACTOR = 250
GALAXY_DIVIDE_FACTOR = 300
STAR_DIVIDE_FACTOR = 20
FLICKERING_STAR_DIVIDE_FACTOR = 3
PULSATING_STAR_DIVIDE_FACTOR = 4


class UniverseFactory:
    """
    Summary
    The UniverseFactory class is responsible for creating and managing celestial objects in a universe. It generates stars, galaxies, nebulae, asteroids, and comets based on specified parameters.
    Example Usage
    # Create an instance of UniverseFactory
    factory = UniverseFactory(win, x, y, width, height, layer)

    # Generate the universe with specified dimensions
    factory.create_universe(x, y, width, height)

    # Delete all celestial objects in the universe
    factory.delete_universe()
    Code Analysis
    Main functionalities
    Generate celestial objects such as stars, galaxies, nebulae, asteroids, and comets in a universe
    Delete celestial objects from the universe

    Methods
    __init__(self, win, x, y, width, height, layer): Initializes the UniverseFactory object with the specified parameters.
    create_universe(self, x, y, width, height): Generates the universe by creating stars, galaxies, nebulae, asteroids, and comets based on the specified dimensions.
    delete_universe(self): Deletes all celestial objects in the universe.
    create_stars(self): Generates stars in the universe.
    create_galaxys(self): Generates galaxies in the universe.
    create_nebulaes(self): Generates nebulae in the universe.
    create_asteroids(self): Generates asteroids in the universe.
    create_comets(self): Generates comets in the universe.

    Fields
    central_compression: A parameter that controls the compression of celestial objects in the universe.
    win: The window object where the universe is displayed.
    layer: The layer of the universe in the display.
    amount: The total number of celestial objects in the universe.
    left_end: The left boundary of the universe.
    right_end: The right boundary of the universe.
    top_end: The top boundary of the universe.
    bottom_end: The bottom boundary of the universe.
    star_images: A dictionary of star images used for generating stars.
    asteroid_images: A dictionary of asteroid images used for generating asteroids.
    comet_images: A dictionary of comet images used for generating comets.
    nebulae_images: A dictionary of nebulae images used for generating nebulae.
    galaxy_images: A dictionary of galaxy images used for generating galaxies.
    star: A list of generated stars.
    pulsating_star: A list of generated pulsating stars.
    flickering_star: A list of generated flickering stars.
    asteroid: A list of generated asteroids.
    nebulae: A list of generated nebulae.
    galaxy: A list of generated galaxies.
    comet: A list of generated comets.
    universe: A list of all celestial objects in the universe.
    quadrant: A list of quadrants in the universe.
    celestial_objects: A dictionary that maps celestial object types to their corresponding lists of objects.
    """

    def __init__(self, win, x, y, width, height, layer):
        self.central_compression = 1
        self.win = win
        self.layer = layer
        self.amount = 0

        # define borders
        self.left_end = x
        self.right_end = width
        self.top_end = y
        self.bottom_end = height

        # images
        self.star_images = {
            0: get_image("star_30x30.png"),
            1: get_image("star_50x50.png"),
            2: get_image("star1_50x50.png"),
            3: get_image("star2_100x100.png")
            }

        self.asteroid_images = {
            0: get_image("asteroid_40x33.png"),
            }

        self.comet_images = {
            0: get_image("comet_90x38.png")
            }

        self.nebulae_images = {
            0: get_image("nebulae_300x300.png")
            }

        self.galaxy_images = {
            0: get_image("galaxy_.png"),
            1: get_image("galaxy3_small.png")
            }

        # drawing lists
        self.star = []
        self.pulsating_star = []
        self.flickering_star = []
        self.asteroid = []
        self.nebulae = []
        self.galaxy = []
        self.comet = []
        self.universe = []
        self.quadrant = []

        # create universe
        self.celestial_objects = {}

    def get_random_image(self, images):
        return random.choice(images)

    def create_artefacts(self, x, y, width, height, amount):  # orig
        all_specials = ["food * 1.5", "energy * 1.5", "minerals * 1.5", "water * 1.5", "technology * 1.5",
                        "buildings_max + 1"]

        def select_resources():
            resources = ["water", "food", "energy", "technology", "minerals"]
            selected_resources = {"water": 0, "food": 0, "energy": 0, "technology": 0, "minerals": 0}
            amount_of_all = random.randint(0, 1000)
            total_amount = 0
            while total_amount < amount_of_all:
                resource = random.choice(resources)
                amount = random.randint(0, amount_of_all)
                if total_amount + amount > 1000:
                    amount = 1000 - total_amount
                if resource in selected_resources:
                    selected_resources[resource] += amount
                else:
                    selected_resources[resource] = amount
                total_amount += amount
            return selected_resources

        image_names = ["artefact1_60x31.png",
                       "meteor_50x50.png",
                       "meteor_60x83.png",
                       "meteor1_50x50.png"
                       ]

        artefact_sizes = {"artefact1_60x31.png": (60, 31),
                          "meteor_50x50.png": (50, 50),
                          "meteor_60x83.png": (int(60) * .5, int(83) * .5),
                          "meteor1_50x50.png": (50, 50)
                          }
        for i in range(int(amount / 2)):
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)
            image_name = random.choice(image_names)
            size = artefact_sizes[image_name]
            width, height = size
            selected_resources = select_resources()
            specials = [random.choice(all_specials)]

            artefact = PanZoomCollectableItem(config.win,
                x=x, y=y, width=width, height=height,
                pan_zoom=pan_zoom_handler,
                image_name=image_name,
                isSubWidget=False,
                transparent=True,
                tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
                infotext=info_panel_text_generator.create_info_panel_collectable_item_text(selected_resources, specials),
                moveable=True,
                energy=selected_resources["energy"],
                minerals=selected_resources["minerals"],
                food=selected_resources["food"],
                technology=selected_resources["technology"],
                water=selected_resources["water"],
                specials=specials,
                parent=self,
                group="collectable_items",
                gif="sphere.gif",
                align_image="center",
                outline_thickness=1,
                outline_threshold=0)

        for i in range(int(amount / 2)):
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)
            selected_resources = select_resources()
            specials = [random.choice(all_specials)]
            artefact = PanZoomCollectableItem(config.win,
                x=x, y=y, width=60, height=60,
                pan_zoom=pan_zoom_handler,
                image_name="sphere.gif",
                isSubWidget=False,
                transparent=True,
                tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
                infotext=info_panel_text_generator.create_info_panel_collectable_item_text(selected_resources, specials),
                moveable=True,
                energy=selected_resources["energy"],
                minerals=selected_resources["minerals"],
                food=selected_resources["food"],
                technology=selected_resources["technology"],
                water=selected_resources["water"],
                specials=specials,
                parent=self,
                group="collectable_items",
                gif="sphere.gif",
                relative_gif_size=0.4,
                align_image="center",
                outline_thickness=1,
                outline_threshold=0)

    def create_stars(self):
        # star images
        for i in range(max(1, int(self.amount / STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            image = random.choice(self.star_images)
            w = image.get_rect().width
            h = image.get_rect().height

            star = CelestialObjectStatic(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="star")

        # flickering stars
        for i in range(max(1, int(self.amount / FLICKERING_STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)
            w = random.randint(1, 10)

            flickering_star = FlickeringStar(self.win, x, y, w, w, layer=self.layer, parent=self, type="flickering_star")

        # puslating stars
        for i in range(max(1, int(self.amount / PULSATING_STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)
            w = 1

            pulsating_star = PulsatingStar(self.win, x, y, w, w, layer=self.layer, parent=self, type="pulsating_star")

    def create_galaxys(self):
        for i in range(max(1, int(self.amount / GALAXY_DIVIDE_FACTOR))):
            image = random.choice(self.galaxy_images)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            galaxy = CelestialObject(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="galaxy")

    def create_nebulaes(self):
        for i in range(max(1, int(self.amount / NEBULAE_DIVIDE_FACTOR))):
            image = random.choice(self.nebulae_images)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            nebulae = CelestialObject(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="nebulae")

    def create_asteroids(self):
        for i in range(max(1, int(self.amount / ASTEROID_DIVIDE_FACTOR))):
            image = random.choice(self.asteroid_images)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            asteroid = Asteroid(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="asteroid")

        for i in range(max(1, int(self.amount / ASTEROID_GIF_DIVIDE_FACTOR))):
            image = random.choice(self.asteroid_images)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            asteroid = Asteroid(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="asteroid", gif="asteroid.gif")

    def create_comets(self):
        for i in range(max(1, int(self.amount / COMET_DIVIDE_FACTOR))):
            image = random.choice(self.comet_images)

            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            comet = Comet(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="comet", gif="comet.gif")

    def create_universe(self, x, y, width, height):
        self.left_end = x
        self.top_end = y
        self.right_end = self.left_end + width
        self.bottom_end = self.top_end + height

        self.create_stars()
        self.create_galaxys()
        self.create_nebulaes()
        self.create_comets()
        self.create_asteroids()

        self.universe = self.star + self.pulsating_star + self.galaxy + self.nebulae + self.comet + self.asteroid  # + self.quadrant

        self.celestial_objects = {
            "star": self.star,
            "pulsating_star": self.pulsating_star,
            "galaxy": self.galaxy,
            "nebulae": self.nebulae,
            "comet": self.comet,
            "asteroid": self.asteroid
            }

    def delete_universe(self):
        all_widgets = WidgetHandler.get_all_widgets()
        celestials = [i for i in all_widgets if issubclass(i.__class__, (CelestialObject, CelestialObjectStatic))]
        for i in celestials:
            WidgetHandler.remove_widget(i)

    def delete_artefacts(self):
        for i in sprite_groups.collectable_items.sprites():
            i.end_object()


universe_factory = UniverseFactory(config.win, 0, 0, config.scene_width, config.scene_height, layer=0)
