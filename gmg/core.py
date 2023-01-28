# core.py

"""This module is the core of this package"""

import socket
import ipaddress
import logging

from . import const

_LOGGER = logging.getLogger(__name__)

class GreenMountainGrill:
    def __init__(self, address, port):
      if not ipaddress.ip_address(address):
         raise ValueError(f'IP address {address} is not valid')
      _LOGGER.debug(f"Initializing grill {address}")
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
            data = b'UR#\x37"\x00\x96\x00\x06\x0b\x142\x19\x19\x19\x19Y\x02\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x03\x00\x00\x00\x00\x00DB02SUF02.3' # Dummy String to indicate TIMEOUT
            _LOGGER.debug(f"Grill at  {address} timed out")

        _LOGGER.debug(f"Status raw response: {data}")
        return data
    
    def __readBuf(self, bytes):
        if bytes[const.grillTemp]+bytes[const.grillTempHigh]*256 == 14115:
           e = 'GRILL TIMED OUT'
        else:
           e = None
        probes = [bytes[const.probeTemp]+(bytes[const.probeTempHigh]*256),bytes[const.probeSetTemp]+(bytes[const.probeSetTemp]*256),bytes[const.probeTemp2],bytes[const.probeSetTemp2]]
        data = {
            'temp':bytes[const.grillTemp]+bytes[const.grillTempHigh]*256,
            'tempSet': bytes[const.grillSetTemp]+bytes[const.grillSetTempHigh]*256,
            'probe': [{'temp':k,'tempSet':v} for k,v in [probes[i:i+2] for i in range(0,len(probes),2)]],
            'state':{
                'power': const.grillStates[bytes[const.grillState]],
                'fire':const.fireStates[bytes[const.fireState]],
                'warning':const.warnStates[bytes[const.warnCode]]
            },
            'test':bytes[4],
            'error': e
        }
        return data
    def status(self):
        data = self.__readBuf(self.__sendCommand(self.address,self.port,const.commands['status']))
        _LOGGER.debug(f"Status response: {data}")
        return data
    def serial(self):
        data = {
             'serial':str(self.__sendCommand(self.address,self.port,const.commands['id']), 'utf-8')
        }
        _LOGGER.debug(f"Status response: {data}")
        
        return data
