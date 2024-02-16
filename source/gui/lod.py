import time

from source.configuration import global_params

BORDER = 10
DEBUG_BORDER = 200


def inside_screen(pos: tuple, **kwargs):
    BORDER_ = kwargs.get("border", BORDER)
    win = kwargs.get("win", global_params.win)

    if global_params.debug:
        BORDER_ = DEBUG_BORDER

    return BORDER_ <= pos[0] <= win.get_width() - BORDER_ and BORDER_ <= pos[1] <= win.get_height() - BORDER_


class LevelOfDetail:
    def __init__(self) -> None:
        self.win = global_params.win
        self.width = self.win.get_width()
        self.height = self.win.get_height()
        self.border = BORDER
        self.left_limit = 0
        self.right_limit = self.width
        self.top_limit = 0
        self.bottom_limit = self.height

    def set_limits(self) -> None:
        self.left_limit = self.border
        self.right_limit = self.width - self.border
        self.top_limit = self.border
        self.bottom_limit = self.height - self.border

    def set_border(self, border: int) -> None:
        self.border = border
        self.set_limits()

    def set_width(self, width: int) -> None:
        self.width = width
        self.set_limits()

    def set_height(self, height: int) -> None:
        self.height = height
        self.set_limits()

    def set_screen_size(self, screen_size: tuple):
        self.set_width(screen_size[0])
        self.set_height(screen_size[1])

    def inside_screen(self, pos: tuple) -> bool:
        if pos[0] < self.left_limit:
            return False
        elif pos[0] > self.right_limit:
            return False
        elif pos[1] < self.top_limit:
            return False
        elif pos[1] > self.bottom_limit:
            return False
        else:
            return True


level_of_detail = LevelOfDetail()

if __name__ == '__main__':
    level_of_detail = LevelOfDetail()
    level_of_detail.set_screen_size((1000, 1000))

    old_start = time.time()
    loops = 10000000
    for _ in range(loops):
        inside_screen_old((_, _))
    old_end = time.time()
    print(f'old took {old_end - old_start} seconds for {loops}')

    new_start = time.time()
    for _ in range(loops):
        level_of_detail.inside_screen((_, _))
    new_end = time.time()
    print(f'new took {new_end - new_start} seconds for {loops}')
