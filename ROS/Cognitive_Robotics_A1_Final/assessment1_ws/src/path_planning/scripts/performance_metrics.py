#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
import os.path

results_dict = {}
latest_goal = 0

import helper_functions as helper

filename = "base_results.txt"
path = os.path.join("~", filename) # will currently write to root

# Class that listens to the /odom topic and compares the recieved messages with the goals it is given on init
class Odom_Listener():
    def __init__(self, goal_dict):
        rospy.Subscriber("/odom", Odometry, self.odom_callback)
        self.goal_dict = goal_dict    
        self.current_goal = self.goal_dict[1]
        
        self.current_goal_idx = 0
        
    # Callback that recieves data from the /odom topic. Writes to the dictionary if the goal is less then .3 metres from the recieved odom value
    def odom_callback(self, msg):
        pose = msg.pose.pose.position
        
        dist_from_goal = helper.straight_distance((pose.x, pose.y), (self.current_goal[0], self.current_goal[1]))
        
        if dist_from_goal < 0.25:
            record_result(self.current_goal_idx, "Travel time end", rospy.Time.now())
            self.current_goal_idx = self.current_goal_idx +1
            self.current_goal = self.goal_dict[self.current_goal_idx]
            write_results(f"Goal {self.current_goal_idx}: Travel time end - {rospy.Time.now()}")


# Subscribes our node to the /move_base/result topic.
def launch_listener(goal_dict):
    Odom_Listener(goal_dict)
    
    
# Adds given results to a dictionary
def record_result(goal, name, value):
    global latest_goal
    global results_dict
    
    new_dict = {}
    new_dict[name] = value
    results_dict[goal] = new_dict
    write_results(f"Goal {goal}: {name} - {value}")
    
    latest_goal = goal # latest goal so the move_base_callback function knows which goal its recieved msg was for.


def write_results(inp):
    with open(os.path.expanduser(path), "a+") as f:
        f.write(inp)
        f.close()
        

def read_results():
    with open("results.txt", "r") as f:
        print(f.read())

# loop through and format the dictionary for the txt file
def format_dict():
    global results_dict
    out_string = ""
    for k, v in sorted(results_dict.items()):
        out_string += f"\n--\nGoal {k}\n"
        for key, val in sorted(v.items()):
            out_string +f"{key}: {val}\n--\n"
    return out_string
    