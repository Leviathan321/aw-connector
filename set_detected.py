# sets static detected object
import time
import rospy
from std_msgs.msg import String
from autoware_msgs.msg import DetectedObjectArray, DetectedObject
import pickle

# Initialize the ROS node
rospy.init_node('example_publisher')

# Create a publisher on the desired topic
publisher = rospy.Publisher('/detection/final_objects', DetectedObjectArray, queue_size=10)

with open("detected_object_template_0.pkl", "rb") as pkl_file:
    detected_object = pickle.load(pkl_file)

# update position
j = 0
start_time =  rospy.Time.now() 
while rospy.Time.now() - start_time < rospy.Duration(4):  # Publish for 4 seconds
    for i in range(0,3):
        detected_object.id = i
        detected_object.label = "pedestrian"
        detected_object.pose.position.x = detected_object.pose.position.x + 9 + i
        detected_object.pose.position.y = detected_object.pose.position.y + 2*j

        detected_objects_array = DetectedObjectArray()
        detected_objects_array.objects.append(detected_object)

        # Set the header for the array message
        detected_objects_array.header.stamp = rospy.Time.now()  # Current time
        detected_objects_array.header.frame_id = "map"  # The coordinate frame for th

    publisher.publish(detected_objects_array)
    rospy.sleep(0.1)  # 10 Hz

    j = j+1
# sets moving detected object