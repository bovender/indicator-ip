import gtk

"""
A menu item view model for an interface.
"""
class MenuItem:
    """
    Returns a RadioMenuItem for the bound Interface.
    """
    def get_item(self):
        try:
            return self.__item
        except:
            self.__item = gtk.RadioMenuItem(None, self._get_menu_label())
            self.__item.connect("activate", self._on_select)
            self.__item.show()
            return self.__item

    """
    Selects the current item.
    """
    def select(self):
        self.get_item().set_active(True)
        #self._on_select(None)

    """
    Initializes an object with a given Interface object.
    """
    def __init__(self, interface):
        self.interface = interface

        """A simple event handler to signal if the RadioMenuItem
        was selected."""
        self.selected = None

    """
    Creates a label for the menu item containing the interface name and
    the IP of the interface.
    """
    def _get_menu_label(self):
        return "{0}: {1}".format(self.interface.name, self.interface.ip)

    """
    Calls the callback function that the self.activated event handler points
    to. The called function receives two arguments: The MenuItem itself and
    the Interface object that it holds.
    """
    def _on_select(self, menu_item):
        if self.selected:
            self.selected(self, self.interface)
