import copy

from source.configuration.game_config import config
from source.editors.deal_select import DealSelect
from source.editors.editor_base.editor_base import EditorBase
from source.handlers.image_handler import overblit_button_image

OFFER_DEAL_PERCENT = 25
MAX_DEALS_PER_PLAYERS = 3


class DealManager(EditorBase):  # new
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs) -> None:
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        #  widgets
        self.overblit_image = None
        self.widgets = []
        self.deals = []
        self.accepted_deals = []
        self.declined_deals = []
        self.last_deals = {}

        # hide initially
        self.hide()

    def set_deal(self, deal) -> None:
        """
        Sets a deal for the current editor, updating various data structures and triggering a repositioning of deals.

        Parameters:
            deal: The deal object to be set for the editor.

        Returns:
            None
        """
        deal.world_x = self.world_x
        self.last_deals[deal.provider_index] = deal
        self.deals.append(deal)
        self.widgets.append(deal)
        self.reposition_deals()

    def get_deals(self) -> list:
        return self.deals

    def get_deals_from_player(self, player) -> list:
        player_deals = []
        for i in self.deals:
            if i.provider_index == player.owner:
                player_deals.append(i)

        return player_deals

    def add_fitting_deal(self, player, lowest_value_key, highest_value_key) -> None:
        """
        Adds a fitting deal for a given player.

        Parameters:
            player (Player): The player for whom the deal is being added.
            lowest_value_key (str): The key representing the lowest value in the deal.
            highest_value_key (str): The key representing the highest value in the deal.

        Returns:
            None

        This function adds a fitting deal for a given player. It first checks if the player has reached the maximum
        number of deals allowed. If not, it calculates the value to offer based on the highest value key and the offer
        deal percentage. The offer and request dictionaries are then created.
        Finally, a DealSelect object is created with the necessary parameters and added to the deals list.
        """
        # limit deals per player
        player_deals = self.get_deals_from_player(player)
        deal_amount = len(player_deals)
        if deal_amount > MAX_DEALS_PER_PLAYERS:
            return

        # calculate the value to offer, this case 25 percent
        offer_value = int(player.get_stock()[highest_value_key] / 100 * OFFER_DEAL_PERCENT)
        offer = {highest_value_key: offer_value}
        request = {lowest_value_key: offer_value}

        deal = DealSelect(
            config.app.win,
            0,
            30,
            300,
            60,
            False,
            offer=offer,
            request=request,
            layer=9,
            parent=config.app,
            player_index=player.owner,
            save=False
            )
        self.set_deal(deal)

    def get_fitting_deal(self, player) -> None:
        """
        Retrieves a fitting deal for a given player.

        Parameters:
            player (Player): The player for whom the fitting deal is being retrieved.

        Returns:
            None

        This function retrieves all deals and compares the keys of each deal with the lowest value key of the player's
        resource stock. If a matching key is found, the deal is agreed to by the player.
        Means the deal_select.agree() method of the deal object in self.deals is called

        Note:
            - The player cannot buy its own deals.
            - The function assumes that the player has an auto economy handler.
        """
        # get all deals
        deals = self.get_deals()
        resource_stock = player.get_resource_stock()

        for i in deals:
            # ensure that player cant buy its own deals
            if not i.provider_index == player.owner:
                # compare keys, get fitting deal
                deal_key = list(i.offer.keys())[0]
                if deal_key == player.auto_economy_handler.get_lowest_value_key(resource_stock):
                    i.agree(player.owner)

    def overblit_deal_icon(self) -> None:
        """
        Overblits the deal icon on the settings panel.

        This function stores the image for overblitting if it hasn't been stored already.
        It then checks if there are any deals. If there are, it overblits the deal icon with a warning image.
        If there are no deals, it resets the image of the deal icon to the stored image.

        Parameters:
            None

        Returns:
            None
        """
        # store the image for overblitting
        if not self.overblit_image:
            self.overblit_image = copy.copy(config.app.settings_panel.deal_manager_icon.image)

        # check if there are any deals
        if len(self.deals) > 0:
            overblit_button_image(config.app.settings_panel.deal_manager_icon, "warning.png", False)
        else:
            # reset the image
            config.app.settings_panel.deal_manager_icon.image = self.overblit_image

    def reposition_deals(self) -> None:
        """
        Repositions the deals in the current instance of the class.

        This function iterates through each deal in the `deals` list and updates the position of each deal based on the current instance's `_hidden`, `rect.width`, `world_x`, `world_y`, and `deals.index(i)` values. The `screen_width`, `screen_x`, and `world_y` attributes of each deal are updated accordingly.

        After repositioning the deals, the `max_height` attribute of the current instance is set to the product of the length of the `deals` list and 30.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        for i in self.deals:
            i._hidden = self._hidden
            i.screen_width = self.rect.width
            i.screen_x = self.world_x
            i.world_y = self.world_y + i.world_height / 2 * self.deals.index(i)

        self.max_height = len(self.deals) * 30

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.drag(events)

    def draw(self):
        self.overblit_deal_icon()
        if not self._hidden and not self._disabled:
            self.reposition_deals()
