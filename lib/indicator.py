import os
import appindicator
import gtk
import dbus
import logging
import version
import interfaces
from dbus.mainloop.glib import DBusGMainLoop
from settings import Settings
from ip import ExternalIp, InternalIp
from helpers import script_path

class IPIndicator:
    __log = logging.getLogger(__name__)

    def __init__(self):
        self.__log.debug('Initializing %s', self.__class__)
        dummy_icon = os.path.join(script_path(), 'images/icon.png')
        self.__log.debug('Loading dummy icon from %s', dummy_icon)
        self.ind = appindicator.Indicator(
            "ip-indicator",
            dummy_icon,
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)

        # Create a settings object and add the external IP 
        # as well as IPs for the network interfaces
        self.settings = Settings()
        ifs = interfaces.Interfaces()
        for interface in ifs.interfaces:
            self.settings.add_ip(InternalIp(interface))
        self.settings.add_ip(ExternalIp())
        self.settings.load()

        self.ind.set_menu(self._setup_menu())
        self._connect_dbus()

        for ip in self.settings.ips.itervalues():
            ip.activated = self._switch_ip
        self.update()

    def _connect_dbus(self):
        self.__log.debug('Connecting to DBus')
        DBusGMainLoop(set_as_default=True)
        system_bus = dbus.SystemBus()
        system_bus.add_signal_receiver(self._on_dbus_state_changed, 
                'StateChanged',
                'org.freedesktop.NetworkManager.Device');
    
    def _setup_menu(self):
        self.__log.debug('Setting up menu')
        menu = gtk.Menu()

        refresh = gtk.MenuItem("Refresh")
        refresh.connect("activate", self._on_refresh)
        refresh.show()
        menu.append(refresh)

        sep = gtk.SeparatorMenuItem()
        sep.show()
        menu.append(sep)

        group_item = self.settings.ips.itervalues().next() \
                .get_menu().get_group()[0]
        for ip in self.settings.ips.itervalues():
            menu_item = ip.get_menu()
            if group_item != menu_item:
                menu_item.set_group(group_item)
            menu.append(menu_item)

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

        return menu

    """
    Updates the label in the indicator bar.
    """
    def update(self):
        name = self.settings.current_ip.get_name()
        ip_address = self.settings.current_ip.ip
        self.__log.debug('Updating indicator for "%s" with IP "%s"',
                name, ip_address)
        self.ind.set_label(ip_address)

    def _switch_ip(self, ip):
        self.__log.info('Switching IP to %s', ip.get_name())
        self.settings.current_ip = ip
        self.settings.save()
        self.update()

    def _on_dbus_state_changed(self, *args, **kwargs):
        self.__log.info('DBus state changed')
        self.update()

    def _on_refresh(self, widget):
        self.__log.info('Refreshing all IPs')
        for ip in self.settings.ips.itervalues():
            ip.update()
        self.update()

    def _on_quit(self, widget):
        self.__log.info('User clicked Quit')
        gtk.main_quit()

    def _on_about(self, widget):
        self.__log.debug('Showing about about box')
        about = gtk.AboutDialog()
        about.set_program_name('indicator-ip')
        about.set_version('Version ' + version.VERSION)
        about.set_website('https://github.com/bovender/unity-ip-indicator')
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

