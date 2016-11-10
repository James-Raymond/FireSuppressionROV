#!/usr/bin/env python

#James Raymond 
#GPS interfaceing code I2C 

import smbus
import time
import MySQLdb						

bus = smbus.SMBus(1)
address = 0x68	#I2C address (A0 & A1 jumpers ON)			
database = MySQLdb.connect(host='localhost',user='root',passwd='root',db='GPS')# link to database

cursor = database.cursor()

			
# single register from GPM.S
def get_single(register):
	try:
	        value = bus.read_byte_data(address, register)
	        return value
	except:
		print "Value could not be read Single register"
		return 0


#double register from GPM.S and convert to tens and units
def get_double(register):
	try:
		value1 = bus.read_byte_data(address, register)
		value2 = bus.read_byte_data(address, register+1)
		value = (value1 * 10) + value2
		return value
	except:
		print "Value could not be read Double register"
		return 0


# Main program
while True:

	# Time
        hours = float(get_double(0))
        minutes =float( get_double(2))
        seconds = float( get_double(4))
	time_gps ="%.0f:%0.f:%.0f"%(hours,minutes,seconds)
	print'Time: ',time_gps

        # Date
        day = float(get_double(6))
        months =float(get_double(8))
        years = float(get_double(12))
        date = "%.0f-%0.f-%.0f"%(day,months,years)
	print 'Date: ', date

	# Headind
        heading = float(get_single(44))*100
        heading += float(get_single(45))*10
        heading += float(get_single(46))
        heading += float(get_single(47))/10
        print "heading:",heading

	# Latitude 
        latitude_degrees = get_double(14)
        latitude_minutes = float(get_double(16))
        latitude_minutes += float(get_single(18))/10
        latitude_minutes += float(get_single(19))/100
        latitude_minutes += float(get_single(20))/1000
	latitude_minutes += float(get_single(21))/10000
	latitude_direction = chr(get_single(22))
	latitude ="%.0f%.5f %s" %(latitude_degrees,latitude_minutes,latitude_direction)
        print 'latitude: ',latitude

	# Longitude 
        longitude_degrees = get_single(23)*100
        longitude_degrees += get_double(24)
        longitude_minutes = float(get_double(26))
        longitude_minutes += float(get_single(28))/10 
        longitude_minutes += float(get_single(29))/100 
        longitude_minutes += float(get_single(30))/1000
        longitude_minutes += float(get_single(31))/10000
        longitude_direction = chr(get_single(32))
        longitude ="%.0f%.5f %s" %(longitude_degrees,longitude_minutes,longitude_direction)
	print 'longitude: ',longitude
	print "\n\n"
        cursor.execute(''' INSERT INTO  data (time , date , latitude , longitude , heading) VALUES (%s,%s,%s,%s,%s) ''',(time_gps, date, latitude, longitude, heading))

        database.commit()

        time.sleep(1)

	














