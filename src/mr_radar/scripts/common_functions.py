#modules for ethernet connection to the radar
import socket
import struct
import binascii

#modules for plotting
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

#module for file management
import os



#given a string of hext digits, a base and a True/False indicating whether the number to be generated is signed or not, will convert to an integer
#file for connecting directly to the radar throught the media converter (no wireshark) or for working with offline text files of the raw data
def hex_converter(hex_string, base, signed):
	value = int(hex_string, 16)
	if (signed):
		if ((value) & (1 << (base -1) )):
			value -= 1 << base
	return value

# the index offset between the start of the packet and the start of the non-header information for sensor events
def sensor_index(idx):
	offset = 16*8
	return (offset+idx)/4

# the index offset between the start of the packet and the start of the scan data for the far and near events
def radar_struct_index(idx, i):
	offset = 16*8 + 256
	return int((offset + idx + i*224)/4)


# given a raw hexlified string that containts the front b' and the trailing '
# will filter out to just the string
def strip_binary(raw_hex_string):
	return raw_hex_string[2:-1]

# converts the non-scan data of the detection packets
def convert_non_scan(hexdata, save_formatted_data):

	#creates a dictionary to store all the values so that they can be called if necessary when processing the scan data
	non_scan_dictionary = {}
	
	#header information
	#print hexdata[0:8]
	headerID = hex_converter(hexdata[0:8],16,False)
	non_scan_dictionary["headerID"] = headerID
	# print(headerID)

	if (headerID!=13107200):

		num_detections = hex_converter(hexdata[84:88],16,False)
		non_scan_dictionary["num_detections"] = num_detections

		if (save_formatted_data):
			# print(hexdata[8:16])
			E2Elength = hex_converter(hexdata[8:16],16,False)
			non_scan_dictionary["E2Elength"] = E2Elength

			clientID = hex_converter(hexdata[16:20],16,False)
			non_scan_dictionary["clientID"] = clientID

			sessionID = hex_converter(hexdata[20:24],16,False)
			non_scan_dictionary["sessionID"] = sessionID

			protocol = hex_converter(hexdata[24:26],16,False)
			non_scan_dictionary["protocol"] = protocol

			intver = hex_converter(hexdata[26:28],16,False)
			non_scan_dictionary["intver"] = intver

			msg_type = hex_converter(hexdata[28:30],16,False)
			non_scan_dictionary["msg_type"] = msg_type

			rtrn_code = hex_converter(hexdata[30:32],16,False)
			non_scan_dictionary["rtrn_code"] = rtrn_code
			
			#additional information E2E
			crc = hex_converter(hexdata[32:36],16,False)
			non_scan_dictionary["crc"] = crc

			lengthe2e = hex_converter(hexdata[36:40],16,False)
			non_scan_dictionary["lengthe2e"] = lengthe2e

			counter = hex_converter(hexdata[40:42],8,False)
			non_scan_dictionary["counter"] = counter	
			
			#packet information
			message_counter = 1 + hex_converter(hexdata[42:44],8,False)
			non_scan_dictionary["message_counter"] = message_counter

			#global_ptptime = int(hexdata[44:60],64)
			internal_time = hex_converter(hexdata[60:68],32,False)
			non_scan_dictionary["internal_time"] = internal_time

			meas_counter = hex_converter(hexdata[68:76],32,False)
			non_scan_dictionary["meas_counter"] = meas_counter

			cycle_counter = hex_converter(hexdata[76:84],32,False)
			non_scan_dictionary["cycle_counter"] = cycle_counter


			v_ambig = hex_converter(hexdata[88:92],16,True)*(0.003051851)
			non_scan_dictionary["v_ambig"] = v_ambig

			cntr_freq = 76 + hex_converter(hexdata[92:94],8,False)*(0.05)
			non_scan_dictionary["cntr_freq"] = cntr_freq

			det_in_packet = hex_converter(hexdata[94:96],8,False)
			non_scan_dictionary["det_in_packet"] = det_in_packet

		if ((save_formatted_data == True) and (num_detections!=0)):
			#far 0 event
			if (headerID == 14417921):
				file_name = "far_0_header_data.csv"
				if not(os.path.isfile("./far_0_header_data.csv")):
					header_string = "headerID" + ", "
					header_string = header_string + "E2Elength" + ", "
					header_string = header_string + "clientID" + ", "
					header_string = header_string + "sessionID" + ", "
					header_string = header_string + "protocol" + ", "
					header_string = header_string + "intver" + ", "
					header_string = header_string + "msg_type" + ", "
					header_string = header_string + "rtrn_code" + ", "
					header_string = header_string + "crc" + ", "
					header_string = header_string + "lengthe2e" + ", "
					header_string = header_string + "counter" + ", "
					header_string = header_string + "message_counter" + ", "
					header_string = header_string + "internal_time" + ", "
					header_string = header_string + "meas_counter" + ", "
					header_string = header_string + "cycle_counter" + ", "
					header_string = header_string + "num_detections" + ", "
					header_string = header_string + "v_ambig" + ", "
					header_string = header_string + "cntr_freq" + ", "
					header_string = header_string + "det_in_packet" + "\n "
					file_handler = open("far_0_header_data.csv","a")
					file_handler.write(header_string)
				else:
					file_handler = open("far_0_header_data.csv","a")


			#far 1 event
			elif (headerID == 14417922):
				file_name = "far_1_header_data.csv"
				if not(os.path.isfile("./far_1_header_data.csv")):
					header_string = "headerID" + ", "
					header_string = header_string + "E2Elength" + ", "
					header_string = header_string + "clientID" + ", "
					header_string = header_string + "sessionID" + ", "
					header_string = header_string + "protocol" + ", "
					header_string = header_string + "intver" + ", "
					header_string = header_string + "msg_type" + ", "
					header_string = header_string + "rtrn_code" + ", "
					header_string = header_string + "crc" + ", "
					header_string = header_string + "lengthe2e" + ", "
					header_string = header_string + "counter" + ", "
					header_string = header_string + "message_counter" + ", "
					header_string = header_string + "internal_time" + ", "
					header_string = header_string + "meas_counter" + ", "
					header_string = header_string + "cycle_counter" + ", "
					header_string = header_string + "num_detections" + ", "
					header_string = header_string + "v_ambig" + ", "
					header_string = header_string + "cntr_freq" + ", "
					header_string = header_string + "det_in_packet" + "\n "
					file_handler = open("far_1_header_data.csv","a")
					file_handler.write(header_string)
				else:
					file_handler = open("far_1_header_data.csv","a")
				

			#near 0 event
			elif (headerID == 14417923):
				file_name = "near_0_header_data.csv"
				if not(os.path.isfile("./near_0_header_data.csv")):
					header_string = "headerID" + ", "
					header_string = header_string + "E2Elength" + ", "
					header_string = header_string + "clientID" + ", "
					header_string = header_string + "sessionID" + ", "
					header_string = header_string + "protocol" + ", "
					header_string = header_string + "intver" + ", "
					header_string = header_string + "msg_type" + ", "
					header_string = header_string + "rtrn_code" + ", "
					header_string = header_string + "crc" + ", "
					header_string = header_string + "lengthe2e" + ", "
					header_string = header_string + "counter" + ", "
					header_string = header_string + "message_counter" + ", "
					header_string = header_string + "internal_time" + ", "
					header_string = header_string + "meas_counter" + ", "
					header_string = header_string + "cycle_counter" + ", "
					header_string = header_string + "num_detections" + ", "
					header_string = header_string + "v_ambig" + ", "
					header_string = header_string + "cntr_freq" + ", "
					header_string = header_string + "det_in_packet" + "\n "
					file_handler = open("near_0_header_data.csv","a")
					file_handler.write(header_string)
				else:
					file_handler = open("near_0_header_data.csv","a")
				

			#near 1 event
			elif (headerID == 14417924):
				file_name = "near_1_header_data.csv"
				if not(os.path.isfile("./near_1_header_data.csv")):
					header_string = "headerID" + ", "
					header_string = header_string + "E2Elength" + ", "
					header_string = header_string + "clientID" + ", "
					header_string = header_string + "sessionID" + ", "
					header_string = header_string + "protocol" + ", "
					header_string = header_string + "intver" + ", "
					header_string = header_string + "msg_type" + ", "
					header_string = header_string + "rtrn_code" + ", "
					header_string = header_string + "crc" + ", "
					header_string = header_string + "lengthe2e" + ", "
					header_string = header_string + "counter" + ", "
					header_string = header_string + "message_counter" + ", "
					header_string = header_string + "internal_time" + ", "
					header_string = header_string + "meas_counter" + ", "
					header_string = header_string + "cycle_counter" + ", "
					header_string = header_string + "num_detections" + ", "
					header_string = header_string + "v_ambig" + ", "
					header_string = header_string + "cntr_freq" + ", "
					header_string = header_string + "det_in_packet" + "\n "
					file_handler = open("near_1_header_data.csv","a")
					file_handler.write(header_string)
				else:
					file_handler = open("near_1_header_data.csv","a")
				
			#near 2 event
			elif (headerID == 14417925):
				file_name = "near_2_header_data.csv"
				if not(os.path.isfile("./near_2_header_data.csv")):
					header_string = "headerID" + ", "
					header_string = header_string + "E2Elength" + ", "
					header_string = header_string + "clientID" + ", "
					header_string = header_string + "sessionID" + ", "
					header_string = header_string + "protocol" + ", "
					header_string = header_string + "intver" + ", "
					header_string = header_string + "msg_type" + ", "
					header_string = header_string + "rtrn_code" + ", "
					header_string = header_string + "crc" + ", "
					header_string = header_string + "lengthe2e" + ", "
					header_string = header_string + "counter" + ", "
					header_string = header_string + "message_counter" + ", "
					header_string = header_string + "internal_time" + ", "
					header_string = header_string + "meas_counter" + ", "
					header_string = header_string + "cycle_counter" + ", "
					header_string = header_string + "num_detections" + ", "
					header_string = header_string + "v_ambig" + ", "
					header_string = header_string + "cntr_freq" + ", "
					header_string = header_string + "det_in_packet" + "\n "
					file_handler = open("near_2_header_data.csv","a")
					file_handler.write(header_string)
				else:
					file_handler = open("near_2_header_data.csv","a")

			write_string = str(headerID) + ", "
			write_string = write_string + str(E2Elength) + ", "	
			write_string = write_string + str(clientID) + ", "	
			write_string = write_string + str(sessionID) + ", "	
			write_string = write_string + str(protocol) + ", "	
			write_string = write_string + str(intver) + ", "	
			write_string = write_string + str(msg_type) + ", "	
			write_string = write_string + str(rtrn_code) + ", "
			write_string = write_string + str(crc) + ", "	
			write_string = write_string + str(lengthe2e) + ", "	
			write_string = write_string + str(counter) + ", "	
			write_string = write_string + str(message_counter) + ", "	
			write_string = write_string + str(internal_time) + ", "	
			write_string = write_string + str(meas_counter) + ", "
			write_string = write_string + str(cycle_counter) + ", "	
			write_string = write_string + str(num_detections) + ", "	
			write_string = write_string + str(v_ambig) + ", "
			write_string = write_string + str(cntr_freq) + ", "
			write_string = write_string + str(det_in_packet) + "\n"
			file_handler.write(write_string)
			file_handler.close()
			



	return non_scan_dictionary


