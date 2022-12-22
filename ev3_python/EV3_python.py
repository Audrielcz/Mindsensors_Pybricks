#!/usr/bin/env pybricks-micropython
#!/usr/bin/env pybricks-micropython


# Version 1.0
# by Bc. Matej Stetka, CTU in Prague
# Made as extension to Mindsensors.com library called mindsensorsPYB.py
# Code is free to use and edit. The only condition is to keep authors name. (and maybe add yours?)


# contents:
#   i2cScanner
#   EVMatrix library
#   MXTMMX library
#   NXTCam5 library

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

from i2c import i2c

## i2cScanner: this function provides scanning possibility for forgoten addresses
def i2cScanner():
    for p in [Port.S1, Port.S2, Port.S3, Port.S4]:
        print("------ Testing", p,"------------")
        for i in range(0, 128, 2):
            try:
                test = I2CDevice(p,(i)>>1)
                print(test.read(0x10, 8).decode("utf-8") )
                print("Sensor on: ",hex(i))
            except:
                pass


## EV3Matrix: this class provides functions for LED Matrix
#  for read and write operations.
class EV3Matrix(i2c):

    ## Command Register
    command_reg = 0x41
    
    ## Brightness register
    brightness_reg = 0x42
    ## Font type register
    font_type_reg = 0x43
    ## Font data register
    font_data_reg = 0x44
    ## Row register
    row_reg = 0x45
    ## Column register
    column_reg = 0x46
    ## Value register
    value_reg = 0x47
    ## Data buffer register
    data_buffer_reg = 0x48

    ## Initialize the class with the i2c address of your LED Matrix.
    #  @param self The object pointer.
    #  @param port Port where LED Matrix is connected.
    #  @param i2c_address Address of your LED Matrix.
    def __init__(self, port, i2c_address=0x22):
        i2c.__init__(self, port, i2c_address)  

    ## Changes i2c address of your LED Matrix.
    #  @param new_add Address to which user want to change.
    def change_address(self, new_add):
        self.writeByte(self.command_reg, (160).to_bytes(2, 'little'))
        self.writeByte(self.command_reg, (170).to_bytes(2, 'little'))
        self.writeByte(self.command_reg, (165).to_bytes(2, 'little'))
        self.writeByte(self.command_reg, new_add.to_bytes(2, 'little'))
        print("New address uploaded, please address this EV3Matrix as:", hex(new_add))

    ## Sets blink mode
    #  @param self The object pointer.
    def blink_mode(self):
        self.writeByte(self.command_reg,'B')
    
    ## Turns on or of one columns on LED Matrix
    #  @param self The object pointer.
    #  @param column The column which should be changed.
    #  @param on_off Bool to turn on or of lights.
    def column(self, column, on_off):
        for i in range(8):
            self.writeArray(self.row_reg,[i,column,on_off])        
            self.writeByte(self.command_reg,'P') 

    ## Writes text to LED Matrix
    #  @param self The object pointer.
    #  @param font Type of font.
    #  @param data Which data to write.
    #  @param brightness Sets brightness to certain level.
    def text(self, font = 0, data = ' ', brightness = 2):
        self.writeArray(self.brightness_reg ,[brightness, font, ord(data)])        
        self.writeByte(self.command_reg,'F')
    
    ## Changes brightness.
    #  @param self The object pointer.
    #  @param brightness Sets brightness to certain level.
    def set_brightness(self, brightness):
        if brightness > 15:
            brightness = 15
            print("Maximum brightness is 15.")
        if brightness < 0:
            brightness = 0
            print("Minimum brightness is 0.")
        self.writeByte(self.brightness_reg,brightness.to_bytes(2, 'little')) 
        self.writeByte(self.command_reg,'I') 
 
    ## Changes state of a pixel.
    #  @param self The object pointer.
    #  @param row Desired row.
    #  @param column Desired column.
    #  @param on_off Bool to turn on or of lights.
    def pixel(self, row, column, on_off):
        self.writeArray(self.row_reg,[row, column, on_off])        
        self.writeByte(self.command_reg,'P')
    
    ## Turns on or of one row on LED Matrix.
    #  @param self The object pointer.
    #  @param row The row which should be changed.
    #  @param on_off Bool to turn on or of lights.
    def row(self, row_data, on_off):
        for i in range(8):
            self.writeArray(self.row_reg,[row_data,i,on_off])        
            self.writeByte(self.command_reg,'P') 

    ## Mirrors/flips data on LED Matrix.
    #  @param self The object pointer.
    def mirror(self):
        self.writeByte(self.command_reg,'V')  

    ## Turns all pixels on.
    #  @param self The object pointer.
    def full(self):
        for i in range(8):
            for j in range(8):
                self.writeArray(self.row_reg,[i,j,1])        
                self.writeByte(self.command_reg,'P')

    ## Turns all pixels off.
    #  @param self The object pointer.
    def clear(self):
        for i in range(8):
            for j in range(8):
                self.writeArray(self.row_reg,[i,j,0])        
                self.writeByte(self.command_reg,'P')
                print(self.readString(self.data_buffer_reg,12),"***")

