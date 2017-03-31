#!/usr/bin/env python
# Michael Saunby. April 2013   
# 
# Read temperature from the TMP006 sensor in the TI SensorTag 
# It's a BLE (Bluetooth low energy) device so using gatttool to
# read and write values. 
#
# Usage.
# sensortag_test.py BLUETOOTH_ADR
#
# To find the address of your SensorTag run 'sudo hcitool lescan'
# You'll need to press the side button to enable discovery.
#
# Notes.
# pexpect uses regular expression so characters that have special meaning
# in regular expressions, e.g. [ and ] must be escaped with a backslash.
#

import pexpect
import sys
import time

def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t



bluetooth_adr = sys.argv[1]
tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
tool.expect('\[LE\]>')
print "Preparing to connect. You might need to press the side button..."
tool.sendline('connect')
# test for success of connect
tool.expect('Connection successful')
tool.sendline('char-write-req 0x2b 0x01')
tool.expect('\[LE\]>')
while True:
    time.sleep(1)
    tool.sendline('char-read-hnd 0x2a')
   # tool.expect('descriptor: .*')
    tool.expect('Notification handle = 0x002a value: 34 .*')
    rval = tool.after.split()
    print rval
    low = floatfromhex(rval[10])
    high = floatfromhex(rval[11])
    temp = (high * 256 + low)/10
   # ambT = floatfromhex(rval[4] + rval[3])
    print temp
   # calcTmpTarget(objT, ambT)
   # print tool

