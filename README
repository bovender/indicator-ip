# indicator-ip

![indicator](https://github.com/bovender/indicator-ip/raw/master/images/screenshot.png)

A Ubuntu [indicator](http://unity.ubuntu.com/projects/appindicators/)
to display the current IP address.

Tested on Ubuntu 14.10 and 15.04 with Unity.

# Installation

  1. Checkout source code.
  2. Auto-run `indicator-ip` on system start-up.

# Command-line options

## `-i INTERFACE, --interface INTERFACE`

Show the IP for the given interface at startup. Use `-i public` to show the public IP.

## `-u URL, --fetch-ip-url URL`

Fetch the IP from the service at URL. By default, indicator-ip uses
`checkip.amazonaws.com` to obtain the public IP. You may want to use
another service such as `icanhazip.com` or any other service that
returns the IP in text form. Note that indicator-ip will refuse to take
output that is longer than 17 bytes (e.g., longer than `xxx.xxx.xxx.xxx`
plus a trailing newline and/or carriage return).

## `-v, --verbose`

Increase verbosity to standard output. Of course this is only meaningful
if you run `indicator-ip` in a terminal. Use one or more `v`'s to set
the debug level to WARN, INFO, or DEBUG (e.g., `-vvv` to see debug
messages).

## `-V, --version`

Print version number and exit.

## `-h, --help`

The usual.


# To do

- Package and distribute via PPA


# Modifications by bovender

The code base by [DJG](https://github.com/sentientwaffle) was completely
overhauled by me in April 2015. I implemented the ability to switch between
internal interfaces and the public IP.


# MIT License

Copyright (c) 2012 [DJG](https://github.com/sentientwaffle),
2015 Daniel Kraus ([bovender](https://github.com/bovender))

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
