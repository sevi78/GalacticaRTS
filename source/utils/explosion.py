from source.multimedia_library.gif_handler import GifHandler


class Explosion:
    def __init__(self, parent, app, gif, **kwargs):
        self.gif_handler = GifHandler(parent, gif, **kwargs)
        self.parent = parent

    def draw(self):
        self.gif_handler.draw()
        if self.gif_handler.index >= len(self.gif_handler.frames):
            self.parent.exploded = True


def explode(self):
    self.target = None
    if hasattr(self, "progressbar"):
        self.progress_bar.hide()

    self.explosion.draw()
