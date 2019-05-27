#!/usr/bin/env python

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys
#import custom message type
from mr_radar.msg import Radar_Data

#importing ROS libraries
import rospy

#module for hex conversions
from detection import spherical_to_3D

#Plot
import pyqtgraph as pg 
import time

class online_plot(object):

	def __init__(self):
		#-----------------------Publisher/Subscriber-----------------------#
		rospy.Subscriber("/radar_data", Radar_Data, self.get_info) #subscriber to radar data
		#-----------------------Constants-----------------------#
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
		self.commandTimer = rospy.Timer(rospy.Duration(1), self.update(curve))


		# app = QtGui.QApplication([])
		# self.w = gl.GLViewWidget()
		# self.w.opts['distance'] = 20
		# self.w.show()
		# self.w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
		# self.w.setBackgroundColor('k')
		# self.w.pan(10,0,0)


		# g = gl.GLGridItem()
		# g.setSpacing(x=1, y=1)
		# g.setSize(x=100, y=100)
		# self.w.addItem(g)

		# a = gl.GLAxisItem()
		# a.setSize(x=100, y=100, z=100)
		# self.w.addItem(a)

	
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

	def update(self, curve):
		(x,y,z) = spherical_to_3D(self.ranges, self.azimuths, self.elevations)
		curve.setData(x, y)

			
if __name__ == '__main__':
	

	#---------------------XY 2D PLOT--------------------------#

	p = pg.plot()
	p.setWindowTitle('Detected Human - Y vs X Plot')
	p.setXRange(0.5,10)
	p.setYRange(-5,5) 
	p.setLabel('bottom', 'X', units='m')
	p.setLabel('left', 'Y', units='m')
	p.setTitle('Detected Human - Y vs X')
	# lege = p.addLegend()
	curve = p.plot(pen=None, symbol='o')
	# lege.addItem(curve, '....Sam')
	p.showGrid(x=1,y=1)
	rospy.init_node('Plotter') #create node
	plotting = online_plot() #create instance

	# t = QtCore.QTimer()
	# t.timeout.connect(plotting.update(curve))
	# t.start(1)
	

	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()


