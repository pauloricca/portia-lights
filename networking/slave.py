import socket
import json
import threading
import time

from events import Event, EVENT_TYPES

class Slave:
    port: int
    isVerbose: bool
    events: list[Event]
    # Master time minus local time. We use this to change the times when we receive events.
    masterTimeDiff: int

    def __init__(
            self,
            port = 63277,
            isVerbose = False,
        ):
        self.port = port
        self.isVerbose = isVerbose
        self.events = []
        self.masterTimeDiff = 0
        
        waitForNetworkThread = threading.Thread(target=self.__receiveToMessagesCycle, daemon=True)
        waitForNetworkThread.start()
    
    def popEvents(self):
        poppedEvents = self.events
        self.events = []
        return poppedEvents
        

    def __receiveToMessagesCycle(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("", self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    self.isVerbose and print(f"Connected by {addr}")
                    message = ''
                    connectionOpen = True
                    while connectionOpen:
                        data = conn.recv(1024)
                        if data:
                            message += data.decode('ascii')
                        else:
                            if message != '':
                                try:
                                    event: Event = json.loads(message, object_hook=asEvent)

                                    # Consume clock sync events
                                    if event.type == EVENT_TYPES.CLOCK_SYNC:
                                        self.masterTimeDiff = event.params['time'] - time.time()
                                    else:
                                        # Adjust event times to compensate master time difference
                                        if event.atTime: event.atTime -= self.masterTimeDiff
                                        self.events.append(event)

                                    self.isVerbose and print("New event:")
                                    self.isVerbose and print(event)
                                except Exception as e:
                                    print("Error parsing message: " + message)
                                    print(e)
                            connectionOpen = False

# Convert event dict converted from json to Event object
def asEvent(jsonEventDict: dict):
    if 'type' not in jsonEventDict:
        return jsonEventDict
    else:
        return Event(
            type=jsonEventDict['type'],
            atTime=jsonEventDict['atTime'] if 'atTime' in jsonEventDict else None,
            params=jsonEventDict['params'] if 'params' in jsonEventDict else {}
        )