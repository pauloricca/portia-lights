import socket
import time
import threading
import subprocess
import json

from constants import *

# TODO: Add Thread locks around messages and slaveIps

class Master:

    def __init__(self):
        # List of slaves with ip, lastSeenAt, messageBuffer
        self.slaves = []
        self.messages = []

        slaveDiscoveryThread = threading.Thread(target=self.__slaveDiscoveryCycle, daemon=True)
        slaveDiscoveryThread.start()

        messageSendingThread = threading.Thread(target=self.__messageSendingCycle, daemon=True)
        messageSendingThread.start()

    def __slaveDiscoveryCycle(self):
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
                            if slave['ip'] == potentialSlaveIp:
                                haveSlaveAlready = True
                                slave['lastSeenAt'] = time.time()
                        
                        if not haveSlaveAlready:
                            self.slaves.append({
                                'ip': potentialSlaveIp,
                                'lastSeenAt': time.time(),
                                'messages': [],
                            })
                    except: {}
            
            # Forget slaves we haven't seen in a while
            slavesToKeep = []
            for slave in self.slaves:
                if slave['lastSeenAt'] > time.time() - FORGET_SLAVES_AFTER_SECONDS:
                    slavesToKeep.append(slave)
            
            self.slaves = slavesToKeep

            print('slaves: ')
            print(self.slaves)

            time.sleep(DISCOVERY_CYCLE_TIME_SECONDS)


    def __messageSendingCycle(self):
        while True:
            for slave in self.slaves:
                messagesToRetry = []
                for message in slave['messages']:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        try:
                            s.connect((slave['ip'], PORT))
                            print("sending message: " + message)
                            s.sendall(str.encode(message))
                            s.close()
                        except Exception as e:
                            print(e)
                            messagesToRetry.append(message)
                slave['messages'] = messagesToRetry

            time.sleep(SEND_MESSAGES_CYCLE_TIME_SECONDS)

    def sendMessage(self, message):
        for slave in self.slaves:
            slave['messages'].append(json.dumps(message))
