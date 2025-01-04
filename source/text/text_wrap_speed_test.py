# import pygame
# from typing import List, Tuple, Dict, Optional
# from dataclasses import dataclass, field
# import time
#
# # Mocking the get_image function since we don't have the actual implementation
# def get_image(name):
#     return pygame.Surface((25, 25))
#
# TEXTBORDER = 10
# FADE_OUT_TIME = 0
#
# @dataclass
# class TextWrapConfig:
#     color: pygame.Color = field(default_factory=lambda: pygame.Color('white'))
#     link_color: pygame.Color = field(default_factory=lambda: pygame.Color('blue'))
#     alarm_color: pygame.Color = field(default_factory=lambda: pygame.Color('red'))
#     border: int = TEXTBORDER
#



import time
from dataclasses import dataclass, field
from typing import List, Tuple

import pygame

from source.multimedia_library.images import scale_image_cached


# Mocking the get_image function
def get_image(name):
    return pygame.Surface((25, 25))

TEXTBORDER = 10
FADE_OUT_TIME = 0

@dataclass
class TextWrapConfig:
    color: pygame.Color = field(default_factory=lambda: pygame.Color('white'))
    link_color: pygame.Color = field(default_factory=lambda: pygame.Color('blue'))
    alarm_color: pygame.Color = field(default_factory=lambda: pygame.Color('red'))
    border: int = TEXTBORDER


# Refactored TextWrap class
class TextWrapRefactored:
    def __init__(self, config: TextWrapConfig = TextWrapConfig()):
        self.config = config
        self.click_surfaces_list: List[Tuple[str, pygame.Rect]] = []
        self.click_surfaces: Dict[str, pygame.Rect] = {}
        self.word_height_sum: int = 0
        self.link_found: bool = False

    def wrap_text(
            self, win: pygame.Surface, text: str, pos: Tuple[int, int], size: Tuple[int, int],
            font: pygame.font.Font, color: pygame.Color = pygame.Color('white'), **kwargs
            ) -> int:
        if not text:
            return pos[1]

        fade_out: bool = kwargs.get("fade_out", False)
        alpha: int = kwargs.get("alpha", 255)
        iconize: List[str] = kwargs.get("iconize", [])
        alarm_links: List[str] = kwargs.get("alarm_links", [])
        replace_text_with_icon: bool = kwargs.get("replace_text_with_icon", False)
        self.color = color

        lines: List[str] = text.split('\n')
        space: int = font.size(' ')[0]
        max_width, max_height = size
        x, y = pos
        x += self.config.border
        y += self.config.border

        self.word_height_sum = 0
        self.click_surfaces_list = []

        for line in lines:
            words: List[str] = line.split()
            for word in words:
                color = self.config.alarm_color if word in alarm_links else self.color
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()

                icon_added, icon_width = self._handle_iconize(win, word, iconize, word_height, x, y, replace_text_with_icon)
                if icon_added:
                    if replace_text_with_icon:
                        x += icon_width + space
                        continue
                    else:
                        x += icon_width + space

                if x + word_width >= max_width:
                    x = pos[0] + self.config.border
                    y += word_height

                self._render_word(win, word_surface, x, y, fade_out, alpha)

                if word in alarm_links:
                    self._set_click_surfaces(word, word_height, word_width, x, y)

                x += word_width + space
                self.word_height_sum = max(self.word_height_sum, y + word_height)

            x = pos[0] + self.config.border
            y += word_height

        y += word_height
        self.word_height_sum = y - pos[1]

        return y

    def _handle_iconize(self, win: pygame.Surface, word: str, iconize: List[str], word_height: int, x: int, y: int, replace_text: bool) -> Tuple[bool, int]:
        if not iconize:
            return False, 0

        image_name = word[:-1] if word.endswith(':') else word
        if image_name not in iconize:
            return False, 0

        resources = ["water", "energy", "food", "minerals", "technology", "population"]
        if image_name in resources:
            image_name = f"{image_name}_25x25.png"
        else:
            image_name = f"{image_name}.png"
            if image_name == "\u2713.png":
                image_name = "check.png"

        img = scale_image_cached(get_image(image_name), (word_height, word_height))
        win.blit(img, (x, y))
        return True, word_height

    def _new_line(self, pos: Tuple[int, int], word_height: int) -> Tuple[int, int]:
        return pos[0] + self.config.border, pos[1] + word_height

    def _render_word(self, win: pygame.Surface, word_surface: pygame.Surface, x: int, y: int, fade_out: bool, alpha: int) -> None:
        if fade_out:
            txt_surf = word_surface.copy()
            alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            win.blit(txt_surf, (x, y))
        else:
            win.blit(word_surface, (x, y))

    def _set_click_surfaces(self, word: str, word_height: int, word_width: int, x: int, y: int) -> None:
        self.click_surfaces_list.append((word, pygame.Rect(x, y, word_width, word_height)))

