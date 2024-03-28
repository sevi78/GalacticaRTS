import copy

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.handlers.image_handler import overblit_button_image


class DealManager(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        #  widgets
        self.overblit_image = None
        self.widgets = []
        self.deals = []

        # hide initially
        self.hide()

    def set_deal(self, deal):
        deal.world_x = self.world_x
        self.deals.append(deal)
        self.widgets.append(deal)
        self.reposition_deals()

    def overblit_deal_icon(self):
        # store the image for overblitting
        if not self.overblit_image:
            self.overblit_image = copy.copy(config.app.resource_panel.deal_manager_icon.image)

        # check if there are any deals
        if len(self.deals) > 0:
            overblit_button_image(config.app.resource_panel.deal_manager_icon, "warning.png", False)
        else:
            # reset the image
            config.app.resource_panel.deal_manager_icon.image = self.overblit_image

    def reposition_deals(self):
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
