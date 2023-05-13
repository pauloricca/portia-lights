import socket
import time
import threading
import subprocess
import json

# TODO: Add Thread locks around messages and slaveIps

class Master:

    # Times in seconds
    def __init__(
            self,
            port = 63277,
            discoveryCycleTime=5,
            sendRetryTime=0.2,
            forgetSlaveTime=30,
            verbose=False,
            macAddressStartMask=''
        ):
        # List of slaves with ip, lastSeenAt, messageBuffer
        self.slaves = []
        self.messages = []
        self.port = port
        self.discoveryCycleTime = discoveryCycleTime
        self.sendRetryTime = sendRetryTime
        self.forgetSlaveTime = forgetSlaveTime
        self.verbose = verbose
        self.macAddressStartMask = macAddressStartMask

        slaveDiscoveryThread = threading.Thread(target=self.__slaveDiscoveryCycle, daemon=True)
        slaveDiscoveryThread.start()

    def __startMessageSendingCycle(self):
        messageSendingThread = threading.Thread(target=self.__messageSendingCycle, daemon=True)
        messageSendingThread.start()

    def __slaveDiscoveryCycle(self):
        while True:
            self.verbose and print("Scanning network...")
            output = subprocess.check_output(("arp", "-a")).decode("ascii")

            # Output will be in this format, each device on a line:
            # ? (IP_ADDRESS) at MAC_ADDRESS on en0 ....

            outputLines = output.split('\n')

            potentialSlaveIps = []
            for outputLine in outputLines:
                lineParts = outputLine.split(' ')
                if len(lineParts) >= 4 and lineParts[3].startswith(self.macAddressStartMask):
                    potentialSlaveIps.append(lineParts[1].replace('(', '').replace(')', ''))

            # Check potential slaves, add new ones with open port, update lastSeenAt on known ones
            for potentialSlaveIp in potentialSlaveIps:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((potentialSlaveIp, self.port))
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
                                'messageBuffer': [],
                            })
                    except: {}
            
            # Forget slaves we haven't seen in a while
            slavesToKeep = []
            for slave in self.slaves:
                if slave['lastSeenAt'] > time.time() - self.forgetSlaveTime:
                    slavesToKeep.append(slave)
            
            self.slaves = slavesToKeep

            self.verbose and print('slaves: ')
            self.verbose and print(self.slaves)

            time.sleep(self.discoveryCycleTime)


    def __messageSendingCycle(self):
        stillHaveMessagesToSend = True
        while stillHaveMessagesToSend:
            stillHaveMessagesToSend = False
            for slave in self.slaves:
                messagesToRetry = []
                for message in slave['messageBuffer']:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        try:
                            s.connect((slave['ip'], self.port))
                            self.verbose and print("sending message '" + message + "' to " + slave['ip'])
                            s.sendall(str.encode(message))
                            s.close()
                            slave['lastSeenAt'] = time.time()
                        except:
                            stillHaveMessagesToSend = True
                            messagesToRetry.append(message)
                slave['messageBuffer'] = messagesToRetry

            time.sleep(self.sendRetryTime)

    def sendMessage(self, message):
        for slave in self.slaves:
            slave['messageBuffer'].append(json.dumps(message))

        self.__startMessageSendingCycle()