# Optimized TextWrap class
class TextWrapOptimized:
    def __init__(self, config: TextWrapConfig = TextWrapConfig()):
        self.config = config
        self.click_surfaces_list: List[Tuple[str, pygame.Rect]] = []
        self.word_height_sum: int = 0
        self.resources = frozenset(["water", "energy", "food", "minerals", "technology", "population"])

    def wrap_text(
            self, win: pygame.Surface, text: str, pos: Tuple[int, int], size: Tuple[int, int],
            font: pygame.font.Font, color: pygame.Color = pygame.Color('white'), **kwargs
    ) -> int:
        if not text:
            return pos[1]

        fade_out: bool = kwargs.get("fade_out", False)
        alpha: int = kwargs.get("alpha", 255)
        iconize: frozenset = frozenset(kwargs.get("iconize", []))
        alarm_links: frozenset = frozenset(kwargs.get("alarm_links", []))
        replace_text_with_icon: bool = kwargs.get("replace_text_with_icon", False)

        lines: List[str] = text.split('\n')
        space: int = font.size(' ')[0]
        max_width, _ = size
        x, y = pos
        x += self.config.border
        y += self.config.border

        self.word_height_sum = 0
        self.click_surfaces_list.clear()

        word_height = font.get_height()

        for line in lines:
            words: List[str] = line.split()
            for word in words:
                color = self.config.alarm_color if word in alarm_links else color
                word_surface = font.render(word, True, color)
                word_width = word_surface.get_width()

                icon_added, icon_width = self._handle_iconize(win, word, iconize, word_height, x, y, replace_text_with_icon)
                if icon_added:
                    if replace_text_with_icon:
                        x += icon_width + space
                        continue
                    x += icon_width + space

                if x + word_width >= max_width:
                    x = pos[0] + self.config.border
                    y += word_height

                self._render_word(win, word_surface, x, y, fade_out, alpha)

                if word in alarm_links:
                    self.click_surfaces_list.append((word, pygame.Rect(x, y, word_width, word_height)))

                x += word_width + space
                self.word_height_sum = max(self.word_height_sum, y + word_height)

            x = pos[0] + self.config.border
            y += word_height

        y += word_height
        self.word_height_sum = y - pos[1]

        return y

    def _handle_iconize(self, win: pygame.Surface, word: str, iconize: frozenset, word_height: int, x: int, y: int, replace_text: bool) -> Tuple[bool, int]:
        if not iconize:
            return False, 0

        image_name = word[:-1] if word.endswith(':') else word
        if image_name not in iconize:
            return False, 0

        if image_name in self.resources:
            image_name = f"{image_name}_25x25.png"
        else:
            image_name = f"{image_name}.png"
            if image_name == "\u2713.png":
                image_name = "check.png"

        img = scale_image_cached(get_image(image_name), (word_height, word_height))
        win.blit(img, (x, y))
        return True, word_height

    def _render_word(self, win: pygame.Surface, word_surface: pygame.Surface, x: int, y: int, fade_out: bool, alpha: int) -> None:
        if fade_out:
            txt_surf = word_surface.copy()
            alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            win.blit(txt_surf, (x, y))
        else:
            win.blit(word_surface, (x, y))

