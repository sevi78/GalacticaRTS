import copy

import pygame

from source.configuration.game_config import config
from source.draw.rectangle import draw_transparent_rounded_rect, draw_dashed_rounded_rectangle
from source.game_play.navigation import navigate_to_position
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image, overblit_button_image, scale_image_cached
from source.multimedia_library.radar_scan_fx import RadarScanFX

PLANET_IMAGE_SIZE = 125
MIN_OBJECT_SIZE = 2
MIN_MAP_SIZE = 240
MAX_MAP_SIZE = 1048
BUTTON_SIZE = 25
WARNING_ICON_SIZE = 32
SCALE_FACTOR = 100
MIN_CAMERA_FOCUS_DASHED_DRAW = 300
MIN_CAMERA_FOCUS_DRAW = 100


class MapPanel:
    """
    Summary:

    The MapPanel class represents a panel that displays a map with various objects such as planets, ships, and
    collectible items. It allows the user to interact with the map by zooming in/out, moving the camera, and toggling
    the visibility of different objects.

    Example Usage:
    # Create a MapPanel object
    map_panel = MapPanel(win, x, y, width, height)

    # Listen for events
    map_panel.listen(events)

    # Draw the map panel
    map_panel.draw()
    Code Analysis
    Main functionalities
    Displaying a map with various objects such as planets, ships, and collectible items.
    Allowing the user to zoom in/out on the map.
    Allowing the user to move the camera to navigate the map.
    Toggling the visibility of different objects on the map.

    Methods:
    __init__(self, win: pygame.surface.Surface, x: int, y: int, width: int, height: int) -> None:
    Initializes the MapPanel object with the specified parameters.
    create_checkboxes(self) -> None: Creates checkboxes for toggling the visibility of different objects on the map.
    update_checkboxes(self) -> None: Updates the checkboxes based on the current visibility settings.
    show_objects(self, object_category) -> None: Toggles the visibility of objects in the specified category.
    scale_map(self, event) -> None: Scales the map based on the mouse wheel event.
    update_camera_position(self) -> None: Updates the camera position based on the mouse movement.
    draw_objects(self, sprites: list, surface: pygame.surface.Surface) -> None:
    Draws the specified objects on the map surface.
    draw_object(self, pos, radius, color, sprite, surface, **kwargs) -> None: Draws a single object on the map surface.
    reposition(self) -> None: Repositions the map panel and checkboxes based on the current window size.
    listen(self, events) -> None: Listens for events and handles user interactions with the map panel.
    draw(self) -> None: Draws the map panel and its contents on the window.

    Fields:
    win: pygame.surface.Surface: The surface on which to draw the map panel.
    world_x: int: The x-coordinate of the top left corner of the map panel in world coordinates.
    world_y: int: The y-coordinate of the top left corner of the map panel in world coordinates.
    world_width: int: The width of the map panel in world coordinates.
    world_height: int: The height of the map panel in world coordinates.
    app: config.app: The global app object.
    scale_direction: int: The scale_direction factor for zooming in/out on the map.
    scale_factor: int: The factor by which to scale_direction the map when zooming.
    name: str: The name of the map panel.
    frame_color: colors.frame_color: The color of the frame around the map panel.
    factor: float: The factor used to convert between world coordinates and screen coordinates.
    background_surface: pygame.surface.Surface: The surface used to draw the map and its objects.
    frame_rect: pygame.Rect: The rectangle representing the frame of the map panel.
    warning_image: pygame.surface.Surface: The image used to display warning icons on the map.
    ctrl_pressed: bool: Flag indicating whether the Ctrl key is pressed.
    left_mouse_button_pressed: bool: Flag indicating whether the left mouse button is pressed.
    checkboxes: list: The list of checkboxes for toggling object visibility.
    checkbox_camera: ImageButton: The checkbox for toggling the visibility of the camera focus.
    checkbox_items: ImageButton: The checkbox for toggling the visibility of collectible items.
    checkbox_orbits: ImageButton: The checkbox for toggling the visibility of orbits.
    checkbox_planets: ImageButton: The checkbox for toggling the visibility of planets.
    checkbox_ships: ImageButton: The checkbox for toggling the visibility of ships.
    show_ships: bool: Flag indicating whether ships should be shown on the map.
    show_planets: bool: Flag indicating whether planets should be shown on the map.
    show_items: bool: Flag indicating whether collectible items should be shown on the map.
    show_ufos: bool: Flag indicating whether UFOs should be shown on the map.
    show_orbits: bool: Flag indicating whether orbits should be shown on the map.
    show_camera: bool: Flag indicating whether the camera focus should be shown on the map.
    show_warnings: bool: Flag indicating whether warning icons should be shown on the map.
    checkbox_frame: pygame.Rect: The rectangle representing the frame around the checkboxes.
    """

    def __init__(self, win: pygame.surface.Surface, x: int, y: int, width: int, height: int) -> None:
        # params
        self.win = win
        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.world_height = height

        # vars
        self.app = config.app
        self.scale_direction = 1
        self.scale_factor = SCALE_FACTOR
        self.name = "map panel"
        self.frame_color = colors.frame_color
        self.factor = self.app.level_handler.data["globals"]["width"] / self.world_width
        self.relative_mouse_x = 0
        self.relative_mouse_y = 0

        # surfaces, rect
        self.background_surface = pygame.Surface((self.world_width, self.world_height))
        self.background_surface_rect = None
        self.frame_rect = pygame.Rect(self.world_x, self.world_y, self.world_width, self.world_height)
        self.images = {}
        self.warning_image = scale_image_cached(get_image("warning.png"), (WARNING_ICON_SIZE, WARNING_ICON_SIZE))

        # interaction stuff
        self.ctrl_pressed = False
        self.left_mouse_button_pressed = False
        self.middle_button_pressed = False
        self.visible = True

        # init checkboxes
        self.checkboxes = []
        self.checkbox_images = None
        self.checkbox_warnings = None
        self.checkbox_ufos = None
        self.checkbox_alpha = None
        self.checkbox_camera = None
        self.checkbox_items = None
        self.checkbox_orbits = None
        self.checkbox_planets = None
        self.checkbox_ships = None

        # init checkbox values
        self.show_ships = True
        self.show_planets = True
        self.show_items = True
        self.show_ufos = True
        self.show_orbits = True
        self.show_camera = True
        self.show_warnings = True
        self.show_images = True
        self.show_alpha = True

        # create checkboxes
        self.checkbox_frame = None
        self.create_checkboxes()
        self._on_hover = False

        self.radar_scan_fx = RadarScanFX(self.win, self.world_x, self.world_y, self.world_width, self.world_height, config.ui_rounded_corner_radius_small)

        # register
        # needed for WidgetHandler
        self.layer = 9
        self._hidden = False
        self.is_sub_widget = True
        WidgetHandler.add_widget(self)

    @property
    def on_hover(self):
        return self._on_hover

    @on_hover.setter
    def on_hover(self, value):
        self._on_hover = value
        if value:
            config.hover_object = self
        else:
            if config.hover_object == self:
                config.hover_object = None

    def create_checkboxes(self) -> None:
        y = self.world_y
        x = self.world_x
        layer = 10

        self.checkbox_ships = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("ships_25x25.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show ships",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("ships"),
                name="ships")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_ships)

        self.checkbox_planets = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("Zeta Bentauri_60x60.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show planets",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("planets"),
                name="planets")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_planets)

        self.checkbox_orbits = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("orbit_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show planets",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("orbits"),
                name="orbits")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_orbits)

        self.checkbox_items = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("artefact1_60x31.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show collectable items",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("items"),
                name="items")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_items)

        self.checkbox_ufos = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("ufo_74x30.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show collectable items",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("ufos"),
                name="ufos")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_ufos)

        self.checkbox_camera = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("camera_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show collectable items",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("camera"),
                name="camera")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_camera)

        self.checkbox_warnings = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("warning.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show collectable items",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("warnings"),
                name="warnings")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_warnings)

        self.checkbox_images = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("paint.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show collectable items",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("images"),
                name="images")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_images)

        self.checkbox_alpha = ImageButton(win=self.win,
                x=self.world_x + x,
                y=y - BUTTON_SIZE,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("alpha.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="",  # "show collectable items",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=layer,
                on_click=lambda: self.show_objects("alpha"),
                name="alpha")

        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(self.checkbox_alpha)

    def update_checkboxes(self) -> None:
        for checkbox in self.checkboxes:
            overblit_button_image(checkbox, "uncheck.png", getattr(self, "show_" + checkbox.name))

    def show_objects(self, object_category) -> None:
        setattr(self, "show_" + object_category, not getattr(self, "show_" + object_category))

    def scale_map(self, event) -> None:
        """Scale mini-map based on mouse wheel input."""
        self.scale_direction = event.y

        # Recalculate world dimensions based on scale direction and factor
        self.world_width += self.scale_direction * self.scale_factor
        self.world_height += self.scale_direction * self.scale_factor

        # Limit size using clamp logic
        self.world_width = max(MIN_MAP_SIZE, min(self.world_width, MAX_MAP_SIZE))
        self.world_height = max(MIN_MAP_SIZE, min(self.world_height, MAX_MAP_SIZE))

        # Update RadarScanFX dimensions directly based on world dimensions,
        # keeping its bottom-left corner fixed at its original position.

        new_x_position = self.radar_scan_fx.x  # Keep original x position unchanged
        new_y_position = self.radar_scan_fx.y - (self.world_height - self.radar_scan_fx.height)  # Adjust upward
        self.radar_scan_fx.scale(new_x_position, new_y_position, self.world_width, self.world_height)

    def update_camera_position(self) -> None:
        # get the mouse position
        mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

        # calculate the relative mouse position when clicked on the map
        dist_x, dist_y = abs(self.background_surface_rect.x - mx), abs(self.background_surface_rect.y - my)

        # multiply with factor to make sure world position is correct
        x, y = dist_x * self.factor, dist_y * self.factor
        self.relative_mouse_x, self.relative_mouse_y = x, y

        # navigate to position
        navigate_to_position(x, y)

    def draw_objects(self, sprites: list, surface: pygame.surface.Surface) -> None:
        # update factor 
        self.factor = self.app.level_handler.data["globals"]["width"] / self.world_width

        # get all objects to display
        for sprite in sprites:
            if hasattr(sprite, "property"):
                # get average color of object
                color = sprite.average_color
                pos = ((sprite.world_x / self.factor), (sprite.world_y / self.factor))
                size = (
                    sprite.world_width / self.factor if sprite.world_width / self.factor > MIN_OBJECT_SIZE else MIN_OBJECT_SIZE,
                    sprite.world_height / self.factor if sprite.world_height / self.factor > MIN_OBJECT_SIZE else MIN_OBJECT_SIZE)

                # planets, sun, moons
                if sprite.property == "planet" and self.show_planets:
                    radius = sprite.world_width / self.factor if sprite.world_width / self.factor > MIN_OBJECT_SIZE else MIN_OBJECT_SIZE

                    if sprite.explored and config.view_explored_planets:
                        color = pygame.color.THECOLORS.get("green")

                    self.draw_object(pos, radius, color, sprite, surface)
                    self.draw_image(pos, size, sprite.image_raw)

                    # draw orbits
                    if self.show_orbits:
                        orbit_objects = [_ for _ in sprite_groups.planets.sprites() if _.orbit_object == sprite]
                        color = colors.ui_darker
                        for i in orbit_objects:
                            radius = i.orbit_radius / self.factor
                            self.draw_object(pos, radius, color, sprite, surface, width=1, draw_anyway=True)

                    if self.show_warnings:
                        if sprite.under_attack:
                            self.draw_image(pos, (
                                WARNING_ICON_SIZE,
                                WARNING_ICON_SIZE), self.warning_image, offset_y=-15, draw_anyway=True)

                # ships
                if sprite.property == "ship" and self.show_ships:
                    radius = sprite.world_width / self.factor if sprite.world_width / self.factor > MIN_OBJECT_SIZE else MIN_OBJECT_SIZE
                    self.draw_object(pos, radius, color, sprite, surface)
                    self.draw_image(pos, size, sprite.image_raw)

                    # display selection
                    if sprite == self.app.ship:
                        self.draw_object(pos, radius, colors.select_color, sprite, surface, draw_anyway=True)

                # ufos
                if sprite.property == "ufo" and self.show_ufos:
                    radius = sprite.world_width / self.factor / 2 if sprite.world_width / self.factor > MIN_OBJECT_SIZE else MIN_OBJECT_SIZE
                    self.draw_object(pos, radius, color, sprite, surface)
                    self.draw_image(pos, size, sprite.image_raw)

                # collectable items
                if sprite.property == "item" and self.show_items:
                    radius = 1
                    self.draw_object(pos, radius, color, sprite, surface)
                    self.draw_image(pos, size, sprite.image_raw)

    def draw_image(self, pos, size, image, **kwargs):
        draw_anyway = kwargs.get("draw_anyway", False)
        if not self.show_images and not draw_anyway:
            return

        offset_x = kwargs.get("offset_x", 0)
        offset_y = kwargs.get("offset_y", 0)

        image_copy = copy.copy(image)
        new_image = scale_image_cached(image_copy, size)
        image_rect = new_image.get_rect()
        pos = pos[0] + offset_x, pos[1] + offset_y
        image_rect.center = pos
        self.background_surface.blit(new_image, image_rect)

    def draw_object(self, pos, radius, color, sprite, surface, **kwargs):
        draw_anyway = kwargs.get("draw_anyway", False)
        if self.show_images and not draw_anyway:
            return

        width = kwargs.get("width", 0)
        # draw object
        pos = ((sprite.world_x / self.factor), (sprite.world_y / self.factor))
        pygame.draw.circle(
                surface=surface,
                color=color,
                center=pos,
                radius=radius,
                width=width)

    def draw_camera_focus(self) -> None:
        if not self.show_camera:
            return

        # calculate the position
        x, y = (pan_zoom_handler.world_offset_x / self.factor), (pan_zoom_handler.world_offset_y / self.factor)

        # Calculate the width and height of the rectangle
        width = config.width / self.factor / pan_zoom_handler.zoom
        height = config.height / self.factor / pan_zoom_handler.zoom

        # draw_dashed_rounded_rectangle(self.background_surface,
        #         pygame.color.THECOLORS["gray31"], pygame.Rect(x, y, width, height), 1, 15 * pan_zoom_handler.zoom, 10)

        pygame.draw.rect(self.background_surface,
                pygame.color.THECOLORS["gray31"], pygame.Rect(x, y, width, height), 1, 3)

    def reposition(self) -> None:
        self.world_y = self.win.get_size()[1] - self.world_height
        buffer_x = 1
        buffer_y = 3
        for i in self.checkboxes:
            i.screen_x = self.world_x + buffer_x + ((BUTTON_SIZE + buffer_x) * self.checkboxes.index(i))
            i.screen_y = self.world_y - buffer_y - BUTTON_SIZE

        self.checkbox_frame = pygame.Rect(self.world_x, self.world_y - BUTTON_SIZE - buffer_y * 2, MIN_MAP_SIZE, BUTTON_SIZE + (
                buffer_y * 2))

    def set_visible(self) -> None:
        self.visible = config.show_map_panel
        for i in self.checkboxes:
            i._hidden = not self.visible

    def listen(self, events) -> None:
        if not self.visible:
            return

        for event in events:
            # ctrl_pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = True

            elif event.type == pygame.KEYUP:
                self.ctrl_pressed = False

            # on hover
            if self.frame_rect.collidepoint(pygame.mouse.get_pos()):
                self.on_hover = True
                # scale_direction map
                if event.type == pygame.MOUSEWHEEL and self.ctrl_pressed:
                    self.scale_map(event)

                # set zoom
                if event.type == pygame.MOUSEWHEEL and not self.ctrl_pressed:
                    self.update_camera_position()

                # navigate
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.ctrl_pressed:
                    # left button
                    if pygame.mouse.get_pressed()[0]:
                        self.left_mouse_button_pressed = True
                    if pygame.mouse.get_pressed()[1]:
                        self.middle_button_pressed = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.left_mouse_button_pressed = False
                    self.middle_button_pressed = False
            else:
                self.on_hover = False

        if self.left_mouse_button_pressed or self.middle_button_pressed:
            self.update_camera_position()

    def draw_frame(self):
        color = (0, 0, 0)
        self.radar_scan_fx.update()

        surf_ = draw_transparent_rounded_rect(self.win, color, self.frame_rect,
                config.ui_rounded_corner_radius_small, config.ui_panel_alpha)

        pygame.draw.rect(self.win, self.frame_color, self.frame_rect,
                config.ui_rounded_corner_small_thickness, config.ui_rounded_corner_radius_small)

    def draw(self) -> None:
        self.set_visible()
        if not self.visible:
            return

        self.reposition()
        self.update_checkboxes()

        # generate rect
        self.frame_rect = pygame.Rect(self.world_x, self.world_y, self.world_width, self.world_height)
        self.background_surface_rect = pygame.Rect(
                self.world_x + config.ui_rounded_corner_radius_small,
                self.world_y + config.ui_rounded_corner_radius_small,
                self.world_width - (config.ui_rounded_corner_radius_small * 2),
                self.world_height - (config.ui_rounded_corner_radius_small * 2))

        # draw the panel, dont set aplha to 255 !!! inperformant, replace it is much better !!!
        if self.show_alpha:
            self.background_surface = pygame.Surface((
                self.world_width - (config.ui_rounded_corner_radius_small * 2),
                self.world_height - (config.ui_rounded_corner_radius_small * 2)))
            self.background_surface.set_alpha(config.ui_panel_alpha)
        else:
            self.background_surface = pygame.Surface((
                self.world_width - (config.ui_rounded_corner_radius_small * 2),
                self.world_height - (config.ui_rounded_corner_radius_small * 2)))

        # draw the frame
        self.draw_frame()

        # draw the objects
        self.draw_objects(sprite_groups.planets.sprites(), self.background_surface)
        self.draw_objects(sprite_groups.ships.sprites(), self.background_surface)
        self.draw_objects(sprite_groups.collectable_items.sprites(), self.background_surface)
        self.draw_objects(sprite_groups.ufos.sprites(), self.background_surface)

        # draw camera focus
        self.draw_camera_focus()

        # draw the map_image
        if self.show_alpha:
            self.win.blit(self.background_surface, self.background_surface_rect, special_flags=pygame.BLEND_RGBA_MAX)
        else:
            self.win.blit(self.background_surface, self.background_surface_rect)

        # draw button frame
        draw_transparent_rounded_rect(self.win, (0, 0, 0), self.checkbox_frame,
                config.ui_rounded_corner_radius_small, config.ui_panel_alpha)

        pygame.draw.rect(self.win, self.frame_color, self.checkbox_frame, config.ui_rounded_corner_small_thickness,
                config.ui_rounded_corner_radius_small)
