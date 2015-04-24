import os
import logging
import re
from ConfigParser import SafeConfigParser

DEFAULT_PROVIDER = 'checkip.amazonaws.com'

"""
Stores and retrieves settings.
"""
class Settings:
    __interface_key = 'interface'
    __url_key = 'url'
    __log = logging.getLogger(__name__)
    __section = 'indicator-ip'

    def __init__(self):
        self.__log.debug('Initializing %s', self.__class__)
        self.parser = self.__create_parser()
        self.interface = None
        self.url = DEFAULT_PROVIDER
        self.load()

    """
    Loads the previous settings.
    """
    def load(self):
        self.__log.info('Loading previous configuration')
        try:
            self.parser.read(self.config_file_path())
            if self.parser.has_section(self.__section):
                self.__log.debug('Loaded config: %s', self.parser.items(self.__section))
                if self.parser.has_option(self.__section, self.__interface_key):
                    self.interface = self.parser.get(self.__section, self.__interface_key)
                self.url = self.parser.get(self.__section, self.__url_key)
                self.sanitize_url()
        except IOError as e:
            self.__log.warning('Could not load config: %s (%s)',
                    e.strerror, e.errno)

    """
    Saves current settings.
    """
    def save(self):
        self.__log.info('Saving current configuration')
        self.parser = self.__create_parser()
        self.parser.add_section(self.__section)
        self.parser.set(self.__section, self.__url_key, self.url)
        self.parser.set(self.__section, self.__interface_key, self.interface)
        self.__log.debug('Configuration to save: %s', self.parser.items(self.__section))
        try:
           file_name = self.config_file_path()
           dir = os.path.dirname(file_name)
           if not os.path.exists(dir):
               os.makedirs(dir)
           with open(file_name, 'w') as f:
               self.parser.write(f)
        except IOError as e:
            self.__log.warning('Could not save config: %s (%s)',
                    e.strerror, e.errno)

    """
    Performs some basic sanity checking on the fetch-ip URL and uses
    the default URL if needed.
    """
    def sanitize_url(self):
        self.__log.debug('Sanitizing URL %s', self.url)
        if not self.url:
            self.url = DEFAULT_PROVIDER
            self.__log.info('Using default IP provider %s', self.url)
            return
        if not re.match('^([a-zA-Z]+://)?[a-zA-Z-_./]+$', self.url):
            self.url = DEFAULT_PROVIDER
            self.__log.warning(
                    'Fetch-IP URL %s has unexpected format, falling back to default %s',
                    self.url)

    """
    Returns the path to the config file.
    """
    def config_file_path(self):
        path = os.path.join(
                os.path.expanduser('~/.config'),
                'indicator-ip',
                'settings')
        self.__log.debug('Config file path: %s', path)
        return path

    def __create_parser(self):
        return SafeConfigParser()
