import rospy
from autoware_msgs.msg import DetectedObjectArray, DetectedObject
import logging as log
import pickle

# Example incomplete structure to store information collected from AW MINI
simout = {
    "times" : {},
    "location" : {
    },
    "velocity" : {
    },
    "types" : {}
}

objects_store = []

def process(msg):
    for obj in msg.objects:
        objects_store.append(obj)

        timestamp = obj.header.stamp.secs + obj.header.stamp.nsecs/10**9

        id = obj.id
        label = obj.label
        location = (obj.pose.position.x, obj.pose.position.y)
        velocity = obj.velocity.linear.x, obj.velocity.linear.y, obj.velocity.linear.z

        # add 
        if len(simout["times"]) == 0:
            simout["times"] = [timestamp]
        else:
            if timestamp not in simout["times"]:
                simout["times"].append(timestamp)

        if label not in simout["types"]:
            simout["types"][label] = [id]
        else:
            if id not in simout["types"][label]:
                simout["types"][label].append(id)

        if id not in simout["location"]:
            simout["location"][id] = [location]
        else:
            simout["location"][id].append(location)
        
        if id not in simout["velocity"]:
            simout["velocity"][id] = [velocity]
        else:
            simout["velocity"][id].append(velocity)

        # TODO Read remaining attributes
        with open(f"detected_object_template_{id}.pkl", "wb") as pkl_file:
            pickle.dump(obj, pkl_file)
                
# Some example time for reading
sim_time = 2

rospy.init_node('subscriber')
rospy.Subscriber("/detection/final_objects", DetectedObjectArray, process)
rospy.sleep(sim_time)

############# output 
print(simout)
