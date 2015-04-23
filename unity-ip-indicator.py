#!/usr/bin/python
import gtk
import logging
from lib.indicator import IPIndicator

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)
    log.info('Starting %s', __file__)
    i = IPIndicator()
    gtk.main()
    log.info('Exiting %s', __file__)

