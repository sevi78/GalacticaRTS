import pygame

from source.multimedia_library.images import get_image

TEXTBORDER = 10
FADE_OUT_TIME = 0


class TextWrap:  # original
    def __init__(self, **kwargs):
        self.click_surfaces_list = []
        self.click_surfaces = {}
        self.color = kwargs.get("color", pygame.Color('white'))
        self.link_color = kwargs.get("link_color", pygame.Color('blue'))
        self.alarm_color = kwargs.get("alarm_color", pygame.Color('red'))
        self.border = TEXTBORDER
        self.word_height_sum = 0
        self.link_found = False

    def wrap_text(self, win, text, pos, size, font, color=pygame.Color('white'), **kwargs) -> None:
        """ text wrapper function:
            Parameters
            ----------
            win : pygame.Surface
                surface to draw text on
            text : str
                text to draw
            pos : tuple
                (x, y) position of text
            size : tuple
                (width, height) size of text
            font : pygame.font.Font
                font to use
            color : pygame.Color
                color of text
            kwargs : dict
                keyword arguments to pass to wrap_text

                fade_out = kwargs.get("fade_out", False)
                alpha = kwargs.get("alpha", 255)

                # this creates an icon for every word in the text that is in zhe list:
                  example : resources = ["water", "energy", "food", "minerals", "technology", "population"]

                iconize = kwargs.get("iconize", [])
        """
        if not text: return

        fade_out = kwargs.get("fade_out", False)
        alpha = kwargs.get("alpha", 255)
        iconize = kwargs.get("iconize", [])
        alarm_links = kwargs.get("alarm_links", [])
        obj = kwargs.get("obj", None)
        self.color = color

        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = size  # Use self instead of undefined surface variable
        x, y = pos
        x += self.border
        y += self.border

        # store the sum of all words to get the max height of all text to resize the panel
        self.word_height_sum = 0

        resources = ["water", "energy", "food", "minerals", "technology", "population"]
        self.click_surfaces_list = []
        # self.link_found  = False
        for line in words:
            for word in line:

                # alarm links
                if word in str(alarm_links):
                    # color = self.link_color
                    self.link_found = True
                else:
                    color = self.color

                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()

                if iconize:
                    if word[-1:] == ":":
                        image_name = word.split(":")[0]
                    else:
                        image_name = word

                    if image_name in iconize:
                        if image_name in resources:
                            image_name = word.split(":")[0] + "_25x25.png"
                        else:
                            image_name = word.split(":")[0] + ".png"

                            # if image_name == "✓.png":
                            #     image_name = "check.png"

                        img = pygame.transform.scale(get_image(image_name), (word_height, word_height))
                        win.blit(img, (x, y))
                        x += word_height + space

                self.word_height_sum += word_height

                if x + word_width >= max_width:
                    x = pos[0] + self.border  # Reset the x.
                    y += word_height  # Start on new row.

                if fade_out:
                    # Create a copy of the original text surface.
                    txt_surf = word_surface.copy()

                    # Fill alpha_surf with this color to set its alpha value.
                    alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
                    alpha_surf.fill((255, 255, 255, alpha))

                    # To make the text surface transparent, blit the transparent
                    # alpha_surf onto it with the BLEND_RGBA_MULT flag.
                    txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    win.blit(txt_surf, (x, y))

                else:
                    win.blit(word_surface, (x, y))

                word_surface.get_rect().x = x
                word_surface.get_rect().y = y

                # add to click surfaces list
                # if word in str(alarm_links):
                #     self.set_click_surfaces(word, word_height, word_width, x, y)
                #     pygame.draw.rect(win, colors.ui_darker, (x, y, word_width, word_height), 1, 3)
                # else:
                #     index_ = line.index(word)
                #     if index_ > 0:
                #         if line[line.index(word)-1] in :
                #             self.set_click_surfaces(word, word_height, word_width, x, y)
                #             pygame.draw.rect(win, colors.ui_darker, (x, y, word_width, word_height), 1, 3)
                if self.link_found:
                    self.set_click_surfaces(word, word_height, word_width, x, y)
                    # pygame.draw.rect(win, colors.ui_darker, (x, y, word_width, word_height), 1, 3)

                x += word_width + space

            x = pos[0] + self.border  # Reset the x.
            y += word_height  # Start on new row.

            # get the last height value
            self.word_height_sum = y

    def set_click_surfaces(self, word, word_height, word_width, x, y):
        self.click_surfaces_list.append((word, pygame.Rect(x, y, word_width, word_height)))


def main():
    pygame.init()
    win = pygame.display.set_mode((600, 600))
    text_wrap = TextWrap()
    run = True
    while run:
        win.fill((0, 0, 0))

        text_wrap.wrap_text(
                win=win,
                text="Hello World! attack ",
                pos=(255, 255),
                size=(150, 30),
                font=pygame.font.SysFont(None, 38),
                color=pygame.color.THECOLORS.get("orange"),
                fade_out=False,
                alpha=255,
                iconize=[],
                alarm_links=["attack"]
                )

        pygame.display.update()
        events = pygame.event.get()
        text_wrap.listen(events)

        for event in events:

            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


if __name__ == '__main__':
    main()
