# README #

'''
This package is a driver (parsing and basic detection) for the Continental RADAR ARS4EO.
The package is written in python for ROS Kinetic.
You will need to build this package using catkin.
Currently configured to listen to IP address 192.168.1.30.
Refer to ARS4EO documentation for further network configuration parameters.

**The launch file radar.launch will run all the required nodes.**

***TOPICS:***

**/radar_data:** Publishes arrays of data obtained from the RADAR per packet. Note that data consisting solely of 0s indicates no detections by the RADAR hence this topic will only output usable (non-zero values) from a particular packet. 

These parameters are:
Header stamp
Number of Detections
Range
Azimuth
Elevation
Relative Radial Velocity
RCS Value
Range Variance
Azimuth Variance
Elevation Variance
Velocity Variance
Signal to Noise Ratio

**/radar_obstacle:** Publishes a binary 1 or 0 if an object is detected within the specified bounding box in cartesian coordinates (Typically of RCS values higher than -7 as expected of living things)

**/radar_cloud:** Publishes /radar_data as a point cloud message which can be used in RViz to visualize the environment the RADAR can see in real time.

'''
