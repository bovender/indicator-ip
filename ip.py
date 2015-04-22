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

def sanitize_ip(ip):
    """Ensure a properly formatted IP string is returned."""
    if not ip:
        return '(IP n/a)'
    if re.match('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', ip):
        return ip.strip()
    else:
        return '?.?.?.?'

def get_ip():
#   ip = subprocess.check_output('ifconfig |\
#       grep -o -P "inet addr:([^ ]*)" |\
#       grep -o -m 1 -P "[0-9.]+"', shell=True)
    # Get internet IP from icanhazip.com or checkip.amazonaws.com
    try:
        ip = subprocess.check_output(
                ['curl', '-s', 'checkip.amazonaws.com'], 
                shell=False)
    except:
        ip = ''
    return sanitize_ip(ip)

class IPIndicator:
    def __init__(self):
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

        i = gtk.MenuItem("Quit")
        i.connect("activate", self.on_quit)
        i.show()
        menu.append(i)

        return menu

    def update(self):
        """
        
        Update the IP address.
        
        """
        ip = get_ip()
        if ip != self.ip:
            self.ip = ip
            self.ind.set_label(ip)

    def on_refresh(self, widget):
        self.update()

    def on_quit(self, widget):
        quit()

if __name__ == "__main__":
    i = IPIndicator()
    gtk.main()

