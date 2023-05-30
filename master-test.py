#!/usr/bin/env python3

import time
from events import EventManager

from networking.master import Master

# Raspberry pis have mac addresses starting with b8
master = Master(macAddressStartMask = 'b8', verbose = True)
eventManager = EventManager()

while True: 
    events = eventManager.popEvents()
    master.pushEvents(events)
    time.sleep(0.1)