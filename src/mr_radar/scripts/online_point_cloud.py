#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import PointCloud, ChannelFloat32
from geometry_msgs.msg import Point32 
from detection import spherical_to_3D
from mr_radar.msg import Radar_Data


class online_point_cloud(object):

	def __init__(self):
		#-----------------------Publisher/Subscriber-----------------------#
		rospy.Subscriber("/radar_data", Radar_Data, self.get_info) #subscriber to radar data
		self.cloud_topic = rospy.Publisher("/radar_cloud", PointCloud, queue_size = 1000) #publisher for radar point cloud
		#-----------------------Constants-----------------------#
		self.ranges = np.zeros(10) #ranges [m]
		self.azimuths = np.zeros(10) #azimuth [rad]
		self.elevations = np.zeros(10) #elevation [rad]
		self.rcss = np.zeros(10) #Radar Cross Section [dbm^2]
		self.time = 0 #time of packet
		self.pack_count = 1 #number of packets read
		point = Point32()
		point.x = 0
		point.y = 0
		point.z = 0
		self.points = [] #list of Point32
		#self.points.extend([point])
		self.inty_vals = [] #list of intensity values
		self.pack_thresh = 5 #number of packets displayed at once
		self.updated = False #lock boolean
		
	def get_info(self,msg):
		if not (self.updated):
			self.updated = True
			self.time = msg.header.stamp #packet time
			self.ranges = np.array(msg.range) #ranges [m]
			self.azimuths = np.array(msg.azimuth) #azimuth [rad]
			self.elevations = np.array(msg.elevation) #elevation [rad]
			self.rcss = np.array(msg.rcs) #Radar Cross Section [dbm^2]
			#call convert point
			self.convert_point(self.ranges,self.azimuths,self.elevations,self.rcss)
			#publish point cloud 
			if self.pack_count % self.pack_thresh == 0:
				self.cloud_pub()
			if self.pack_count >= 1000:
				self.pack_count = 0
		return
	
	def convert_point(self,ranges,azimuths,elevations,rcss):
		self.pack_count += 1 #increment packet counter
		#append channel intensity based on rcs
		self.inty_vals.extend(rcss.tolist())
		#convert to Cartesian from Spherical
		(x,y,z) = spherical_to_3D(ranges, azimuths, elevations)
		for i in range(0,np.shape(x)[0]):
			point = Point32()
			point.x = x[i]
			point.y = y[i]
			point.z = z[i]
			self.points.extend([point])
		self.updated = False
			
	def cloud_pub(self):
		#create point cloud object
		cloud = PointCloud()
		cloud.header.stamp = rospy.Time.now() #time stamp
		cloud.header.frame_id = 'map'
		cloud.points = self.points #Cartesian points
		channel = ChannelFloat32()
		channel.name = 'intensity'
		channel.values = self.inty_vals #rcs intensities
		cloud.channels = [channel]
		self.cloud_topic.publish(cloud) #publish point cloud object
		#reset points and intesnities
		self.points = []
		self.inty_vals = []
		
if __name__ == '__main__':
	rospy.init_node('Radar_Cloud') #create node
	p_cloud = online_point_cloud() #create instance
	rospy.spin()	
	
		
		

