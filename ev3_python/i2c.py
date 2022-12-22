#!/usr/bin/env pybricks-micropython
#!/usr/bin/env pybricks-micropython

#Version 1.01


from pybricks.hubs import EV3Brick
from pybricks.iodevices import I2CDevice
from pybricks.iodevices import  AnalogSensor
from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import Font

import os
import sys
import time

# state constants
ON = True
OFF = False

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

## mindsensors_i2c: this class provides i2c functions
#  for read and write operations.
class i2c():
    
    def __init__(self,port, i2c_address):
        self.port = port
        self.i2c_address=i2c_address
        self.i2c = I2CDevice(port,i2c_address>>1)
        #self.port.mode = 'other-i2c'


    def errMsg(self):
        print ("Error accessing 0x%02X: Check your I2C address" % self.address)
        return -1

    ## Read a string from your i2c device starting at a given location
    #  @param self The object pointer.
    #  @param reg The first register of the string to read from.
    #  @param length The length of the string.
    def readString(self, reg, length):
        return self.i2c.read(reg, length)


    ## Read an unsigned byte from your i2c device at a given location
    #  @param self The object pointer.
    #  @param reg The register to read from.
    def readByte(self, reg):
        a =self.i2c.read(reg, 1)
        return int.from_bytes(a, "little")

    ## Write a byte to your i2c device at a given location
    #  @param self The object pointer.
    #  @param reg The register to write value at.
    #  @param value Value to write.
    def writeByte(self, reg, value):
        
        self.i2c.write( reg,value)
        pass

    ## Write a command to your i2c device at a command location
    #  @param self The object pointer.
    #  @param comamnd to write .
    def issueCommand(self,  value):
       self.i2c.write( 0x42, value)
             


    ## Read a byte array from your i2c device starting at a given location
    #  @param self The object pointer.
    #  @param reg The first register in the array to read from.
    #  @param length The length of the array.
    def readArray(self, reg, length):

        return self.i2c.read(reg, length)
        
    ## Write a byte array from your i2c device starting at a given location
    #  @param self The object pointer.
    #  @param reg The first register in the array to write to.
    #  @param arr The array to write.
    def writeArray(self, reg, arr):
        return self.i2c.write(reg, bytearray(arr))
        
    ## Read a signed byte from your i2c device at a given location
    #  @param self The object pointer.
    #  @param reg The register to read from.
    def readByteSigned(self, reg):
        a = self.i2c.read(reg, 1)
        signed_a =int.from_bytes(a, "little") #ctypes.c_byte.value 
        return signed_a

    ## Write an unsigned 16 bit integer from your i2c device from a given location. little endian write integers.
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to write.
    #  @param int The integer to write.
    def writeInteger(self, reg, i):        
        i = int(i)
        results = self.i2c.write(reg, [i%256, (i>>8)%256])

    ## Read a signed 16 bit integer from your i2c device from a given location. Big endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readIntegerSignedBE(self, reg):
        a = self.readIntegerBE(reg)
        if a&0x8000 : a = a -65535 
        return a       
    
    ## Read a signed 16 bit integer from your i2c device from a given location. little endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readIntegerSigned(self, reg):
        a = self.readInteger(reg)
        if a&0x8000 : a = a -65535 
        return a

    ## Read an unsigned 32bit integer from your i2c device from a given location. Big endian read integers.
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readLongBE(self, reg):
        
        results = self.i2c.read(reg,4)
        return results[3] + (results[2]<<8)+(results[1]<<16)+(results[0]<<24)           
        
    ## Read an unsigned 32bit integer from your i2c device from a given location. little endian read integers.
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readLong(self, reg):
        results = self.i2c.read(reg,4)
        return results[0] + (results[1]<<8)+(results[2]<<16)+(results[3]<<24)       

    ## Read a signed 32bit integer from your i2c device from a given location. Big endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readLongSignedBE(self, reg):
        a = self.readLongBE(reg)
        if a&0x80000000 : a = a -0xFFFFFFFF
        return a    
          
    ## Read a signed 32bit integer from your i2c device from a given location. little endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readLongSigned(self, reg):
        a = self.readLong(reg)
        if a&0x80000000 : a = a -0xFFFFFFFF
        return a

    ##  Read the firmware version of the i2c device
    #  @param self The object pointer.
    def GetFirmwareVersion(self):
        try:
            ver = self.readString(0x00, 8)
            return ver
        except:
            print( "Error: Could not retrieve Firmware Version" )
            print ("Check I2C address and device connection to resolve issue")
            return ""

    ## Read an unsigned 16 bit integer from your i2c device from a given location.  Big-endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readIntegerBE(self, reg):        
        results = self.i2c.read( reg, 2)
        return results[1] + (results[0]<<8)
        
    ## Read an unsigned 16 bit integer from your i2c device from a given location. little endian read integers.
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readInteger(self, reg):        
        try:
            results = self.i2c.read(reg, 2)
            return results[0] + (results[1]<<8)
        except:
            return 0    

    ##  Read the vendor name of the i2c device
    #  @param self The object pointer.
    def GetVendorName(self):
        try:
            vendor = self.readString(0x08, 8)
            return vendor
        except:
            print ("Error: Could not retrieve Vendor Name")
            print ("Check I2C address and device connection to resolve issue")
            return ""
            
    ##  Read the i2c device id
    #  @param self The object pointer.
    def GetDeviceId(self):
        try:    
            device = self.readString(0x10, 8)
            return device
        except:
            print ("Error: Could not retrieve Device ID")
            print ("Check I2C address and device connection to resolve issue")
            return ""    