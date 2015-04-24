# IP Indicator

![indicator](https://github.com/bovender/indicator-ip/raw/master/images/screenshot.png)

A Ubuntu [indicator](http://unity.ubuntu.com/projects/appindicators/)
to display the current IP address.

Tested on Ubuntu 14.10 with Unity.

# Installation

  1. Checkout source code.
  2. Auto-run `indicator-ip` on system start-up.

# Configuration

The indicator applet will store the last used interface in a config file in

        ~/.config/indicator-ip/settings

This file may also contain an alternative URL to fetch the public IP:

        [indicator-ip]
        url = icanhazip.com ; <-- this would be the alternative URL
        interface = public


# To do

- Implement command line arguments to fetch public IP and to set log level.


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
