import time

import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.event_text import event_text
from source.gui.widgets.buttons.image_button import ImageButton
from source.multimedia_library.images import get_image
from source.text.text_wrap import TextWrap

BUTTON_SIZE = 12
DEAL_LIFETIME = 120  # seconds
PROVIDER_TEXT_X_OFFSET = 10
OFFER_TEXT_X_OFFSET = 100
REQUEST_TEXT_X_OFFSET = 200
TIME_TEXT_X_OFFSET = 315
ICONIZE_RESOURCES = ["food", "energy", "water", "minerals", "technology"]


class DealSelect(EditorBase, TextWrap):
    """
    Summary

    The DealSelect class is a subclass of EditorBase and TextWrap. It represents a deal between two players in a game.
    The class handles the creation of buttons, the agreement or decline of the deal, and the display of relevant
    information such as the provider, offer, request, and remaining time.

    Example Usage:
    deal = DealSelect(win, x, y, width, height, offer=offer, request=request, player_index=provider_index, buyer_index=buyer_index)
    deal.agree(buyer)
    deal.decline()
    deal.draw()

    Code Analysis
    Main functionalities

    Creation of buttons for agreeing or declining the deal
    Handling the agreement or decline of the deal, including resource transfers between the provider and buyer
    Displaying the provider, offer, request, and remaining time of the deal
    Hiding and showing the deal
    Cleaning up references and deleting the deal object

    Methods:
    __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs): Initializes the DealSelect object with the
    given parameters and optional keyword arguments.
    create_buttons(self): Creates the buttons for agreeing or declining the deal.
    agree(self, buyer): Transfers resources from the provider to the buyer and vice versa.
    decline(self): Declines the deal.
    clean_up_references(self): Removes the deal from lists and deletes it.
    generate_provider_text(self): Generates the text for the provider.
    generate_offer_text(self): Generates the text for the offer.
    generate_request_text(self): Generates the text for the request.
    generate_time_text(self): Generates the text for the remaining time.
    draw_provider_text(self): Draws the provider text on the screen.
    draw_offer_text(self): Draws the offer text on the screen.
    draw_request_text(self): Draws the request text on the screen.
    draw_time_text(self): Draws the remaining time text on the screen.
    draw_buttons(self): Draws the buttons on the screen.
    draw_provider_image(self): Draws the provider image on the screen.
    reposition_buttons(self): Repositions the buttons on the screen.
    draw(self): Draws the deal on the screen.

    Fields:
    offer: The offer of the deal.
    request: The request of the deal.
    widgets: The widgets associated with the deal.
    provider_index: The index of the provider player.
    buyer_index: The index of the buyer player.
    provider_image: The image of the provider player.
    life_time: The lifetime of the deal.
    start_time: The start time of the deal.
    end_time: The end time of the deal.
    remaining_time: The remaining time of the deal.
    font: The font used for text rendering.
    provider_text: The text for the provider.
    offer_text: The text for the offer.
    request_text: The text for the request.
    time_text: The text for the remaining time.
    buttons: The buttons associated with the deal.
    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs) -> None:
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        TextWrap.__init__(self)

        # args/kwargs
        self.offer = kwargs.get("offer", None)
        self.request = kwargs.get("request", None)
        self.widgets = []
        self.provider_index = kwargs.get("player_index", 0)
        self.buyer_index = kwargs.get("buyer_index", 0)
        self.provider_image = pygame.transform.scale(get_image(config.app.players[self.provider_index].image_name),
                (20, 20))

        # timing to delete after some time
        self.life_time = DEAL_LIFETIME
        self.start_time = time.time()
        self.end_time = self.start_time + self.life_time
        self.remaining_time = DEAL_LIFETIME

        # create widgets
        self.create_buttons()

        # generate text
        self.font = pygame.font.SysFont(config.font_name, 12)
        self.provider_text = ""
        self.offer_text = ""
        self.request_text = ""
        self.time_text = ""
        self.generate_provider_text()
        self.generate_offer_text()
        self.generate_request_text()

        # hide initially
        self.hide()
        self.max_height = 25

    def __repr__(self) -> str:
        return f"DealSelect: provider: {config.app.players[self.provider_index].name}, {self.offer} for {self.request}"

    def create_buttons(self) -> None:
        agree_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE * 3,
                y=self.world_y + TOP_SPACING + 5,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("thumps_up.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                image_raw=pygame.transform.scale(
                        get_image("thumps_up.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="agree!",
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=9,
                onClick=lambda: self.agree(self.buyer_index),
                name="agree_button"
                )

        self.buttons.append(agree_button)
        self.widgets.append(agree_button)

        decline_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE - BUTTON_SIZE / 2,
                y=self.world_y + TOP_SPACING + 5,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.flip(
                        pygame.transform.scale(get_image("thumps_upred.png"), (BUTTON_SIZE, BUTTON_SIZE)), 1, 1),
                image_raw=pygame.transform.flip(
                        pygame.transform.scale(get_image("thumps_upred.png"), (BUTTON_SIZE, BUTTON_SIZE)), 1, 1),
                tooltip="decline!",
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=9,
                onClick=lambda: self.decline(),
                name="decline_button"
                )

        self.buttons.append(decline_button)
        self.widgets.append(decline_button)

        for i in self.buttons:
            i.hide()

    def agree(self, buyer) -> None:
        """
        transfers resources from provider to buyer and vise versa
        """

        # get provider stuff
        provider = config.app.players[self.provider_index]
        provider_resource = list(self.offer.keys())[0]
        provider_value = list(self.offer.values())[0]

        # # check if enough resources to buy the deal:
        # if getattr(provider, provider_resource) < provider_value:
        #     return

        # get buyer stuff
        self.buyer_index = buyer
        buyer = config.app.players[self.buyer_index]
        buyer_resource = list(self.request.keys())[0]
        buyer_value = list(self.request.values())[0]

        # Check if the buyer has enough resources to buy the deal:
        buyer_resource_amount = getattr(buyer, buyer_resource, 0)  # Default to 0 if attribute does not exist
        remaining_resources = buyer_resource_amount - buyer_value
        if buyer_resource_amount - buyer_value < 0:
            event_text.set_text(f"You don't have enough resources to make this deal! you are missing: {remaining_resources} of {buyer_resource}")
            return

        # set the values
        # subtract from provider
        setattr(provider, provider_resource, getattr(provider, provider_resource) - provider_value)
        # add to buyer
        setattr(buyer, provider_resource, getattr(buyer, provider_resource) + provider_value)

        # subtract from buyer
        setattr(buyer, buyer_resource, getattr(buyer, buyer_resource) - buyer_value)
        # add to provider
        setattr(provider, buyer_resource, getattr(provider, buyer_resource) + buyer_value)

        text = f"{provider.name} gave {provider_value} {provider_resource} to {buyer.name}, received {buyer_value} {buyer_resource} from {buyer.name}"
        event_text.text = text

        # finally delete the object
        self.clean_up_references(accepted=True)

    def decline(self) -> None:
        # print("deal_select: decline!!!")
        self.clean_up_references(accepted=False)

    def clean_up_references(self, accepted) -> None:
        """
        Removes the instance from the deal manager lists and deletes it.

        Args:
            accepted (bool): Whether the deal was accepted or declined.

        Returns:
            None

        Raises:
            None

        This function removes the instance from the deal manager lists and deletes it. It first checks if the instance is
        present in the `deals` list of the deal manager. If it is, it appends the instance to the `accepted_deals` list
        if `accepted` is True, or to the `declined_deals` list if `accepted` is False. Then, it removes the instance from
        the `deals` list. After that, it calls the `reposition_deals` method of the deal manager to reposition the deals.
        Finally, it calls the `__del__` method of the instance to delete it.
        """
        # remove from lists and delete it
        if self in config.app.deal_manager.deals:

            if accepted:
                config.app.deal_manager.add_accepted_deal(self)
            else:
                config.app.deal_manager.add_declined_deal(self)

        self.__del__()

    def generate_provider_text(self) -> None:
        text = f"{config.app.players[self.provider_index].name} offers:  "
        self.provider_text = text

    def generate_offer_text(self) -> None:
        text = ""
        for key, value in self.offer.items():
            text += f"{value} {key} "
        self.offer_text = text

    def generate_request_text(self) -> None:
        text = f" for: "
        for key, value in self.request.items():
            text += f"{value} {key} "
        self.request_text = text

    def generate_time_text(self) -> None:
        # remaining time text
        current_time = time.time()
        self.remaining_time = self.end_time - current_time
        self.time_text = f"deal ends in: {int(self.remaining_time)} s"

    def draw_provider_text(self) -> None:
        self.wrap_text(
                win=self.win,
                text=self.provider_text,
                pos=(self.world_x + PROVIDER_TEXT_X_OFFSET, self.world_y + TOP_SPACING - 3),
                font=self.font,
                size=(3000, self.world_height),
                color=self.frame_color)

    def draw_offer_text(self) -> None:
        self.wrap_text(
                win=self.win,
                text=self.offer_text,
                pos=(self.world_x + OFFER_TEXT_X_OFFSET, self.world_y + TOP_SPACING - 3),
                font=self.font,
                size=(3000, self.world_height),
                color=self.frame_color,
                **{"iconize": ICONIZE_RESOURCES})

    def draw_request_text(self) -> None:
        self.wrap_text(
                win=self.win,
                text=self.request_text,
                pos=(self.world_x + REQUEST_TEXT_X_OFFSET, self.world_y + TOP_SPACING - 3),
                font=self.font,
                size=(3000, self.world_height),
                color=self.frame_color,
                **{"iconize": ICONIZE_RESOURCES})

    def draw_time_text(self) -> None:
        self.wrap_text(
                win=self.win,
                text=self.time_text,
                pos=(self.world_x + TIME_TEXT_X_OFFSET, self.world_y + TOP_SPACING - 3),
                font=self.font,
                size=(3000, self.world_height),
                color=self.frame_color)

    def draw_buttons(self) -> None:
        for i in self.buttons:
            i._hidden = False
            # dont know why this is needed, dirty hack
            self.win.blit(i.image, i.rect)

    def draw_provider_image(self) -> None:
        self.win.blit(self.provider_image, (self.world_x, self.world_y + TOP_SPACING))

    def reposition_buttons(self) -> None:
        """
        Repositions the buttons in the GUI.

        This function iterates over each button in the `buttons` list and repositions them based on their name.
        The buttons are repositioned using their `screen_x` and `screen_y` attributes.

        Parameters:
            None

        Returns:
            None
        """
        for i in self.buttons:
            i._hidden = False
            i._disabled = False
            if i.name == "agree_button":
                i.screen_x = self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE * 3
                i.screen_y = self.world_y + TOP_SPACING + 5

            if i.name == "decline_button":
                i.screen_x = self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE - BUTTON_SIZE / 2
                i.screen_y = self.world_y + TOP_SPACING + 5

    def draw(self) -> None:
        # end the deal after some time: DEAL_LIFETIME
        if self.remaining_time <= 0.0:
            self.clean_up_references(accepted=False)

        if not self._hidden and not self._disabled:
            self.draw_frame(corner_radius=3, corner_thickness=1)
            self.draw_provider_image()
            self.draw_provider_text()
            self.draw_offer_text()
            self.draw_request_text()
            self.generate_time_text()
            self.draw_time_text()
            self.reposition_buttons()
            self.draw_buttons()


def main():
    pygame.init()
    pygame.display.set_caption("DealEdit")
    screen = pygame.display.set_mode((800, 600))
    editor = DealSelect(screen, 100, 30, 220, 60, False, offer={"energy": 50}, request={"food": 30}, layer=9)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            screen.fill((0, 0, 0))

            editor.listen(events)
            editor.show()
            editor.draw()

            pygame.display.flip()


if __name__ == "__main__":
    main()
