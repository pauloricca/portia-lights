#!/usr/bin/env python3

import time

from networking.master import Master

# Raspberry pis have mac addresses starting with b8
master = Master(macAddressStartMask = 'b8', verbose = True)

while True: 
    time.sleep(10)
    master.sendMessage({"event": "BAM", "arg": 1})