import socket
import time
import threading

PORT = 65432
BUFFER_SIZE = 1024

def receiveEvents():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                message = ''
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if data:
                        message += data.decode('ascii')
                    else:
                        print(message)
                        break

def startSlave():
    waitForNetworkThread = threading.Thread(target=receiveEvents, daemon=True)
    waitForNetworkThread.start()
