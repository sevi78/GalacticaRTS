from dataclasses import dataclass, field
from typing import List, Tuple

import pygame

from source.multimedia_library.images import get_image, scale_image_cached

TEXTBORDER = 10
FADE_OUT_TIME = 0


@dataclass
class TextWrapConfig:
    color: pygame.Color = field(default_factory=lambda: pygame.Color('white'))
    link_color: pygame.Color = field(default_factory=lambda: pygame.Color('blue'))
    alarm_color: pygame.Color = field(default_factory=lambda: pygame.Color('red'))
    border: int = TEXTBORDER


class TextWrap:  # Optimized, best working so far
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

    def _handle_iconize(
            self, win: pygame.Surface, word: str, iconize: frozenset, word_height: int, x: int, y: int,
            replace_text: bool
            ) -> Tuple[bool, int]:

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


class TextWrap___:  # OptimizedIII, not working outside test ??
    __slots__ = (
        'config', 'click_surfaces_list', 'word_height_sum', 'resources', 'image_cache', 'word_cache', 'last_text',
        'last_font_size')

    def __init__(self):
        self.config = TextWrapConfig()
        self.click_surfaces_list = []
        self.word_height_sum = 0
        self.resources = ["water", "energy", "food", "minerals", "technology", "population"]
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
        iconize = kwargs.get("iconize", [])
        alarm_links = kwargs.get("alarm_links", [])
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
                size=(300, 30),
                font=pygame.font.SysFont(None, 12),
                color=pygame.color.THECOLORS.get("orange"),
                fade_out=False,
                alpha=255,
                iconize=[],
                alarm_links=["attack"]
                )

        pygame.display.update()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


if __name__ == '__main__':
    main()
