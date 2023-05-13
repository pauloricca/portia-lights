import socket
import time
import threading
import subprocess
from constants import *

# TODO: Add Thread locks around messages and slaveIps

class Master:

    def __init__(self):
        # List of slaves with ip, lastSeenAt, messageBuffer
        self.slaves = []
        self.start()
        self.messages = []

    def discoverSlaves(self):
        while True:
            print("Scanning network...")
            output = subprocess.check_output(("arp", "-a")).decode("ascii")

            # Output will be in this format, each device on a line:
            # ? (IP_ADDRESS) at MAC_ADDRESS on en0 ....

            outputLines = output.split('\n')

            potentialSlaveIps = []
            for outputLine in outputLines:
                lineParts = outputLine.split(' ')
                # Raspberry pis have mac addresses starting with b8
                if len(lineParts) >= 4 and lineParts[3].startswith('b8'):
                    potentialSlaveIps.append(lineParts[1].replace('(', '').replace(')', ''))

            # Check potential slaves, add new ones with open port, update lastSeenAt on known ones
            for potentialSlaveIp in potentialSlaveIps:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((potentialSlaveIp, PORT))
                        s.close()

                        haveSlaveAlready = False
                        for slave in self.slaves:
                            if slave.ip == potentialSlaveIp:
                                haveSlaveAlready = True
                                slave.lastSeenAt = time.time()
                        
                        if not haveSlaveAlready:
                            self.slaves.append({
                                'ip': potentialSlaveIp,
                                'lastSeenAt': time.time(),
                                'messages': [],
                            })
                    except:
                        potentialSlaveIps.remove(potentialSlaveIp)

            self.slaves = potentialSlaveIps
            print(potentialSlaveIps)

            time.sleep(DISCOVERY_CYCLE_TIME_SECONDS)


    def sendMessages(self):
        while True:
            time.sleep(SEND_MESSAGES_CYCLE_TIME_SECONDS)


    def start(self):
        discoverSlavesThread = threading.Thread(target=self.discoverSlaves, daemon=True)
        discoverSlavesThread.start()

        sendMessagesThread = threading.Thread(target=self.sendMessages, daemon=True)
        sendMessagesThread.start()
