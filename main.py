#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import struct

# Declare motors 
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
weapon = Motor(Port.A)
cs = ColorSensor(Port.S1)
# ir = InfraredSensor(Port.S1)

# brick.display.image('untitled.png')

robot = DriveBase(left_motor, right_motor, 43.2, 114)
# Initialize variables. 
# Assuming sticks are in the middle when starting.
right_stick_x = 124
right_stick_y = 124

# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
 
    val: float or int
    src: tuple
    dst: tuple
 
    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


infile_path = "/dev/input/event4"

# open file in binary mode
in_file = open(infile_path, "rb")

# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)
line_follower = False
invert = 1



while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    if ev_type == 3 and code == 0:
        right_stick_x = value
    if ev_type == 3 and code == 1:
        right_stick_y = value
    if ev_type == 1 and code == 307 and value ==1:
        weapon.run_angle(100,30, Stop.COAST,False)
    if ev_type == 1 and code == 308 and value ==1:
        weapon.run_time(720,5000, Stop.COAST,False)
    if ev_type == 1 and code == 305 and value == 1:
        invert = invert*-1
    if ev_type == 1 and code == 304 and value == 1:
        while(True):
            print(cs.color())
            if cs.color() == None:
                next
            elif cs.color() > 2:
                robot.drive_time(50, 80, 300)
            else:
                robot.drive_time(50,-30,300)
            if Button.LEFT in brick.buttons():
                break

    # Scale stick positions to -100,100
    forward = scale(right_stick_y, (0,255), (200,-200))*invert
    left = scale(right_stick_x, (0,255), (200,-200))

    # Set motor voltages. If we're steering left, the left motor
    # must run backwards so it has a -left component
    # It has a forward component for going forward too. 
    left_motor.dc(forward - left)
    right_motor.dc(forward + left)

    # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()
