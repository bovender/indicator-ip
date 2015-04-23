import os
import yaml
import logging

"""
Stores and retrieves settings.
"""
class Settings:
    __interface_key = 'interface'
    __url_key = 'url'
    __log = logging.getLogger(__name__)

    def __init__(self):
        self.__log.debug('Initializing %s', self.__class__)
        self.interface = None
        self.url = None

    """
    Loads the previous settings.
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
            config = {}
        self.__log.debug('Loaded config: %s', config)
        self.interface = config.get(self.__interface_key)
        self.url = config.get(self.__url_key)

    """
    Saves current settings.
    """
    def save(self):
        self.__log.info('Saving current configuration')
        config = { 
                self.__interface_key: self.interface,
                self.__url_key: self.url
                }
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

