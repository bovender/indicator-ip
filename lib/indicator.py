import os
import appindicator
import gtk
import dbus
import time
import logging
import version
import interface
from interfaces import Interfaces
from menu_item import MenuItem
from dbus.mainloop.glib import DBusGMainLoop
from settings import Settings
from helpers import script_path

class IPIndicator:
    """
    Updates the label in the indicator bar. Does not refetch current IPs!
    """
    def update(self):
        self.__log.info('Updating indicator label')
        self.ind.set_label(self.selected_interface.ip)

    """
    Fetches the current interfaces and their IPs.
    """
    def refresh(self):
        self.__log.info('Refreshing')
        try:
            previous = self.selected_interface.name
        except AttributeError:
            previous = None

        # Rebuild the dictionary of interfaces and the menu
        self.interfaces = Interfaces(self.settings.url)
        self._create_menu()

        # Select previously selected interface again
        if self.interfaces.has_interface(previous):
            self.__log.debug('Using previously selected interface %s', previous)
            self._menu_items[previous].select()
        else:
            self.__log.debug(
                    'Previously selected interface %s no longer exists, using public',
                    previous)
            self._menu_items[interface.PUBLIC].select()

        self.update()

    __log = logging.getLogger(__name__)

    def __init__(self, settings):
        self.__log.debug('Initializing %s', self.__class__)
        dummy_icon = os.path.join(script_path(), 'images/icon.png')
        self.__log.debug('Loading dummy icon from %s', dummy_icon)
        self.ind = appindicator.Indicator(
            "ip-indicator",
            dummy_icon,
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)

        self.settings = settings
        self.__log.debug('Settings: %s', vars(settings))
        self.selected_interface = None
        self.refresh()
        if self.interfaces.has_interface(self.settings.interface):
            self.__log.debug('Using interface %s from settings',
                    self.settings.interface)
            self._menu_items[self.settings.interface].select()
        else:
            self.__log.debug('Cannot use interface %s from settings',
                    self.settings.interface)
        self._connect_dbus()

    def _connect_dbus(self):
        self.__log.info('Connecting to DBus')
        DBusGMainLoop(set_as_default=True)
        system_bus = dbus.SystemBus()
        system_bus.add_signal_receiver(self._on_dbus_state_changed, 
                'PropertiesChanged',
                'org.freedesktop.NetworkManager.Connection.Active')
    
    def _create_menu(self):
        self.__log.info('Building menu')
        menu = gtk.Menu()

        refresh = gtk.MenuItem("Refresh")
        refresh.connect("activate", self._on_manual_refresh)
        refresh.show()
        menu.append(refresh)

        sep = gtk.SeparatorMenuItem()
        sep.show()
        menu.append(sep)

        # Build the list of interfaces
        group = None
        self._menu_items = {}
        for interface in self.interfaces.interfaces.itervalues():
            item = MenuItem(interface)
            item.selected = self._select_interface
            if not group:
                group = item.get_item().get_group()[0]
            else:
                item.get_item().set_group(group)
            menu.append(item.get_item())
            self._menu_items[interface.name] = item
        self.__log.debug('Menu items: %s', self._menu_items)

        sep = gtk.SeparatorMenuItem()
        sep.show()
        menu.append(sep)

        a = gtk.MenuItem("About")
        a.connect("activate", self._on_about)
        a.show()
        menu.append(a)

        q = gtk.MenuItem("Quit")
        q.connect("activate", self._on_quit)
        q.show()
        menu.append(q)

        self.ind.set_menu(menu)

    def _select_interface(self, menu_item, interface):
        self.__log.info('Selecting interface: %s', interface.name)
        self.selected_interface = interface
        self.update()

    def _on_dbus_state_changed(self, *args, **kwargs):
        self.__log.info('DBus state changed')
        time.sleep(0.3)
        self.refresh()

    def _on_manual_refresh(self, widget):
        self.__log.info('User triggered manual refresh')
        self.refresh()

    def _on_quit(self, widget):
        self.__log.info('=== User clicked Quit ===')
        self.settings.interface = self.selected_interface.name
        self.settings.save()
        gtk.main_quit()

    def _on_about(self, widget):
        self.__log.debug('Showing about about box')
        about = gtk.AboutDialog()
        about.set_program_name('indicator-ip')
        about.set_version('Version ' + version.VERSION)
        about.set_website('https://github.com/bovender/indicator-ip')
        about.set_authors([
                'DJG (https://github.com/sentientwaffle)',
                'Daniel Kraus (https://github.com/bovender)'])
        about.set_copyright('(c) 2012 DJG, 2015 Daniel Kraus')
        about.set_comments('Show the current IP address as indicator.')
        about.set_license("""
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject
to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.""")
        response = about.run()
        about.hide()
