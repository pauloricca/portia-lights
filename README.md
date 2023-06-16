# Set up

$ sudo raspi-config

In System > enable go to command line, logged in
And in Interface Options > enable both SSH and SPI

To play audio as root we need to make the usb audio interface the default interface on root

Alsa config to make usb audio the default on the root account
https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config

$ sudo echo "blacklist snd_bcm2835" >> /etc/modprobe.d/raspi-blacklist.conf

Then enable the USB audio card with

$ sudo nano /lib/modprobe.d/aliases.conf

find the line with:

options snd-usb-audio index=-2

and put a # in the beginning of that line. Then exit and save file.

$ sudo reboot

Now the usb audio should be the first when we type

$ sudo aplay -l

# Install

$ sudo pip3 install -r requirements.txt

# Running

$ ./start
$ ./stop

# When installing new libraries

$ pip3 freeze > requirements.txt

# Add script to boot

$ sudo crontab -e

Add line:

@reboot /home/admin/spider/start