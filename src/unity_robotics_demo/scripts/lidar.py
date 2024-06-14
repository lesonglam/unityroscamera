#!/usr/bin/env python
# license removed for brevity

import rospy
from sensor_msgs.msg import PointCloud2 , PointField
import sensor_msgs.point_cloud2 as pc2
import numpy as np
import time
import socket
import open3d as o3d

previous_t = time.time() 

# Global variable to store the latest LiDAR data
lidar_data = None


# create visualizer and window.
vis = o3d.visualization.Visualizer()
vis.create_window(height=720, width=1080)

# initialize pointcloud instance.
pcd = o3d.geometry.PointCloud()
# *optionally* add initial points
points = np.random.rand(10, 3)
pcd.points = o3d.utility.Vector3dVector(points) 
# include it in the visualizer before non-blocking visualization.
vis.add_geometry(pcd) 
# to add new points each dt secs.
dt = 0.2

def update_visualization(loaded_arr):
    global previous_t
    if time.time() - previous_t > dt: 
        # loaded_arr  = read_data(filepath)
        if loaded_arr is not None:
            pcd.points = o3d.utility.Vector3dVector(loaded_arr*0.2)    #*.2 as zoom out    
            vis.update_geometry(pcd)
            # print(loaded_arr.shape)       
        previous_t = time.time()  
    vis.poll_events()
    # keep_running = vis.poll_events()
    vis.update_renderer()


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
    global previous_t 
    lidar_data = pointcloud2_to_array(msg)[:,:3]  
    if time.time() - previous_t > .2: 
        # send_data(lidar_data)  #create  text file
        update_visualization(lidar_data)
        # print(lidar_data)
    previous_t = time.time() 
def listener(): 
    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber("/mid/points", PointCloud2, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

 


 