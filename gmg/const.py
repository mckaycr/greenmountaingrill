# const.py

""" This module defines project-level constants"""

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