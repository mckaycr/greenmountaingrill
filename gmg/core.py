# core.py

"""This module is the core of this package"""

import socket
from . import const
class GreenMountainGrill:
    def __init__(self, address, port):
        self.address = address
        self.port = port
    
    def __sendCommand(self, address, port, command):
        msg = bytes(command, 'utf-8')
        sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
        sock.settimeout(5)
        try:
            sock.sendto(msg, (address, port))
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            sock.close()
        except socket.timeout:
            data = 'timeout'
        return data
    
    def __readBuf(self, bytes):
        probes = [bytes[probeTemp]+(bytes[probeTempHigh]*256),bytes[probeSetTemp]+(bytes[probeSetTemp]*256),bytes[probeTemp2],bytes[probeSetTemp2]]
        data = {
            'temp':bytes[grillTemp]+bytes[grillTempHigh]*256,
            'tempSet': bytes[grillSetTemp]+bytes[grillSetTempHigh]*256,
            'probe': [{'temp':k,'tempSet':v} for k,v in [probes[i:i+2] for i in range(0,len(probes),2)]],
            'state':{
                'power': grillStates[bytes[grillState]],
                'fire':fireStates[bytes[fireState]],
                'warning':warnStates[bytes[warnCode]]
            },
            'test':bytes[4],
            'error':None
        }
        return data
    def status(self):
        data = self.__readBuf(self.__sendCommand(self.address,self.port,commands['status']))
        return data
