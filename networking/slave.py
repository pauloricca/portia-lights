import socket
import json
import threading
from events import Event

class Slave:
    events: list[Event]

    def __init__(
            self,
            port = 63277,
            verbose = False,
        ):
        self.port = port
        self.verbose = verbose
        self.events = []
        
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
                    self.verbose and print(f"Connected by {addr}")
                    message = ''
                    connectionOpen = True
                    while connectionOpen:
                        data = conn.recv(1024)
                        if data:
                            message += data.decode('ascii')
                        else:
                            if message != '':
                                try:
                                    messageObj = json.loads(message, object_hook=asEvent)
                                    self.events.append(messageObj)
                                    self.verbose and print("New event:")
                                    self.verbose and print(messageObj)
                                except Exception as e:
                                    print("Error parsing message: " + message)
                                    print(e)
                            connectionOpen = False

def asEvent(jdict: dict):
    if 'type' not in jdict:
        return jdict
    else:
        return Event(type=jdict['type'], params=jdict['params'] if 'params' in jdict else {})