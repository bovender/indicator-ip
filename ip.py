#!/usr/bin/python
import os
import subprocess
import appindicator
import gtk
import re
import dbus
from dbus.mainloop.glib import DBusGMainLoop

"""Semantic version."""
VERSION = '0.9.0'

class IPIndicator:
    def __init__(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.get_ip_method = 'get_external_ip'
        self.ip = ""
        self.ind = appindicator.Indicator(
            "ip-indicator",
            os.path.join(self.dir, 'images/icon.png'),
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.connect_dbus()
        self.update()
        self.ind.set_menu(self.setup_menu())

    def connect_dbus(self):
        DBusGMainLoop(set_as_default=True)
        system_bus = dbus.SystemBus()
        system_bus.add_signal_receiver(self.on_dbus_state_changed, 
                'StateChanged',
                'org.freedesktop.NetworkManager.Device');
    
    def setup_menu(self):
        menu = gtk.Menu()

        refresh = gtk.MenuItem("Refresh")
        refresh.connect("activate", self.on_refresh)
        refresh.show()
        menu.append(refresh)

        sep = gtk.SeparatorMenuItem()
        sep.show()
        menu.append(sep)

        e = gtk.RadioMenuItem(None, "External")
        e.connect("activate", self.on_use_external)
        e.set_active(True)
        e.show()
        menu.append(e)

        i = gtk.RadioMenuItem(e, "Internal")
        i.connect("activate", self.on_use_internal)
        i.show()
        menu.append(i)

        sep = gtk.SeparatorMenuItem()
        sep.show()
        menu.append(sep)

        a = gtk.MenuItem("About")
        a.connect("activate", self.on_about)
        a.show()
        menu.append(a)

        q = gtk.MenuItem("Quit")
        q.connect("activate", self.on_quit)
        q.show()
        menu.append(q)

        return menu

    def update(self):
        """
        
        Update the IP address.
        
        """
        ip = getattr(self, self.get_ip_method)()
        if ip != self.ip:
            self.ip = ip
            self.ind.set_label(ip)

    def on_use_internal(self, widget):
        self.get_ip_method = 'get_internal_ip'
        self.update()

    def on_use_external(self, widget):
        self.get_ip_method = 'get_external_ip'
        self.update()

    def on_refresh(self, widget):
        self.update()

    def on_about(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name('unity-ip-indicator')
        about.set_version('Version ' + VERSION)
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

    def on_quit(self, widget):
        quit()

    def on_dbus_state_changed(self, *args, **kwargs):
        self.update()

    def sanitize_ip(self, ip):
        """Ensure a properly formatted IP string is returned."""
        if not ip:
            return '(IP n/a)'
        if re.match('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', ip):
            return ip.strip()
        else:
            return '?.?.?.?'

    def get_internal_ip(self):
        try:
            ip = subprocess.check_output('ifconfig |\
                grep -o -P "inet addr:([^ ]*)" |\
                grep -o -m 1 -P "[0-9.]+"', shell=True)
        except:
            ip = ''
        return self.sanitize_ip(ip)

    def get_external_ip(self):
        # Get internet IP from icanhazip.com or checkip.amazonaws.com
        try:
            ip = subprocess.check_output(
                    ['curl', '-s', 'checkip.amazonaws.com'], 
                    shell=False)
        except:
            ip = ''
        return self.sanitize_ip(ip)

if __name__ == "__main__":
    i = IPIndicator()
    gtk.main()

