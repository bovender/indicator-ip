import subprocess

"""
Enumerates the network interfaces on the system by calling
the external 'ip' command.
"""
class Interfaces:
    def __init__(self):
        all_interfaces = subprocess.check_output(
            'ip -4 --oneline addr show | awk \'{ print $2 }\'',
            shell=True)
        self.interfaces = all_interfaces.splitlines()
        try:
            self.interfaces.remove('lo')
        except:
            pass