def convert_scan(hexdata, file_name, size, save_formatted_data):

	# creating the numpy arrays 
	ranges = np.zeros(size)
	azimuths = np.zeros(size)
	elevations = np.zeros(size)
	rcss = np.zeros(size)


	range_vars = np.zeros(size)
	vels = np.zeros(size)
	vel_vars = np.zeros(size)

	az_vars = np.zeros(size)
	el_vars = np.zeros(size)

	snrs = np.zeros(size)


	actual_packet_count = 0

	if (save_formatted_data):
		f = open(file_name,"a")

	# for every detection (38 in far0, far1, near0 and near1, 32 in near2)
	# has been changed to incorporate the actual number of scans so that 0s aren't produced
	for i in range(size):
		# string starts with the number of the detection (local to the packet)

		f_range = 0 + .0045778*hex_converter((hexdata[radar_struct_index(0,i):radar_struct_index(16,i)]),16,False)
		f_ElAng = 0 + (9.58767*(10**-5))*hex_converter((hexdata[radar_struct_index(64,i):radar_struct_index(80,i)]),16,True)
		f_AzAng0 = 0 + (9.58767*(10**-5))*hex_converter((hexdata[radar_struct_index(32,i):radar_struct_index(48,i)]),16,True)
		f_AzAng1 = 0 + (9.58767*(10**-5))*hex_converter((hexdata[radar_struct_index(48,i):radar_struct_index(64,i)]),16,True)
		f_RCS0 = 0 + 0.003051851*hex_converter((hexdata[radar_struct_index(80,i):radar_struct_index(96,i)]),16,True)
		f_RCS1 = 0 + 0.003051851*hex_converter((hexdata[radar_struct_index(96,i):radar_struct_index(112,i)]),16,True)
		f_Prob0 = 0 + 0.003937008*hex_converter((hexdata[radar_struct_index(112,i):radar_struct_index(120,i)]),8,False)
		f_Prob1 = 0 + 0.003937008*hex_converter((hexdata[radar_struct_index(120,i):radar_struct_index(128,i)]),8,False)
		f_Pdh0 = 0 + 0.003937008*hex_converter((hexdata[radar_struct_index(208,i):radar_struct_index(216,i)]),8,False)

		f_RangeVar = 0 + 0.000152593*hex_converter((hexdata[radar_struct_index(128,i):radar_struct_index(144,i)]),16,False)
		f_VrelRadVar = 0 + 0.000152593*hex_converter((hexdata[radar_struct_index(144,i):radar_struct_index(160,i)]),16,False)
		f_AzAngVar0 =  0 + (1.52593*(10**-5))*hex_converter((hexdata[radar_struct_index(160,i):radar_struct_index(176,i)]),16,False)
		f_AzAngVar1 = 0 + (1.52593*(10**-5))*hex_converter((hexdata[radar_struct_index(176,i):radar_struct_index(192,i)]),16,False)
		f_ElAngVar = 0 + (1.52593*(10**-5))*hex_converter((hexdata[radar_struct_index(192,i):radar_struct_index(208,i)]),16,False)
		f_SNR = 11+ 0.1*hex_converter((hexdata[radar_struct_index(208,i):radar_struct_index(216,i)]),16,False)
		f_VrelRad = 0 + .0045778*hex_converter((hexdata[radar_struct_index(16,i):radar_struct_index(32,i)]),16,True)


		if ((f_Pdh0 < .2) and not(f_range == 0)):
			ranges[actual_packet_count] = f_range
			range_vars[actual_packet_count] = f_RangeVar

			elevations[actual_packet_count] = f_ElAng
			el_vars[actual_packet_count] = f_ElAngVar

			vels[actual_packet_count] = f_VrelRad
			vel_vars[actual_packet_count] = f_VrelRadVar

			snrs[actual_packet_count] = f_SNR


			if (f_Prob0>f_Prob1):
				rcss[actual_packet_count] = f_RCS0
				azimuths[actual_packet_count] = f_AzAng0
				az_vars[actual_packet_count] = f_AzAngVar0
			else:
				rcss[actual_packet_count] = f_RCS1
				azimuths[actual_packet_count] = f_AzAng1
				az_vars[actual_packet_count] = f_AzAngVar1


			actual_packet_count = actual_packet_count + 1

		if (save_formatted_data):
			formatted_string = str(i) + ", "
			formatted_string = formatted_string + str(f_range) + ", " 
			
			formatted_string = formatted_string + str(f_VrelRad) + ", " 
			
			formatted_string = formatted_string + str(f_AzAng0) + ", " 
			
			formatted_string = formatted_string + str(f_AzAng1) + ", " 
			
			formatted_string = formatted_string + str(f_ElAng) + ", " 
			
			formatted_string = formatted_string + str(f_RCS0) + ", " 

			formatted_string = formatted_string + str(f_RCS1) + ", " 
			
			formatted_string = formatted_string + str(f_Prob0) + ", " 
			
			formatted_string = formatted_string + str(f_Prob1) + ", " 

			formatted_string = formatted_string + str(f_RangeVar) + ", "
			
			formatted_string = formatted_string + str(f_VrelRadVar) + ", "

			formatted_string = formatted_string + str(f_AzAngVar0) + ", "

			formatted_string = formatted_string + str(f_AzAngVar1) + ", " 

			formatted_string = formatted_string + str(f_ElAngVar) + ", " 
			
			formatted_string = formatted_string + str(f_Pdh0) + ", "
			
			formatted_string = formatted_string + str(f_SNR) + "\n"

			f.write(formatted_string)

	if (save_formatted_data):
		f.close()

	ranges = ranges[0:actual_packet_count]
	vels = vels[0:actual_packet_count]
	azimuths = azimuths[0:actual_packet_count]
	elevations = elevations[0:actual_packet_count]
	rcss = rcss[0:actual_packet_count]

	range_vars = range_vars[0:actual_packet_count]
	vel_vars = vel_vars[0:actual_packet_count]
	el_vars = el_vars[0:actual_packet_count]
	az_vars = az_vars[0:actual_packet_count]
	snrs = snrs[0:actual_packet_count]



	return (ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count)


