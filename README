## Install

$ pip3 install -r requirements.txt

## To play audio as root we need to make the usb audio interface the default interface on root

# Alsa config to make usb audio the default on the root account
https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config

$ sudo echo "blacklist snd_bcm2835" >> /etc/modprobe.d/raspi-blacklist.conf

# Then enable the USB audio card with

$ sudo nano /lib/modprobe.d/aliases.conf

# find the line with:

options snd-usb-audio index=-2

# and put a # in the beginning of that line. Then exit and save file.

$ sudo reboot

# Now the usb audio should be the first when we type

$ sudo aplay -l

## Running

$ sudo ./spider.py

## When installing new libraries

$ pip freeze > requirements.txt