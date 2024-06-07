import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.gui.widgets.buttons.button import Button
from source.handlers.color_handler import colors
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds
from source.text.text_wrap import TextWrap


class EventPanel(TextWrap, EditorBase):
    def __init__(self, win, x, y, width, height, interface_variables, **kwargs):
        TextWrap.__init__(self)
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)

        self.name = "event panel"
        self.layer = kwargs.get("layer", 10)
        self.win = win
        self.parent = kwargs.get("parent")
        self.frame_color = colors.frame_color
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.font_size = 32
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.title_font = pygame.font.SysFont(config.font_name, 50)
        self.center = kwargs.get("center", True)

        # surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect[0] = x
        self.surface_rect[1] = y
        self.image = kwargs.get("image", get_image("event_panel.png"))
        self.image_scaled = pygame.transform.scale(self.image, (width, height))

        # text
        self.size = (width + self.get_screen_x() - self.get_screen_width() / 6,
                     height + self.get_screen_height())  # used for text wrapper, makes no sense but works

        self.title = None
        self.title_surface_rect = None
        self.title_surface = None

        self.body = None
        self.end_text = None
        self.end_text_surface_rect = None
        self.end_text_surface = None

        self.functions = []

        # Buttons
        self.yes_button = Button(self.win, self.get_screen_x() + self.get_screen_width() / 2 - 30,
                                           self.world_y + self.get_screen_height(), 60, 60, is_sub_widget=False,
                image=pygame.transform.scale(get_image("yes_icon.png"), (60, 60)),
                transparent=True, parent=self, on_click=lambda: self.accept())

        self.no_button = Button(self.win, self.get_screen_x() + self.get_screen_width() / 2 + 30,
                                          self.world_y + self.get_screen_height(), 60, 60, is_sub_widget=False,
                image=pygame.transform.scale(get_image("no_icon.png"), (60, 60)),
                transparent=True, parent=self, on_click=lambda: self.decline())

        self.max_height = height
        self.hide()

    def accept(self):
        if not self._hidden:
            if self.functions:
                # if self.game_event.deal:
                #     self.game_event.deal.make_deal()
                #
                # else:
                getattr(config.app.game_event_handler, self.functions["yes"])()

            self.hide()
            config.game_paused = False

    def decline(self):
        if not self._hidden:
            if self.functions:
                # if self.game_event.deal:
                #     self.game_event.deal.make_deal()
                #
                # else:
                if hasattr(config.app.game_event_handler, self.functions["no"]):
                    getattr(config.app.game_event_handler, self.functions["no"])()
                else:
                    print(f"event_panel. error: cannot call: {self.functions['no']}")

            self.hide()
            config.game_paused = False

    def set_text(self, event):
        self.title = event.title
        self.body = event.body
        self.end_text = event.end_text
        self.functions = event.functions

        if not self.functions:
            self.yes_button.hide()
            self.no_button.hide()
        if self.functions:
            if "yes" in self.functions.keys():
                self.yes_button.show()
            if "no" in self.functions.keys():
                self.no_button.show()

        self.show()

    def set_game_event(self, event):
        self.image = event.image
        self.image_raw = event.image
        event.set_body()
        self.set_text(event)
        # config.app.pause_game()
        config.game_paused = True

    def listen(self, events):
        mouse_state = mouse_handler.get_mouse_state()
        if mouse_state == MouseState.LEFT_CLICK:
            if not self.functions:
                if not self._hidden:
                    config.game_paused = False

                self.hide()

    def draw(self):
        if not self._hidden:
            # image
            self.win.blit(self.image_scaled, self.surface_rect)
            # self.draw_frame()

            # title
            self.title_surface = self.title_font.render(self.title, self.font, colors.ui_dark)
            self.title_surface_rect = self.title_surface.get_rect()
            self.title_surface_rect.x = self.world_x + self.get_screen_width() / 2 - self.title_surface.get_width() / 2
            self.title_surface_rect.y = (self.world_y + self.get_screen_height() / 8)
            self.win.blit(self.title_surface, self.title_surface_rect)

            # body
            self.wrap_text(self.win, self.body, (self.get_position()[0] + self.get_screen_width() / 6,
                                                 self.title_surface_rect.y + 60), self.size, self.font, colors.ui_dark)

            # end_text
            self.end_text_surface = self.font.render(self.end_text, self.font, colors.ui_dark)
            self.end_text_surface_rect = self.end_text_surface.get_rect()
            self.end_text_surface_rect.x = self.world_x + self.get_screen_width() / 2 - self.end_text_surface.get_width() / 2
            self.end_text_surface_rect.y = self.world_y + self.get_screen_height() - self.get_screen_height() / 3
            self.win.blit(self.end_text_surface, self.end_text_surface_rect)

            # buttons
            self.yes_button.set_position((
                self.world_x + self.get_screen_width() / 2 - self.yes_button.get_screen_width(),
                self.end_text_surface_rect.y + self.yes_button.get_screen_height() / 2))

            self.no_button.set_position((self.world_x + self.get_screen_width() / 2, self.yes_button.get_screen_y()))

            # sound
            pygame.mixer.music = sounds.intro_drama
            pygame.mixer.music.play(fade_ms=1000)

        else:
            pygame.mixer.Sound.fadeout(sounds.intro_drama, 5000)
            self.yes_button.hide()
            self.no_button.hide()
