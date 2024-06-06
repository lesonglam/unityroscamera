# import open3d as o3d
# import numpy as np
# import rospy
# import threading
# from lidar import lidar_data

# def visualize():
    
#     vis = o3d.visualization.Visualizer()
#     vis.create_window()
#     pcd = o3d.geometry.PointCloud()

#     while not rospy.is_shutdown():
#         if lidar_data is not None:
#             pcd.points = o3d.utility.Vector3dVector(lidar_data)
#             vis.clear_geometries()
#             vis.add_geometry(pcd)
#             vis.poll_events()
#             vis.update_renderer()
#             print(lidar_data)

# if __name__ == '__main__':
#     # Start the ROS node in a separate thread
#     rospy_thread = threading.Thread(target=lambda: rospy.init_node('open3d_lidar_node', anonymous=True))
#     rospy_thread.start()

#     visualize()

# Data read & write
import numpy as np
 
# Visualization
import open3d as o3d
import pptk # works with Python 3.6

pc_txt = np.loadtxt('./data/modelnet40_airplane_0001.txt', delimiter=',')
print('Shape of the point cloud:', pc_txt.shape)
points = pc_txt[:,:3]
colors = pc_txt[:,3:]
vis = pptk.viewer(points, colors) # Start the interactive visualization
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)
# visualization
o3d.visualization.draw_geometries([pcd])