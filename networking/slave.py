import socket
import json
import threading

class Slave:

    def __init__(
            self,
            port = 63277,
            verbose = False,
            onMessage = None
        ):
        self.port = port
        self.verbose = verbose
        self._onMessageCallback = onMessage
        
        waitForNetworkThread = threading.Thread(target=self.__receiveToMessagesCycle, daemon=True)
        waitForNetworkThread.start()

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
                                    messageObj = json.loads(message)
                                    if self._onMessageCallback: self._onMessageCallback(messageObj)
                                    self.verbose and print("New event:")
                                    self.verbose and print(messageObj)
                                except Exception as e:
                                    print("Error parsing message: " + message)
                                    print(e)
                            connectionOpen = False
