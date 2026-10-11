import rospy

def write_results(input):
    with open("results.txt", "a") as f:
        f.write(input+"\n")
        
        
def read_results():
    with open("results.txt", "r") as f:
        print(f.read())