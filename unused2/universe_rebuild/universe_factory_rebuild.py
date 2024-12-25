import random

from source.gui.lod import level_of_detail
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.position_handler import get_random_pos
from source.multimedia_library.images import get_image, get_gif_frames
from source.pan_zoom_sprites.pan_zoom_collectable_item import PanZoomCollectableItem
from source.test.universe_rebuild.celestial_object_rebuild import PulsatingStar, \
    CelestialObject, MovingCelestialObject, FlickeringStar
from database.config.universe_config import *
from source.text.info_panel_text_generator import info_panel_text_generator

level_of_detail.debug = True


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

    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, layer: int) -> None:
        self.central_compression = 1
        self.win = win
        self.layer = layer
        self.amount = AMOUNT

        # define borders
        self.left_end = x
        self.right_end = width
        self.top_end = y
        self.bottom_end = height
        self.center = None

        # images
        self.star_images: dict[int, str] = {
            0: "star_30x30.png",
            1: "star_50x50.png",
            2: "star1_50x50.png",
            3: "star2_100x100.png",
            4: "star_white.png",
            5: "star_white2.png",
            6: "star_turk.png",
            7: "star_yellow.png",
            8: "star_red.png"
            }

        self.asteroid_images: dict[int, str] = {
            0: "asteroid_40x33.png",
            1: "meteor_50x50.png",
            2: "meteor1_50x50.png",
            3: "moon_60x57.png"
            }

        self.asteroid_gifs: dict[int, str] = {
            0: "asteroid.gif"
            }

        self.comet_images: dict[int, str] = {
            0: "comet_90x38.png",
            1: "shooting star_60x60.png"
            }

        self.comet_gifs: dict[int, str] = {
            0: "comet.gif",
            1: "fireball.gif"
            }

        self.comet_directions: dict[str, tuple[float, float]] = {
            "comet_90x38.png": (-1.5, 0.5),
            "shooting star_60x60.png": (1.5, 1.0),
            "comet.gif": (-1.5, 1.0),
            "fireball.gif": (-1.5, 0.1)
            }

        self.comet_relative_gif_sizes: dict[str, float] = {
            "comet_90x38.png": 1.0,
            "shooting star_60x60.png": 1.5,
            "comet.gif": 0.5,
            "fireball.gif": 1.0
            }

        self.nebulae_images: dict[int, str] = {
            0: "nebulae_300x300.png"
            }

        self.galaxy_images: dict[int, str] = {
            0: "galaxy_.png",
            1: "galaxy3_small.png",
            2: "Black_eye_galaxy.png",
            3: "galaxy_2.png",
            4: "galaxy_3.png",

            }

        self.spiral_galaxies = ["galaxy_2.png", "galaxy_3.png"]

        self.artefact_images = ["artefact1_60x31.png",
                                "meteor_50x50.png",
                                "meteor_60x83.png",
                                "meteor1_50x50.png"
                                ]
        self.artefact_sizes = {
            "artefact1_60x31.png": (60, 31),
            "meteor_50x50.png": (50, 50),
            "meteor_60x83.png": (int(60) * .5, int(83) * .5),
            "meteor1_50x50.png": (50, 50)
            }

        # drawing lists
        self.star = []
        self.pulsating_star = []
        self.flickering_star = []
        self.asteroid = []
        self.nebulae = []
        self.galaxy = []
        self.comet = []
        self.artefact = []
        self.universe = []

        # create universe
        self.celestial_objects = {}

    def create_artefacts(self, amount: int, **kwargs) -> None:
        collectable_items = kwargs.get("collectable_items", None)

        def select_resources() -> dict:
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

        all_specials = ["food * 1.5", "energy * 1.5", "minerals * 1.5", "water * 1.5", "technology * 1.5",
                        "buildings_max + 1"]

        if collectable_items:
            for collectable_item, dict_ in collectable_items.items():
                if dict_["image_name"].endswith(".png"):
                    relative_gif_size = 1.0
                else:
                    relative_gif_size = 0.4

                artefact = PanZoomCollectableItem(
                        self.win,
                        x=dict_["world_x"],
                        y=dict_["world_y"],
                        width=dict_["world_width"],
                        height=dict_["world_height"],
                        pan_zoom=pan_zoom_handler,
                        image_name=dict_["image_name"],
                        is_sub_widget=False,
                        transparent=True,
                        tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
                        infotext=info_panel_text_generator.create_info_panel_collectable_item_text(
                                dict_["resources"], dict_["specials"]),
                        moveable=True,
                        energy=dict_["resources"]["energy"],
                        minerals=dict_["resources"]["minerals"],
                        food=dict_["resources"]["food"],
                        technology=dict_["resources"]["technology"],
                        water=dict_["resources"]["water"],
                        specials=dict_["specials"],
                        parent=self,
                        group="collectable_items",
                        relative_gif_size=relative_gif_size,
                        align_image="center",
                        outline_thickness=1,
                        outline_threshold=0)

        else:
            # create random static artefacts
            for i in range(int(amount / 2)):
                x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)
                image_name = random.choice(self.artefact_images)
                size = self.artefact_sizes[image_name]
                width, height = size
                selected_resources = select_resources()
                specials = [random.choice(all_specials)]

                self.artefact.append(PanZoomCollectableItem(
                        self.win,
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        pan_zoom=pan_zoom_handler,
                        image_name=image_name,
                        is_sub_widget=False,
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
                        outline_threshold=0))

            # create spherical, animated artefacts
            for i in range(int(amount / 2)):
                x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)
                selected_resources = select_resources()
                specials = [random.choice(all_specials)]
                self.artefact.append(PanZoomCollectableItem(
                        self.win,
                        x=x, y=y, width=60, height=60,
                        pan_zoom=pan_zoom_handler,
                        image_name="sphere.gif",
                        is_sub_widget=False,
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
                        relative_gif_size=0.4,
                        align_image="center",
                        outline_thickness=1,
                        outline_threshold=0))

    def create_stars(self) -> None:
        # star images
        for i in range(max(1, int(self.amount / STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            image_name = random.choice(self.star_images)
            image = get_image(image_name)
            # w = image.get_rect().width
            # h = image.get_rect().height
            w, h = 30, 30

            self.star.append(CelestialObject(
                    self.win,
                    x,
                    y,
                    w,
                    h,
                    pan_zoom_handler,
                    image_name,
                    layer=self.layer,
                    parent=self,
                    type="star",
                    initial_rotation=random.randint(0, 360)))

        # flickering stars
        for i in range(max(1, int(self.amount / FLICKERING_STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)
            w = random.randint(1, 10)

            self.star.append(FlickeringStar(
                    self.win,
                    x,
                    y,
                    w,
                    w,
                    pan_zoom_handler,
                    "",
                    layer=self.layer,
                    parent=self,
                    type="flickering_star"))

        # puslating stars
        for i in range(max(1, int(self.amount / PULSATING_STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)
            w = 1

            self.star.append(PulsatingStar(
                    self.win,
                    x,
                    y,
                    w,
                    w,
                    pan_zoom_handler,
                    "",
                    layer=self.layer,
                    parent=self,
                    type="pulsating_star"))

    def create_galaxys(self) -> None:
        for i in range(max(1, int(self.amount / GALAXY_DIVIDE_FACTOR))):
            image_name = random.choice(self.galaxy_images)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            if image_name in self.spiral_galaxies:
                self.galaxy.append(MovingCelestialObject(
                        self.win,
                        x,
                        y,
                        w,
                        h,
                        pan_zoom_handler,
                        image_name,
                        align_image="center",
                        layer=self.layer,
                        parent=self,
                        type="galaxy",
                        initial_rotation=random.randint(0, 360),
                        # image_alpha=GALAXY_IMAGE_ALPHA,
                        enable_rotate=True,
                        speed=0,
                        rotation_speed=random.uniform(0.001, 0.01)))

            else:
                self.galaxy.append(CelestialObject(
                        self.win,
                        x,
                        y,
                        w,
                        h,
                        pan_zoom_handler,
                        image_name,
                        layer=self.layer,
                        parent=self,
                        type="galaxy",
                        initial_rotation=random.randint(0, 360),
                        image_alpha=GALAXY_IMAGE_ALPHA))

    def create_nebulaes(self) -> None:
        for i in range(max(1, int(self.amount / NEBULAE_DIVIDE_FACTOR))):
            image_name = random.choice(self.nebulae_images)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            self.nebulae.append(CelestialObject(
                    self.win,
                    x,
                    y,
                    w,
                    h,
                    pan_zoom_handler,
                    image_name,
                    layer=self.layer,
                    parent=self,
                    type="nebulae",
                    initial_rotation=random.randint(0, 360),
                    image_alpha=NEBULAE_IMAGE_ALPHA))

    def create_asteroids(self) -> None:
        # asteroid images
        for i in range(max(1, int(self.amount / ASTEROID_DIVIDE_FACTOR))):
            image_name = random.choice(self.asteroid_images)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            self.asteroid.append(MovingCelestialObject(
                    self.win,
                    x,
                    y,
                    w,
                    h,
                    pan_zoom_handler,
                    image_name,
                    layer=self.layer,
                    parent=self,
                    type="asteroid",
                    enable_rotate=True,
                    speed=random.uniform(0.01, 0.5), ))

        # asteroid gifs
        for i in range(max(1, int(self.amount / ASTEROID_GIF_DIVIDE_FACTOR))):
            image_name = random.choice(self.asteroid_gifs)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            gif_frames = get_gif_frames(image_name)
            max_gif_frame = len(gif_frames) - 1

            self.asteroid.append(MovingCelestialObject(
                    self.win,
                    x,
                    y,
                    w,
                    h,
                    pan_zoom_handler,
                    image_name,
                    layer=self.layer,
                    parent=self,
                    type="asteroid",
                    relative_gif_size=0.15,
                    gif_index=random.randint(0, max_gif_frame)))

    def create_comets(self) -> None:
        # comet images
        for i in range(max(1, int(self.amount / COMET_DIVIDE_FACTOR))):
            image_name = random.choice(self.comet_images)
            image = get_image(image_name)

            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            self.comet.append(MovingCelestialObject(
                    self.win,
                    x,
                    y,
                    w,
                    h,
                    pan_zoom_handler,
                    image_name,
                    layer=self.layer,
                    parent=self,
                    type="comet",
                    direction=self.comet_directions[image_name],
                    speed=random.uniform(0.01, 0.5),
                    relative_gif_size=self.comet_relative_gif_sizes[image_name]))

        # comet gifs
        for i in range(max(1, int(self.amount / COMET_DIVIDE_FACTOR))):
            image_name = random.choice(self.comet_gifs)
            image = get_image(image_name)

            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.left_end, self.right_end, self.top_end, self.bottom_end, self.central_compression)

            gif_frames = get_gif_frames(image_name)
            max_gif_frame = len(gif_frames) - 1

            self.comet.append(MovingCelestialObject(
                    self.win,
                    x,
                    y,
                    w,
                    h,
                    pan_zoom_handler,
                    image_name,
                    layer=self.layer,
                    parent=self,
                    type="comet",
                    direction=self.comet_directions[image_name],
                    speed=random.uniform(0.01, 0.5),
                    gif_index=random.randint(0, max_gif_frame),
                    relative_gif_size=self.comet_relative_gif_sizes[image_name]))

    def create_universe(self, x: int, y: int, width: int, height: int, collectable_items_amount: int, **kwargs) -> None:
        collectable_items = kwargs.get("collectable_items", None)
        self.left_end = LEFT_END
        self.top_end = TOP_END
        self.right_end = RIGHT_END
        self.bottom_end = BOTTOM_END
        self.center = CENTER

        self.create_stars()
        self.create_galaxys()
        # self.create_nebulaes()
        self.create_comets()
        self.create_asteroids()
        # self.create_artefacts(x, y, width, height, collectable_items_amount, collectable_items=collectable_items)

        self.universe = self.star + self.pulsating_star + self.galaxy + self.nebulae + self.comet + self.asteroid + self.artefact

        self.celestial_objects = {
            "star": self.star,
            "pulsating_star": self.pulsating_star,
            "galaxy": self.galaxy,
            "nebulae": self.nebulae,
            "comet": self.comet,
            "asteroid": self.asteroid,
            "collectable_item": self.artefact
            }

    # def delete_universe(self)->None:
    #     all_widgets = WidgetHandler.get_all_widgets()
    #     celestials = [i for i in all_widgets if issubclass(i.__class__, (CelestialObject, CelestialObjectStatic))]
    #     for i in celestials:
    #         WidgetHandler.remove_widget(i)
    #
    # def delete_artefacts(self)->None:
    #     for i in sprite_groups.collectable_items.sprites():
    #         i.end_object()


def main():
    pygame.init()
    width, height = 1820, 1080
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    universe_factory = UniverseFactory(screen, 0, 0, width, height, layer=0)
    # universe_factory.amount = int(math.sqrt(math.sqrt(WORLD_WIDTH)) * UNIVERSE_DENSITY)
    universe_factory.create_universe(0, 0, WORLD_WIDTH, WORLD_HEIGHT, 10)

    running = True
    while running:
        events = pygame.event.get()
        pan_zoom_handler.listen(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for obj in universe_factory.universe:
                        obj.use_image_cache = not obj.use_image_cache

            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for obj in universe_factory.universe:
            obj.debug = False
            obj.update()
            obj.draw()

        pygame.display.flip()
        pygame.display.set_caption(f"Universe Factory: {clock.get_fps()}")
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
