class PanZoomVisibilityHandler:
    def __init__(self, **kwargs):
        self.children = None
        self._hidden = False
        self._disabled = False
        self.widgets = []

    def hide(self):
        """hides self and its widgets
        """
        self._hidden = True
        for i in self.widgets:
            i.hide()

    def show(self):
        """shows self and its widgets
        """
        self._hidden = False
        for i in self.widgets:
            i.show()

    def disable(self):
        self._disabled = True

    def enable(self):
        self._disabled = False

    def isVisible(self):
        return not self._hidden

    def set_children_visible(self, value):
        for i in self.children:
            if i._hidden:
                i.show()
            else:
                i.hide()
