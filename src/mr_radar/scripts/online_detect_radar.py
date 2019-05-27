#!/usr/bin/env python
#file for detecting obstacles ahead of car

#importing ROS libraries
import rospy

#import message type
from mr_radar.msg import Radar_Data
from std_msgs.msg import Int8

#modules for arrays
import numpy as np 

#module for hex conversions
from detection import bin_flag, flag_counter 



class online_detect_radar(object):

	def __init__(self):
		#-----------------------Publisher/Subscriber-----------------------#
		rospy.Subscriber("/radar_data", Radar_Data, self.get_info) #subscriber to radar data
		self.brake = rospy.Publisher("/radar_obstacle", Int8, queue_size = 1000) #publisher for binary flag topic
		#-----------------------Constants-----------------------#
		self.flag_counter = 0 #no. of detections inside boundary zone
		self.ranges = np.zeros(10) #ranges [m]
		self.azimuths = np.zeros(10) #azimuth [rad]
		self.elevations = np.zeros(10) #elevation [rad]
		self.rel_vels = np.zeros(10) #relative velocity [m/s]
		self.rcss = np.zeros(10) #Radar Cross Section [dbm^2]
		self.range_vars = np.zeros(10) #range variance
		self.az_vars = np.zeros(10) #azimuth variance
		self.el_vars = np.zeros(10) #elevation variance
		self.vel_vars = np.zeros(10) #velocity variance
		self.snrs = np.zeros(10) #Signal-Noise Ratio [dbr]
		self.time = 0 #time of packet
		self.updated = False #update boolean

	
	def get_info(self,msg):
		if not(self.updated):
			self.time = msg.header.stamp #packet time
			self.ranges = np.array(msg.range) #ranges [m]
			self.azimuths = np.array(msg.azimuth) #azimuth [rad]
			self.elevations =np.array(msg.elevation) #elevation [rad]
			self.rel_vels = np.array(msg.rel_vel) #relative velocity [m/s]
			self.rcss = np.array(msg.rcs) #Radar Cross Section [dbm^2]
			self.range_vars = np.array(msg.range_var) #range variance
			self.az_vars = np.array(msg.az_var) #azimuth variance
			self.el_vars = np.array(msg.el_var) #elevation variance
			self.vel_vars = np.array(msg.vel_var) #velocity variance
			self.snrs = np.array(msg.snr) #Signal-Noise Ratio [dbr]
			self.updated = True #new information received
		return
	
	def pub(self,flag_raised):
		self.brake.publish(flag_raised)
		return

			
if __name__ == '__main__':
	rospy.init_node('Detection') #create node
	detector = online_detect_radar() #create instance
	flag_raised = 0
	try:
		while not rospy.is_shutdown():

			if detector.updated: #when a new packet is published on /radar_data
				#call detection function
				(detector.flag_counter) = flag_counter(detector.ranges, detector.azimuths, detector.elevations, detector.rcss, detector.rel_vels, detector.flag_counter,detector.snrs)    
				flag_raised = bin_flag(detector.flag_counter)
				detector.updated = False
				#if verified obstacle
			if (flag_raised):
				# flag_counter_string = "Flag Counter: " + str(detector.flag_counter)
				# print(flag_counter_string)
				# detector.pub(flag_raised) #publish to binary topic
				detector.pub(flag_raised) #publish to binary topic
				flag_raised = 0
				detector.flag_counter = 0
	except KeyboardInterrupt: #in the event of keyboard interrupt shutdown the socket connection
		rospy.loginfo('Radar shutting down.')
