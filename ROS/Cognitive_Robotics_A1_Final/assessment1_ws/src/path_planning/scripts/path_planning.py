#!/usr/bin/env python3

import rospy
import ethan_astar
from pp_msgs.srv import PathPlanningPlugin, PathPlanningPluginResponse
from geometry_msgs.msg import Twist
from gridviz import GridViz
import performance_metrics
import helper_functions as helper



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
  origin = [-0.600000, -6.700000, 00.000000] #hint: find this in your YAML map file

  grid_visualisation = GridViz(costmap, resolution, origin, start, goal, width)

  WAYPOINTS = [
               2501,
               10337, 
               2397, 
               12817
              ]

  entire_path = []
  segment_start = start
  goal_dict = {1: 0, 2: 0, 3: 0, 4: 0}
 
 # convert each goal waypoint to world coords so we can compare it with the odom 
  for num, waypoint in enumerate(WAYPOINTS):
    (x,y) = helper.idx_to_xy(waypoint, width)
    world_coord = helper.convert_2d_to_world(x, y, origin, resolution)
    goal_dict[num+1] = world_coord
  
  performance_metrics.launch_listener(goal_dict)
  
  # calculate the shortest path
  for num, waypoint in enumerate(WAYPOINTS):
    performance_metrics.write_results(f"Goal{num+1}: Execution time start - {rospy.Time.now()}\n")
    
    # Call A* algorithm
    path = ethan_astar.a_star_smoothed(segment_start, waypoint, width, height, costmap, resolution, origin, grid_visualisation)

    if not path:
      rospy.logwarn("No path returned by the path algorithm")
      path = []
      
      # Record results to the performance_metrics script
      performance_metrics.write_results(f"Goal {num+1}: Execution time end - DNF\n")
      performance_metrics.write_results(f"Goal {num+1}: Path length - DNF\n")
      
    else:
      rospy.loginfo('Path segment sent to navigation stack.')
      
      # Record results to the performance_metrics script
      performance_metrics.write_results(f"Goal{num+1}: Execution time end - {rospy.Time.now()}\n")
      performance_metrics.write_results(f"Goal{num+1}: Path length - {len(path)}\n")
      performance_metrics.write_results(f"Goal {num+1}: Travel time start - {rospy.Time.now()}\n")
      

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
