#file for connecting directly to the radar throught the media converter (no wireshark) or for working with offline text files of the raw data

#importing modules

#modules for ethernet connection to the radar
import socket
import struct
import binascii


#modules for plotting
from detection import *


#module for file management
import os

#importing helper functions
from common_functions import convert_all_radar

#modules for user-friendliness
import time
# import keyboard





def online_overall_extract(save_formatted_data,save_raw_data, save_arrays, num_packets, endless):
	

	if (save_formatted_data):
		far_0_radar_data = open("far_0_radar_data.csv","w")
		far_0_radar_data.write("Number, range, VrelRad, AzAng0, AzAng1, ElAng, RCS0, RCS1, Prob0, Prob1, RangeVar, VrelRadVar, AzAngVar0, AzAngVar1, ElAngVar, Pdh0, SNR \n")
		far_0_radar_data.close()

		far_1_radar_data = open("far_1_radar_data.csv","w")
		far_1_radar_data.write("Number, range, VrelRad, AzAng0, AzAng1, ElAng, RCS0, RCS1, Prob0, Prob1, RangeVar, VrelRadVar, AzAngVar0, AzAngVar1, ElAngVar, Pdh0, SNR \n")
		far_1_radar_data.close()

		near_0_radar_data = open("near_0_radar_data.csv","w")
		near_0_radar_data.write("Number, range, VrelRad, AzAng0, AzAng1, ElAng, RCS0, RCS1, Prob0, Prob1, RangeVar, VrelRadVar, AzAngVar0, AzAngVar1, ElAngVar, Pdh0, SNR \n")
		near_0_radar_data.close()

		near_1_radar_data = open("near_1_radar_data.csv","w")
		near_1_radar_data.write("Number, range, VrelRad, AzAng0, AzAng1, ElAng, RCS0, RCS1, Prob0, Prob1, RangeVar, VrelRadVar, AzAngVar0, AzAngVar1, ElAngVar, Pdh0, SNR \n")
		near_1_radar_data.close()

		near_2_radar_data = open("near_2_radar_data.csv","w")
		near_2_radar_data.write("Number, range, VrelRad, AzAng0, AzAng1, ElAng, RCS0, RCS1, Prob0, Prob1, RangeVar, VrelRadVar, AzAngVar0, AzAngVar1, ElAngVar, Pdh0, SNR \n")
		near_2_radar_data.close()


	MCAST_GRP = '225.0.0.1'
	MCAST_PORT = 31122
	IS_ALL_GROUPS = True
	interfaceIP = struct.unpack(">L", socket.inet_aton('192.168.1.30'))[0]
	# print(interfaceIP)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

	if IS_ALL_GROUPS:
		# on this port, receives ALL multicast groups
		sock.bind(('', MCAST_PORT))
	else:
		# on this port, listen ONLY to MCAST_GRP
		sock.bind((MCAST_GRP, MCAST_PORT))
	host = '192.168.1.30'

	print('host: ' + host) #prints in terminal
	sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
	sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, 
				   socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

	print('Connection Established') #prints in terminal
	
	if (not(endless)):
		
		index_counter = 0
		max_packets = num_packets
		overall_size = 38*max_packets

		

	else:
		overall_size = 0

	packet_counter = 0

	overall_ranges = np.zeros(overall_size)
	overall_azimuths = np.zeros(overall_size)
	overall_elevations = np.zeros(overall_size)
	overall_rcss = np.zeros(overall_size)

	overall_range_vars = np.zeros(overall_size)
	overall_vels = np.zeros(overall_size)
	overall_vel_vars = np.zeros(overall_size)

	overall_az_vars = np.zeros(overall_size)
	overall_el_vars = np.zeros(overall_size)

	overall_snrs = np.zeros(overall_size)

	flag_counter = 0

	start_time = time.time()
	while ((endless) or (packet_counter < max_packets)):
		# if (keyboard.is_pressed('q')):
		# 	print ("Breaking out of loop")
		# 	break
		# print (packet_counter)
		try:
			data, addr = sock.recvfrom(1500)
			hexdata = binascii.hexlify(data)
			
			(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, size) = convert_all_radar(hexdata, save_formatted_data, save_raw_data)

			# can use the above individual arrays for live plotting within this loop if necessary

			(flag_raised, flag_counter) = binary_flag(ranges, azimuths, elevations, rcss, vels, flag_counter)
			# print (flag_raised)

			if (flag_raised):
				flag_counter_string = "Flag Counter: " + str(flag_counter)
				print(flag_counter_string)
				flag_counter = 0

			if (not(endless)):
				overall_ranges[index_counter:index_counter+size] = ranges
				overall_azimuths[index_counter:index_counter+size] = azimuths
				overall_elevations[index_counter:index_counter+size] = elevations
				overall_rcss[index_counter:index_counter+size] = rcss

				overall_range_vars[index_counter:index_counter+size] = range_vars
				overall_vels[index_counter:index_counter+size] = vels
				overall_vel_vars[index_counter:index_counter+size] = vel_vars

				overall_az_vars[index_counter:index_counter+size] = az_vars
				overall_el_vars[index_counter:index_counter+size] = el_vars

				overall_snrs[index_counter:index_counter+size] = snrs


				index_counter = index_counter + size
			
			else:

				overall_ranges = np.concatenate((overall_ranges,ranges))
				overall_azimuths = np.concatenate((overall_azimuths,azimuths))
				overall_elevations = np.concatenate((overall_elevations,azimuths))
				overall_rcss = np.concatenate((overall_rcss,rcss))

				overall_range_vars =  np.concatenate((overall_range_vars, range_vars))
				overall_vels = np.concatenate((overall_vels, vels))
				overall_vel_vars = np.concatenate((overall_vel_vars, vel_vars))

				overall_az_vars = np.concatenate((overall_az_vars, az_vars))
				overall_el_vars = np.concatenate((overall_el_vars, el_vars))

				overall_snrs = np.concatenate((overall_snrs, snrs))

			# can use the above overall arrays for live plotting within this loop if necessary


			if (len(ranges)):
				packet_counter += 1


			
		except socket.error as e:
			print('Expection')
			hexdata = binascii.hexlify(data)
			print('Data = %s' % hexdata)
	

	if (not(endless)):
		overall_ranges = overall_ranges[0:index_counter]
		overall_azimuths = overall_azimuths[0:index_counter]
		overall_elevations = overall_elevations[0:index_counter]
		overall_rcss = overall_rcss[0:index_counter]
		overall_vels = overall_vels[0:index_counter]

		overall_range_vars = overall_range_vars[0:index_counter]
		overall_el_vars = overall_el_vars[0:index_counter]
		overall_az_vars = overall_az_vars[0:index_counter]
		overall_vel_vars = overall_vel_vars[0:index_counter]
		overall_snrs = overall_snrs[0:index_counter]



		

	if (save_arrays):
		np.savetxt('overall_ranges.out', overall_ranges, delimiter=',')
		np.savetxt('overall_azimuths.out', overall_azimuths, delimiter=',')
		np.savetxt('overall_elevations.out', overall_elevations, delimiter=',')
		np.savetxt('overall_rcss.out', overall_rcss, delimiter=',')

		np.savetxt('overall_range_vars.out', overall_range_vars, delimiter=',')
		np.savetxt('overall_az_vars.out', overall_az_vars, delimiter=',')
		np.savetxt('overall_el_vars.out', overall_el_vars, delimiter=',')
		np.savetxt('overall_snrs.out', overall_snrs, delimiter=',')

		np.savetxt('overall_vel_vars.out', overall_vel_vars, delimiter=',')
		np.savetxt('overall_vels.out', overall_vels, delimiter=',')



	end_time = time.time()
	time_taken = end_time - start_time
	precision = 4
	time_taken_string = str( "{:.{}f}".format(time_taken, precision ) ) 
	time_string = "Time Taken from 1st packet to " + str(packet_counter) + " packets: " + (time_taken_string) + " seconds"
	print(time_string)


	return (overall_ranges, overall_azimuths, overall_elevations, overall_vels,  overall_rcss, overall_range_vars, overall_az_vars, overall_el_vars, overall_vel_vars, overall_snrs, packet_counter, time_taken_string)






#online_overall_extract(directory_sub_folder, save_formatted_data,save_raw_data, save_arrays, num_packets, endless)
# (overall_ranges, overall_azimuths, overall_elevations, overall_vels,  overall_rcss, overall_range_vars, overall_az_vars, overall_el_vars, overall_vel_vars, overall_snrs) = online_overall_extract(directory_sub_folder, False, False, True, 1000, True)

# (x, y, z) = spherical_to_3D(overall_ranges, overall_azimuths, overall_elevations)
# xyz_scatter_plot(x, y, z, overall_rcss)