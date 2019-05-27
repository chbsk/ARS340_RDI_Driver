#!/usr/bin/env python

#---------------------------------------------------------------------------#
# The following code is used to listen to a UDP multicast broadcast from an
# ARS430 module. Each UDP packet received is converted based on the packaging 
# scheme provided by Continental. The subsequent data is the printed to the 
# /radar_data topic using a custom message definition.
#---------------------------------------------------------------------------#

#importing ROS libraries
import rospy

#import custom message type
from mr_radar.msg import Radar_Data

#modules for ethernet connection to the radar
import socket
import struct
import binascii

#modules for arrays
import numpy as np 

#module for hex conversions
from common_functions import convert_all_radar

class online_extract_radar(object):

	def __init__(self):
		#-----------------------Publisher-----------------------#
		self.pub = rospy.Publisher("/radar_data", Radar_Data, queue_size = 1000) #publisher
		
		#---------------------Socket Setup----------------------#
		MCAST_GRP = '225.0.0.1' #multicast group
		MCAST_PORT = 31122 #multicast port
		IS_ALL_GROUPS = True
		interfaceIP = struct.unpack(">L", socket.inet_aton('192.168.1.30'))[0] # radar IP
		rospy.loginfo(interfaceIP)

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

		if IS_ALL_GROUPS:
			# on this port, receives ALL multicast groups
			self.sock.bind(('', MCAST_PORT))
		else:
			# on this port, listen ONLY to MCAST_GRP
			self.sock.bind((MCAST_GRP, MCAST_PORT))
		host = '192.168.1.30'
	
		rospy.loginfo('host: ' + host) #prints in terminal
		self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
		self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

		rospy.loginfo('Connection Established') #prints in terminal	
	
	# Radar data publisher 
	def publish_radar(self,ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count):
		#create msg type
		msg = Radar_Data()
		#assign values
		msg.header.stamp = rospy.Time.now() #ROS time
		msg.num_det = actual_packet_count #number of detections in packet
		msg.range = ranges.tolist() #ranges [m]
		msg.azimuth = azimuths.tolist() #azimuth [rad]
		msg.elevation = elevations.tolist() #elevation [rad]
		msg.rel_vel = vels.tolist() #relative velocity [m/s]
		msg.rcs = rcss.tolist() #Radar Cross Section [dbm^2]
		msg.range_var = range_vars.tolist() #range variance
		msg.az_var = az_vars.tolist() #azimuth variance
		msg.el_var = el_vars.tolist() #elevation variance
		msg.vel_var = vel_vars.tolist() #velocity variance
		msg.snr = snrs.tolist() #Signal-Noise Ratio [dbr]
		#publish message
		self.pub.publish(msg)
		return

if __name__ == '__main__':
	rospy.init_node('Reader') #create node
	reader = online_extract_radar() #create instance
	try:
		while not rospy.is_shutdown():
			try:
				data, addr = reader.sock.recvfrom(1500) #receive data with a buffer of 1500 bytes
				hexdata = binascii.hexlify(data)
				#call custom conversion function
				(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_all_radar(hexdata, 0,0)
				#publish data
				if len(ranges)>0:
					reader.publish_radar(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) 
			except socket.error as e:
				print('Expection')
				rospy.loginfo('Radar shutting down.')
	except KeyboardInterrupt: #in the event of keyboard interrupt shutdown the socket connection
		reader.sock.shutdown(socket.SHUT_RDWR)
		reader.sock.close()
