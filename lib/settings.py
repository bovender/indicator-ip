import os
import yaml
import logging

"""
Holds a dictionary of IP objects and makes the last used IP type persist in
a file in the user's ~/.config directory.
"""
class Settings:
    __key = 'ip'
    __log = logging.getLogger(__name__)

    def __init__(self):
        self.__log.debug('Initializing %s', self.__class__)
        self.ips = {}
        self.current_ip = None

    """
    Adds an IP object to the dictionary.
    """
    def add_ip(self, ip):
        self.__log.info('Adding IP with name %s', ip.get_name())
        self.ips[ip.get_name()] = ip

    """
    Loads the last used IP from the config file.
    """
    def load(self):
        self.__log.info('Loading previous configuration')
        config = None
        try:
            with open(self.config_file_path(), 'r') as f:
                config = yaml.load(f)
        except IOError as e:
            self.__log.warning('Could not load config: %s (%s)',
                    e.strerror, e.errno)
        if not config:
            config = { self.__key: '' }
        self.current_ip = self.ips.get(config.get(self.__key))
        if self.current_ip:
            self.__log.debug('Using IP for "%s"', self.current_ip.get_name())
        else:
            default = self.ips.itervalues().next()
            self.__log.debug('Using default IP for "%s"', default.get_name())
            self.current_ip = default
        self.current_ip.activate()

    """
    Saves the last used IP to the config file.
    """
    def save(self):
        self.__log.info('Saving current configuration')
        config = { self.__key: self.current_ip.get_name() }
        self.__log.debug('Configuration to save: %s', config)
        try:
           file_name = self.config_file_path()
           dir = os.path.dirname(file_name)
           if not os.path.exists(dir):
               os.makedirs(dir)
           with open(file_name, 'w') as f:
               yaml.dump(config, f)
        except IOError as e:
            self.__log.warning('Could not save config: %s (%s)',
                    e.strerror, e.errno)

    """
    Returns the path to the config file.
    """
    def config_file_path(self):
        path = os.path.join(
                os.path.expanduser('~/.config'),
                'indicator-ip',
                'settings.yml')
        self.__log.debug('Config file path: %s', path)
        return path