## NXTCam5: this class provides functions for NXTCam5.
#  for read and write operations.
class NXTCam5(i2c):

    ## Command register
    command_reg = 0x41

    ## Object count register
    count_obj_reg = 0x42

    ## 1st object
    ## Color of 1st object register
    clr_1st_reg = 0x43
    ## Top left X coordinate of 1st object register
    x_up_left_1st_reg = 0x44
    ## Top left Y coordinate of 1st object register
    y_up_left_1st_reg = 0x45
    ## Bottom right X coordinate of 1st object register
    x_lo_right_1st_reg = 0x46
    ## Bottom right Y coordinate of 1st object register
    y_lo_right_1st_reg = 0x47

    #2nd object
    clr_2nd_reg = 0x48
    x_up_left_2nd_reg = 0x49
    y_up_left_2nd_reg = 0x4A
    x_lo_right_2nd_reg = 0x4B
    y_lo_right_2nd_reg = 0x4C

    #3rd object
    clr_3rd_reg = 0x4D
    x_up_left_3rd_reg = 0x4E
    y_up_left_3rd_reg = 0x4F
    x_lo_right_3rd_reg = 0x50
    y_lo_right_3rd_reg = 0x51

    #4th object
    clr_4th_reg = 0x52
    x_up_left_4th_reg = 0x53
    y_up_left_4th_reg = 0x54
    x_lo_right_4th_reg = 0x55
    y_lo_right_4th_reg = 0x56

    #5th object
    clr_5th_reg = 0x57
    x_up_left_5th_reg = 0x58
    y_up_left_5th_reg = 0x59
    x_lo_right_5th_reg = 0x5A
    y_lo_right_5th_reg = 0x5B

    #6th object
    clr_6th_reg = 0x5C
    x_up_left_6th_reg = 0x5D
    y_up_left_6th_reg = 0x5E
    x_lo_right_6th_reg = 0x5F
    y_lo_right_6th_reg = 0x60

    #7th object
    clr_7th_reg = 0x61
    x_up_left_7th_reg = 0x62
    y_up_left_7th_reg = 0x63
    x_lo_right_7th_reg = 0x64
    y_lo_right_7th_reg = 0x65

    #8th object
    clr_8th_reg = 0x66
    x_up_left_8th_reg = 0x67
    y_up_left_8th_reg = 0x68
    x_lo_right_8th_reg = 0x69
    y_lo_right_8th_reg = 0x6A

    ## Initialize the class with the i2c address of your NXTCam5.
    #  @param self The object pointer.
    #  @param port Port where NXTCam5 is connected.
    #  @param i2c_address Address of your NXTCam5.
    def __init__(self, port,i2c_address=0x02):
        i2c.__init__(self,port, i2c_address)  

    ## Selects object tracking mode.
    #  @param self The object pointer.
    def select_object_tracking_mode(self):
        self.writeByte(0x41,'B') 

    ## Selects face tracking mode.
    #  @param self The object pointer.
    def select_face_tracking_mode(self):
        self.writeByte(0x41,'F') 

    ## Starts capturing continuous movie.
    #  @param self The object pointer.
    def begin_capture_continuos_movie(self):
        self.writeByte(0x41,'R') 

    ## Records short clip.
    #  @param self The object pointer.
    def capture_short_clip(self):
        self.writeByte(0x41,'M') 

    ## Captures picture.
    #  @param self The object pointer. 
    def capture_still_picture(self):
        self.writeByte(0x41,'P') 

    ## Selects eye tracking mode.
    #  @param self The object pointer. 
    def select_eye_tracking_mode(self):
        self.writeByte(0x41,'e')   

    ## Selects QRcode tracking mode.
    #  @param self The object pointer. 
    def select_QRcode_tracking_mode(self):
        self.writeByte(0x41,'Q')   

    ## Selects line tracking mode.
    #  @param self The object pointer. 
    def select_line_tracking_mode(self):
        self.writeByte(0x41,'L') 
    
    ## Locks tracing buffer.
    #  @param self The object pointer.
    def lock_tracing_buffer(self):
        self.writeByte(0x41,'J') 

    ## Unlocks tracing buffer.
    #  @param self The object pointer.  
    def unlock_tracing_buffer(self):
        self.writeByte(0x41,'K') 


    ## Counts visible objects.
    #  @param self The object pointer.
    def count_objects(self):
        self.select_object_tracking_mode()
        return self.readByte(self.count_obj_reg)

    ## Gets info for first object.
    #  @param self The object pointer.
    #  @param mode Sets the mode of tracing.
    def get_1st_object_info(self, mode = "object"): #mode: object, face, eye, line
        info = []
        if mode == "object":
            self.select_object_tracking_mode()
        elif mode == "face":
            self.select_face_tracking_mode()
        elif mode == "eye":
            self.select_eye_tracking_mode()
        elif mode == "line":
            self.select_line_tracking_mode()
        else:
            return("no valid mode selected")
        info.append(self.readByte(self.clr_1st_reg)) #TODO:Colors in bigger numbers. maybe readINT????
        info.append(self.readByte(self.x_up_left_1st_reg))
        info.append(self.readByte(self.y_up_left_1st_reg))
        info.append(self.readByte(self.x_lo_right_1st_reg))
        info.append(self.readByte(self.y_lo_right_1st_reg))
        return info 

    ## Gets info for all objects.
    #  @param self The object pointer.
    #  @param mode Sets the mode of tracing.
    def get_all_object_info(self, mode = "object"):
        info = []
        all_info = []

        if mode == "object":
            self.select_object_tracking_mode()
        elif mode == "face":
            self.select_face_tracking_mode()
        elif mode == "eye":
            self.select_eye_tracking_mode()
        elif mode == "line":
            self.select_line_tracking_mode()
        else:
            return("no valid mode selected")

        num_objects = self.count_objects()

        if num_objects > 0:
            info.append(self.readByte(self.clr_1st_reg)) 
            info.append(self.readByte(self.x_up_left_1st_reg))
            info.append(self.readByte(self.y_up_left_1st_reg))
            info.append(self.readByte(self.x_lo_right_1st_reg))
            info.append(self.readByte(self.y_lo_right_1st_reg))
            all_info.append(info)
            info = []

        if num_objects > 1:
            info.append(self.readByte(self.clr_2nd_reg)) 
            info.append(self.readByte(self.x_up_left_2nd_reg))
            info.append(self.readByte(self.y_up_left_2nd_reg))
            info.append(self.readByte(self.x_lo_right_2nd_reg))
            info.append(self.readByte(self.y_lo_right_2nd_reg))
            all_info.append(info)
            info = []

        if num_objects > 2:
            info.append(self.readByte(self.clr_3rd_reg))
            info.append(self.readByte(self.x_up_left_3rd_reg))
            info.append(self.readByte(self.y_up_left_3rd_reg))
            info.append(self.readByte(self.x_lo_right_3rd_reg))
            info.append(self.readByte(self.y_lo_right_3rd_reg))
            all_info.append(info)
            info = []

        if num_objects > 3:
            info.append(self.readByte(self.clr_4th_reg))
            info.append(self.readByte(self.x_up_left_4th_reg))
            info.append(self.readByte(self.y_up_left_4th_reg))
            info.append(self.readByte(self.x_lo_right_4th_reg))
            info.append(self.readByte(self.y_lo_right_4th_reg))
            all_info.append(info)
            info = []

        if num_objects > 4:
            info.append(self.readByte(self.clr_5th_reg)) 
            info.append(self.readByte(self.x_up_left_5th_reg))
            info.append(self.readByte(self.y_up_left_5th_reg))
            info.append(self.readByte(self.x_lo_right_5th_reg))
            info.append(self.readByte(self.y_lo_right_5th_reg))
            all_info.append(info)
            info = []

        if num_objects > 5:
            info.append(self.readByte(self.clr_6th_reg)) 
            info.append(self.readByte(self.x_up_left_6th_reg))
            info.append(self.readByte(self.y_up_left_6th_reg))
            info.append(self.readByte(self.x_lo_right_6th_reg))
            info.append(self.readByte(self.y_lo_right_6th_reg))
            all_info.append(info)
            info = []

        if num_objects > 6:
            info.append(self.readByte(self.clr_7th_reg)) 
            info.append(self.readByte(self.x_up_left_7th_reg))
            info.append(self.readByte(self.y_up_left_7th_reg))
            info.append(self.readByte(self.x_lo_right_7th_reg))
            info.append(self.readByte(self.y_lo_right_7th_reg))
            all_info.append(info)
            info = []
            
        if num_objects > 7:
            info.append(self.readByte(self.clr_8th_reg)) 
            info.append(self.readByte(self.x_up_left_8th_reg))
            info.append(self.readByte(self.y_up_left_8th_reg))
            info.append(self.readByte(self.x_lo_right_8th_reg))
            info.append(self.readByte(self.y_lo_right_8th_reg))
            all_info.append(info)

        return all_info 


