#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

brick.sound.beep()

left = Motor(Port.B)
right = Motor(Port.C)
robot = DriveBase(left, right, 43.2, 114)
sensor = InfraredSensor(Port.S1)
while(True):
    robot.drive(200, 0)
    if(sensor.distance()<10):
        robot.drive_time(-200,0, 2000)
        robot.drive_time(200, 90, 1000) 
        wait(1000)
        