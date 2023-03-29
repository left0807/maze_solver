from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import random
from collections import deque
import os
import time

height = 15
width = 15
curdeg = 0
edge = [[1 for range(width)] for range(height)]

left = DistanceSensor('C')
right = DistanceSensor('D')
front = DistanceSensor('E')
motor_pair = MotorPair('A', 'B')

def turn(left):
    hub.motion_sensor.reset_yaw_angle()
    if left:
        while -89 < hub.motion_sensor.get_yaw_angle():
            motor_pair.start(-95, 50)
    else:
        while 89 > hub.motion_sensor.get_yaw_angle():
            motor_pair.start(95, 50)

    motor_pair.stop()
    if left: curdeg+=1
    else: curdeg -= 1;

    if(curdeg == -1): curdeg = 3
    if(curdeg == 4): curdeg = 0


def neighbour(pos):
    ava = []
    x, y = pos;

    if cur == 0:
        if front.get_distance_cm() < 10: ava.append((x+1, y))
        if left.get_distance_cm() < 10: ava.append((x, y+1))
        if right.get_distance_cm() < 10: ava.append((x, y-1))
    elif cur = 1:
        if front.get_distance_cm() < 10: ava.append((x, y+1))
        if left.get_distance_cm() < 10: ava.append((x-1, y))
        if right.get_distance_cm() < 10: ava.append((x+1, y))
    elif cur == 2:
        if front.get_distance_cm() < 10: ava.append((x-1, y))
        if left.get_distance_cm() < 10: ava.append((x, y-1))
        if right.get_distance_cm() < 10: ava.append((x, y+1))
    else:
        if front.get_distance_cm() < 10: ava.append((x, y-1))
        if left.get_distance_cm() < 10: ava.append((x+1, y))
        if right.get_distance_cm() < 10: ava.append((x-1, y))

    return ava

def dfs_solve(start, end):
    stack = [start]
    visited = set()
    prex, prey = start;

    while stack:
        move((prex, prey), stack[-1])

        visited.insert(stack[-1])
        y, x = stack.pop()

        if((y,x) == end):
            print("Done!")
            return None;
        
        found = False
        for dy, dx in neighbour((y, x)):
            if (dx, dy) is not in visited:
                stack.append((dy, dx))
                found = True
        
        if not found:
            move((x,y), (prex, prey))

        prex=x
        prey=y

    return None

# Call the BFS algorithm to find the shortest path

hub.motion_sensor.reset_yaw_angle()

dfs_solve((0, 0), (height-1, width-1))
turn(90)
