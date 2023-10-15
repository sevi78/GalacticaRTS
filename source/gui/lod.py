from source.utils import global_params

BORDER = 10
DEBUG_BORDER = 200


def level_of_detail(obj):
    win = global_params.win
    is_disabled = obj._disabled
    is_hidden = obj._hidden

    if not 0 + BORDER <= obj.get_screen_x() <= win.get_width() - BORDER and 0 + BORDER <= obj.get_screen_y() <= win.get_height() - BORDER:
        obj.disable()
        obj.hide()
    else:
        if not is_disabled:
            obj.enable()
        if not is_hidden:
            obj.show()


def inside_screen__(x, y, **kwargs):
    BORDER_ = kwargs.get("border", BORDER)

    if global_params.debug:
        BORDER_ = DEBUG_BORDER

    win = global_params.win
    # if 0 + test <= x <= global_params.win.get_width() - test and 0 + test <= y <= global_params.win.get_height() - test:
    if 0 + BORDER_ <= x <= win.get_width() - BORDER_ and 0 + BORDER_ <= y <= win.get_height() - BORDER_:
        return True
    else:
        return False


def inside_screen__(pos, **kwargs):
    BORDER_ = kwargs.get("border", BORDER)

    if global_params.debug:
        BORDER_ = DEBUG_BORDER

    win = global_params.win
    # if 0 + test <= x <= global_params.win.get_width() - test and 0 + test <= y <= global_params.win.get_height() - test:
    if 0 + BORDER_ <= pos[0] <= win.get_width() - BORDER_ and 0 + BORDER_ <= pos[1] <= win.get_height() - BORDER_:
        return True
    else:
        return False

def inside_screen(pos, **kwargs):
    BORDER_ = kwargs.get("border", BORDER)

    if global_params.debug:
        BORDER_ = DEBUG_BORDER

    win = global_params.win
    # if 0 + test <= x <= global_params.win.get_width() - test and 0 + test <= y <= global_params.win.get_height() - test:
    # if BORDER_ <= pos[0] <= win.get_width() - BORDER_ and BORDER_ <= pos[1] <= win.get_height() - BORDER_:
    #     return True
    # else:
    #     return False
    return BORDER_ <= pos[0] <= win.get_width() - BORDER_ and BORDER_ <= pos[1] <= win.get_height() - BORDER_
