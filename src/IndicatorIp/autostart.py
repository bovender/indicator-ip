import os
import logging

def enable():
    log = logging.getLogger(__name__)
    log.info("Writing autostart file")
    path = __get_autostart_path()
    log.debug(path)
    if not os.path.isfile(path):
        print "Enabling autostart."
        try:
            with open(path, 'w') as f:
                f.write("""[Desktop Entry]
                Type=Application
                Exec=indicator-ip
                Hidden=false
                NoDisplay=false
                X-GNOME-Autostart-enabled=true
                Name=IP Indicator
                Name[en_US]=IP Indicator
                Name[de_DE]=IP-Indicator
                Comment=Displays IP addresses.
                Comment[en_US]=Displays IP addresses.
                Comment[de_DE]=Zeigt die aktuellen IP-Adressen.""")
        except (OSError, IOError) as e:
            print "Could not write file; error: {} ({})".format(e.strerror, e.errno)
            log.warn("Failed to write file; error: {} ({})".format(e.strerror, e.errno))
    else:
        print "Autostart is already enabled."
        print "If it does not work, please inspect the file {}".format(path)
        log.info("Autostart is already enabled")

def disable():
    log = logging.getLogger(__name__)
    path = __get_autostart_path()
    log.info("Disabling autostart")
    log.debug(path)
    if not os.path.isfile(path):
        print "Autostart is not enabled at the moment."
        log.info('Autostart .desktop file not found')
    else:
        print "Disabling autostart."
        log.info("Removing autostart .desktop file")
        try:
            os.remove(path)
        except OSError as e:
            print "Could not remove file; error: {} ({})".format(e.strerror, e.errno)
            log.warn("Failed to delete file; error: {} ({})".format(e.strerror, e.errno))

def __get_autostart_path():
    return os.path.join(
            os.getenv('HOME'), '.config', 'autostart', 'indicator-ip.desktop')
