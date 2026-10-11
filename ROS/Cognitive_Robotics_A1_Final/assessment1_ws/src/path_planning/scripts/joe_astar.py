#!/usr/bin/env python

import rospy
import math
from algorithms.neighbors import find_neighbors
import heapq
from typing import Dict, List
import gridviz

#Helper functions

def index_to_cor(i, width):
    """convert 1d array to x,y grid coordinates
    :param i: index in array
    :param width: num of colomuns in grid
    :returns: x: horizontal pos,
              Y: vertical pos"""
    x = i % width
    y= i // width
    return x, y

def calculate_heuristic(pos1_idx, pos2_idx, width):
    """Calculate euclidian distance between two points stored as indices
    :param pos1_idx: index of first node
    :param pos2_idx:index of second node
    :param width: number of columns in grid
    :return: return straight line distance as float
    """
    x1, y1 = index_to_cor(pos1_idx, width)
    x2, y2 = index_to_cor(pos2_idx, width)
    return math.hypot(x2-x1, y2 - y1)

def reconstruct_path(came_from:Dict[int, int], start, goal):
    """Rebuild final path after A* finishes route
    :paran came_from: list of nodes representing total path
    :param start: index of starting node
    :param goal: index of goal """
    #if goal is never added to came_from, goal is unreachable
    if goal not in came_from and goal!= start:
        return []

    #initialize path
    path = [goal]
    current = goal
    # walk backwards through aoth and append to path
    while current !=start:
        current=came_from[current]
        path.append(current)

    #return inverse of path
    return path[::-1]

def a_star(start, goal, width, height, costmap, resolution, origin, grid_visualisation):

    open_heap = [] #holds discovered nodes, each entry is in the format (f_cost, node index)
    orthogonal_step_cost = 1.0 #baseline movement

    #push start node onto heap
    start_h = calculate_heuristic(start, goal, width)
    heapq.heappush(open_heap, (start_h, start))

    came_from:Dict[int, int]={} #store parent pointers
    g_cost:Dict [int, float] = {start:0.0} #store best known cost to reach each node

    closed_set = set() #explored nodes

    #Main body
    while open_heap:
        f_curr, current = heapq.heappop(open_heap) #select node with smallest total cost(f)

        #verify if popped f-cost is best currently known g, stops expanding outdated entries for smae node
        if f_curr> g_cost.get(current, float('inf'))+ calculate_heuristic(current, goal, width):
            continue


        #verify same node cant be expanded twice
        if current in closed_set:
            continue
        closed_set.add(current)

        if grid_visualisation:
            grid_visualisation.set_color(current, "orange")

        #goal test
        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            if grid_visualisation:
                for p in path:
                grid_visualisation.set_color(p, "pale yellow")
            return path

        neighbors = find_neighbors(current, width, height,costmap, orthogonal_step_cost)

        for neighbor_index, step_cost in neighbors:
            if neighbor_index in closed_set: #skip closed nodes
                continue
            tentative_g = g_cost[current] + step_cost #Cost to reach neighbour via current

            #Update neighbor if neighbor is unknown or theres a cheaper path to oit
            if(neighbor_index not in g_cost or tentative_g< g_cost[neighbor_index]):

                #update parent and costs to new best-known
                came_from[neighbor_index]= current
                g_cost[neighbor_index]= tentative_g

                #Compute f = g + h and push onto heap
                h = calculate_heuristic(neighbor_index, goal, width)
                f = tentative_g + h

                heapq.heappush(open_heap,(f, neighbor_index))
                if grid_visualisation:
                    grid_visualisation.set_color(neighbor_index, "lime_green")

    return []
