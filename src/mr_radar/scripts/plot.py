from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys

# Method takes in arrays for range, azimuth, and elevation and converts to x,y,z coordinates
def spherical_to_3D(range1, azimuth1, elevation1):

	range_new = range1
	azimuth_new = azimuth1
	elevation_new = elevation1

	# Convert from spherical to euclidean coordinates
	x_new = range_new * np.cos(azimuth_new) * np.cos(elevation_new)
	y_new = range_new * np.sin(azimuth_new) * np.cos(elevation_new)
	z_new = range_new * np.sin(elevation_new)

	return (x_new, y_new, z_new)


def update():

	global i, sp3, pos3

	if i > (len(x)-n):
		print('ABORT, ABORT, ABORT.... loljk')
		pos3[0:(n-(len(x)-i)),0] = pos3[(len(x)-i):,0]
		pos3[0:(n-(len(x)-i)),1] = pos3[(len(x)-i):,1]
		pos3[0:(n-(len(x)-i)),2] = pos3[(len(x)-i):,2]
		pos3[(n-(len(x)-i)):,0] = x[i:]
		pos3[(n-(len(x)-i)):,1] = y[i:]
		pos3[(n-(len(x)-i)):,2] = y[i:]
		i = 0
		return None

	pos3[:,0] = x[i:i+n]
	pos3[:,1] = y[i:i+n]
	pos3[:,2] = z[i:i+n]
	#pos3[:,2] = z[i:i+n]
	# color = np.empty((n,4), dtype=np.float32)
	# color[:,3] = 1
	# color[:,0] = np.clip(rcss[i:i+n]/12, 0, 1)
	# color[:,1] = np.clip(rcss[i:i+n]/2, 0, 1)
	# color[:,2] = np.clip(rcss[i:i+n]/27, 0, 1)
	sp3.setData(pos=pos3)
	i += 1
	



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	ranges = np.loadtxt('Moving Outdoors/overall_ranges.out')
	azimuths = np.loadtxt('Moving Outdoors/overall_azimuths.out')
	elevations = np.loadtxt('Moving Outdoors/overall_elevations.out')
	rcss = np.loadtxt('Moving Outdoors/overall_rcss.out')

	(x_full,y_full,z_full) = spherical_to_3D(ranges, azimuths, elevations)


	x_thresh_low = 0.05
	x_thresh_high = 7
	y_thresh = 2 # Half width of car plus 20%
	z_thresh_high = 2, 
	z_thresh_low = 0 # Humans are taller than 1m usually
	rcs_thresh = -40
	flag_thresh = 1

	k=0
	x=np.zeros(0)
	y=np.zeros(0)
	z=np.zeros(0)
	while k < len(x_full):

		if (x_full[k] < x_thresh_high and x_full[k] > x_thresh_low) and (np.fabs(y_full[k]) < y_thresh) and  (z_full[k] < z_thresh_high and z_full[k] > z_thresh_low) and (rcss[k]> rcs_thresh):
			
			x = np.concatenate((x, [x_full[k]]))
			y = np.concatenate((y, [y_full[k]]))
			z = np.concatenate((z, [z_full[k]]))
			
		k += 1

	#---------------COMMENT OUT FOR DETECTIONS----------------#
	# x = x_full
	# y = y_full
	# z = z_full
	#---------------------------------------------------------#

	app = QtGui.QApplication([])
	w = gl.GLViewWidget()
	w.opts['distance'] = 20
	w.show()
	w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
	w.setBackgroundColor('k')
	w.pan(10,0,0)


	g = gl.GLGridItem()
	g.setSpacing(x=1, y=1)
	g.setSize(x=100, y=100)
	w.addItem(g)

	a = gl.GLAxisItem()
	a.setSize(x=100, y=100, z=100)
	w.addItem(a)

	i = 0

	n = 10

	#-----------------COMMENT OUT FOR FULL PLOTS-----------------#
	pos3 = np.zeros((n,3))
	pos3[:,0] = x[0:n]
	pos3[:,1] = y[0:n]
	pos3[:,2] = z[0:n]
	#------------------------------------------------------------#

	#--------------COMMENT OUT FOR ANIMATED PLOTTING-------------#
	# pos3 = np.zeros((len(x_full),3))
	# pos3[:,0] = x_full
	# pos3[:,1] = y_full
	# pos3[:,2] = z_full
	#------------------------------------------------------------#


	sp3 = gl.GLScatterPlotItem(pos=pos3, color=(0.2,1,0.2,1), size=0.2, pxMode=False)
	w.addItem(sp3)

	#-----------------COMMENT OUT FOR FULL PLOTS-----------------#
	t = QtCore.QTimer()
	t.timeout.connect(update)
	t.start(50)
	#------------------------------------------------------------#
	
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()

