import gtk
import subprocess
import re
import logging

IP_REGEX = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'

"""
Abstract base class that represents an IP type (e.g. external
vs. internal; might implement ability to handle different interfaces
in the future.
"""
class Ip:
    _log = logging.getLogger(__name__)

    def __init__(self):
        self._log.debug('Initializing %s', self.__class__)
        # self.activated is a simple event handler for a callback function that
        # is executed whenever this IP type is activated.  The callback
        # function must take one argument, which is the instance of Ip calling
        # the function.
        self.activated = None
        self.update()

    """
    Returns the type name of this IP, e.g. 'internal' or 'external'.
    """
    def get_name(self):
        raise NotImplementedError('This method must be overriden.')

    """
    Returns an instance of RadioMenuItem for this IP.
    """
    def get_menu(self):
        try:
            return self.__menu
        except:
            self._log.debug('Creating new menu item for %s',
                    self.get_name())
            self.__menu = gtk.RadioMenuItem(None, self._get_menu_label())
            self.__menu.connect("activate", self._on_activate)
            self.__menu.show()
            return self.__menu

    def activate(self):
        self.__menu.set_active(True)

    """
    Updates the IP and menu label.
    """
    def update(self):
        self._update_ip()
        self.get_menu().set_label(self._get_menu_label())

    """
    Calls the callback function that the self.activated event handler points
    to.
    """
    def _on_activate(self, menuitem):
        if self.activated:
            self.activated(self)

    """
    Updates the current IP. Internal use.
    """
    def _update_ip(self):
        self._log.debug('Fetching IP for %s', self.get_name())
        self.ip = self._fetch_ip()
        if self.ip and re.match(IP_REGEX, self.ip):
            self.ip = self.ip.strip()
        else:
            self.ip = '?.?.?.?'

    """
    Returns the current IP.
    """
    def _fetch_ip(self):
        raise NotImplementedError('This method must be overriden.')

    """
    Builds the label for the menu item using the current IP.
    """
    def _get_menu_label(self):
        return self.get_name() + ' (' + self.ip + ')'

"""
Represents the 'external' IP outside of the current subnet.
"""
class ExternalIp(Ip):
    def get_name(self):
        return 'External'

    def _fetch_ip(self):
        # provider = 'icanhazip.com'
        provider = 'checkip.amazonaws.com'
        self._log.debug('Fetching new external IP from %s', provider)
        return subprocess.check_output(
                ['curl', '-s', provider],
                shell=False)

"""
Represents the IP that the default network interface is bound to.
"""
class InternalIp(Ip):
    def get_name(self):
        return 'Internal'

    def _fetch_ip(self):
        self._log.debug('Fetching new internal IP')
        return subprocess.check_output('ifconfig |\
            grep -o -P "inet addr:([^ ]*)" |\
            grep -o -m 1 -P "[0-9.]+"', shell=True)
