import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Method takes in arrays for range, azimuth, and elevation and converts to x,y,z coordinates
def spherical_to_3D(range1, azimuth1, elevation1):

	range_new = range1
	azimuth_new = -azimuth1
	elevation_new = elevation1

	# Convert from spherical to euclidean coordinates
	x_new = range_new * np.cos(azimuth_new) * np.cos(elevation_new)
	y_new = range_new * np.sin(azimuth_new) * np.cos(elevation_new)
	z_new = range_new * np.sin(elevation_new)

	return (x_new, y_new, z_new)

	# Method takes in x,y,z coordinates and rcs values and produces a scatter plot
def xy_scatter_plot(range1, azimuth1, elevation1, ax1):
	(x, y, z) = spherical_to_3D(range1, azimuth1, elevation1)
	ax1.clear()
	ax1.scatter(x, y)

def start_fig():
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.set_xlim(0,4)
	ax.set_ylim(-5,5)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

def xyz_scatter_plot(x, y, z, rcs):

	fig = plt.figure()
	ax = Axes3D(fig)
	ax.set_xlim(0,4)
	ax.set_ylim(-5,5)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	curr_path = ax.scatter(x, y, z, zdir='z', s = 2, c = rcs)

	# change to fig.show for live
	# plt.show()
	plt.savefig('3D Isometric View.png')
	# fig.canvas.draw()
	# curr_path.remove()


def flag_counter(range1, azimuth1, elevation1, rcs1, rvel1, flag_counter, SNR):
	# Define stopping thresholds
	(x, y, z) = spherical_to_3D(range1, azimuth1, elevation1)

	k2 = 0.0637 # Constant to reduce x threshold for higher reltive velocity
	k1 = 0.1
	k0 = 0.8


	x_thresh_low = 0.05
	y_thresh = 0.5 # Half width of car plus 20%
	z_thresh_high = 2, 
	z_thresh_low = -0.5 # Humans are taller than 1m usually
	rcs_thresh = -15
	

	i = 0
	
	while i < len(x): 

		if rvel1[i] < 0:
			x_thresh_high = k2*np.fabs(rvel1[i]**2) + k1*np.fabs(rvel1[i]) + k0
		else:
			x_thresh_high = k0

		if (x[i] < x_thresh_high and x[i] > x_thresh_low) and (np.fabs(y[i]) < y_thresh) and (z[i] < z_thresh_high and z[i] > z_thresh_low) and (rcs1[i]> rcs_thresh):
			flag_counter += 1
			print("------------NEW LINE------------")
			print("RCS: " + str(rcs1[i]))
			print("X: " + str(x[i]))
			print("X_THRESH: " + str(x_thresh_high))
			print("Y: " + str(y[i]))
			print("Z: " + str(z[i]))
			print("SNR: " + str(SNR[i]))
			print("rvel: " + str(rvel1[i]))

		i += 1

	
	return (flag_counter)

def bin_flag(flag_counter):
	# Define stopping thresholds
	flag_thresh = 1
	return (flag_counter > flag_thresh)