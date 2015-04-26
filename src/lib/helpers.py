from os.path import dirname, realpath, join

"""
Returns the base directory of the script.
This function assumes that it is defined in a subdirectory
one level below the base directory of the executing script.
Symlinks are followed.
"""
def script_path():
    return realpath(join(dirname(realpath(__file__)), '..'))
