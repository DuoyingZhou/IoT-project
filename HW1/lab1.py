import math
import mraa
import time
import pyupm_i2clcd as lcd
import pyupm_grove as grove
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.setCursor(0,0)
myLcd.setColor(53, 39, 249)
myLcd.write("Temperature")
switch_pin_number=8
switch = mraa.Gpio(switch_pin_number)
switch.dir(mraa.DIR_IN)

tempSensor = mraa.Aio(1)

try:
    while(1):
        if(switch.read()):
            myLcd.setCursor(1,0)
            myLcd.setColor(53, 39, 249)
            a  = tempSensor.read()
            print a
            B = 4275
            R0 = 100000 
            R = 1023.0/a - 1.0
            R = 100000.0 * R
            temperature = 1.0/(math.log(R/100000.0)/B + 1/298.15) - 273.15
            #temp = grove.GroveTemp(1)
            #celsius = temp.value()
            #print celsius
            T = "%.1f" % temperature
            myLcd.write(str(T))
            #myLcd.write(str(celsius))
            time.sleep(0.5)
except KeyboardInterrupt:
    exit
