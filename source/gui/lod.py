from source.configuration import global_params

BORDER = 10
DEBUG_BORDER = 200


def inside_screen(pos, **kwargs):
    BORDER_ = kwargs.get("border", BORDER)

    if global_params.debug:
        BORDER_ = DEBUG_BORDER

    win = global_params.win

    return BORDER_ <= pos[0] <= win.get_width() - BORDER_ and BORDER_ <= pos[1] <= win.get_height() - BORDER_
