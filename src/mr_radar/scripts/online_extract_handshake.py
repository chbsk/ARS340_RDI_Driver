#!/usr/bin/env python
#file for connecting directly to the radar throught the media converter (no wireshark)

#importing ROS libraries
import rospy

#modules for ethernet connection to the radar
import socket
import struct
import binascii
#import keyboard

#modules for plotting
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

#module for file management
import os
from common_functions import convert_all_radar

class online_extract_radar(object):

	def __init__(self):
	
		MCAST_GRP = '225.0.0.1'
		MCAST_PORT = 31122
		IS_ALL_GROUPS = True
		interfaceIP = struct.unpack(">L", socket.inet_aton('192.168.1.30'))[0]
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

if __name__ == '__main__':
	rospy.init_node('Reader')
	reader = online_extract_radar() #create instance
	
	
	
