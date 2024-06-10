#!/usr/bin/env python
# license removed for brevity

import rospy
from sensor_msgs.msg import PointCloud2 , PointField
import sensor_msgs.point_cloud2 as pc2
import numpy as np
import time
import socket
previous_time = time.time() 

# Global variable to store the latest LiDAR data
lidar_data = None
txt=""
count = 0
def pointcloud2_to_array(cloud_msg):
    # Helper function to convert PointCloud2 message to numpy array
    dtype_list = []
    for field in cloud_msg.fields:
        if field.datatype == PointField.FLOAT32:
            dtype_list.append((field.name, np.float32))
        elif field.datatype == PointField.UINT16:
            dtype_list.append((field.name, np.uint16))
        # Add other field data types if needed
    # Create numpy array from the point cloud data
    cloud_arr = np.frombuffer(cloud_msg.data, dtype=np.dtype(dtype_list))
    # cloud_arr = np.array(cloud_arr)
    x = cloud_arr['x']
    y = cloud_arr['y']
    z = cloud_arr['z']
    intensity = cloud_arr['intensity']
    ring = cloud_arr['ring']
    time = cloud_arr['time']    
    # Stack columns to form an (n, 6) array
    points_array = np.column_stack((x, y, z, intensity, ring, time))    
    return points_array 
def send_data(lidar):
    filepath = "/home/admin2/ros-tcp-unity/src/unity_robotics_demo/scripts/data/test.txt"
    np.savetxt(filepath, lidar, delimiter=',')  
    print(time.time(), "just updated")
    # print(lidar_data)
 
def callback(msg):
    global lidar_data 
    global previous_time 
    lidar_data = pointcloud2_to_array(msg)[:,:3]  
    if time.time() - previous_time > .2: 
        send_data(lidar_data) 
    previous_time = time.time() 
def listener(): 
    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber("/mid/points", PointCloud2, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

 


 