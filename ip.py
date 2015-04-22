#!/usr/bin/python
import os
import subprocess
import appindicator
import gtk
import re

ICON = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "images/icon.png"
        )

class IPIndicator:
    def __init__(self):
        self.get_ip_method = 'get_external_ip'
        self.ip = ""
        self.ind = appindicator.Indicator("ip-indicator", ICON,
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.update()
        self.ind.set_menu(self.setup_menu())
    
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

    def on_quit(self, widget):
        quit()

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