class TextWrapOptimizedII:
    def __init__(self, config: TextWrapConfig = TextWrapConfig()):
        self.config = config
        self.click_surfaces_list: List[Tuple[str, pygame.Rect]] = []
        self.word_height_sum: int = 0
        self.resources = frozenset(["water", "energy", "food", "minerals", "technology", "population"])
        self.image_cache: Dict[Tuple[str, int], pygame.Surface] = {}
        self.last_text: str = ""
        self.last_font_size: int = 0

    def wrap_text(
            self, win: pygame.Surface, text: str, pos: Tuple[int, int], size: Tuple[int, int],
            font: pygame.font.Font, color: pygame.Color = pygame.Color('white'), **kwargs
    ) -> int:
        # Check if text or font size has changed
        current_font_size = font.get_height()
        if text != self.last_text or current_font_size != self.last_font_size:
            self.clear_cache()
            self.last_text = text
            self.last_font_size = current_font_size

        # Rest of the wrap_text method remains the same
        if not text:
            return pos[1]

        fade_out: bool = kwargs.get("fade_out", False)
        alpha: int = kwargs.get("alpha", 255)
        iconize: frozenset = frozenset(kwargs.get("iconize", []))
        alarm_links: frozenset = frozenset(kwargs.get("alarm_links", []))
        replace_text_with_icon: bool = kwargs.get("replace_text_with_icon", False)

        lines: List[str] = text.split('\n')
        space: int = font.size(' ')[0]
        max_width, _ = size
        x, y = pos
        x += self.config.border
        y += self.config.border

        self.word_height_sum = 0
        self.click_surfaces_list.clear()

        word_height = font.get_height()

        for line in lines:
            words: List[str] = line.split()
            for word in words:
                color = self.config.alarm_color if word in alarm_links else color
                word_surface = font.render(word, True, color)
                word_width = word_surface.get_width()

                icon_added, icon_width = self._handle_iconize(win, word, iconize, word_height, x, y, replace_text_with_icon)
                if icon_added:
                    if replace_text_with_icon:
                        x += icon_width + space
                        continue
                    x += icon_width + space

                if x + word_width >= max_width:
                    x = pos[0] + self.config.border
                    y += word_height

                self._render_word(win, word_surface, x, y, fade_out, alpha)

                if word in alarm_links:
                    self.click_surfaces_list.append((word, pygame.Rect(x, y, word_width, word_height)))

                x += word_width + space
                self.word_height_sum = max(self.word_height_sum, y + word_height)

            x = pos[0] + self.config.border
            y += word_height

        y += word_height
        self.word_height_sum = y - pos[1]

        return y

    def _handle_iconize(self, win: pygame.Surface, word: str, iconize: frozenset, word_height: int, x: int, y: int, replace_text: bool) -> Tuple[bool, int]:
        if not iconize:
            return False, 0

        image_name = word[:-1] if word.endswith(':') else word
        if image_name not in iconize:
            return False, 0

        if image_name in self.resources:
            image_name = f"{image_name}_25x25.png"
        else:
            image_name = f"{image_name}.png"
            if image_name == "\u2713.png":
                image_name = "check.png"

        # Check if the scaled image is in the cache
        cache_key = (image_name, word_height)
        if cache_key not in self.image_cache:
            # If not in cache, load, scale, and cache the image
            original_img = get_image(image_name)
            scaled_img = scale_image_cached(original_img, (word_height, word_height))
            self.image_cache[cache_key] = scaled_img
        else:
            # If in cache, use the cached image
            scaled_img = self.image_cache[cache_key]

        win.blit(scaled_img, (x, y))
        return True, word_height

    def clear_cache(self):
        """Clear the image cache when it's no longer needed."""
        self.image_cache.clear()

    def _render_word(
            self, win: pygame.Surface, word_surface: pygame.Surface, x: int, y: int, fade_out: bool, alpha: int
            ) -> None:
        if fade_out:
            txt_surf = word_surface.copy()
            alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            win.blit(txt_surf, (x, y))
        else:
            win.blit(word_surface, (x, y))


import pygame
from typing import List, Tuple, Dict


