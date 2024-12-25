# create a PanZoomSpriteBase object
    # base = PanZoomSpriteBase(
    #         win=screen,
    #         world_x=WIDTH // 2,
    #         world_y=HEIGHT // 2,
    #         world_width=300,
    #         world_height=300,
    #         layer=0,
    #         group=all_sprites)

    # for i in range(10000):
    #     x,y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    #     base = PanZoomSpriteBase(
    #             win=screen,
    #             world_x=x,
    #             world_y=y,
    #             world_width=3,
    #             world_height=3,
    #             layer=0,
    #             group=all_sprites)
    #

    # create stars
    # # flickering star
    # for i in range(20000):
    #     x, y = random.randint(0, world_width), random.randint(0, world_height)
    #     base = PanZoomFlickeringStar(
    #             win=screen,
    #             world_x=x,
    #             world_y=y,
    #             world_width=10,
    #             world_height=10,
    #             layer=0,
    #             group=all_sprites)
    #
    # pulsating star
    # for i in range(20000):
    #     x, y = random.randint(0, world_width), random.randint(0, world_height)
    #     base = PanZoomPulsatingStar(
    #             win=screen,
    #             world_x=x,
    #             world_y=y,
    #             world_width=3,
    #             world_height=3,
    #             layer=0,
    #             group=all_sprites)
    #
    # pan zoom image
    # for i in range(20000):
    #     x, y = random.randint(0, world_width), random.randint(0, world_height)
    #     r = random.randint(0, 360)
    #     base = PanZoomImage(
    #             win=screen,
    #             world_x=x,
    #             world_y=y,
    #             world_width=200,
    #             world_height=200,
    #             layer=0,
    #             group=all_sprites,
    #             image_name="galaxy_2.png",
    #             image_alpha=50,
    #             rotation_angle=r
    #             )

    # # # pan zoom gif
    # for i in range(10000):
    #     x, y = random.randint(0, world_width), random.randint(0, world_height)
    #     r = random.randint(0, 360)
    #     base = PanZoomGif(
    #             win=screen,
    #             world_x=x,
    #             world_y=y,
    #             world_width=200,
    #             world_height=200,
    #             layer=0,
    #             group=all_sprites,
    #             gif_name="asteroid.gif",
    #             gif_index=random.randint(0, len(get_gif_frames("asteroid.gif"))),
    #             gif_animation_time=None,
    #             loop_gif=True,
    #             kill_after_gif_loop=False,
    #             image_alpha=None,
    #             rotation_angle=r
    #             )

    # # # pan zoom moving gif
    # for i in range(2000):
    #     x, y = random.randint(0, world_width), random.randint(0, world_height)
    #     r = random.randint(0, 360)
    #     dx, dy = random.randint(-15, 15), random.randint(-15, 15)
    #     movement_speed = random.randint(1, 15)
    #     gif_frames = get_gif_frames("asteroid.gif")
    #     gif_frames_amount = len(gif_frames)
    #     gif_index = random.randint(0, gif_frames_amount)
    #     moving_asteroid = PanZoomMovingGif(
    #             win=screen,
    #             world_x=x,
    #             world_y=y,
    #             world_width=200,
    #             world_height=200,
    #             layer=0,
    #             group=all_sprites,
    #             gif_name="asteroid.gif",
    #             gif_index=gif_index,
    #             gif_animation_time=None,
    #             loop_gif=True,
    #             kill_after_gif_loop=False,
    #             image_alpha=None,
    #             rotation_angle=r,
    #             movement_speed=movement_speed,
    #             direction=Vector2(dx, dy)
    #             )

    # # pan zoom moving gif

    # # pan zoom moving rotating sprite
    # for i in range(2000):
    #     x, y = random.randint(0, world_width), random.randint(0, world_height)
    #     r = random.randint(0, 360)
    #     dx, dy = random.randint(-15, 15), random.randint(-15, 15)
    #     movement_speed = random.randint(1, 15)
    #
    #     moving_asteroid = PanZoomMovingRotatingSprite(
    #             win=screen,
    #             world_x=x,
    #             world_y=y,
    #             world_width=200,
    #             world_height=200,
    #             layer=0,
    #             group=all_sprites,
    #             image_name="asteroid_40x33.png",
    #             image_alpha=None,
    #             rotation_angle=r,
    #             rotation_speed=0.5,
    #             movement_speed=movement_speed,
    #             direction=Vector2(dx, dy)
    #             )

    # rotating spiral galaxy
    # for i in range(20):
    #     x, y = random.randint(0, world_width), random.randint(0, world_height)
    #     r = random.randint(0, 360)
    #     dx, dy = random.randint(-15, 15), random.randint(-15, 15)
    #     movement_speed = random.randint(1, 15)
    #
    #     spiral = PanZoomMovingRotatingSprite(
    #             win=screen,
    #             world_x=x,
    #             world_y=y,
    #             world_width=200,
    #             world_height=200,
    #             layer=0,
    #             group=all_sprites,
    #             image_name="galaxy_2.png",
    #             image_alpha=None,
    #             rotation_angle=r,
    #             rotation_speed=0.1,
    #             movement_speed=0,
    #             direction=Vector2(0, 0),
    #             initial_rotation=True
    #             )

    # # create reference sprite
    # reference_image_name = "galaxy_2.png"
    # reference_sprite = PanZoomSpriteBase(
    #         win=screen,
    #         world_x=WIDTH // 2,
    #         world_y=HEIGHT // 2,
    #         world_width=300,
    #         world_height=300,
    #         image_name=reference_image_name,
    #         image_alpha=50,
    #         gif_index=1,
    #         loop_gif=True,
    #         kill_after_gif_loop=False,
    #         gif_animation_time=None,
    #         rotation_angle=0.0,
    #         rotation_speed=0.1,
    #         movement_speed=0,
    #         direction=Vector2(0.0, 0.0),
    #         layer=0,
    #         group=all_sprites)
    #
    # # create reference sprite
    # ship_name = "spaceship.png"
    # ship = PanZoomSpriteBase(
    #         win=screen,
    #         world_x=WIDTH // 2,
    #         world_y=HEIGHT // 2,
    #         world_width=30,
    #         world_height=30,
    #         image_name=ship_name,
    #         image_alpha=None,
    #         gif_index=1,
    #         loop_gif=True,
    #         kill_after_gif_loop=False,
    #         gif_animation_time=None,
    #         rotation_angle=100.0,
    #         rotation_speed=0.0,
    #         movement_speed=0,
    #         direction=Vector2(0.0, 0.0),
    #         layer=1,
    #         group=all_sprites)
    #
    # # Create sprites with initial direction for circular movement
    # sprite_image_name = "asteroid.gif"
    # image = get_image(sprite_image_name)
    #
    # w = int(image.get_rect().width / 3)
    # h = int(image.get_rect().height / 3)
    #
    # sprite = PanZoomSpriteBase(
    #         win=screen,
    #         world_x=WIDTH // 2,
    #         world_y=HEIGHT // 2,
    #         world_width=w,
    #         world_height=h,
    #         image_name=sprite_image_name,
    #         image_alpha=None,
    #         gif_index=1,
    #         loop_gif=True,
    #         kill_after_gif_loop=False,
    #         gif_animation_time=None,
    #         rotation_angle=0.0,
    #         rotation_speed=0,
    #         movement_speed=2,
    #         direction=Vector2(1.0, 0.0),
    #         layer=2,
    #         group=all_sprites)