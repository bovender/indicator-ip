#!/bin/sh
grep -oP '(?<=VERSION = ")[^"]+' src/IndicatorIp/version.py
