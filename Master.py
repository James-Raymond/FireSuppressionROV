#To check if the camera is connected run
#	vcgencmd get_camera
#Type into VLC in network stream
#	 tcp/h264://my_pi_address:8000/

#!/usr/bin/env python
#James Raymond 
#GPS interfaceing code I2C 

import smbus
import time
import MySQLdb	
import socket
import time
import picamera
import threading




 

class myThread (threading.Thread):
        def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
                while True:
                        print "Starting " + self.name
                        GPS(self.name,1)

class myThread2 (threading.Thread):
        def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
                while True:
                        print "Starting " + self.name
                        camera()

# single register from GPM.S
def get_single(register):
        bus = smbus.SMBus(1)
        address = 0x68	#I2C address (A0 & A1 jumpers ON)
	try:
	        value = bus.read_byte_data(address, register)
	        return value
	except:
		print "Value could not be read Single register"
		return 0


	


#double register from GPM.S and convert to tens and units
def get_double(register):
        bus = smbus.SMBus(1)
        address = 0x68	#I2C address (A0 & A1 jumpers ON)
	try:
		value1 = bus.read_byte_data(address, register)
		value2 = bus.read_byte_data(address, register+1)
		value = (value1 * 10) + value2
		return value
	except:
		print "Value could not be read Double register"
		return 0
	
def camera():
                with picamera.PiCamera() as camera:
                        camera.resolution = (640,480)
                        camera.framerate = 25

                        server_socket = socket.socket()
                        server_socket.bind(('0.0.0.0',8000))
                        server_socket.listen(0)

                        #Accept a single connection and make a file-like object out of it
                        connection = server_socket.accept()[0].makefile('wb')
                        try:
                                camera.start_recording(connection, format='h264')
                                camera.wait_recording(1000)
                                camera.stop_recording()

                        finally:
                                connection.close()
                                server_socket.close()
                                

def GPS(threadName,delay):
        database = MySQLdb.connect(host='localhost',user='root',passwd='root',db='GPS')# link to database
	id=0
        cursor = database.cursor()

        

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
        date_gps = "%.0f-%0.f-%.0f"%(years,months,day)
	print 'Date: ', date_gps

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
        cursor.execute(''' INSERT INTO `data`( `id`,`time`, `date`, `latitude-degrees`, `latitude-minutes`, `latitude-direction`, `longitude-degrees`, `longitude-minutes`, `longitude-direction`, `heading`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s ) ''',(id,time_gps, date_gps, latitude_degrees, latitude_minutes, latitude_direction, longitude_degrees, longitude_minutes, longitude_direction, heading))
        database.commit()
        time.sleep(delay)

# Create new threads
thread1 = myThread(1, "Thread-1")
thread2 = myThread2(2, "Thread-2")

# Start new Threads
thread1.start()
thread2.start()

print "Exiting Main Thread"

        