def convert_all_radar(hexdata, save_formatted_data, save_raw_data):
	raw_hex_string = str(hexdata)
	# print (raw_hex_string)
	print_string = raw_hex_string + "\n"

	if (save_raw_data):	
		all_packets = open("all_packets_raw.txt","a")
		all_packets.write(print_string)
		all_packets.close()
	stripped_hex_string = raw_hex_string
	non_scan_dictionary = convert_non_scan(stripped_hex_string, save_formatted_data)
	headerID = non_scan_dictionary.get("headerID")


	if (headerID == 13107200):
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Sensor Status \n")
			packet_list.close()
			sensor_status_raw = open("sensor_status_raw.txt","a")
			sensor_status_raw.write(print_string)
			sensor_status_raw.close()

		ranges = np.zeros(0)
		azimuths = np.zeros(0)
		elevations = np.zeros(0)
		rcss = np.zeros(0)
		range_vars = np.zeros(0)
		vels = np.zeros(0)
		vel_vars = np.zeros(0)

		az_vars = np.zeros(0)
		el_vars = np.zeros(0)

		snrs = np.zeros(0)

		actual_packet_count = 0

	#far 0 event
	elif (headerID == 14417921):
		num_detections = min(38,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Far 0 \n")
			packet_list.close()
			far_0_raw = open("far_0_raw.txt","a")
			far_0_raw.write(print_string)
			far_0_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "far_0_radar_data.csv", num_detections, save_formatted_data)

	#far 1 event
	elif (headerID == 14417922):
		num_detections = min(38,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Far 1 \n")
			packet_list.close()

		if (save_formatted_data):
			far_0_raw = open("far_1_raw.txt","a")
			far_0_raw.write(print_string)
			far_0_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "far_1_radar_data.csv", num_detections, save_formatted_data)
		

	#near 0 event
	elif (headerID == 14417923):
		num_detections = min(38,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Near 0 \n")
			packet_list.close()
			far_0_raw = open("Near_0_raw.txt","a")
			far_0_raw.write(print_string)
			far_0_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "near_0_radar_data.csv", num_detections, save_formatted_data)
		

	#near 1 event
	elif (headerID == 14417924):
		num_detections = min(38,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Near 1 \n")
			packet_list.close()
			far_0_raw = open("Near_1_raw.txt","a")
			far_0_raw.write(print_string)
			far_0_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "near_1_radar_data.csv", num_detections, save_formatted_data)
		
	#near 2 event
	elif (headerID == 14417925):
		num_detections = min(32,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Near 2 \n")
			packet_list.close()
			far_0_raw = open("Near_2_raw.txt","a")
			far_0_raw.write(print_string)
			far_0_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "near_2_radar_data.csv", num_detections, save_formatted_data)
		
	

	return (ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count)



