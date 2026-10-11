import ast

file_list= [("path_planner-6.log", 2048, "path_planner-6_output.txt"),
              ("local_costmap.txt", 40, "local_costmap_output.txt"),
              ("global_costmap.txt", 384, "global_costmap_output.txt")]

option = file_list[0]

map_file = option[0]
width = option[1]
out_file = option[2]

print("file option: ",option)
print("file: ", map_file)
print("width: ", width)

with open(map_file, "r") as f:
    line = f.readline().strip()

# Convert string to list
numbers = ast.literal_eval(line)

print(len(numbers))
print("length mod",width, len(numbers) % width)

# validation
if len(numbers) % width != 0:
    raise ValueError("Data length is not divisible by width")

# make 2D list
array_2d = [numbers[i:i+width] for i in range(0, len(numbers), width)]

with open("output/" + out_file, "w") as f:
    for row in array_2d:
        f.write(str(row) + "\n")