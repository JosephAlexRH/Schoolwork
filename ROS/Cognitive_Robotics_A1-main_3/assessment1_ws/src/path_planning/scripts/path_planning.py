#!/usr/bin/env python3

import rospy
import ethan_astar
from pp_msgs.srv import PathPlanningPlugin, PathPlanningPluginResponse
from geometry_msgs.msg import Twist
from gridviz import GridViz
import performance_metrics
import helper_functions as helper


# def make_plan(req):
#   ''' 
#   Callback function used by the service server to process
#   requests from clients. It returns a msg of type PathPlanningPluginResponse
#   ''' 
#   costmap = req.costmap_ros
#   # number of columns in the occupancy grid
#   width = req.width
#   # number of rows in the occupancy grid
#   height = req.height
#   start = req.start
#   goal = req.goal
#   # side of each grid map square in meters
#   resolution = 0.05
#   # origin of grid map
#   origin = [-0.600000, -6.700000, 90.000000] #hint: find this in your YAML map file

#   rospy.loginfo("goal: %g", goal)

#   grid_visualisation = GridViz(costmap, resolution, origin, start, goal, width)

#   # time statistics
#   start_time = rospy.Time.now()

#   # calculate the shortest path

#   path = ethan_astar.a_star_smoothed(start, goal, width, height, costmap, resolution, origin, grid_visualisation)


#   if not path:
#     rospy.logwarn("No path returned by the path algorithm")
#     path = []
#   else:
#     # additional code here as per your implementation, e.g., computing/displaying your performance metrics
#     rospy.loginfo('Path sent to navigation stack')

#   resp = PathPlanningPluginResponse()
#   resp.plan = path
#   return resp

def make_plan(req):
  rospy.loginfo("make plan called")
  ''' 
  Callback function used by the service server to process
  requests from clients. It returns a msg of type PathPlanningPluginResponse
  ''' 
  costmap = req.costmap_ros
  # number of columns in the occupancy grid
  width = req.width
  # number of rows in the occupancy grid
  height = req.height
  start = req.start
  goal = req.goal
  # side of each grid map square in meters
  resolution = 0.05
  # origin of grid map
  origin = [-0.600000, -6.700000, 90.000000] #hint: find this in your YAML map file

  grid_visualisation = GridViz(costmap, resolution, origin, start, goal, width)

  WAYPOINTS = [20521]

  entire_path = []
  segment_start = start
  goal_list = []
 
 # convert each goal waypoint to world coords so we can compare it with the odom 
  for waypoint in WAYPOINTS:
    (x,y) = helper.idx_to_xy(waypoint, width)
    (world_x, world_y) = helper.convert_2d_to_world(x, y, origin, resolution)
    goal_list.append((world_x, world_y))
  
  performance_metrics.launch_listener(goal_list)
  
  # calculate the shortest path
  for num, waypoint in enumerate(WAYPOINTS):
    rospy.loginfo(f"Planning: {segment_start} -> {waypoint}")
    rospy.loginfo(f"Start cost: {costmap[segment_start]}")
    rospy.loginfo(f"Goal cost: {costmap[waypoint]}")
    
    performance_metrics.record_result(num, "Execution time start", rospy.Time.now())
    
    # Call A* algorithm
    path = ethan_astar.a_star_smoothed(segment_start, waypoint, width, height, costmap, resolution, origin, grid_visualisation)

    if not path:
      rospy.logwarn("No path returned by the path algorithm")
      path = []
      
      # Record results to the performance_metrics script
      performance_metrics.record_result(num, "Execution time end", "DNF")
      performance_metrics.record_result(num, "Path length", "DNF")
      performance_metrics.record_result(num, "Travel time start", "DNF")
      performance_metrics.print_summary(num)
      
    else:
      rospy.loginfo('Path segment sent to navigation stack.')
      
      # Record results to the performance_metrics script
      performance_metrics.record_result(num, "Execution time end", rospy.Time.now())
      performance_metrics.record_result(num, "Path length", len(path))
      performance_metrics.record_result(num, "Travel time start", rospy.Time.now())
      performance_metrics.print_summary(num)

      # add to full path
      entire_path.extend(path)
      segment_start = waypoint
      
  resp = PathPlanningPluginResponse()
  resp.plan = entire_path
  return resp

def clean_shutdown():
  cmd_vel.publish(Twist())
  rospy.sleep(1)

if __name__ == '__main__':
  rospy.init_node('path_planning_server', log_level=rospy.INFO, anonymous=False)
  make_plan_service = rospy.Service("/move_base/SrvClientPlugin/make_plan", PathPlanningPlugin, make_plan)
  cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
  rospy.on_shutdown(clean_shutdown)

  while not rospy.core.is_shutdown():
    rospy.rostime.wallsleep(0.5)
  rospy.Timer(rospy.Duration(2), rospy.signal_shutdown('Shutting down'), oneshot=True)