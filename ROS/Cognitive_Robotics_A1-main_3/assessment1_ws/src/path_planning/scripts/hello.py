h = calculate_heuristic(neighbor_index, goal, width)
f = tentative_g + h
heapq.heappush(open_heap, (f, neighbor_index))

#Heuristic function
f(n) = g(n) + h(n)


rotation = math.atan2(cross, dot)
rotation_cost = rotation_weight * abs(rotation)

time_trans = distance / vel_trans
time_rot = abs(theta) / vel_rot
time_cost = weight * (time_trans + time_rot)