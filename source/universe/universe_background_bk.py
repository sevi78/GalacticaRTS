import math
import random

import pygame

from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.universe.celestial_objects.asteroid import Asteroid
from source.universe.celestial_objects.celestial_object import CelestialObject
from source.universe.celestial_objects.celestial_object_static import CelestialObjectStatic
from source.universe.celestial_objects.comet import Comet
from source.universe.celestial_objects.stars import FlickeringStar, PulsatingStar

from source.utils import global_params
from source.multimedia_library.images import images, pictures_path
from source.utils.positioning import limit_positions


class Universe(WidgetBase):
    """Main functionalities:
    The Universe class is responsible for creating and managing the celestial objects in the game universe.
    It creates stars, galaxies, nebulae, asteroids, comets, and quadrants, and stores them in lists.
    It also handles drawing the objects on the screen and listening for events.

    Methods:
    - create_stars(): creates the different types of stars and adds them to the star list
    - create_galaxys(): creates galaxies and adds them to the galaxy list
    - create_nebulaes(): creates nebulae and adds them to the nebulae list
    - create_asteroids(): creates asteroids and adds them to the asteroid list
    - create_comets(): creates comets and adds them to the comet list
    - create_quadrant(): creates quadrants and adds them to the quadrant list
    - create_universe(): calls all the create methods to create the entire universe
    - draw(): draws all the celestial objects on the screen
    - listen(): listens for events (currently empty)

    Fields:
    - parent: the parent object of the universe
    - layer: the layer of the universe
    - amount: the number of celestial objects to create
    - left_end, right_end, top_end, bottom_end: the borders of the universe
    - star_images, asteroid_images, comet_images, nebulae_images, galaxy_images: dictionaries of images for each type of
      celestial object
    - star, pulsating_star, asteroid, nebulae, galaxy, comet, universe, quadrant: lists of celestial objects"""
    __slots__ = WidgetBase.__slots__ + (
        'amount', 'left_end', 'right_end', 'top_end', 'bottom_end', 'screen_size', 'star_images', 'asteroid_images',
        'comet_images', 'nebulae_images', 'galaxy_images', 'star', 'pulsating_star','flickering_star', 'asteroid',
        'nebulae', 'galaxy', 'comet', 'universe', 'quadrant', 'celestial_objects', 'average_draw_time', 'min_draw_time',
        'max_draw_time'
        )

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        # Moveable.__init__(self, x, y, width, height, kwargs)

        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 0)
        self.amount = int(math.sqrt(math.sqrt(width)) * global_params.settings["universe_density"])

        # define borders
        self.left_end = 0  # -self.get_screen_width()
        self.right_end = self.get_screen_width()
        self.top_end = 0  # -self.get_screen_height()
        self.bottom_end = self.get_screen_height()
        self.screen_size = (0, 0)

        # images
        self.star_images = {
            0: images[pictures_path]["stars"]["star_30x30.png"],
            1: images[pictures_path]["stars"]["star_50x50.png"],
            2: images[pictures_path]["stars"]["star1_50x50.png"],
            3: images[pictures_path]["stars"]["star2_100x100.png"]
            }

        self.asteroid_images = {
            0: images[pictures_path]["celestial objects"]["asteroid_40x33.png"],
            }

        self.comet_images = {
            0: images[pictures_path]["celestial objects"]["comet_90x38.png"]
            }

        self.nebulae_images = {
            0: images[pictures_path]["celestial objects"]["nebulae_300x300.png"]
            }

        self.galaxy_images = {
            0: images[pictures_path]["celestial objects"]["galaxy_.png"],
            1: images[pictures_path]["celestial objects"]["galaxy3_small.png"]
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
        self.create_universe()

        self.average_draw_time = 0.0
        self.min_draw_time = 0.0
        self.max_draw_time = 10.0

        self.set_screen_size((global_params.WIDTH_CURRENT, global_params.HEIGHT_CURRENT))

    def create_stars(self):
        # star images
        for i in range(int(self.amount / 20)):
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            select = random.randint(0, len(self.star_images.keys()) - 1)
            image = pygame.transform.scale(self.star_images[select], (15, 15))
            w = image.get_rect().width
            h = image.get_rect().height

            star = CelestialObjectStatic(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="star")

        # flickering stars
        for i in range(int(self.amount / 3)):
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)
            w = random.randint(1, 10)

            flickering_star = FlickeringStar(self.win, x, y, w, w, layer=self.layer, parent=self, type="flickering_star")

        # puslating stars
        for i in range(int(self.amount / 3)):
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)
            w = 1

            pulsating_star = PulsatingStar(self.win, x, y, w, w, layer=self.layer, parent=self, type="pulsating_star")

    def create_galaxys(self):
        for i in range(int(self.amount / 300)):
            select = random.randint(0, len(self.galaxy_images.keys()) - 1)
            image = self.galaxy_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            galaxy = CelestialObjectStatic(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="galaxy")

    def create_nebulaes(self):
        for i in range(int(self.amount / 250)):
            select = random.randint(0, len(self.nebulae_images.keys()) - 1)
            image = self.nebulae_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            nebulae = CelestialObjectStatic(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="nebulae")

    def create_asteroids(self):
        for i in range(int(self.amount / 150)):
            select = random.randint(0, len(self.asteroid_images.keys()) - 1)
            image = self.asteroid_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            asteroid = Asteroid(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="asteroid")

        for i in range(int(self.amount / 50)):
            select = random.randint(0, len(self.asteroid_images.keys()) - 1)
            image = self.asteroid_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            asteroid = Asteroid(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="asteroid", gif="asteroid.gif")

    def create_comets(self):
        for i in range(int(self.amount / 350)):
            select = random.randint(0, len(self.comet_images.keys()) - 1)
            image = self.comet_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            comet = Comet(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="comet")

    def create_quadrant(self):
        scene_width, scene_height = global_params.scene_width, global_params.scene_height

        quadrant_amount = 10
        quadrant_size_x = int(scene_width / quadrant_amount)
        quadrant_size_y = int(scene_height / quadrant_amount)

        for x in range(quadrant_amount):
            for y in range(quadrant_amount):
                w, h = quadrant_size_x, quadrant_size_y
                quadrant = CelestialObject(
                    self.win, quadrant_size_x * x, quadrant_size_y * y, w, h,
                    image=None, layer=0, parent=self, type="quadrant")

    def create_universe(self):
        self.create_stars()
        self.create_galaxys()
        self.create_nebulaes()
        self.create_comets()
        self.create_asteroids()
        # self.create_quadrant()

        self.universe = self.star + self.pulsating_star + self.galaxy + self.nebulae + self.comet + self.asteroid  # + self.quadrant
        # print("Scene Objects: ", len(self.universe))
        self.celestial_objects = {
            "star": self.star,
            "pulsating_star": self.pulsating_star,
            "galaxy": self.galaxy,
            "nebulae": self.nebulae,
            "comet": self.comet,
            "asteroid": self.asteroid
            }

    def draw__(self):
        # start_time = time.time()

        for celestial_objects in self.celestial_objects.values():
            for celestial_object in celestial_objects:
                limit_positions(celestial_object)
                celestial_object.draw()

        # for celestial_object in self.universe:
        #     limit_positions(celestial_object)
        #     celestial_object.draw()

        # endtime = time.time()
        #
        # differ = endtime - start_time
        #
        # if not differ == 0.0:
        #     if differ > self.min_draw_time:
        #         self.min_draw_time = differ
        #
        #     if differ < self.max_draw_time:
        #         self.max_draw_time = differ
        #
        #     self.average_draw_time = self.min_draw_time - self.max_draw_time
        #
        #     print (self.min_draw_time, self.average_draw_time, self.max_draw_time)
        # list: 0.00598907470703125 0.005022525787353516 0.0009665489196777344
        # dict: 0.005986452102661133 0.005039691925048828 0.0009467601776123047

    def draw(self):
        for celestial_objects in self.celestial_objects.values():
            for celestial_object in celestial_objects:
                limit_positions(celestial_object, self.screen_size)
                celestial_object.draw()

#
# pygame.init()
# width, height = 1920,1080
# win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
# bg =  Background(width, height, win)
# bg.create_stars(int(width/15))
# run = True
#
# while run:
#     for e in pygame.event.get():
#         if e.type == pygame.QUIT:
#             run = False
#
#     bg.draw()
#     pygame.display.update()
#
#
# pygame.quit()
# sys.exit()
