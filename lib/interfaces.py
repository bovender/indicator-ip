import subprocess
import interface 
import logging

"""
Enumerates the network interfaces on the system by calling
the external 'ip' command, and provides a list of IP objects.
"""
class Interfaces:
    __log = logging.getLogger(__name__)

    def __init__(self, fetch_ip_url):
        """Holds a multi-line string of all interfaces with IPv4 addresses."""
        self.all_interfaces = None
        self.__fetch_ip_url = fetch_ip_url
        self.build_list()

    """
    Obtains a list of network interfaces by invoking the system's
    'ip' command, and creates Ip objects for each of them (except
    'lo').
    """
    def build_list(self):
        self.__log.info('Building interface list')
        self.all_interfaces = subprocess.check_output(
            'ip -4 --oneline addr show | awk \'{ print $2 }\'',
            shell=True)
        self.__log.debug('Using %s', self.all_interfaces.replace('\n', ' '))
        if_names = self.all_interfaces.splitlines()
        try:
            if_names.remove('lo')
        except:
            pass
        # Put the default 'external' interface into the list.
        self.interfaces = { 
                interface.PUBLIC: interface.Public(self.__fetch_ip_url)
                }
        for name in if_names:
            i = interface.Internal(name)
            self.interfaces[name] = i
        self.__log.debug('Interfaces: %s', self.interfaces)

    """
    Returns True if the list of interfaces contains 'name', False it not.
    """
    def has_interface(self, name):
        return name in self.interfaces
