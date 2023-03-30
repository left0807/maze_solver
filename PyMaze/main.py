from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import random
from collections import deque
import os
import time

# # # # #
# # # # #
# # # # #
# # # # #
# # # # #
# # # # #


# left = DistanceSensor('C')
# right = DistanceSensor('D')
# front = DistanceSensor('E')
# motor_pair = MotorPair('A', 'B')

# def turn(left):
#     hub.motion_sensor.reset_yaw_angle()
#     if left:
#         while -89 < hub.motion_sensor.get_yaw_angle():
#             motor_pair.start(-95, 50)
#     else:
#         while 89 > hub.motion_sensor.get_yaw_angle():
#             motor_pair.start(95, 50)

#     motor_pair.stop()
#     if left: curdeg+=1
#     else: curdeg -= 1;

#     if(curdeg == -1): curdeg = 3
#     if(curdeg == 4): curdeg = 0


# def neighbour(pos):
#     neighbour = []
#     x, y = pos;

#     if cur == 0:
#         if front.get_distance_cm() < 10: neighbour.append((x+1, y))
#         if left.get_distance_cm() < 10: neighbour.append((x, y+1))
#         if right.get_distance_cm() < 10: neighbour.append((x, y-1))
#     elif cur = 1:
#         if front.get_distance_cm() < 10: neighbour.append((x, y+1))
#         if left.get_distance_cm() < 10: neighbour.append((x-1, y))
#         if right.get_distance_cm() < 10: neighbour.append((x+1, y))
#     elif cur == 2:
#         if front.get_distance_cm() < 10: neighbour.append((x-1, y))
#         if left.get_distance_cm() < 10: neighbour.append((x, y-1))
#         if right.get_distance_cm() < 10: neighbour.append((x, y+1))
#     else:
#         if front.get_distance_cm() < 10: neighbour.append((x, y-1))
#         if left.get_distance_cm() < 10: neighbour.append((x+1, y))
#         if right.get_distance_cm() < 10: neighbour.append((x-1, y))

#     return neighbour

direction = 0
width = 20
height = 20
maze = [ ['#' for i in range(width)] for j in range(height)]

# left = DistanceSensor('C')
# right = DistanceSensor('D')
# front = DistanceSensor('E')
# motor_pair = MotorPair('A', 'B')
def print_maze():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(*[" ".join(row) for row in maze], sep="\n")
    time.sleep(0.05)

def turn(left):
    # hub.motion_sensor.reset_yaw_angle()
    # if left:
    #     while -89 < hub.motion_sensor.get_yaw_angle():
    #         motor_pair.start(-95, 50)
    # else:
    #     while 89 > hub.motion_sensor.get_yaw_angle():
    #         motor_pair.start(95, 50)

    # motor_pair.stop()
    if left: direction += 1
    else: direction -= 1

    if direction < 0: direction += 4
    if direction >= 4: direction -= 4;


def neighbours(pos):
    x, y = pos;
    ava = []
    neighbour = [(x, y+1), (x-1, y), (x, y-1), (x+1, y)]
    neighbour = neighbour[direction:] + neighbour[:direction]

    for dx, dy in [1, 0], [0, 1], [-1, 0], [0, -1]:
        if not maze[x+dx][y+dy] == '#':
            ava.append([x+dx, y+dy]);
    # for lego
    # if front.get_distance_cm() < 10: ava.append(neighbour[0])
    # if left.get_distance_cm() < 10: ava.append(neighbour[1])
    # if right.get_distance_cm() < 10: ava.append(neighbour[2])

    return ava

def move(cur, target):
    maze[cur[0]][cur[1]] = '.'
    maze[target[0]][target[1]] = '@'


def dfs_build():
    stack = [(1, 1)]

    while stack:
        x, y = stack[-1]
        maze[x][y] = '.'
        # Create list of unvisited neighbors
        neighbors = []
        if x > 2 and maze[x-2][y] == '#':
            neighbors.append((x-2, y))
        if y > 2 and maze[x][y-2] == '#':
            neighbors.append((x, y-2))
        if x < width-3 and maze[x+2][y] == '#':
            neighbors.append((x+2, y))
        if y < height-3 and maze[x][y+2] == '#':
            neighbors.append((x, y+2))

        if neighbors:
            nx, ny = random.choice(neighbors)
            mx, my = (x+nx)//2, (y+ny)//2
            maze[mx][my] = '.'  # Mark wall between current and next cell as empty
            stack.append((nx, ny))  # Add next cell to stack
        else:
            stack.pop()  # Backtrack if no unvisited neighbors


visited = set()

def dfs_solve(start, end, path):
    if start == end: 
        return path
    
    if tuple(start) in visited:
        return []
    
    visited.add(tuple(start))
    for neighbour in neighbours(start):
        if tuple(neighbour) in visited : continue
        move(start, neighbour)
        print_maze()
        if not dfs_solve(neighbour, end, path+start) == []: 
            return path
        move(neighbour, start)
        print_maze()

    return []


dfs_build()
for i in range(width):
    maze[0][i] = maze[height-1][i] = '#'
for i in range(height):
    maze[i][0] = maze[i][width-1] = '#'

dfs_solve([1, 1], [width-1, height-1], [])
