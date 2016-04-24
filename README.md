# indicator-ip

![indicator](https://github.com/bovender/indicator-ip/raw/master/src/IndicatorIp/images/screenshot.png)

A Ubuntu [indicator](http://unity.ubuntu.com/projects/appindicators/)
to display the current IP address.

Tested on Ubuntu 14.10, 15.04, 15.10 and 16.04 with Unity.


## Installation

### PPA

        sudo apt-add-repository ppa:bovender/bovender
        sudo apt-get update
        sudo apt-get install indicator-ip

This will install the program and configure automatic start at login. To
run it right away, press `ALT+F2` to open the Unity command prompt and
enter `indicator-ip`. 

### Git repository

  1. Checkout source code.
  2. Auto-run `PATH_TO_REPO/src/indicator-ip` on system start-up.


## Description

**indicator-ip** adds an indicator and menu to the indicator bar and
shows the IP addresses of any connected network interfaces as well as
the public IP that belongs to this computer on the internet.

The public IP is fetched from a service that must return nothing but the
IP address in plain text form. The default service is
`checkip.amazonaws.com`. An alternative service (e.g., `icanhazip.com`
can be given on the command line.


## Options

### `-i INTERFACE, --interface INTERFACE`

Show the IP for the given interface at startup. Use **`-i public`** to
show the public IP.

### `-u URL, --fetch-ip-url URL`

Fetch the IP from the service at URL. By default, **indicator-ip** uses
`checkip.amazonaws.com` to obtain the public IP. You may want to use
another service such as `icanhazip.com` or any other service that
returns the IP in text form. Note that indicator-ip will refuse to take
output that is longer than 17 bytes (e.g., longer than `xxx.xxx.xxx.xxx`
plus a trailing newline and/or carriage return).

### `-v, --verbose`

Increase verbosity to standard output. Of course this is only meaningful
if you run **indicator-ip** in a terminal. Use one or more **`v`** to set
the debug level to WARN, INFO, or DEBUG (e.g., **`-vvv`** to see debug
messages).

### `-V, --version`

Print version number and exit.

### `-h, --help`

The usual.

### `--autostart`

Enables autostart upon Unity login. This is done by creating a file
`indicator-ip.desktop` in `~/.config/autostart`. If you want to change
the IP provider service, add the **-u** option to the command line in
the autostart file. When run with root privileges, this will enable 
autostart system-wide.

### `--no-autostart`

Disables automatic start of the applet during Unity login by removing
the file `~/.config/autostart/indicator-ip.desktop` . When run with root 
privileges, this will disable autostart system-wide.


## Files

*~/.config/autostart/indicator-ip.desktop*

Autostart file (created by the **--autostart** option, removed by
**-no-autostart**).
                

## Website

<https://github.com/bovender/indicator-ip>


## History

- [DJG](https://github.com/sentientwaffle) wrote the original script
  (https://github.com/sentientwaffle/unity-ip-indicator) in May 2012.
- In April and May 2015, [Daniel Kraus](https://github.com/bovender)
  extended the script with additional features such as the ability to
  fetch the public IP, and provides a `.deb` package in his personal
  package archive (ppa:bovender/bovender).


## Copyright

Copyright (c) 2012 [DJG](https://github.com/sentientwaffle),
2015-2016 Daniel Kraus ([bovender](https://github.com/bovender))

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject
to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

<!-- vim: set tw=72: -->
