import gtk
import subprocess
import re
import logging

PUBLIC = 'public'
NO_IP = '---.---.---.---'
IP_REGEX = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'

"""
Abstract base class that represents a network interface.
"""
class Interface():
    _log = logging.getLogger(__name__)

    def __init__(self):
        self._log.debug('Initializing %s', self.__class__)
        self.name = None
        self.update()

    def activate(self):
        self.__menu.set_active(True)

    """
    Updates the current IP.
    """
    def update(self):
        self._log.debug('Fetching IP for %s', self.name)
        try:
            self.ip = self._fetch_ip()
        except:
            self.ip = None
        if self.ip and re.match(IP_REGEX, self.ip):
            self.ip = self.ip.strip()
        else:
            self.ip = NO_IP

    """
    Fetches the current IP for this interface.
    """
    def _fetch_ip(self):
        raise NotImplementedError('This method must be overriden.')

"""
A dummy 'interface' that fetches the public IP that identifies this computer
on the internet.
"""
class Public(Interface):
    """
    Initializes the object. An optional URL for an IP provider can be given;
    this provider must return nothing else but the IP in text form.
    """
    def __init__(self, provider):
        self._log.debug('Initializing %s', self.__class__)
        self.name = PUBLIC
        self.provider = provider
        self.update()

    def _fetch_ip(self):
        self._log.debug('Fetching new external IP from %s', self.provider)
        # Use shell=False also for security!
        return subprocess.check_output(
                ['curl', '--max-filesize 15', '-s', self.provider],
                shell=False)

"""
Represents an internal interface.
"""
class Internal(Interface):
    def __init__(self, interface_name):
        self._log.debug('Initializing %s', self.__class__)
        self.name = interface_name
        self.update()

    def _fetch_ip(self):
        self._log.debug('Fetching IP for interface ' + self.name)
        # TODO: Sanitize self.name before writing it to the shell.
        return subprocess.check_output(
            'ip -4 --oneline addr show "' + self.name + '" |\
            grep -o -P "(?<=inet )([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"',
            shell=True)
