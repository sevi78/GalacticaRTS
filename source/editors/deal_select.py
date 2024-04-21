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



class DealSelect(EditorBase, TextWrap):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
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
        self.deal_text = ""
        self.time_text = ""
        self.generate_deal_text()

        # hide initially
        self.hide()
        self.max_height = 25

    def __repr__(self):
        return f"DealSelect: provider: {config.app.players[self.provider_index].name}, {self.offer} for {self.request}"

    def create_buttons(self):
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

    def agree(self, buyer):
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
        self.clean_up_references()

    def decline(self):
        # print("deal_select: decline!!!")
        self.clean_up_references()

    def clean_up_references(self):
        if self in config.app.deal_manager.deals:
            config.app.deal_manager.deals.remove(self)

        config.app.deal_manager.reposition_deals()
        self.__del__()

    def generate_deal_text(self):
        # offer and requet text
        text = f"{config.app.players[self.provider_index].name} offers:  "

        for key, value in self.offer.items():
            text += f"{value} {key} "

        text += f" for: "
        for key, value in self.request.items():
            text += f"{value} {key} "

        self.deal_text = text

    def generate_time_text(self):
        # remaining time text
        current_time = time.time()
        self.remaining_time = self.end_time - current_time
        self.time_text = f" deal end in: {int(self.remaining_time)} s"


    def draw_deal_text(self):
        self.wrap_text(
            win=self.win,
            text=self.deal_text,
            pos=(self.world_x + 10, self.world_y + TOP_SPACING - 3),
            font=self.font,
            size=(3000, self.world_height),
            color=self.frame_color,
            iconize=["food", "energy", "water", "minerals", "technology"])
    def draw_time_text(self):
        self.wrap_text(
            win=self.win,
            text=self.time_text,
            pos=(self.world_x + 280, self.world_y + TOP_SPACING - 3),
            font=self.font,
            size=(3000, self.world_height),
            color=self.frame_color)

    def draw_buttons(self):
        for i in self.buttons:
            i._hidden = False
            # dont know why this is needed, dirty hack
            self.win.blit(i.image, i.rect)

    def draw_provider_image(self):
        self.win.blit(self.provider_image, (self.world_x, self.world_y + TOP_SPACING))

    def reposition_buttons(self):
        for i in self.buttons:
            i._hidden = False
            i._disabled = False
            if i.name == "agree_button":
                i.screen_x = self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE * 3
                i.screen_y = self.world_y + TOP_SPACING + 5

            if i.name == "decline_button":
                i.screen_x = self.get_screen_x() + self.get_screen_width() - BUTTON_SIZE - BUTTON_SIZE / 2
                i.screen_y = self.world_y + TOP_SPACING + 5

    def draw(self):
        # end the deal after some time: DEAL_LIFETIME
        if self.remaining_time <= 0.0:
            self.clean_up_references()

        if not self._hidden and not self._disabled:
            self.draw_frame(corner_radius=3, corner_thickness=1)
            self.draw_provider_image()
            self.draw_deal_text()
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
