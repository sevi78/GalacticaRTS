import pygame

from source.configuration.game_config import config
from source.draw.rectangle import draw_transparent_rounded_rect
from source.gui.container.container_config import FONT_SIZE, WIDGET_SIZE, TEXT_SPACING
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image, scale_image_cached
from source.text.text_formatter import format_number
from source.text.text_wrap import TextWrap


class ContainerWidgetItem(TextWrap):
    """
    The ContainerWidgetItem class is a class that represents an item in a container. It is responsible for managing the
    position, size, image, and text of the item, as well as handling user interactions such as hiding, showing, and
    drawing the item.

    Example Usage
    # Create a Pygame window surface
    win = pygame.display.set_mode((800, 600))

    # Load an image for the item
    image = pygame.image.load("item_image.png")

    # Create a ContainerWidgetItem instance
    item = ContainerWidgetItem(win, 100, 100, 50, 50, image, 0)

    # Hide the item
    item.hide()

    # Show the item
    item.show()

    # Draw the item on the window surface
    item.draw()
    Code Analysis
    Main functionalities
    Initializing an instance of the ContainerWidgetItem class with the necessary parameters.
    Managing the position, size, image, and text of the item.
    Handling user interactions such as hiding, showing, and drawing the item.

    Methods
    __init__(self, win, x, y, width, height, image, index, **kwargs): Initializes a new instance of the
    ContainerWidgetItem class with the given parameters.
    set_text(self): Sets the text of the item based on its associated object.
    set_state_image(self): Sets the state image of the item based on its associated object.
    set_position(self, pos): Sets the position of the item and its widgets.
    hide(self): Hides the item.
    show(self): Shows the item.
    draw_text(self): Draws the text of the item on the window surface.
    draw_hover_rect(self): Draws a transparent rounded rectangle around the item when it is being hovered over.
    draw_images(self): Draws the image and state image of the item on the window surface.
    draw(self): Draws the item on the window surface.

    Fields
    win: The Pygame window surface.
    world_x: The x-coordinate of the item in the world.
    world_y: The y-coordinate of the item in the world.
    image_raw: The raw image of the item.
    image: The scaled image of the item.
    rect: The rectangle that represents the position and size of the item.
    index: The index of the item.
    world_width: The width of the item in the world.
    world_height: The height of the item in the world.
    _hidden: A flag indicating whether the item is hidden or not.
    obj: The object associated with the item.
    parent: The parent of the item.
    widgets: The list of widgets contained within the item.
    text: The text of the item.
    font_size: The font size of the item's text.
    font: The font used for the item's text.
    state_image: The state image of the item.
    state_image_rect: The rectangle that represents the position and size of the state image.
    """

    def __init__(self, win, x, y, width, height, image, index, **kwargs) -> None:
        """
        Initializes a new instance of the ContainerWidgetItem class.
        these objects are getting initialized everytime a filter is applied to the container!

        Args:
            win (pygame.Surface): The Pygame window surface.
            x (int): The x-coordinate of the item.
            y (int): The y-coordinate of the item.
            width (int): The width of the item.
            height (int): The height of the item.
            image (pygame.Surface): The image of the item.
            index (int): The index of the item.
            **kwargs: Additional keyword arguments.

        Keyword Args:
            obj (optional): The object associated with the item. Defaults to None.
            parent (optional): The parent of the item. Defaults to None.

        Returns:
            None
        """
        TextWrap.__init__(self)
        self.win = win
        self.world_x = x
        self.world_y = y
        self.image_raw = image
        self.image = scale_image_cached(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.index = index
        self.world_width = width
        self.world_height = height
        self._hidden = False
        self.obj = kwargs.get("obj", None)
        self.parent = kwargs.get("parent", None)
        self.container_name = kwargs.get("container_name", None)
        self.container = kwargs.get("container", None)
        self.item_buttons = kwargs.get("item_buttons", None)
        self.widgets = kwargs.get("item_buttons", None)

        # text
        self.text = ""
        self.font_size = FONT_SIZE
        self.font = pygame.sysfont.SysFont(None, FONT_SIZE)

        # state image
        self.state_image = None
        self.state_image_rect = None
        self.set_text_and_state_image()

        # buttons
        self.create_buttons()

    def create_buttons(self):
        """
        "agree": {
            "image": scale_image_cached(get_image("thumps_up.png"), (button_size, button_size)),
            "f": lambda: test()
            },
        """
        if not self.item_buttons:
            return

        for i in self.widgets:
            i.parent = self

    def set_position(self, pos) -> None:
        """
        Sets the position of the object in the game world.

        This function takes a tuple of two integers, `pos`, which represents the x and y coordinates of the object's new
        position in the game world. It updates the `world_x` and `world_y` attributes of the object to the new position.

        The function also updates the position of the object's rectangle (`self.rect`) by setting its `topleft`
        attribute to the new position. This ensures that the object's visual representation is correctly positioned in
        the game world.

        Additionally, the function iterates over all the widgets associated with the object and updates their positions
        accordingly. Each widget's `win` attribute is set to the object's window (`self.win`), and their `set_position`
        method is called with the object's new position as the argument.

        If the object has a `state_image` attribute, the function retrieves the appropriate image from the object's
        state engine's image drawer based on the current state. The image is then scaled to a smaller size
        (`WIDGET_SIZE / 3`) and assigned to the `state_image` attribute. The `state_image_rect` attribute is also
        updated to the new position of the `state_image`.

        Parameters:
            pos (tuple of int): The new position of the object in the game world.
        """

        self.world_x, self.world_y = pos
        self.rect.topleft = pos

        for widget in self.widgets:
            widget.win = self.win
            widget.set_position(self.rect.topleft)

        if hasattr(self, "state_image"):
            if self.state_image is not None:
                self.state_image_rect = self.state_image.get_rect()
                self.state_image_rect.x = self.rect.x + 25
                self.state_image_rect.y = self.rect.y

    def hide(self) -> None:
        self._hidden = True

    def show(self) -> None:
        self._hidden = False

    def set_text_and_state_image(self) -> None:
        """
        Sets the text and state image of the widget based on the object it represents.

        Returns:
            str: The text to be displayed on the widget. It can be one of the following:
                - "unknown planet" if the object is a PanZoomPlanet and it has not been explored.
                - The name of the object if it is a PanZoomPlanet and it has been explored.
                - The name and energy of the object if it is a PanZoomShip/PanZoomRescueDrone.
                - The index of the object if it is None.
        """
        ships = ["PanZoomShip", "PanZoomRescueDrone"]
        self.text = ""

        # if an object to display
        if self.obj:
            _class = self.obj.__class__.__name__
            # planets
            if _class == "PanZoomPlanet":
                # text
                if self.obj.owner == -1:
                    self.text = "unknown planet"
                else:
                    self.text = (f"{self.obj.name} belongs to {config.app.players[self.obj.owner].name}, population:"
                                 f" {format_number(self.obj.economy_agent.population, 1)}/{format_number(self.obj.economy_agent.population_limit, 1)}, buildings: {len(self.obj.economy_agent.buildings)}")

                # state image
                if self.obj.owner != -1:
                    image_name = config.app.players[self.obj.owner].image_name
                else:
                    image_name = "question_mark.png"

                self.state_image = scale_image_cached(get_image(image_name), (
                    WIDGET_SIZE, WIDGET_SIZE))
                self.state_image_rect = self.state_image.get_rect()


            # ships
            elif _class in ships:
                # text
                self.text += f"{self.obj.name}, owner: {config.app.players[self.obj.owner].name}, energy: {format_number(self.obj.energy, 1)}"

                # state image
                self.state_image = scale_image_cached(get_image(
                        self.obj.state_engine.image_drawer.state_image_names[self.obj.state_engine.state]), (
                    WIDGET_SIZE / 3, WIDGET_SIZE / 3))
                self.state_image_rect = self.state_image.get_rect()

            elif _class == "Trade":
                # text
                self.text += f"{self.obj.__str__(config.app.players[self.obj.owner_index].name)}"

            elif _class == "Game":
                """
                    self.id = str(uuid.uuid4())
                    self.host_id = host_id
                    self.level_id = level_id
                    self.max_players = max_players
                    self.players = {host_id: {"ready": False}}
                    self.state = "lobby"  # "lobby", "starting", "running"
                    self.start_time = None

                """
                self.text, players = self.obj.get_container_widget_string()

                # state image
                try:
                    if self.obj.players[str(config.app.game_client.id)]["ready"]:
                        image_name = "thumps_upred_flipped.png"
                    else:
                        image_name = "thumps_up.png"

                    button = [_ for _ in self.widgets if _.name == "join_game"][0]
                    button.init_image(image_name)
                except KeyError:
                    print ("set_text_and_state_image.key error: this is because level handler has player set to a lower value than the number of players in the game. this is a bug and will be fixed soon")

        # if no object to display (like files or anything else, not implemented yet)
        else:
            self.text += f", index: {self.index}"

        self.create_buttons()

    def draw_text(self) -> None:
        if self.parent:
            text_width = self.parent.world_width - (WIDGET_SIZE * 2)
        else:
            text_width = 400

        self.wrap_text(
                self.win,
                self.text,
                (self.world_x + WIDGET_SIZE + TEXT_SPACING, self.world_y),
                (text_width, FONT_SIZE),
                self.font,
                colors.frame_color,
                iconize=["energy", "food", "minerals", "technology", "population", "buildings", "water"])

    def draw_hover_rect(self) -> None:
        """
        Draws a hover rectangle on the screen if the widget has a parent and the mouse is hovering over it.

        This function first checks if the widget has a parent. If it does, it sets the width of the hover rectangle
        to the width of the parent widget. Then, it checks if the mouse is hovering over the parent widget by
        calling the `collidepoint` method of the parent's rectangle. If the mouse is hovering over the parent,
        it calculates the start and end y-coordinates of the hover rectangle based on the parent's position,
        scroll offset, and scroll factor. It then checks if the y-coordinate of the mouse is within the range
        of the start and end y-coordinates. If it is, it calls the `draw_transparent_rounded_rect` function
        to draw the hover rectangle on the screen.

        This function does not take any parameters and does not return anything.
        """
        if self.parent:
            self.rect.width = self.parent.world_width
            if self.parent.rect.collidepoint(pygame.mouse.get_pos()):
                # set start x: the position for the rect to start. no way to explain the logic ---... :()
                start_y = ((self.parent.rect.y + (self.index + self.parent.scroll_offset_y) * self.parent.scroll_factor)
                           - self.parent.scroll_factor)

                end_y = start_y + self.parent.scroll_factor

                if pygame.mouse.get_pos()[1] in range(int(start_y), int(end_y)):
                    draw_transparent_rounded_rect(self.win, colors.ui_dark, self.rect, 0, 75)

    def draw_images(self) -> None:
        """
        Draws the images of the object on the window surface.

        This function blits the `image` attribute of the object onto the `win` surface using the `rect` attribute as the
        image position.
        If the object has a `state_image` attribute, it blits the `state_image` onto the `win` surface using the
        `state_image_rect` attribute as the position.

        Parameters:
            None

        Returns:
            None
        """
        self.win.blit(self.image, self.rect)
        if hasattr(self, "state_image"):
            if self.state_image is not None:
                self.win.blit(self.state_image, self.state_image_rect)

        # draw buttons
        for i in self.widgets:
            i.draw()

    def listen(self, events):
        for i in self.widgets:
            i.listen(events)
            # print (f"listen i: {i}")

    def draw(self) -> None:
        self.rect.topleft = (self.world_x, self.world_y)

        if not self._hidden:
            # if self.parent:
            #     for index, (key, value) in enumerate(self.item_buttons.items()):
            #         self.item_buttons_dict[key]["dest"] = (
            #             self.parent.rect.width - 50 - ((value["image"].get_rect().width + 5) * index), self.rect.top)

            self.draw_images()
            self.draw_text()
            self.draw_hover_rect()
