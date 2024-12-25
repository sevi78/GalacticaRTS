import math
import random

from pygame import Vector2, Rect

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.position_handler import get_random_pos
from source.multimedia_library.images import get_image, get_gif_frames
from source.pan_zoom_sprites.pan_zoom_collectable_item import PanZoomCollectableItem
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomImage, \
    PanZoomMovingRotatingImage, PanZoomMovingRotatingGif, PanZoomGif
from source.pan_zoom_sprites.pan_zoom_stars.pan_zoom_stars import PanZoomFlickeringStar, PanZoomPulsatingStar
from database.config.universe_config import *
from source.text.info_panel_text_generator import info_panel_text_generator

level_of_detail.debug = False
all_sprites = sprite_groups.universe


class UniverseFactory:
    def __init__(self, win: pygame.Surface, world_rect: Rect) -> None:
        self.central_compression = 1
        self.win = win
        self.amount = AMOUNT
        self.world_rect = world_rect

        # images
        self.star_images: dict[int, str] = {
            0: "star_30x30.png",
            1: "star.png",
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
            0: "asteroid.gif",
            1: "asteroid_cratered.gif",
            2: "asteroid_bennu.gif",
            3: "asteroid_hotglue.gif",
            4: "asteroid_white.gif"
            }

        self.comet_images: dict[int, str] = {
            0: "comet_90x38.png",
            1: "shooting star_60x60.png"
            }

        self.comet_gifs: dict[int, str] = {
            0: "comet.gif",
            1: "fireball.gif",
            2: "comet_blue.gif"
            }

        self.comet_directions: dict[str, tuple[float, float]] = {
            "comet_90x38.png": (-1.5, 0.5),
            "shooting star_60x60.png": (1.5, 1.0),
            "comet.gif": (-1.5, 1.0),
            "fireball.gif": (-1.5, 0.1),
            "comet_blue.gif": (-2.5, -10.0)
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

        self.galaxy_gifs: dict[int, str] = {
            0: "galaxy_blue.gif",
            # 1: "galaxy_2.gif",
            2: "spiral_galaxy.gif",
            }

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

    def select_random_image(self, image_dict: dict[int, str], index: int) -> str:
        """
        Selects an image from the provided dictionary based on the given index.
        If the index is not a key in the dictionary, a random image is selected.

        Args:
            image_dict (dict[int, str]): A dictionary where keys are integers
            and values are image file names.
            index (int): The index of the desired image.

        Returns:
            str: The name of the selected image.
        """
        # Check if the index is a valid key in the image dictionary
        if index in image_dict:
            return image_dict[index]
        else:
            # If not, select a random image from the dictionary
            return random.choice(list(image_dict.values()))

    def create_artefacts(self, amount, **kwargs):  # orig
        collectable_items = kwargs.get("collectable_items", None)

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

        all_specials = ["food * 1.5", "energy * 1.5", "minerals * 1.5", "water * 1.5", "technology * 1.5",
                        "buildings_max + 1"]

        if collectable_items:
            for collectable_item, dict_ in collectable_items.items():
                if dict_["image_name"].endswith(".png"):
                    relative_gif_size = 1.0
                else:
                    relative_gif_size = 0.4

                artefact = PanZoomCollectableItem(
                        config.win,
                        x=dict_["world_x"],
                        y=dict_["world_y"],
                        width=dict_["world_width"],
                        height=dict_["world_height"],
                        image_name=dict_["image_name"],
                        is_sub_widget=False,
                        transparent=True,
                        tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
                        infotext=info_panel_text_generator.create_info_panel_collectable_item_text(
                                dict_["resources"], dict_["specials"]),
                        moveable=True,
                        resources=dict_["resources"],
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
                x, y = get_random_pos(self.world_rect, self.central_compression)
                image_name = random.choice(self.artefact_images)
                size = self.artefact_sizes[image_name]
                width, height = size
                selected_resources = select_resources()
                specials = [random.choice(all_specials)]

                artefact = PanZoomCollectableItem(
                        config.win,
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        image_name=image_name,
                        is_sub_widget=False,
                        transparent=True,
                        tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
                        infotext=info_panel_text_generator.create_info_panel_collectable_item_text(selected_resources, specials),
                        moveable=True,
                        resources=selected_resources,
                        specials=specials,
                        parent=self,
                        group="collectable_items",
                        gif="sphere.gif",
                        align_image="center",
                        outline_thickness=1,
                        outline_threshold=0)

            # create spherical, animated artefacts
            for i in range(int(amount / 2)):
                x, y = get_random_pos(self.world_rect, self.central_compression)
                selected_resources = select_resources()
                specials = [random.choice(all_specials)]
                artefact = PanZoomCollectableItem(
                        config.win,
                        x=x, y=y, width=60, height=60,
                        pan_zoom=pan_zoom_handler,
                        image_name="sphere.gif",
                        is_sub_widget=False,
                        transparent=True,
                        tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
                        infotext=info_panel_text_generator.create_info_panel_collectable_item_text(selected_resources, specials),
                        moveable=True,
                        resources=selected_resources,
                        specials=specials,
                        parent=self,
                        group="collectable_items",
                        relative_gif_size=0.4,
                        align_image="center",
                        outline_thickness=1,
                        outline_threshold=0)

    def create_stars(self) -> None:
        # star images
        for i in range(max(1, int(self.amount / STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.world_rect, self.central_compression)

            image_name = random.choice(self.star_images)
            image = get_image(image_name)
            # w = image.get_rect().width
            # h = image.get_rect().height
            w, h = 30, 30
            r = random.randint(0, 360)

            self.star.append(PanZoomImage(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=h,
                    layer=STAR_LAYER,
                    group=all_sprites,
                    image_name=image_name,
                    image_alpha=None,
                    rotation_angle=r
                    ))

        # flickering stars
        for i in range(max(1, int(self.amount / FLICKERING_STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.world_rect, self.central_compression)
            w = random.randint(1, 10)

            self.star.append(PanZoomFlickeringStar(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=w,
                    layer=STAR_LAYER,
                    group=all_sprites))

        # puslating stars
        for i in range(max(1, int(self.amount / PULSATING_STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.world_rect, self.central_compression)
            w = 1

            self.star.append(PanZoomPulsatingStar(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=2,
                    world_height=2,
                    layer=STAR_LAYER,
                    group=all_sprites))

    def create_galaxys(self) -> None:
        for i in range(max(1, int(self.amount / GALAXY_DIVIDE_FACTOR))):
            # image_name = random.choice(self.galaxy_images)
            image_name = self.select_random_image(self.galaxy_images, i)
            image = get_image(image_name)
            w = int(image.get_rect().width / 2)
            h = int(image.get_rect().height / 2)
            x, y = get_random_pos(self.world_rect, self.central_compression)
            r = random.randint(0, 360)

            self.galaxy.append(PanZoomImage(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=h,
                    layer=GALAXY_LAYER,
                    group=all_sprites,
                    image_name=image_name,
                    image_alpha=GALAXY_IMAGE_ALPHA,
                    rotation_angle=r,
                    initial_rotation=True
                    ))

        # galaxy gifs
        for i in range(max(1, int(self.amount / GALAXY_GIF_DIVIDE_FACTOR))):
            image_name = self.select_random_image(self.galaxy_gifs, i)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            gif_frames = get_gif_frames(image_name)
            max_gif_frame = len(gif_frames) - 1

            self.galaxy.append(PanZoomGif(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=h,
                    layer=GALAXY_LAYER,
                    group=all_sprites,
                    gif_name=image_name,
                    gif_index=random.randint(0, max_gif_frame),
                    gif_animation_time=None,
                    loop_gif=True,
                    kill_after_gif_loop=False,
                    image_alpha=None,
                    rotation_angle=0
                    ))

    def create_nebulaes(self) -> None:
        for i in range(max(1, int(self.amount / NEBULAE_DIVIDE_FACTOR))):
            # image_name = random.choice(self.nebulae_images)
            image_name = self.select_random_image(self.nebulae_images, i)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            r = random.randint(0, 360)

            self.nebulae.append(PanZoomImage(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=h,
                    layer=NEBULAE_LAYER,
                    group=all_sprites,
                    image_name=image_name,
                    image_alpha=NEBULAE_IMAGE_ALPHA,
                    rotation_angle=r,
                    initial_rotation=True
                    ))

    def create_asteroids(self) -> None:
        # asteroid images
        for i in range(max(1, int(self.amount / ASTEROID_DIVIDE_FACTOR))):
            image_name = self.select_random_image(self.asteroid_images, i)
            image = get_image(image_name)
            w = image.get_rect().width * 3
            h = image.get_rect().height * 3
            x, y = get_random_pos(self.world_rect, self.central_compression)
            r = random.randint(0, 360)
            dx, dy = random.randint(-360, 360), random.randint(-360, 360)
            movement_speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
            rotation_speed = random.uniform(-ASTEROID_MAX_ROTATION, ASTEROID_MAX_ROTATION)

            self.asteroid.append(PanZoomMovingRotatingImage(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=h,
                    layer=ASTEROID_LAYER,
                    group=all_sprites,
                    image_name=image_name,
                    image_alpha=None,
                    rotation_angle=r,
                    rotation_speed=rotation_speed,
                    movement_speed=movement_speed,
                    direction=Vector2(dx, dy),
                    world_rect=self.world_rect
                    ))

        # asteroid gifs
        for i in range(max(1, int(self.amount / ASTEROID_GIF_DIVIDE_FACTOR))):
            # image_name = random.choice(self.asteroid_gifs)
            image_name = self.select_random_image(self.asteroid_gifs, i)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            gif_frames = get_gif_frames(image_name)
            max_gif_frame = len(gif_frames) - 1
            r = random.randint(0, 360)
            dx, dy = random.randint(-360, 360), random.randint(-360, 360)
            movement_speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)

            self.asteroid.append(PanZoomMovingRotatingGif(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=h,
                    layer=ASTEROID_LAYER,
                    group=all_sprites,
                    gif_name=image_name,
                    gif_index=random.randint(0, max_gif_frame),
                    gif_animation_time=None,
                    loop_gif=True,
                    kill_after_gif_loop=False,
                    image_alpha=None,
                    rotation_angle=r,
                    movement_speed=movement_speed,
                    direction=Vector2(dx, dy),
                    world_rect=self.world_rect
                    ))

    def create_comets(self) -> None:
        # comet images
        for i in range(max(1, int(self.amount / COMET_DIVIDE_FACTOR))):
            image_name = self.select_random_image(self.comet_images, i)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            movement_speed = random.uniform(0.05, 0.5)

            self.comet.append(PanZoomMovingRotatingImage(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=h,
                    layer=COMET_LAYER,
                    group=all_sprites,
                    image_name=image_name,
                    image_alpha=None,
                    rotation_angle=0,
                    rotation_speed=0,
                    movement_speed=movement_speed,
                    direction=Vector2(self.comet_directions[image_name]),
                    world_rect=self.world_rect
                    ))

        # comet gifs
        for i in range(max(1, int(self.amount / COMET_DIVIDE_FACTOR))):
            # image_name = random.choice(self.comet_gifs)
            image_name = self.select_random_image(self.comet_gifs, i)
            image = get_image(image_name)
            w = image.get_rect().width
            h = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            gif_frames = get_gif_frames(image_name)
            max_gif_frame = len(gif_frames) - 1

            self.comet.append(PanZoomMovingRotatingGif(
                    win=self.win,
                    world_x=x,
                    world_y=y,
                    world_width=w,
                    world_height=h,
                    layer=COMET_LAYER,
                    group=all_sprites,
                    gif_name=image_name,
                    gif_index=random.randint(0, max_gif_frame),
                    gif_animation_time=None,
                    loop_gif=True,
                    kill_after_gif_loop=False,
                    image_alpha=None,
                    rotation_angle=0,
                    movement_speed=random.uniform(0.01, 0.5),
                    direction=Vector2(self.comet_directions[image_name]),
                    world_rect=self.world_rect)
                    )

    def create_universe(self, world_rect: Rect = WORLD_RECT, collectable_items_amount=0, **kwargs) -> None:
        collectable_items = kwargs.get("collectable_items", None)
        self.world_rect = world_rect
        self.create_stars()
        self.create_galaxys()
        self.create_nebulaes()
        self.create_comets()
        self.create_asteroids()
        self.create_artefacts(collectable_items_amount, collectable_items=collectable_items)

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

        # Print out the counts of objects and keys in the corresponding dictionaries
        for name, obj_list in self.celestial_objects.items():
            print(f"{name.capitalize()} count: {len(obj_list)}")  # Length of the list
            if name == "star":
                print(f"Star images created: {len(self.star)} of {len(self.star_images)}")  # Length of the dict keys
            elif name == "pulsating_star":
                print(f"Pulsating star images created: {len(self.pulsating_star)} of {len(self.star_images)}")
            elif name == "galaxy":
                print(f"Galaxy images created: {len(self.galaxy)} of {len(self.galaxy_images)}")
            elif name == "nebulae":
                print(f"Nebulae images created: {len(self.nebulae)} of {len(self.nebulae_images)}")
            elif name == "comet":
                print(f"Comet images created: {len(self.comet)} of {len(self.comet_images)}")
            elif name == "asteroid":
                print(f"Asteroid images created: {len(self.asteroid)} of {len(self.asteroid_images)}")
                print(f"Asteroid GIFs created: {len([gif for gif in self.asteroid if gif.image_name in self.asteroid_gifs.values()])} of {len(self.asteroid_gifs)}")
            elif name == "collectable_item":
                print(f"Collectable items created: {len(self.artefact)} of {len(self.artefact_images)}")

    def delete_universe(self) -> None:
        for sprite in self.universe:
            sprite.kill()
        self.universe.clear()
        all_sprites.empty()

        # all_widgets = WidgetHandler.get_all_widgets()
        # celestials = [i for i in all_widgets if issubclass(i.__class__, (CelestialObject, CelestialObjectStatic))]
        # for i in celestials:
        #     WidgetHandler.remove_widget(i)

    #
    def delete_artefacts(self) -> None:
        for i in sprite_groups.collectable_items.sprites():
            i.end_object()


def main():
    pygame.init()
    width, height = 1820, 1080
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    universe_factory = UniverseFactory(screen, WORLD_RECT)
    universe_factory.amount = int(math.sqrt(math.sqrt(universe_factory.world_rect.width)) * UNIVERSE_DENSITY)
    universe_factory.create_universe(WORLD_RECT, collectable_items=10)

    pan_zoom_handler.zoom_min = 1000 / WORLD_RECT.width

    running = True
    while running:
        events = pygame.event.get()
        pan_zoom_handler.listen(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    universe_factory.delete_universe()

            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.update()
        pygame.display.set_caption(f"Universe Factory: {clock.get_fps()} with {len(universe_factory.universe)} objects")
        clock.tick(60)
        # print (f"zoom: {pan_zoom_handler.zoom},paan_zoom_handler.zoom_min: {pan_zoom_handler.zoom_min}, pan_zoom_handler.zoom_max: {pan_zoom_handler.zoom_max}")

    pygame.quit()


if __name__ == "__main__":
    main()

universe_factory = UniverseFactory(config.win, pygame.Rect(0, 0, config.scene_width, config.scene_height))