class TextWrapOptimizedIII:
    __slots__ = (
    'config', 'click_surfaces_list', 'word_height_sum', 'resources', 'image_cache', 'word_cache', 'last_text',
    'last_font_size')

    def __init__(self, config):
        self.config = config
        self.click_surfaces_list = []
        self.word_height_sum = 0
        self.resources = frozenset(["water", "energy", "food", "minerals", "technology", "population"])
        self.image_cache = {}
        self.word_cache = {}
        self.last_text = ""
        self.last_font_size = 0

    def wrap_text(self, win, text, pos, size, font, color=pygame.Color('white'), **kwargs):
        if not text:
            return pos[1]

        current_font_size = font.get_height()
        if text != self.last_text or current_font_size != self.last_font_size:
            self.clear_cache()
            self.last_text = text
            self.last_font_size = current_font_size

        fade_out = kwargs.get("fade_out", False)
        alpha = kwargs.get("alpha", 255)
        iconize = frozenset(kwargs.get("iconize", []))
        alarm_links = frozenset(kwargs.get("alarm_links", []))
        replace_text_with_icon = kwargs.get("replace_text_with_icon", False)

        lines = text.split('\n')
        space_width = font.size(' ')[0]
        max_width = size[0]
        x, y = pos
        x += self.config.border
        y += self.config.border

        self.word_height_sum = 0
        self.click_surfaces_list.clear()

        word_height = current_font_size

        for line in lines:
            words = line.split()
            line_surface = self._render_line(font, words, color, alarm_links)
            line_width = line_surface.get_width()

            if x + line_width > max_width:
                self._wrap_line(win, words, font, color, alarm_links, iconize, replace_text_with_icon,
                        x, y, max_width, word_height, space_width, fade_out, alpha)
            else:
                win.blit(line_surface, (x, y))
                self._handle_line_icons(win, words, iconize, word_height, x, y, replace_text_with_icon)
                y += word_height

            x = pos[0] + self.config.border
            self.word_height_sum = max(self.word_height_sum, y + word_height)

        y += word_height
        self.word_height_sum = y - pos[1]

        return y

    def _render_line(self, font, words, color, alarm_links):
        surfaces = []
        for word in words:
            if word not in self.word_cache:
                word_color = self.config.alarm_color if word in alarm_links else color
                self.word_cache[word] = font.render(word, True, word_color)
            surfaces.append(self.word_cache[word])

        total_width = sum(surf.get_width() for surf in surfaces) + (len(surfaces) - 1) * font.size(' ')[0]
        line_surface = pygame.Surface((total_width, font.get_height()), pygame.SRCALPHA)
        x = 0
        for surf in surfaces:
            line_surface.blit(surf, (x, 0))
            x += surf.get_width() + font.size(' ')[0]
        return line_surface

    def _wrap_line(
            self, win, words, font, color, alarm_links, iconize, replace_text_with_icon,
            x, y, max_width, word_height, space_width, fade_out, alpha
            ):
        for word in words:
            word_surface = self.word_cache.get(word) or font.render(word, True,
                    self.config.alarm_color if word in alarm_links else color)
            word_width = word_surface.get_width()

            icon_added, icon_width = self._handle_iconize(win, word, iconize, word_height, x, y, replace_text_with_icon)
            if icon_added:
                if replace_text_with_icon:
                    x += icon_width + space_width
                    continue
                x += icon_width + space_width

            if x + word_width >= max_width:
                x = self.config.border
                y += word_height

            self._render_word(win, word_surface, x, y, fade_out, alpha)

            if word in alarm_links:
                self.click_surfaces_list.append((word, pygame.Rect(x, y, word_width, word_height)))

            x += word_width + space_width

    def _handle_line_icons(self, win, words, iconize, word_height, x, y, replace_text_with_icon):
        for word in words:
            icon_added, icon_width = self._handle_iconize(win, word, iconize, word_height, x, y, replace_text_with_icon)
            if icon_added:
                x += icon_width + win.get_height() // 2  # Approximate space width

    def _handle_iconize(self, win, word, iconize, word_height, x, y, replace_text):
        if not iconize:
            return False, 0

        image_name = word[:-1] if word.endswith(':') else word
        if image_name not in iconize:
            return False, 0

        if image_name in self.resources:
            image_name = f"{image_name}_25x25.png"
        else:
            image_name = f"{image_name}.png"
            if image_name == "\u2713.png":
                image_name = "check.png"

        cache_key = (image_name, word_height)
        if cache_key not in self.image_cache:
            original_img = get_image(image_name)
            scaled_img = scale_image_cached(original_img, (word_height, word_height))
            self.image_cache[cache_key] = scaled_img
        else:
            scaled_img = self.image_cache[cache_key]

        win.blit(scaled_img, (x, y))
        return True, word_height

    def _render_word(self, win, word_surface, x, y, fade_out, alpha):
        if fade_out:
            txt_surf = word_surface.copy()
            alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            win.blit(txt_surf, (x, y))
        else:
            win.blit(word_surface, (x, y))

    def clear_cache(self):
        self.image_cache.clear()
        self.word_cache.clear()


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

                            if image_name == "\u2713.png":
                                image_name = "check.png"
                                word = ""
                                word_surface = None

                        img = scale_image_cached(get_image(image_name), (word_height, word_height))
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
                    if word_surface:
                        win.blit(word_surface, (x, y))
                if word_surface:
                    word_surface.get_rect().x = x
                    word_surface.get_rect().y = y

                if self.link_found:
                    self.set_click_surfaces(word, word_height, word_width, x, y)

                x += word_width + space

            x = pos[0] + self.border  # Reset the x.
            y += word_height  # Start on new row.

            # get the last height value
            self.word_height_sum = y

    def set_click_surfaces(self, word, word_height, word_width, x, y):
        if word:
            self.click_surfaces_list.append((word, pygame.Rect(x, y, word_width, word_height)))
