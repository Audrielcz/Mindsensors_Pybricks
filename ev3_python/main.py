#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog

from pybricks.media.ev3dev import Font

from EV3_python import *

import os
import sys
import time



def matrixTest() : #testing MATRIX functions

    # Create your objects here.
    ev3 = EV3Brick()
    matrix= EV3Matrix(Port.S1,0x22)


    print(matrix.GetFirmwareVersion())
    print(matrix.GetDeviceId())

    #matrix.blink_mode()

    matrix.clear()

    matrix.text(0,'S',1)
    #matrix.pixel(7,7,1)
    #matrix.mirror()
    
    #matrix.row(3,2)
    
    #matrix.full()
    #matrix.clear()

    #matrix.pixel(7,7,False)

    #matrix.row(0,False)
    matrix.column(0,True)

    #matrix.set_brightness(10)
    #time.sleep(1)

    

    ev3.speaker.beep()

def cameraTest(): #testing Camera functions
    ev3 = EV3Brick()
    camera = NXTCam5(Port.S2,0x02)

    print(camera.GetFirmwareVersion())
    print(camera.GetDeviceId())

    print(camera.count_objects())
    print(camera.get_all_object_info("object"))

def objectTest(): #testing Camera input with MATRIX as output
    ev3 = EV3Brick()
    camera = NXTCam5(Port.S2,0x02)
    matrix= EV3Matrix(Port.S1,0x22)

    print(camera.GetFirmwareVersion())
    print(camera.GetDeviceId())

    camera.select_object_tracking_mode()
    while True:
        data = camera.count_objects()
        matrix.text(0,str(data),1)
        time.sleep(1)

def muxTest():
    ev3 = EV3Brick()
    mux = NXTMMX(Port.S3,0x6)
    print(mux.GetFirmwareVersion())
    print(mux.GetDeviceId())
    print(mux.get_voltage())
    
    """
    for i in range(128):
        try:
            mux = NXTMMX(Port.S3,i2c_address = i+1)
            print("NXTMMX on: ",hex(i+1))
            print(mux.GetFirmwareVersion())
            print(mux.GetDeviceId())
            print(mux.get_voltage())
            break
        except:
            print("Nothing on: ",hex(i+1))
    """
    #mux.motor1_run(100)
    #mux.motor2_run(100)
    #mux.motors_tank_move(50,50)

    #mux.motor1_run_time(50, 5)
    #mux.motor2_run_time(50, 5)

    #mux.motor1_run_angle(50, 360)
    #mux.motor2_run_angle(50, 360)

    #mux.motor1_run_target(50, -360, wait = False)
    #mux.motor2_run_target(50, -360)

    #mux.motor1_run_until_stalled(50)
    #mux.motor2_run_until_stalled(50)

    #mux.motor1_run_time(-50, 5, wait = False)
    #mux.motor2_run_time(-50, 5)

    mux.motor1_run_time(-50, 5)
    mux.motors_stop()

    #mux.change_address(0x06)


matrixTest()
#cameraTest()
#objectTest()
#muxTest()

#i2cScanner()