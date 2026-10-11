#!/usr/bin/env python3
import rospy
import math

def idx_to_xy(i, width):
    return (i % width, i // width)

def xy_to_idx(x, y, width):
    return y * width + x

def convert_1d_to_2d(costmap, width):
    """
    takes a 1D array and a width and returns a 2D representation of the array
    """
    array_2d = [costmap[i:i+width] for i in range(0, len(costmap), width)]
    return array_2d

def convert_2d_to_world(x,y, origin, resolution):
    world_x = origin[0] + x * resolution
    world_y = origin[1] + y * resolution
    return world_x, world_y

def straight_distance(start_xy, goal_xy):
    return math.sqrt((start_xy[0] - goal_xy[0])**2 + (start_xy[1] - goal_xy[1])**2)
