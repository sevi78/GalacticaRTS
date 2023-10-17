import pygame

TEXTBORDER = 10


class TextWrap:
    def __init__(self):
        self.border = TEXTBORDER
        self.word_height_sum = 0
        self.text_surfaces = {}

    def wrap_text(self, text, pos, size, font, color=pygame.Color('white')):
        """ text wrapper function """
        if not text: return
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = size  # Use self instead of undefined surface variable
        x, y = pos

        x += self.border
        y += self.border

        # store the sum of all words to get the max height of all text to resize the panel
        self.word_height_sum = 0

        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()

                self.word_height_sum += word_height

                if x + word_width >= max_width:
                    x = pos[0] + self.border  # Reset the x.
                    y += word_height  # Start on new row.
                self.text_surfaces[str(x) + "_" + str(y)] = word_surface
                self.win.blit(word_surface, (x, y))
                x += word_width + space

            x = pos[0] + self.border  # Reset the x.
            y += word_height  # Start on new row.

            # get the last height value
            self.word_height_sum = y

#
# import textwrap
#
# class TextWrap_not_wrapping_anymore:
#     def __init__(self):
#         self.border = TEXTBORDER
#         self.word_height_sum = 0
#         self.text_surfaces = {}
#
#     def wrap_text(self, text, pos, size, font, color=pygame.Color('white')):
#         """ text wrapper function """
#         if not text: return
#         words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
#         space = font.size(' ')[0]  # The width of a space.
#         max_width, max_height = size  # Use self instead of undefined surface variable
#         x, y = pos
#
#         x += self.border
#         y += self.border
#
#         # store the sum of all words to get the max height of all text to resize the panel
#         self.word_height_sum = 0
#
#         # Wrap the text using textwrap module
#         wrapped_lines = []
#         for line in words:
#             wrapped_lines.extend(textwrap.wrap(' '.join(line), width=max_width))
#
#         for line in wrapped_lines:
#             line_surface = font.render(line, 0, color)
#             line_width, line_height = line_surface.get_size()
#
#             self.word_height_sum += line_height
#
#             # Center the line horizontally
#             x_offset = (max_width - line_width) // 2
#
#             self.text_surfaces[str(x) + "_" + str(y)] = line_surface
#             self.win.blit(line_surface, (x + x_offset, y))
#             y += line_height
#
#         # get the last height value
#         self.word_height_sum = y
#
# import textwrap
#
# class TextWrap__:
#     def __init__(self):
#         self.border = TEXTBORDER
#         self.word_height_sum = 0
#         self.text_surfaces = {}
#
#     def wrap_text(self, text, pos, size, font, color=pygame.Color('white')):
#         """ text wrapper function """
#         if not text: return
#         words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
#         space = font.size(' ')[0]  # The width of a space.
#         max_width, max_height = size  # Use self instead of undefined surface variable
#         x, y = pos
#
#         x += self.border
#         y += self.border
#
#         # store the sum of all words to get the max height of all text to resize the panel
#         self.word_height_sum = 0
#
#         # Wrap the text using textwrap module
#         wrapped_lines = []
#         for line in words:
#             wrapped_lines.extend(textwrap.wrap(' '.join(line), width=max_width))
#
#         # Calculate the maximum width of the text based on the available space
#         max_line_width = max(font.size(line)[0] for line in wrapped_lines)
#
#         for line in wrapped_lines:
#             line_surface = font.render(line, 0, color)
#             line_width, line_height = line_surface.get_size()
#
#             self.word_height_sum += line_height
#
#             # Center the line horizontally and ensure it stays within the borders
#             x_offset = (max_width - max_line_width) // 2
#             if x_offset < 0:
#                 x_offset = 0
#
#             self.text_surfaces[str(x) + "_" + str(y)] = line_surface
#             self.win.blit(line_surface, (x + x_offset, y))
#             y += line_height
#
#         # get the last height value
#         self.word_height_sum = y
#
# import textwrap
#
# class TextWrap__:
#     def __init__(self):
#         self.border = TEXTBORDER
#         self.word_height_sum = 0
#         self.text_surfaces = {}
#
#     import textwrap
#
# class TextWrap__:
#     def __init__(self):
#         self.border = TEXTBORDER
#         self.word_height_sum = 0
#         self.text_surfaces = {}
#
#     def wrap_text(self, text, pos, size, font, color=pygame.Color('white')):
#         """ text wrapper function """
#         if not text: return
#         words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
#         space = font.size(' ')[0]  # The width of a space.
#         max_width, max_height = size  # Use self instead of undefined surface variable
#         x, y = pos
#
#         x += self.border
#         y += self.border
#
#         # store the sum of all words to get the max height of all text to resize the panel
#         self.word_height_sum = 0
#
#         # Wrap the text using textwrap module
#         wrapped_lines = []
#         for line in words:
#             wrapped_lines.extend(textwrap.wrap(' '.join(line), width=max_width - 2 * self.border))
#
#         # Calculate the maximum width of the wrapped text
#         max_line_width = max(font.size(line)[0] for line in wrapped_lines)
#
#         for line in wrapped_lines:
#             line_surface = font.render(line, 0, color)
#             line_width, line_height = line_surface.get_size()
#
#             self.word_height_sum += line_height
#
#             # Center the line horizontally and ensure it stays within the borders
#             x_offset = (max_width - max_line_width) // 2
#             if x_offset < 0:
#                 x_offset = 0
#
#             self.text_surfaces[str(x) + "_" + str(y)] = line_surface
#             self.win.blit(line_surface, (x + x_offset, y))
#             y += line_height
#
#         # get the last height value
#         self.word_height_sum = y
#
#
# import textwrap
#
# class TextWrap_ai_shit:
#     def __init__(self):
#         self.border = TEXTBORDER
#         self.word_height_sum = 0
#         self.text_surfaces = {}
#
#     def wrap_text(self, text, pos, size, font, color=pygame.Color('white')):
#         """ text wrapper function """
#         if not text: return
#         words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
#         space = font.size(' ')[0]  # The width of a space.
#         max_width, max_height = size  # Use self instead of undefined surface variable
#         x, y = pos
#
#         x += self.border
#         y += self.border
#
#         # store the sum of all words to get the max height of all text to resize the panel
#         self.word_height_sum = 0
#
#         # Wrap the text using textwrap module
#         wrapped_lines = []
#         for line in words:
#             wrapped_lines.extend(textwrap.wrap(' '.join(line), width=max_width - 2 * self.border))
#
#         # Calculate the maximum width of the wrapped text
#         max_line_width = max(font.size(line)[0] for line in wrapped_lines)
#
#         for line in wrapped_lines:
#             line_surface = font.render(line, 0, color)
#             line_width, line_height = line_surface.get_size()
#
#             self.word_height_sum += line_height
#
#             # Center the line horizontally and ensure it stays within the borders
#             x_offset = (max_width - max_line_width) // 2
#             if x_offset < 0:
#                 x_offset = 0
#
#             self.text_surfaces[str(x) + "_" + str(y)] = line_surface
#             self.win.blit(line_surface, (x + x_offset, y))
#             y += line_height
#
#         # get the last height value
#         self.word_height_sum = y
