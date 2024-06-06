#!/usr/bin/env python
# license removed for brevity
import rospy
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import numpy as np

# Global variable to store the latest LiDAR data
lidar_data = None

def callback(msg):
    global lidar_data 
    points_list = []

    for point in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True):
        points_list.append([point[0], point[1], point[2]])
        print("x, y, z: " , point[0] ," ",  point[1]," ", point[2])

    lidar_data = np.array(points_list)

def listener():
    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber("/mid/points", PointCloud2, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
