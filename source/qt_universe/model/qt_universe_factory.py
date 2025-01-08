import math


from source.handlers.color_handler import get_average_color
from source.handlers.position_handler import get_random_pos
from source.multimedia_library.images import get_image, get_gif_frames, get_image_names_from_folder
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_model_config.qt_config import POINTS_AMOUNT
from source.qt_universe.model.qt_model_config.qt_universe_config import *
from source.qt_universe.model.qt_object_factory import *
from source.text.info_panel_text_generator import info_panel_text_generator


class ImageProvider:
    def __init__(self):
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

        self.collectable_item_images = {
            0:"artefact1_60x31.png",
            1:"meteor_50x50.png",
            2:"meteor_60x83.png",
            3:"meteor1_50x50.png"}

        self.collectable_item_gifs = {
            0:"sphere.gif"
            }

        # self.artefact_sizes = {
        #     "artefact1_60x31.png": (60, 31),
        #     "meteor_50x50.png": (50, 50),
        #     "meteor_60x83.png": (int(60) * .5, int(83) * .5),
        #     "meteor1_50x50.png": (50, 50),
        #     "sphere.gif": (100, 100)
        #     }

        self.planet_images: dict[int, str] = {
            0: "GIN V.S.X.O._150x150.png",
            1: "Helios 12_150x150.png",
            2: "Kepler-22b_150x150.png",
            3: "P0101_150x150.png",
            4: "ur-anus_150x150.png",
            }

        self.planet_gifs: dict[int, str] = {
            0: "Io.gif",
            1: "moon.gif",
            2: "moon1.gif",
            3: "moon_alien.gif",
            4: "venus_slow.gif",
            }

        self.sun_images = {get_image_names_from_folder("suns").index(i): i for i in get_image_names_from_folder("suns")}
        self.sun_gifs = {get_image_names_from_folder("gifs").index(i): i for i in get_image_names_from_folder("gifs") if
                         i.startswith("sun")}

        self.gif_frames = {v: get_gif_frames(v) for d in
                           (self.asteroid_gifs, self.comet_gifs, self.galaxy_gifs, self.planet_gifs, self.sun_gifs,self.collectable_item_gifs ) for
                           v in d.values()}

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


