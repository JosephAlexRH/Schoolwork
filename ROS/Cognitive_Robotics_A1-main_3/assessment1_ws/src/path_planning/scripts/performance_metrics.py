#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
import os.path

results_dict = {}
latest_goal = 0

filename = "results.txt"
path = os.path.join("~", filename) # will currently write to root

GOAL_THRESHOLD = 0.15

# Class that listens to the /odom topic and compares the recieved messages with the goals it is given on init
class Odom_Listener():
    def __init__(self, goal_list):
        rospy.Subscriber("/odom", Odometry, self.odom_callback)
        self.goal_list = goal_list    
        self.current_goal = self.goal_list.pop(0)
        
# Callback that recieves data from the /move_base/result topic. Writes to the dictionary if the navigation was a success or failure.
    def odom_callback(self, msg):
        if self.current_goal is None:
            return

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        dist = ((x - self.current_goal[0])**2 + (y - self.current_goal[1])**2) ** 0.5

        if dist < GOAL_THRESHOLD:
            travel_end = rospy.Time.now()
            record_result(self.current_goal_idx, "Travel time end", travel_end)

            # Compute and print travel time if start was recorded
            goal_data = results_dict.get(self.current_goal_idx, {})
            travel_start = goal_data.get("Travel time start")
            if travel_start and travel_start != "DNF":
                travel_secs = (travel_end - travel_start).to_sec()
                record_result(self.current_goal_idx, "Travel time (s)", round(travel_secs, 3))

            print_summary(self.current_goal_idx)

            # Move to next goal
            self.current_goal_idx += 1
            if self.current_goal_idx < len(self.goal_list):
                self.current_goal = self.goal_list[self.current_goal_idx]
            else:
                self.current_goal = None
                rospy.loginfo("All goals reached!")


# Subscribes our node to the /move_base/result topic.
def launch_listener(goal_list):
    Odom_Listener(goal_list)
    
    
# Adds given results to a dictionary
def record_result(goal, name, value):
    global latest_goal
    
    results_dict.setdefault(goal, {})[name] = value
    
    # TODO: remove this when we get to path_planning 
    write_results(f"Goal {goal} | {name}: {value}")
    
    latest_goal = goal # latest goal so the move_base_callback function knows which goal its recieved msg was for.
def print_summary(goal_idx):
    """Prints a clean summary of metrics for a completed goal."""
    data = results_dict.get(goal_idx, {})

    exec_start = data.get("Execution time start")
    exec_end   = data.get("Execution time end")
    path_len   = data.get("Path length")
    travel_s   = data.get("Travel time (s)", "pending")

    # Compute execution time
    if exec_start and exec_end and exec_end != "DNF":
        exec_secs = (exec_end - exec_start).to_sec()
    else:
        exec_secs = "DNF"

    summary = (
        f"\noal {goal_idx} Summary\n"
        f"  Path length (cells) : {path_len}\n"
        f"  Execution time (s)  : {round(exec_secs, 3) if isinstance(exec_secs, float) else exec_secs}\n"
        f"  Travel time (s)     : {travel_s}\n"
        f"=========================================\n"
    )

    rospy.loginfo(summary)
    write_results(summary)

def write_results(input):
    with open(os.path.expanduser(path), "a+") as f:
        f.write(input+"\n")
        f.close()
        
        
def read_results():
    with open("results.txt", "r") as f:
        print(f.read())
        

    