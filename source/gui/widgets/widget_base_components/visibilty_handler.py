from source.handlers.widget_handler import WidgetHandler


class VisibilityHandler:
    def __init__(self, is_sub_widget=False, **kwargs):
        self._is_sub_widget = is_sub_widget
        self._hidden = False
        self._disabled = False
        self.layer = kwargs.get("layer", 9)
        self.widgets = []
        if is_sub_widget:
            self.hide()

    def set_visible(self):
        if self._hidden:
            self.show()
        else:
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

    def is_sub_widget(self):
        return self._is_sub_widget

    def set_is_sub_widget(self, is_sub_widget):
        self._is_sub_widget = is_sub_widget
        if is_sub_widget:
            WidgetHandler.remove_widget(self)
        else:
            WidgetHandler.add_widget(self)

    def is_visible(self):
        return not self._hidden

    def set_children_visible(self, value):
        for i in self.children:
            if i._hidden:
                i.show()
            else:
                i.hide()