def convert_all_offline(save_formatted_data, stripped_hex_string):
	print_string = "b'" + stripped_hex_string + "'\n"

	
	non_scan_dictionary = convert_non_scan(stripped_hex_string, save_formatted_data)
	headerID = non_scan_dictionary.get("headerID")


	if (headerID == 13107200):
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Sensor Status \n")
			packet_list.close()
			sensor_status_raw = open("sensor_status_raw.txt","a")
			sensor_status_raw.write(print_string)
			sensor_status_raw.close()

		ranges = np.zeros(0)
		azimuths = np.zeros(0)
		elevations = np.zeros(0)
		rcss = np.zeros(0)

		range_vars = np.zeros(0)
		vels = np.zeros(0)
		vel_vars = np.zeros(0)

		az_vars = np.zeros(0)
		el_vars = np.zeros(0)

		snrs = np.zeros(0)


		actual_packet_count = 0

	#far 0 event
	elif (headerID == 14417921):
		num_detections = min(38,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Far 0 \n")
			packet_list.close()
			far_0_raw = open("far_0_raw.txt","a")
			far_0_raw.write(print_string)
			far_0_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "far_0_radar_data.csv", num_detections, save_formatted_data)

	#far 1 event
	elif (headerID == 14417922):
		num_detections = min(38,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Far 1 \n")
			packet_list.close()

		if (save_formatted_data):
			far_1_raw = open("far_1_raw.txt","a")
			far_1_raw.write(print_string)
			far_1_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "far_1_radar_data.csv", num_detections, save_formatted_data)
		

	#near 0 event
	elif (headerID == 14417923):
		num_detections = min(38,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Near 0 \n")
			packet_list.close()
			near_0_raw = open("near_0_raw.txt","a")
			near_0_raw.write(print_string)
			near_0_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "near_0_radar_data.csv", num_detections, save_formatted_data)
		

	#near 1 event
	elif (headerID == 14417924):
		num_detections = min(38,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Near 1 \n")
			packet_list.close()
			near_1_raw = open("near_1_raw.txt","a")
			near_1_raw.write(print_string)
			near_1_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "near_1_radar_data.csv", num_detections, save_formatted_data)
		
	#near 2 event
	elif (headerID == 14417925):
		num_detections = min(32,non_scan_dictionary.get("num_detections"))
		if (save_formatted_data):
			packet_list = open("packet_list.txt","a")
			packet_list.write("Near 2 \n")
			packet_list.close()
			near_0_raw = open("near_2_raw.txt","a")
			near_0_raw.write(print_string)
			near_0_raw.close()
		
		(ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count) = convert_scan(stripped_hex_string, "near_2_radar_data.csv", num_detections, save_formatted_data)
		
	

	return (ranges, azimuths, elevations, vels,  rcss, range_vars, az_vars, el_vars, vel_vars, snrs, actual_packet_count)



def packet_splitter(all_packets_string):
	index_1 = all_packets_string.find("'")
	if (index_1 == -1):
		return ("","")
	irrelevant_string = all_packets_string[0:index_1+1]
	relevant_string = all_packets_string[index_1+1:]
	index_2 = relevant_string.find("'")
	if (index_2 == -1):
		return ("","")
	one_packet = relevant_string[index_1+1-len(irrelevant_string):index_2]
	remaining_packets = relevant_string[index_2+1:]
	return(one_packet,remaining_packets)



