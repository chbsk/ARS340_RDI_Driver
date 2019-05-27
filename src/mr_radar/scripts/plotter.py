#!/usr/bin/env python
#file for detecting obstacles ahead of car

#importing ROS libraries
import rospy

#import message type
from mr_radar.msg import Radar_Data
from std_msgs.msg import Int8

#modules for arrays
import numpy as np 

#plotting modules
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

#module for hex conversions
from detection import spherical_to_3D



class online_plotter(object):

	def __init__(self):
		#-----------------------Publisher-----------------------#
		rospy.Subscriber("/radar_data", Radar_Data, self.get_info) #subscriber to radar data
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
		#---------------Plotting stacks of 50 packets-------------#
		self.x_stack = []
		self.y_stack = []
		self.x_total = np.zeros(3000)
		self.y_total = np.zeros(3000)

	
	def get_info(self,msg):
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

	def animate(self, i):

		(x, y, z) = spherical_to_3D(self.ranges, self.azimuths, self.elevations)

		# if(i%10 != 0):
		#     self.x_stack = np.concatenate((self.x_stack, x))
		#     self.y_stack = np.concatenate((self.y_stack, y))
		# else:
		#     self.x_total[0:(len(self.x_total)-len(self.x_stack))] = self.x_total[len(self.x_stack):]
		#     self.x_total[(len(self.x_total)-len(self.x_stack)):] = self.x_stack 

		#     self.y_total[0:(len(self.y_total)-len(self.y_stack))] = self.y_total[len(self.y_stack):]
		#     self.y_total[(len(self.y_total)-len(self.y_stack)):] = self.y_stack

		#     self.x_stack = []
		#     self.y_stack = []

		#     ax.clear()
		#     ax.set_xlim(0, 2)
		#     ax.set_ylim(-5, 5)
		#     ax.set_title('Live Plot')
		#     ax.set_xlabel('X')
		#     ax.set_ylabel('Y')
		#     ax.scatter(self.x_total, self.y_total)
		if i%30 == 0:
			ax.clear()
		ax.set_xlim(0, 2)
		ax.set_ylim(-5, 5)
		ax.set_title('Live Plot')
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.scatter(x, y)

if __name__ == '__main__':
	rospy.init_node('Plotting') #create node
	plotter = online_plotter() #create instance
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ani = animation.FuncAnimation(fig, plotter.animate, interval=3, repeat=False)
	plt.show()