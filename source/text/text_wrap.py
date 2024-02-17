import pygame

from source.multimedia_library.images import get_image

TEXTBORDER = 10
FADE_OUT_TIME = 0


class TextWrap:  # original
    def __init__(self, **kwargs):

        self.border = TEXTBORDER
        self.word_height_sum = 0

    def wrap_text(self, win, text, pos, size, font, color=pygame.Color('white'), **kwargs):
        """ text wrapper function """
        if not text: return
        fade_out = kwargs.get("fade_out", False)
        alpha = kwargs.get("alpha", 255)
        iconize = kwargs.get("iconize", [])

        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = size  # Use self instead of undefined surface variable
        x, y = pos
        x += self.border
        y += self.border

        # store the sum of all words to get the max height of all text to resize the panel
        self.word_height_sum = 0

        resources = ["water", "energy", "food", "minerals", "technology", "population"]

        for line in words:
            for word in line:

                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                # pygame.draw.rect(win, colors.ui_darker,(x,y,word_width, word_height),1 )

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

                x += word_width + space

            x = pos[0] + self.border  # Reset the x.
            y += word_height  # Start on new row.

            # get the last height value
            self.word_height_sum = y
