import pygame

from source.configuration.game_config import config
from source.gui.container.container_widget_item import ContainerWidgetItem
from source.gui.widgets.buttons.button import Button
from source.multimedia_library.images import get_image



class DealItem(ContainerWidgetItem):
    def __init__(self, win, x, y, width, height, image, index, **kwargs):
        self.player_index = kwargs.get('player_index', 0)
        self.image = get_image(config.app.players[self.player_index].image_name)
        self.offer = kwargs.get('offer', None)
        self.request = kwargs.get('request', None)
        ContainerWidgetItem.__init__(self, win, x, y, width, height, image, index, **kwargs)

        # Buttons
        self.accept_button = Button(
            win,
            self.world_x,
            self.world_y,
            self.world_height,
            self.world_height,
            isSubWidget = False,
            image = pygame.transform.scale(get_image("yes_icon.png"),
                (self.world_height, self.world_height)),
            transparent = True,
            parent = self,
            onClick = lambda: self.accept(),
            layer= 10)

        self.widgets.append(self.accept_button)


        # self.accept_button.show()

        # self.no_button = Button(self.win, self.get_screen_x() + self.get_screen_width() / 2 + 30,
        #                                   self.world_y + self.get_screen_height(), 60, 60, isSubWidget=False,
        #     image=pygame.transform.scale(get_image("no_icon.png"), (60, 60)),
        #     transparent=True, parent=self, onClick=lambda: self.decline())

        self.set_position((x,y))


    def set_text(self):
        text = f"offer: {self.offer} request: {self.request}"
        return text

    def accept(self):
        pass