## NXTMMX: this class provides functions for NXTMMX.
#  for read and write operations.
class NXTMMX(i2c):

    ## Command register
    command_reg = 0x41

    ## Motor 1 parameters
    ## Motor 1 encoder register
    m1_encoder_reg = 0x42 #0x42-0x45 (long)
    ## Motor 1 speed register
    m1_speed_reg = 0x46
    ## Motor 1 time register
    m1_time_reg = 0x47 #in sec
    ## Motor 1 command register B
    m1_command_reg_B = 0x48
    ## Motor 1 command register A
    m1_command_reg_A = 0x49

    ## Motor 2 parameters
    ## Motor 2 encoder register
    m2_encoder_reg = 0x4A #0x4A-0x4D (long)
    ## Motor 2 speed register
    m2_speed_reg = 0x4E
    ## Motor 2 time register
    m2_time_reg = 0x4F #in sec
    ## Motor 2 command register B
    m2_command_reg_B = 0x50
    ## Motor 2 command register A
    m2_command_reg_A = 0x51

    ## Motor read parameters
    ## Motor 1 read encoder register
    m1_read_encoder_reg = 0x62 #0x62-0x65 (long)
    ## Motor 2 read encoder register
    m2_read_encoder_reg = 0x66 #0x66-0x69 (long)
    ## Motor 1 read status register
    m1_read_status_reg  = 0x72
    ## Motor 2 read status register
    m2_read_status_reg  = 0x73
    ## Motor 1 read tasks register
    m1_read_tasks_reg   = 0x76
    ## Motor 2 read tasks register
    m2_read_tasks_reg   = 0x77

    ## advanced PID control registers
    ## kP encoder register
    kP_encoder_reg = 0x7A #0x7A-0x7B (int)
    ## kI encoder register
    kI_encoder_reg = 0x7C #0x7C-0x7D (int)
    ## kD encoder register
    kD_encoder_reg = 0x7E #0x7E-0x7F (int)

    ## kP speed register
    kP_speed_reg = 0x80 #0x80-0x81 (int)
    ## kI speed register
    kI_speed_reg = 0x82 #0x82-0x83 (int)
    ## kD speed register
    kD_speed_reg = 0x84 #0x84-0x85 (int)

    ## Pass count register
    pass_count_reg = 0x86
    ## Tolerance register
    tolerance_reg = 0x87
    ## Voltage register for EV3
    voltage_reg = 0x90

    ## Initialize the class with the i2c address of your NXTMMX.
    #  @param self The object pointer.
    #  @param port Port where NXTMMX is connected.
    #  @param i2c_address Address of your NXTMMX.
    def __init__(self, port, i2c_address = 0x06):
        i2c.__init__(self, port, i2c_address) 

    ## Changes i2c address of your LED Matrix.
    #  @param new_add Address to which user want to change.
    def change_address(self, new_add):
        self.writeByte(self.command_reg, (160).to_bytes(2, 'little'))
        self.writeByte(self.command_reg, (170).to_bytes(2, 'little'))
        self.writeByte(self.command_reg, (165).to_bytes(2, 'little'))
        self.writeByte(self.command_reg, new_add.to_bytes(2, 'little'))
        print("New address uploaded, please address this NXTMMX as:", hex(new_add))

    ## Motor 1 command register writer.
    #  @param self The object pointer.
    #  @param speed_control     Bool for speed control
    #  @param ramp              Bool for motor ramping
    #  @param relative_change   Bool for relative change
    #  @param encoder_control   Bool for encoder control
    #  @param brake_float       Bool for type of stoppage
    #  @param encoder_feedback  Bool for motor encoder feedback
    #  @param timed_control     Bool for motor timed control
    #  @param go                Bool to start the motor
    def m1_send(self, speed_control = 1, ramp = 0, relative_change = 0, encoder_control = 0, brake_float = 0, encoder_feedback = 0, timed_control = 0, go = 0):
        m1 = str(go)+str(timed_control)+str(encoder_feedback)+str(brake_float)+str(encoder_control)+str(relative_change)+str(ramp)+str(speed_control)            
        self.writeByte(self.m1_command_reg_A, int(m1, 2).to_bytes((len(m1) + 7) // 8, 'little'))

    ## Motor 2 command register writer.
    #  @param self The object pointer.
    #  @param speed_control     Bool for speed control
    #  @param ramp              Bool for motor ramping
    #  @param relative_change   Bool for relative change
    #  @param encoder_control   Bool for encoder control
    #  @param brake_float       Bool for type of stoppage
    #  @param encoder_feedback  Bool for motor encoder feedback
    #  @param timed_control     Bool for motor timed control
    #  @param go                Bool to start the motor
    def m2_send(self, speed_control = 1, ramp = 0, relative_change = 0, encoder_control = 0, brake_float = 0, encoder_feedback = 0, timed_control = 0, go = 0):
        m2 = str(go)+str(timed_control)+str(encoder_feedback)+str(brake_float)+str(encoder_control)+str(relative_change)+str(ramp)+str(speed_control)      
        self.writeByte(self.m2_command_reg_A, int(m2, 2).to_bytes((len(m2) + 7) // 8, 'little'))

    ## Motor 1 status register reader.
    #  @param self The object pointer.
    #  @param print_it Bool for detailed status register information
    def get_m1_status(self, print_it = 0):
        result = [eval(i) for i in list("{:08b}".format(self.readByte(self.m1_read_status_reg)))]
        if print_it == 1:
            print("--------------")
            text = ["Motor is stalled:","Motor is in timed mode:","Motor is overloaded:","Motor is in brake mode:","Positional Control is ON:","Motor is powered:","Motor is ramping:","Speed Control is ON:"]
            for i in range(len(result)):
                print(text[i]," ", result[i])
            print("--------------")
        return result 

    ## Motor 2 status register reader.
    #  @param self The object pointer.
    #  @param print_it Bool for detailed status register information
    def get_m2_status(self, print_it = 0):
        result = [eval(i) for i in list("{:08b}".format(self.readByte(self.m2_read_status_reg)))]
        if print_it == 1:
            print("--------------")
            text = ["Motor is stalled:","Motor is in timed mode:","Motor is overloaded:","Motor is in brake mode:","Positional Control is ON:","Motor is powered:","Motor is ramping:","Speed Control is ON:"]
            for i in range(len(result)):
                print(text[i]," ", result[i])
            print("--------------")
        return result 

    ## Resets all encoder values to 0.
    #  @param self The object pointer.
    def reset_all_encoders(self):
        self.writeByte(self.command_reg,'R')  

    ## Starts both motors at the same time.
    #  @param self The object pointer.
    def issue_command_to_both_motors(self): #synchronized starting
        self.writeByte(self.command_reg,'S')

    ## Returns voltage of NXTMMX in milivolts
    #  @param self The object pointer.
    def get_voltage(self): #in mV
        return self.readByte(self.command_reg)*37

    ## Returns speed of Motor 1.
    #  @param self The object pointer.
    def motor1_get_speed(self):
        return self.readByte(self.m1_speed_reg)
    
    ## Returns speed of Motor 2.
    #  @param self The object pointer.
    def motor2_get_speed(self):
        return self.readByte(self.m2_speed_reg)
    
    ## Returns angle of Motor 1.
    #  @param self The object pointer.
    def motor1_get_angle(self):
        return self.readLong(self.m1_read_encoder_reg)
    
    ## Returns angle of Motor 2.
    #  @param self The object pointer.
    def motor2_get_angle(self):
        return self.readLong(self.m2_read_encoder_reg)

    ## Resets angle of Motor 1.
    #  @param self The object pointer.
    def motor1_reset_angle(self):
        self.writeByte(self.command_reg,'r')
    
    ## Resets angle of Motor 2.
    #  @param self The object pointer.
    def motor2_reset_angle(self):
        self.writeByte(self.command_reg,'s')
    
    ## Resets angle of both Motors.
    #  @param self The object pointer.
    def motors_reset_angle(self):
        self.writeByte(self.command_reg,'r')
        self.writeByte(self.command_reg,'s')
    
    ## Puts Motor 1 to float mode.
    #  @param self The object pointer.
    def motor1_stop(self): #float
        self.writeByte(self.command_reg,'a')

    ## Puts Motor 2 to float mode.
    #  @param self The object pointer.
    def motor2_stop(self): #float
        self.writeByte(self.command_reg,'b')

    ## Puts both Motors to float mode.
    #  @param self The object pointer.
    def motors_stop(self): #float
        self.writeByte(self.command_reg,'c')
    
    ## Puts Motor 1 to break mode.
    #  @param self The object pointer.
    def motor1_brake(self):
        self.writeByte(self.command_reg,'A')
    
    ## Puts Motor 2 to break mode.
    #  @param self The object pointer.
    def motor2_brake(self):
        self.writeByte(self.command_reg,'B')

    ## Puts both Motors to break mode.
    #  @param self The object pointer.
    def motors_brake(self):
        self.writeByte(self.command_reg,'C')

    ## Starts unlimited run of Motor 1.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 1.
    def motor1_run(self, speed):
        self.writeByte(self.m1_speed_reg, speed.to_bytes(2, 'little'))
        self.m1_send(go = 1)
        
    ## Starts unlimited run of Motor 2.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 2.
    def motor2_run(self, speed):
        self.writeByte(self.m2_speed_reg, speed.to_bytes(2, 'little'))
        self.m2_send(go = 1)
    
    ## Starts unlimited run for both Motors.
    #  @param self The object pointer.
    #  @param speed_m1 The speed of the Motor 1.
    #  @param speed_m2 The speed of the Motor 2.
    def motors_tank_move(self, speed_m1, speed_m2): 
        self.writeByte(self.m1_speed_reg, speed_m1.to_bytes(2, 'little'))
        self.writeByte(self.m2_speed_reg, speed_m2.to_bytes(2, 'little'))
        self.issue_command_to_both_motors()

    def motors_steering_move(self, speed_m1, speed_m2): #TODO
        pass

    ## Starts timed run for Motor 1.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 1.
    #  @param run_time The time for which motor should run in seconds.
    #  @param wait Should the function wait for completion?
    def motor1_run_time(self, speed, run_time, wait = True):
        self.writeByte(self.m1_speed_reg, speed.to_bytes(2, 'little'))
        self.writeByte(self.m1_time_reg, run_time.to_bytes(2, 'little'))
        self.m1_send(timed_control = 1, go = 1)  
        if wait:
            while True:
                if self.get_m1_status()[1] == 0:
                    break     

    ## Starts timed run for Motor 2.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 2.
    #  @param run_time The time for which motor should run in seconds.
    #  @param wait Should the function wait for completion?
    def motor2_run_time(self, speed, run_time, wait = True):
        self.writeByte(self.m2_speed_reg, speed.to_bytes(2, 'little'))
        self.writeByte(self.m2_time_reg, run_time.to_bytes(2, 'little'))
        self.m2_send(timed_control = 1, go = 1)
        if wait:
            while True:
                if self.get_m2_status()[1] == 0:
                    break
    
    ## Starts encoder angled run for Motor 1.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 1.
    #  @param rotation_angle The angle for which should motor turn.
    #  @param wait Should the function wait for completion?
    def motor1_run_angle(self, speed, rotation_angle, wait = True): # negative speed doesn't change anything
        self.writeByte(self.m1_speed_reg, speed.to_bytes(2, 'little'))
        self.writeArray(self.m1_encoder_reg, ((rotation_angle + self.motor1_get_angle()) & 0xFFFFFFFF).to_bytes(4, 'little'))
        self.m1_send(encoder_control = 1, go = 1)
        if wait:
            while True:
                if self.get_m1_status()[4] == 0:
                    break

    ## Starts encoder angled run for Motor 2.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 2.
    #  @param rotation_angle The angle for which should motor turn.
    #  @param wait Should the function wait for completion?        
    def motor2_run_angle(self, speed, rotation_angle, wait = True): # negative speed doesn't change anything
        self.writeByte(self.m2_speed_reg, speed.to_bytes(2, 'little'))
        self.writeArray(self.m2_encoder_reg, ((rotation_angle + self.motor2_get_angle()) & 0xFFFFFFFF).to_bytes(4, 'little'))
        self.m2_send(encoder_control = 1, go = 1)
        if wait:
            while True:
                if self.get_m2_status()[4] == 0:
                    break

    ## Starts encoder angled full rotation run for Motor 1.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 1.
    #  @param rotation_count The of full rotations for which should motor turn.
    #  @param wait Should the function wait for completion?
    def motor1_run_rotation(self, speed, rotation_count, wait = True): # negative speed doesn't change anything
        self.writeByte(self.m1_speed_reg, speed.to_bytes(2, 'little'))
        self.writeArray(self.m1_encoder_reg, (((360 * rotation_count) + self.motor1_get_angle()) & 0xFFFFFFFF).to_bytes(4, 'little'))
        self.m1_send(encoder_control = 1, go = 1)
        if wait:
            while True:
                if self.get_m1_status()[4] == 0:
                    break

    ## Starts encoder angled full rotation run for Motor 2.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 2.
    #  @param rotation_count The of full rotations for which should motor turn.
    #  @param wait Should the function wait for completion?        
    def motor2_run_rotation(self, speed, rotation_count, wait = True): # negative speed doesn't change anything
        self.writeByte(self.m2_speed_reg, speed.to_bytes(2, 'little'))
        self.writeArray(self.m2_encoder_reg, (((360 * rotation_count) + self.motor2_get_angle()) & 0xFFFFFFFF).to_bytes(4, 'little'))
        self.m2_send(encoder_control = 1, go = 1)
        if wait:
            while True:
                if self.get_m2_status()[4] == 0:
                    break

    ## Starts absolute encoder angled run for Motor 1.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 1.
    #  @param target_angle The angle to which should motor turn.
    #  @param wait Should the function wait for completion?
    def motor1_run_target(self, speed, target_angle, wait = True): # negative speed doesn't change anything
        self.writeByte(self.m1_speed_reg, speed.to_bytes(2, 'little'))
        self.writeArray(self.m1_encoder_reg, ((target_angle) & 0xFFFFFFFF).to_bytes(4, 'little'))
        self.m1_send(encoder_control = 1, go = 1)
        if wait:
            while True:
                if self.get_m1_status()[4] == 0:
                    break
    
    ## Starts absolute encoder angled run for Motor 2.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 2.
    #  @param target_angle The angle to which should motor turn.
    #  @param wait Should the function wait for completion?
    def motor2_run_target(self, speed, target_angle, wait = True): # negative speed doesn't change anything
        self.writeByte(self.m2_speed_reg, speed.to_bytes(2, 'little'))
        self.writeArray(self.m2_encoder_reg, ((target_angle) & 0xFFFFFFFF).to_bytes(4, 'little'))
        self.m2_send(encoder_control = 1, go = 1)
        if wait:
            while True:
                if self.get_m2_status()[4] == 0:
                    break

    ## Starts Motor 1 untill the motor is stalled.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 1.
    #  @param threshold The threshold count on which the motor should stop.
    def motor1_run_until_stalled(self, speed, threshold = 30):
        self.writeByte(self.m1_speed_reg, speed.to_bytes(2, 'little'))
        self.m1_send(go = 1)
        overload = 0
        while True:
            if self.get_m1_status()[2] == 1:
                overload = overload + 1
                if overload > threshold:
                    self.motor1_brake()
                    print("Motor 1 overloaded!")
                    self.motor1_stop()
                    break
            else:
                overload = 0
    
    ## Starts Motor 2 untill the motor is stalled.
    #  @param self The object pointer.
    #  @param speed The speed of the Motor 2.
    #  @param threshold The threshold count on which the motor should stop.
    def motor2_run_until_stalled(self, speed, threshold = 30):
        self.writeByte(self.m2_speed_reg, speed.to_bytes(2, 'little'))
        self.m2_send(go = 1)
        overload = 0
        while True:
            if self.get_m2_status()[2] == 1:
                overload = overload + 1
                if overload > threshold:
                    self.motor2_brake()
                    print("Motor 2 overloaded!")
                    self.motor2_stop()
                    break
            else:
                overload = 0

    def motor1_dc(self, dc): #TODO advanced future
        pass
    
    def motor2_dc(self, dc): #TODO advanced future
        pass

    def motor1_track_target(self, target_angle): #TODO advanced future
        pass
    
    def motor2_track_target(self, target_angle): #TODO advanced future
        pass

    def motor1_control(self): #TODO advanced future
        pass
    
    def motor2_control(self):  #TODO advanced future
        pass