from source.handlers.widget_handler import WidgetHandler


class VisibilityHandler:
    def __init__(self, isSubWidget=False, **kwargs):
        self._isSubWidget = isSubWidget
        self._hidden = False
        self._disabled = False
        self.layer = kwargs.get("layer", None)
        self.layers = kwargs.get("layers", None)
        self.widgets = []
        if isSubWidget:
            self.hide()

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

    def isSubWidget(self):
        return self._isSubWidget

    def setIsSubWidget(self, isSubWidget):
        self._isSubWidget = isSubWidget
        if isSubWidget:
            WidgetHandler.removeWidget(self)
        else:
            WidgetHandler.addWidget(self)

    def isVisible(self):
        return not self._hidden

    def set_children_visible(self, value):
        for i in self.children:
            if i._hidden:
                i.show()
            else:
                i.hide()
