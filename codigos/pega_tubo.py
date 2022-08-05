#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank = MoveTank(OUTPUT_A, OUTPUT_B)
steering = MoveSteering(OUTPUT_A, OUTPUT_B)

spkr = Sound()
btn = Button()
radio = Radio()

us = UltrasonicSensor(INPUT_3)
us2 = UltrasonicSensor(INPUT_4)
us3 = UltrasonicSensor(INPUT_2)
gyro = GyroSensor(INPUT_5)
# ultrasonic_sensor_in7 = UltrasonicSensor(INPUT_7)


wheel_dim = 5.6
wheel_circ = 2 * math.pi * (wheel_dim / 2)
robot_dm = 15.2

velocidade_walk = 40
velocidade_turn = 20

robot_odo = robot_dm / wheel_dim

walk_kp = 2

def rotate(num):
    e = (num - gyro.angle) * walk_kp
    e = max(min(e, 100), -100)
    
    while e != 0:
        velocidade = min(e, 20)
        
        tank.on(velocidade, -velocidade)
        
        e = (num - gyro.angle) * walk_kp
        e = max(min(e, 100), -100)
    
    tank.stop()
    # aplicar kalman
    
    
def walk(dis_cm, direction, speed = 40):
    
    degrees = (dis_cm / wheel_circ) * 360
    target = left_motor.position + degrees
    # tank_drive.on_for_degrees(velocidade, velocidade, degrees)
    
    initial_pos = left_motor.position
    
    controle_velocidade = speed
    while left_motor.position <= target:
        e = (direction - gyro.angle) * walk_kp
        e = max(min(e, 100), -100)
        
        # derivada para a velocidade
        dist_from_target = target - left_motor.position
        dist_from_start = left_motor.position - initial_pos
        
        if(dist_from_target < 200):
            controle_velocidade = dist_from_target/200
            velocidade = max(speed * controle_velocidade, 10)
            
        elif (dist_from_start < 200):
            controle_velocidade = dist_from_start/200
            velocidade = max(speed * controle_velocidade, 10)
            
        else:
            velocidade = speed
        
        steering.on(e, velocidade)
    tank.stop()
    
def walk_until_us(distance, direction):
    wheel_circ = 2 * math.pi * (wheel_dim / 2)
    
    initial_pos = left_motor.position
    controle_velocidade = velocidade_walk
    
    
    while (us.distance_centimeters >= distance):
        e = (direction - gyro.angle) * walk_kp
        e = max(min(e, 100), -100)
        
        dist_from_start = left_motor.position - initial_pos
            
        if (dist_from_start < 200):
            controle_velocidade = dist_from_start/200
            velocidade = max(velocidade_walk * controle_velocidade, 10)
        else:
            velocidade = velocidade_walk
        
        steering.on(e, velocidade)
    tank.stop()
    
def walk_until_us2(distance, direction):
    wheel_circ = 2 * math.pi * (wheel_dim / 2)
    
    initial_pos = left_motor.position
    controle_velocidade = velocidade_walk
    
    
    while (us2.distance_centimeters >= distance):
        e = (direction - gyro.angle) * walk_kp
        e = max(min(e, 100), -100)
        
        dist_from_start = left_motor.position - initial_pos
            
        if (dist_from_start < 200):
            controle_velocidade = dist_from_start/200
            velocidade = max(velocidade_walk * controle_velocidade, 10)
        else:
            velocidade = velocidade_walk
        
        steering.on(e, velocidade)
    tank.stop()
    
def walk_until_us_less(distance, direction):
    wheel_circ = 2 * math.pi * (wheel_dim / 2)
    
    initial_pos = left_motor.position
    controle_velocidade = velocidade_walk
    
    
    while (us.distance_centimeters <= distance):
        e = (direction - gyro.angle) * walk_kp
        e = max(min(e, 100), -100)
        
        dist_from_start = left_motor.position - initial_pos
            
        if (dist_from_start < 200):
            controle_velocidade = dist_from_start/200
            velocidade = max(velocidade_walk * controle_velocidade, 10)
        else:
            velocidade = velocidade_walk
        
        steering.on(e, velocidade)
    tank.stop()
    

walk_until_us(100, 0)
a = left_motor.position
print(a)
walk_until_us_less(100, 0)
b = left_motor.position
print(b)

volta = b - a

print(volta)
volta_cm = (volta/360) * wheel_circ
print("Cm:", volta_cm)

rotate(180)

walk_until_us2(100, 180)

walk(volta_cm/2, 180)

rotate(270)

a = us3.distance_centimeters
walk(a-2, 270)
    
    
    
    
    
