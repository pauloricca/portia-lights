#!/usr/bin/env python3

import time

from networking.master import Master

master = Master()

while True: 
    time.sleep(10)
    master.sendMessage({"event": "BAM", "arg": 1})