# def test_performance():
#     pygame.init()
#     win = pygame.display.set_mode((800, 600))
#     font = pygame.font.SysFont(None, 24)
#
#     text = "This is a long text that should wrap properly.\nIt contains multiple sentences\nand even an attack word. water: energy: food:"
#     pos = (50, 50)
#     size = (700, 500)
#     color = pygame.Color('white')
#     kwargs = {
#         "fade_out": False,
#         "alpha": 255,
#         "iconize": ["water", "energy", "food"],
#         "alarm_links": ["attack"],
#         "replace_text_with_icon": False
#     }
#
#     iterations = 1000
#
#     # Test original TextWrap
#     text_wrap = TextWrap()
#     start_time = time.time()
#     for _ in range(iterations):
#         text_wrap.wrap_text(win, text, pos, size, font, color, **kwargs)
#     original_time = time.time() - start_time
#
#     # Test refactored original implementation
#     text_wrap_refactored = TextWrapRefactored()
#     start_time = time.time()
#     for _ in range(iterations):
#         text_wrap_refactored.wrap_text(win, text, pos, size, font, color, **kwargs)
#     refactored_time = time.time() - start_time
#
#     # Test optimized implementation
#     text_wrap_optimized = TextWrapOptimized()
#     start_time = time.time()
#     for _ in range(iterations):
#         text_wrap_optimized.wrap_text(win, text, pos, size, font, color, **kwargs)
#     optimized_time = time.time() - start_time
#
#     print(f"Original TextWrap: {original_time:.4f} seconds")
#     print(f"Refactored Original: {refactored_time:.4f} seconds")
#     print(f"Optimized implementation: {optimized_time:.4f} seconds")
#     print(f"Speed improvement (Optimized vs Original): {(original_time - optimized_time) / original_time * 100:.2f}%")
#     print(f"Speed improvement (Optimized vs Refactored): {(refactored_time - optimized_time) / refactored_time * 100:.2f}%")
#
#     fastest_time = min(original_time, refactored_time, optimized_time)
#     if fastest_time == original_time:
#         print("The original TextWrap is the fastest.")
#     elif fastest_time == refactored_time:
#         print("The refactored original implementation is the fastest.")
#     else:
#         print("The optimized version is the fastest.")
#
#     pygame.quit()
#
# if __name__ == '__main__':
#     test_performance()
# def test_performance():
#     pygame.init()
#     win = pygame.display.set_mode((800, 600))
#     font = pygame.font.SysFont(None, 24)
#
#     text = "This is a long text that should wrap properly.\nIt contains multiple sentences\nand even an attack word. water: energy: food:"
#     pos = (50, 50)
#     size = (700, 500)
#     color = pygame.Color('white')
#     kwargs = {
#         "fade_out": False,
#         "alpha": 255,
#         "iconize": ["water", "energy", "food"],
#         "alarm_links": ["attack"],
#         "replace_text_with_icon": False
#     }
#
#     iterations = 1000
#
#     # Test original TextWrap
#     text_wrap = TextWrap()
#     start_time = time.time()
#     for _ in range(iterations):
#         text_wrap.wrap_text(win, text, pos, size, font, color, **kwargs)
#     original_time = time.time() - start_time
#
#     # Test refactored original implementation
#     text_wrap_refactored = TextWrapRefactored()
#     start_time = time.time()
#     for _ in range(iterations):
#         text_wrap_refactored.wrap_text(win, text, pos, size, font, color, **kwargs)
#     refactored_time = time.time() - start_time
#
#     # Test first optimized implementation
#     text_wrap_optimized = TextWrapOptimized()
#     start_time = time.time()
#     for _ in range(iterations):
#         text_wrap_optimized.wrap_text(win, text, pos, size, font, color, **kwargs)
#     optimized_time = time.time() - start_time
#
#     # Test new optimized implementation with caching
#     text_wrap_optimized_ii = TextWrapOptimizedII()
#     start_time = time.time()
#     for _ in range(iterations):
#         text_wrap_optimized_ii.wrap_text(win, text, pos, size, font, color, **kwargs)
#     optimized_ii_time = time.time() - start_time
#
#     print(f"Original TextWrap: {original_time:.4f} seconds")
#     print(f"Refactored Original: {refactored_time:.4f} seconds")
#     print(f"First Optimized implementation: {optimized_time:.4f} seconds")
#     print(f"New Optimized implementation (with caching): {optimized_ii_time:.4f} seconds")
#     print(f"Speed improvement (OptimizedII vs Original): {(original_time - optimized_ii_time) / original_time * 100:.2f}%")
#     print(f"Speed improvement (OptimizedII vs Refactored): {(refactored_time - optimized_ii_time) / refactored_time * 100:.2f}%")
#     print(f"Speed improvement (OptimizedII vs First Optimized): {(optimized_time - optimized_ii_time) / optimized_time * 100:.2f}%")
#
#     fastest_time = min(original_time, refactored_time, optimized_time, optimized_ii_time)
#     if fastest_time == original_time:
#         print("The original TextWrap is the fastest.")
#     elif fastest_time == refactored_time:
#         print("The refactored original implementation is the fastest.")
#     elif fastest_time == optimized_time:
#         print("The first optimized version is the fastest.")
#     else:
#         print("The new optimized version with caching is the fastest.")
#
#
#
#     pygame.quit()
#
# if __name__ == '__main__':
#     test_performance()