class UniverseFactory(ImageProvider):
    def __init__(self, win: pygame.Surface, world_rect: Rect, game_object_manager) -> None:
        super().__init__()
        self.game_object_manager = game_object_manager
        self.central_compression = 1
        self.win = win
        self.amount = POINTS_AMOUNT
        self.world_rect = world_rect

    def create_artefacts_(self, amount, **kwargs):  # orig
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

    def create_collectable_items(self):
        # artefacts images
        for i in range(max(1, int(self.amount / COLLECTABLE_ITEM_DIVIDE_FACTOR))):
            image_name = self.select_random_image(self.collectable_item_images, i)
            image = get_image(image_name)
            image_alpha = None
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width * 3
            height = image.get_rect().height * 3
            x, y = get_random_pos(self.world_rect, self.central_compression)
            rotation_angle = random.randint(0, 360)
            dx, dy = random.randint(-360, 360), random.randint(-360, 360)
            movement_speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
            rotation_speed = random.uniform(-ASTEROID_MAX_ROTATION, ASTEROID_MAX_ROTATION)
            layer = COLLECTABLE_ITEM_LAYER
            id_ = len(self.game_object_manager.all_objects)
            direction = Vector2(dx, dy)
            wrap_around = True
            type_ = "collectable_item_image"

            new_object = create_qt_moving_image(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    image_name=image_name,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle,
                    rotation_speed=rotation_speed,
                    movement_speed=movement_speed,
                    direction=direction,
                    wrap_around=wrap_around
                    )

            self.game_object_manager.add_object(new_object)

        # artefacts gifs
        for i in range(max(1, int(self.amount / COLLECTABLE_ITEM_DIVIDE_FACTOR/2))):
            # image_name = random.choice(self.asteroid_gifs)
            image_name = self.select_random_image(self.collectable_item_gifs, i)
            image = get_image(image_name)
            image_alpha = None
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width
            height = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            gif_frames = self.gif_frames[image_name]
            max_gif_frame = len(gif_frames) - 1
            gif_index = random.randint(0, max_gif_frame)
            gif_animation_time = None
            loop_gif = True
            kill_after_gif_loop = False
            rotation_angle = random.randint(0, 360)
            rotation_speed = 0
            dx, dy = random.randint(-360, 360), random.randint(-360, 360)
            movement_speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
            direction = Vector2(dx, dy)

            type_ = "collectable_item_gif"
            layer = COLLECTABLE_ITEM_LAYER
            id_ = len(self.game_object_manager.all_objects)
            wrap_around = True

            new_object = create_qt_moving_gif(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    gif_name=image_name,
                    gif_index=gif_index,
                    gif_animation_time=gif_animation_time,
                    loop_gif=loop_gif,
                    kill_after_gif_loop=kill_after_gif_loop,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle,
                    rotation_speed=rotation_speed,
                    movement_speed=movement_speed,
                    direction=direction,
                    wrap_around=wrap_around
                    )
            self.game_object_manager.add_object(new_object)

    def create_stars(self) -> None:
        start_time = time.time()
        # star images
        for i in range(max(1, int(self.amount / STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.world_rect, self.central_compression)
            image_name = self.select_random_image(self.star_images, i)
            image = get_image(image_name)
            image_alpha = None
            color = get_average_color(image, consider_alpha=True)
            width, height = 30, 30
            rotation_angle = random.randint(0, 360)
            id_ = len(self.game_object_manager.all_objects)
            layer = STAR_LAYER
            type_ = "star_image"

            new_object = create_qt_image(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    image_name=image_name,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle
                    )

            self.game_object_manager.add_object(new_object)

        # flickering stars
        for i in range(max(1, int(self.amount / FLICKERING_STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.world_rect, self.central_compression)
            width = random.randint(1, 10)
            height = width
            colors = [(random.randint(0, config.star_brightness), random.randint(0, config.star_brightness),
                       random.randint(0, config.star_brightness)) for _ in range(10)]

            rotation_angle = random.randint(0, 360)
            id_ = len(self.game_object_manager.all_objects)
            layer = STAR_LAYER
            type_ = "flickering_star"

            new_object = create_qt_flickering_star(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    colors=colors,
                    type_=type_
                    )

            self.game_object_manager.add_object(new_object)

        # puslating stars
        for i in range(max(1, int(self.amount / PULSATING_STAR_DIVIDE_FACTOR))):
            x, y = get_random_pos(self.world_rect, self.central_compression)
            width = 1
            height = width
            layer = STAR_LAYER
            id_ = len(self.game_object_manager.all_objects)
            type_ = "pulsating_star"

            new_object = create_qt_pulsating_star(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    type_=type_
                    )

            self.game_object_manager.add_object(new_object)

        end_time = time.time()
        duration = end_time - start_time
        print(f"create_stars took{duration:.6f} seconds")

    def create_galaxys(self) -> None:
        start_time = time.time()

        for i in range(max(1, int(self.amount / GALAXY_DIVIDE_FACTOR))):
            # image_name = random.choice(self.galaxy_images)
            image_name = self.select_random_image(self.galaxy_images, i)
            image = get_image(image_name)
            image_alpha = GALAXY_IMAGE_ALPHA
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width
            height = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            rotation_angle = random.randint(0, 360)
            id_ = len(self.game_object_manager.all_objects)
            type_ = "qt_image"
            layer = GALAXY_LAYER

            new_object = create_qt_image(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    image_name=image_name,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle
                    )

            self.game_object_manager.add_object(new_object)

        # galaxy gifs
        for i in range(max(1, int(self.amount / GALAXY_GIF_DIVIDE_FACTOR))):
            image_name = self.select_random_image(self.galaxy_gifs, i)
            image = get_image(image_name)
            image_alpha = GALAXY_IMAGE_ALPHA
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width
            height = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            rotation_angle = random.randint(0, 360)
            gif_frames = self.gif_frames[image_name]
            max_gif_frame = len(gif_frames) - 1
            id_ = len(self.game_object_manager.all_objects)
            layer = GALAXY_LAYER
            gif_index = random.randint(0, max_gif_frame)
            gif_animation_time = None
            loop_gif = True
            kill_after_gif_loop = False
            type_ = "qt_gif"

            new_object = create_qt_gif(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    gif_name=image_name,
                    gif_index=gif_index,
                    gif_animation_time=gif_animation_time,
                    loop_gif=loop_gif,
                    kill_after_gif_loop=kill_after_gif_loop,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle
                    )

            self.game_object_manager.add_object(new_object)

        end_time = time.time()
        duration = end_time - start_time
        print(f"create_galaxys took{duration:.6f} seconds")

    def create_nebulaes(self) -> None:
        start_time = time.time()
        for i in range(max(1, int(self.amount / NEBULAE_DIVIDE_FACTOR))):
            # image_name = random.choice(self.nebulae_images)
            image_name = self.select_random_image(self.nebulae_images, i)
            image = get_image(image_name)
            image_alpha = NEBULAE_IMAGE_ALPHA
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width
            height = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            rotation_angle = random.randint(0, 360)
            id_ = len(self.game_object_manager.all_objects)
            layer = NEBULAE_LAYER
            type_ = "qt_image"

            new_object = create_qt_image(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    image_name=image_name,
                    image_alpha=image_alpha,
                    color=color,
                    type_="qt_image",
                    rotation_angle=rotation_angle
                    )

            self.game_object_manager.add_object(new_object)

        end_time = time.time()
        duration = end_time - start_time
        print(f"create_nebulaes took{duration:.6f} seconds")

    def create_asteroids(self) -> None:
        start_time = time.time()
        # asteroid images
        for i in range(max(1, int(self.amount / ASTEROID_DIVIDE_FACTOR))):
            image_name = self.select_random_image(self.asteroid_images, i)
            image = get_image(image_name)
            image_alpha = None
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width * 3
            height = image.get_rect().height * 3
            x, y = get_random_pos(self.world_rect, self.central_compression)
            rotation_angle = random.randint(0, 360)
            dx, dy = random.randint(-360, 360), random.randint(-360, 360)
            movement_speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
            rotation_speed = random.uniform(-ASTEROID_MAX_ROTATION, ASTEROID_MAX_ROTATION)
            layer = ASTEROID_LAYER
            id_ = len(self.game_object_manager.all_objects)
            direction = Vector2(dx, dy)
            wrap_around = True
            type_ = "asteroid_image"

            new_object = create_qt_moving_image(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    image_name=image_name,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle,
                    rotation_speed=rotation_speed,
                    movement_speed=movement_speed,
                    direction=direction,
                    wrap_around=wrap_around
                    )

            self.game_object_manager.add_object(new_object)

        # asteroid gifs
        for i in range(max(1, int(self.amount / ASTEROID_GIF_DIVIDE_FACTOR))):
            # image_name = random.choice(self.asteroid_gifs)
            image_name = self.select_random_image(self.asteroid_gifs, i)
            image = get_image(image_name)
            image_alpha = None
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width
            height = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            gif_frames = self.gif_frames[image_name]
            max_gif_frame = len(gif_frames) - 1
            gif_index = random.randint(0, max_gif_frame)
            gif_animation_time = None
            loop_gif = True
            kill_after_gif_loop = False
            rotation_angle = random.randint(0, 360)
            rotation_speed = 0
            dx, dy = random.randint(-360, 360), random.randint(-360, 360)
            movement_speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
            direction = Vector2(dx, dy)

            type_ = "asteroid_gif"
            layer = ASTEROID_LAYER
            id_ = len(self.game_object_manager.all_objects)
            wrap_around = True

            new_object = create_qt_moving_gif(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    gif_name=image_name,
                    gif_index=gif_index,
                    gif_animation_time=gif_animation_time,
                    loop_gif=loop_gif,
                    kill_after_gif_loop=kill_after_gif_loop,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle,
                    rotation_speed=rotation_speed,
                    movement_speed=movement_speed,
                    direction=direction,
                    wrap_around=wrap_around
                    )

            self.game_object_manager.add_object(new_object)

        end_time = time.time()
        duration = end_time - start_time
        print(f"create_asteroids took{duration:.6f} seconds")

    def create_comets(self) -> None:
        start_time = time.time()
        # comet images
        for i in range(max(1, int(self.amount / COMET_DIVIDE_FACTOR))):
            image_name = self.select_random_image(self.comet_images, i)
            image = get_image(image_name)
            image_alpha = None
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width
            height = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            movement_speed = random.uniform(0.05, 0.5)
            layer = COMET_LAYER
            id_ = len(self.game_object_manager.all_objects)
            type_ = "comet_image"
            rotation_angle = 0
            rotation_speed = 0
            direction = Vector2(self.comet_directions[image_name])
            wrap_around = True

            new_object = create_qt_moving_image(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    image_name=image_name,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle,
                    rotation_speed=rotation_speed,
                    movement_speed=movement_speed,
                    direction=direction,
                    wrap_around=wrap_around
                    )

            self.game_object_manager.add_object(new_object)

        # comet gifs
        for i in range(max(1, int(self.amount / COMET_DIVIDE_FACTOR))):
            # image_name = random.choice(self.comet_gifs)
            image_name = self.select_random_image(self.comet_gifs, i)
            image = get_image(image_name)
            image_alpha = None
            color = get_average_color(image, consider_alpha=True)
            width = image.get_rect().width
            height = image.get_rect().height
            x, y = get_random_pos(self.world_rect, self.central_compression)
            gif_frames = self.gif_frames[image_name]

            max_gif_frame = len(gif_frames) - 1
            gif_index = random.randint(0, max_gif_frame)
            gif_animation_time = None
            loop_gif = True
            kill_after_gif_loop = False

            layer = COMET_LAYER
            id_ = len(self.game_object_manager.all_objects)
            type_ = "comet_gif"
            rotation_angle = 0
            rotation_speed = 0
            movement_speed = random.uniform(0.01, 0.5)
            direction = Vector2(self.comet_directions[image_name])
            wrap_around = True

            new_object = create_qt_moving_gif(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    layer=layer,
                    id_=id_,
                    gif_name=image_name,
                    gif_index=gif_index,
                    gif_animation_time=gif_animation_time,
                    loop_gif=loop_gif,
                    kill_after_gif_loop=kill_after_gif_loop,
                    image_alpha=image_alpha,
                    color=color,
                    type_=type_,
                    rotation_angle=rotation_angle,
                    rotation_speed=rotation_speed,
                    movement_speed=movement_speed,
                    direction=direction,
                    wrap_around=wrap_around
                    )

            self.game_object_manager.add_object(new_object)

        end_time = time.time()
        duration = end_time - start_time
        print(f"create_comets took{duration:.6f} seconds")

    def create_planets(self):
        def create_sun_gifs(all_planets, orbit_radius_max, orbit_radius_min, orbit_speed_max, orbit_speed_min):
            for i in range(max(1, int(self.amount / (SUN_DIVIDE_FACTOR)))):
                # image_name = random.choice(self.comet_gifs)
                image_name = self.select_random_image(self.sun_gifs, i)
                image = get_image(image_name)
                image_alpha = None
                color = get_average_color(image, consider_alpha=True)
                width = image.get_rect().width
                height = image.get_rect().height
                x, y = get_random_pos(self.world_rect, self.central_compression)
                gif_frames = self.gif_frames[image_name]
                max_gif_frame = len(gif_frames) - 1
                gif_index = random.randint(0, max_gif_frame)
                rotation_angle = 0
                rotation_speed = 0

                orbit_speed = random.uniform(orbit_speed_min, orbit_speed_max)
                orbit_radius = random.randint(orbit_radius_min, orbit_radius_max)
                id_ = len(self.game_object_manager.all_objects)
                layer = SUN_LAYER
                type_ = "sun"

                gif_animation_time = None
                loop_gif = True
                kill_after_gif_loop = False
                wrap_around = True
                movement_speed = random.uniform(0.01, 0.5)
                direction = Vector2((0, 0))
                orbit_direction = 0
                new_object = create_qt_moving_gif(
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        layer=layer,
                        id_=id_,
                        gif_name=image_name,
                        gif_index=gif_index,
                        gif_animation_time=gif_animation_time,
                        loop_gif=loop_gif,
                        kill_after_gif_loop=kill_after_gif_loop,
                        image_alpha=image_alpha,
                        color=color,
                        type_=type_,
                        rotation_angle=rotation_angle,
                        rotation_speed=rotation_speed,
                        movement_speed=movement_speed,
                        direction=direction,
                        wrap_around=wrap_around,
                        orbit_angle=rotation_angle,
                        orbit_speed=orbit_speed,
                        orbit_radius=orbit_radius,
                        orbit_direction=orbit_direction
                        )

                self.game_object_manager.add_object(new_object)
                all_planets.append(new_object)

        def create_sun_images(all_planets, orbit_radius_max, orbit_radius_min, orbit_speed_max, orbit_speed_min):
            for i in range(max(1, int(self.amount / (SUN_DIVIDE_FACTOR)))):
                image_name = self.select_random_image(self.sun_images, i)
                image = get_image(image_name)
                image_alpha = None
                color = get_average_color(image, consider_alpha=True)
                width = image.get_rect().width
                height = image.get_rect().height
                x, y = get_random_pos(self.world_rect, self.central_compression)
                movement_speed = random.uniform(0.05, 0.5)
                rotation_angle = 0
                rotation_speed = 0

                orbit_speed = random.uniform(orbit_speed_min, orbit_speed_max)
                orbit_radius = random.randint(orbit_radius_min, orbit_radius_max)
                orbit_angle = 0

                id_ = len(self.game_object_manager.all_objects)
                layer = SUN_LAYER
                type_ = "sun"

                gif_animation_time = None
                loop_gif = True
                kill_after_gif_loop = False
                wrap_around = True

                direction = Vector2((0, 0))
                orbit_direction = 0
                wrap_around = True

                new_object = create_qt_moving_image(
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        layer=layer,
                        id_=id_,
                        image_name=image_name,
                        image_alpha=image_alpha,
                        color=color,
                        type_=type_,
                        rotation_angle=rotation_angle,
                        rotation_speed=rotation_speed,
                        movement_speed=movement_speed,
                        direction=direction,
                        wrap_around=wrap_around,
                        orbit_angle=orbit_angle,
                        orbit_speed=orbit_speed,
                        orbit_radius=orbit_radius,
                        orbit_direction=orbit_direction)

                self.game_object_manager.add_object(new_object)
                all_planets.append(new_object)

        def create_planet_gifs(all_planets, orbit_radius_max, orbit_radius_min, orbit_speed_max, orbit_speed_min):
            for i in range(max(1, int(self.amount / PlANET_DIVIDE_FACTOR / 2))):
                # image_name = random.choice(self.comet_gifs)
                image_name = self.select_random_image(self.planet_gifs, i)
                image = get_image(image_name)
                image_alpha = None
                color = get_average_color(image, consider_alpha=True)
                width = image.get_rect().width / 2
                height = image.get_rect().height / 2
                x, y = get_random_pos(self.world_rect, self.central_compression)
                gif_frames = self.gif_frames[image_name]
                max_gif_frame = len(gif_frames) - 1
                gif_index = random.randint(0, max_gif_frame)
                orbit_angle = random.randint(0, 360)
                # if image_name.startswith("moon"):

                orbit_speed = random.uniform(orbit_speed_min, orbit_speed_max)
                orbit_radius = random.randint(orbit_radius_min, orbit_radius_max)
                orbit_direction = random.choice([-1, 1])

                type_ = "moon" if image_name.startswith("moon") else "planet"
                layer = PLANET_LAYER

                id_ = len(self.game_object_manager.all_objects)

                gif_animation_time = None
                loop_gif = True
                kill_after_gif_loop = False
                wrap_around = False
                movement_speed = random.uniform(0.01, 0.5)
                direction = Vector2((0, 0))
                rotation_angle = 0
                rotations_speed = 0

                if type_ == "moon":
                    orbit_radius = random.randint(int(orbit_radius_min / 3), int(orbit_radius_max / 3))
                    width, height = int(width / 3), int(height / 3)

                else:
                    orbit_speed = random.uniform(orbit_speed_min / 2, orbit_speed_max / 2)

                new_object = create_qt_moving_gif(
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        layer=layer,
                        id_=id_,
                        gif_name=image_name,
                        gif_index=gif_index,
                        gif_animation_time=gif_animation_time,
                        loop_gif=loop_gif,
                        kill_after_gif_loop=kill_after_gif_loop,
                        image_alpha=image_alpha,
                        color=color,
                        type_=type_,
                        rotation_angle=rotation_angle,
                        rotation_speed=rotations_speed,
                        movement_speed=movement_speed,
                        direction=direction,
                        wrap_around=wrap_around,
                        orbit_angle=orbit_angle,
                        orbit_speed=orbit_speed,
                        orbit_radius=orbit_radius,
                        orbit_direction=orbit_direction)

                self.game_object_manager.add_object(new_object)
                all_planets.append(new_object)

        def create_planet_images(
                all_planets, orbit_radius_max, orbit_radius_min, orbit_speed_max, orbit_speed_min
                ):
            for i in range(max(1, int(self.amount / PlANET_DIVIDE_FACTOR))):
                image_name = self.select_random_image(self.planet_images, i)
                image = get_image(image_name)
                color = get_average_color(image, consider_alpha=True)
                width = image.get_rect().width
                height = image.get_rect().height
                x, y = get_random_pos(self.world_rect, self.central_compression)
                movement_speed = random.uniform(0.05, 0.5)
                orbit_angle = random.randint(0, 360)
                orbit_speed = random.uniform(orbit_speed_min, orbit_speed_max)
                orbit_radius = random.randint(orbit_radius_min, orbit_radius_max)
                orbit_direction = random.choice([-1, 1])
                layer = PLANET_LAYER
                id_ = len(self.game_object_manager.all_objects)
                image_alpha = None
                type_ = "planet"
                rotation_angle = 0
                rotation_speed = 0
                direction = Vector2((0, 0))
                wrap_around = False

                new_object = create_qt_moving_image(
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        layer=layer,
                        id_=id_,
                        image_name=image_name,
                        image_alpha=image_alpha,
                        color=color,
                        type_=type_,
                        rotation_angle=rotation_angle,
                        rotation_speed=rotation_speed,
                        movement_speed=movement_speed,
                        direction=direction,
                        wrap_around=wrap_around,
                        orbit_angle=orbit_angle,
                        orbit_speed=orbit_speed,
                        orbit_radius=orbit_radius,
                        orbit_direction=orbit_direction
                        )

                self.game_object_manager.add_object(new_object)
                all_planets.append(new_object)

        start_time = time.time()
        all_planets = []
        orbit_speed_min = 0.001
        orbit_speed_max = 0.005
        orbit_radius_min = 1000
        orbit_radius_max = 3000

        # planet images
        create_planet_images(all_planets, orbit_radius_max, orbit_radius_min, orbit_speed_max, orbit_speed_min)

        # # planet gifs
        create_planet_gifs(all_planets, orbit_radius_max, orbit_radius_min, orbit_speed_max, orbit_speed_min)
        #
        # # sun images
        create_sun_images(all_planets, orbit_radius_max, orbit_radius_min, orbit_speed_max, orbit_speed_min)
        #
        # # sun gifs
        create_sun_gifs(all_planets, orbit_radius_max, orbit_radius_min, orbit_speed_max, orbit_speed_min)

        self.game_object_manager.rebuild_qtree()
        self.game_object_manager.set_orbit_object()

        end_time = time.time()
        duration = end_time - start_time
        print(f"create_planets took{duration:.6f} seconds")

    def delete_universe(self) -> None:
        self.game_object_manager.all_objects = []
        self.game_object_manager.dynamic_objects = []
        self.game_object_manager._qtree.clear()

    def create_universe_from_data(self, data: dict) -> None:
        for key, obj in data.items():
            class_name = obj["class_name"]
            match class_name:
                case "QTFlickeringStar":
                    self.game_object_manager.add_object(QTFlickeringStar(x=obj["x"],
                            y=obj["y"],
                            width=obj["width"],
                            height=obj["height"],
                            layer=obj["layer"],
                            id_=obj["id"],
                            colors=obj["colors"],
                            type_=obj["type"],
                            ))

                case "QTPulsatingStar":
                    self.game_object_manager.add_object(QTPulsatingStar(x=obj["x"],
                            y=obj["y"],
                            width=obj["width"],
                            height=obj["height"],
                            layer=obj["layer"],
                            id_=obj["id"],
                            type_=obj["type"],
                            ))

                case "QTImage":
                    self.game_object_manager.add_object(QTImage(x=obj["x"],
                            y=obj["y"],
                            width=obj["width"],
                            height=obj["height"],
                            layer=obj["layer"],
                            id_=obj["id"],
                            type_=obj["type"],
                            image_name=obj["image_name"],
                            image_alpha=obj["image_alpha"],
                            color=obj["color"],
                            rotation_angle=obj["rotation_angle"]
                            ))

                case "QTGif":
                    self.game_object_manager.add_object(QTGif(x=obj["x"],
                            y=obj["y"],
                            width=obj["width"],
                            height=obj["height"],
                            layer=obj["layer"],
                            id_=obj["id"],
                            gif_name=obj["gif_name"],
                            gif_index=obj["gif_index"],
                            gif_animation_time=obj["gif_animation_time"],
                            loop_gif=obj["loop_gif"],
                            kill_after_gif_loop=obj["kill_after_gif_loop"],
                            image_alpha=obj["image_alpha"],
                            color=obj["color"],
                            type_=obj["type"],
                            rotation_angle=obj["rotation_angle"]
                            ))

                case "QTMovingImage":
                    self.game_object_manager.add_object(QTMovingImage(x=obj["x"],
                            y=obj["y"],
                            width=obj["width"],
                            height=obj["height"],
                            layer=obj["layer"],
                            id_=obj["id"],
                            image_name=obj["image_name"],
                            image_alpha=obj["image_alpha"],
                            color=obj["color"],
                            type_=obj["type"],
                            rotation_angle=obj["rotation_angle"],
                            rotation_speed=obj["rotation_speed"],
                            movement_speed=obj["movement_speed"],
                            direction=Vector2(obj["direction"]["x"], obj["direction"]["y"]),
                            wrap_around=obj["wrap_around"],
                            orbit_angle=obj["orbit_angle"],
                            orbit_speed=obj["orbit_speed"],
                            orbit_radius=obj["orbit_radius"],
                            orbit_direction=obj["orbit_direction"]
                            ))

                case "QTMovingGif":
                    self.game_object_manager.add_object(QTMovingGif(x=obj["x"],
                            y=obj["y"],
                            width=obj["width"],
                            height=obj["height"],
                            layer=obj["layer"],
                            id_=obj["id"],
                            gif_name=obj["gif_name"],
                            gif_index=obj["gif_index"],
                            gif_animation_time=obj["gif_animation_time"],
                            loop_gif=obj["loop_gif"],
                            kill_after_gif_loop=obj["kill_after_gif_loop"],
                            image_alpha=obj["image_alpha"],
                            color=obj["color"],
                            type_=obj["type"],
                            rotation_angle=obj["rotation_angle"],

                            rotation_speed=obj["rotation_speed"],
                            movement_speed=obj["movement_speed"],
                            direction=Vector2(obj["direction"]["x"], obj["direction"]["y"]),
                            wrap_around=obj["wrap_around"],
                            orbit_angle=obj["orbit_angle"],
                            orbit_speed=obj["orbit_speed"],
                            orbit_radius=obj["orbit_radius"],
                            orbit_direction=obj["orbit_direction"]
                            ))

        self.game_object_manager.set_orbit_object_by_id()

        self.game_object_manager.set_orbit_object()

    def create_universe(self, world_rect: Rect = WORLD_RECT, collectable_items_amount=0, **kwargs) -> None:
        start_time = time.time()
        # collectable_items = kwargs.get("collectable_items", None)
        self.world_rect = world_rect
        self.create_stars()
        self.create_galaxys()
        self.create_nebulaes()
        self.create_comets()
        self.create_asteroids()
        self.create_planets()
        self.create_collectable_items()


        # # update them for proper initialization
        pan_zoom_handler.set_zoom(pan_zoom_handler.get_zoom() + 0.0001)
        # for obj in self.game_object_manager.all_objects:
        #     self.game_object_manager.update_objects_position(obj)
        #     self.game_object_manager.update_objects_size(obj)
        #     # self.game_object_manager.update_objects_rect(obj)

        end_time = time.time()

        duration = end_time - start_time
        print(f"Universe created in {duration:.6f} seconds")

        # self.create_artefacts(collectable_items_amount, collectable_items=collectable_items)






def main():
    pygame.init()
    width, height = 1820, 1080
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    universe_factory = UniverseFactory(screen, WORLD_RECT)
    universe_factory.amount = int(math.sqrt(math.sqrt(universe_factory.world_rect.width)) * UNIVERSE_DENSITY)
    universe_factory.create_universe(WORLD_RECT, collectable_items_amount=10)

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
        clock.tick(6000)
        # print (f"zoom: {pan_zoom_handler.zoom},paan_zoom_handler.zoom_min: {pan_zoom_handler.zoom_min}, pan_zoom_handler.zoom_max: {pan_zoom_handler.zoom_max}")

    pygame.quit()


if __name__ == "__main__":
    main()
