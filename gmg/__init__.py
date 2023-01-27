# __init__.py
__version__ = "0.0.1"

import socket

grillTemp = 2
grillTempHigh = 3
probeTemp = 4
probeTempHigh = 5
grillSetTemp = 6
grillSetTempHigh = 7
probeTemp2 = 16
probeSetTemp2 = 18
curveRemainTime = 20
warnCode = 24
probeSetTemp = 28
probeSetTempHigh = 29
grillState = 30
grillMode = 31
fireState = 32
fileStatePercent = 33
profileEnd = 34
grillType = 35
pelletAlarm1 = 48
pelletAlarm2 = 50
grillStates = {
    0: 'OFF',
    1: 'ON',
    2: 'FAN',
    3: 'REMAIN',
  }
fireStates = {
    0: 'DEFAULT',
    1: 'OFF',
    2: 'STARTUP',
    3: 'RUNNING',
    4: 'COOLDOWN',
    5: 'FAIL',
  }
warnStates = {
    0: 'FAN_OVERLOADED',
    1: 'AUGER_OVERLOADED',
    2: 'IGNITOR_OVERLOADED',
    3: 'BATTERY_LOW',
    4: 'FAN_DISCONNECTED',
    5: 'AUGER_DISCONNECTED',
    6: 'IGNITOR_DISCONNECTED',
    7: 'LOW_PELLET',
  }
commands ={
    'on':'UK001!',
    'off':'UK004!',
    'status':'UR001!',
    'id':'UL!',
    'tempSet':{
      'grill':'UT',
      'probe1':'UF',
      'probe2':'Uf',
    }
}

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