def test_performance():
    pygame.init()
    win = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 24)

    text = "This is a long text that should wrap properly.\nIt contains multiple sentences\nand even an attack word. water: energy: food:"
    pos = (50, 50)
    size = (700, 500)
    color = pygame.Color('white')
    kwargs = {
        "fade_out": False,
        "alpha": 255,
        "iconize": ["water", "energy", "food"],
        "alarm_links": ["attack"],
        "replace_text_with_icon": False
    }

    iterations = 1000

    # Test original TextWrap
    text_wrap = TextWrap()
    start_time = time.time()
    for _ in range(iterations):
        text_wrap.wrap_text(win, text, pos, size, font, color, **kwargs)
    original_time = time.time() - start_time

    # Test refactored original implementation
    text_wrap_refactored = TextWrapRefactored()
    start_time = time.time()
    for _ in range(iterations):
        text_wrap_refactored.wrap_text(win, text, pos, size, font, color, **kwargs)
    refactored_time = time.time() - start_time

    # Test first optimized implementation
    text_wrap_optimized = TextWrapOptimized()
    start_time = time.time()
    for _ in range(iterations):
        text_wrap_optimized.wrap_text(win, text, pos, size, font, color, **kwargs)
    optimized_time = time.time() - start_time

    # Test optimized implementation with caching
    text_wrap_optimized_ii = TextWrapOptimizedII()
    start_time = time.time()
    for _ in range(iterations):
        text_wrap_optimized_ii.wrap_text(win, text, pos, size, font, color, **kwargs)
    optimized_ii_time = time.time() - start_time

    # Test new optimized implementation III
    text_wrap_optimized_iii = TextWrapOptimizedIII(TextWrapConfig())
    start_time = time.time()
    for _ in range(iterations):
        text_wrap_optimized_iii.wrap_text(win, text, pos, size, font, color, **kwargs)
    optimized_iii_time = time.time() - start_time

    print(f"Original TextWrap: {original_time:.4f} seconds")
    print(f"Refactored Original: {refactored_time:.4f} seconds")
    print(f"First Optimized implementation: {optimized_time:.4f} seconds")
    print(f"Optimized implementation with caching: {optimized_ii_time:.4f} seconds")
    print(f"New Optimized implementation III: {optimized_iii_time:.4f} seconds")
    print(f"Speed improvement (OptimizedIII vs Original): {(original_time - optimized_iii_time) / original_time * 100:.2f}%")
    print(f"Speed improvement (OptimizedIII vs Refactored): {(refactored_time - optimized_iii_time) / refactored_time * 100:.2f}%")
    print(f"Speed improvement (OptimizedIII vs First Optimized): {(optimized_time - optimized_iii_time) / optimized_time * 100:.2f}%")
    print(f"Speed improvement (OptimizedIII vs OptimizedII): {(optimized_ii_time - optimized_iii_time) / optimized_ii_time * 100:.2f}%")

    fastest_time = min(original_time, refactored_time, optimized_time, optimized_ii_time, optimized_iii_time)
    if fastest_time == original_time:
        print("The original TextWrap is the fastest.")
    elif fastest_time == refactored_time:
        print("The refactored original implementation is the fastest.")
    elif fastest_time == optimized_time:
        print("The first optimized version is the fastest.")
    elif fastest_time == optimized_ii_time:
        print("The optimized version with caching is the fastest.")
    else:
        print("The new optimized version III is the fastest.")

    pygame.quit()

if __name__ == '__main__':
    test_performance()

