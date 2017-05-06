#        tcp/h264://my_pi_address:8000/
#To check if the camera is connected run
#	vcgencmd get_camera
#Type into VLC in network stream
#	 tcp/h264://my_pi_address:8000/

#!/usr/bin/env python
#James Raymond 
#GPS interfaceing code I2C 
import matplotlib as mpl
mpl.use('Agg')
import smbus
import time
import MySQLdb	
import socket
import time
import picamera
import threading
import select, string, sys,os
import  subprocess 
import RPi.GPIO as GPIO
import numpy as np
import skimage
from skimage import io, exposure, transform, img_as_float, img_as_ubyte
from time import sleep
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageOps
from resizeimage import resizeimage


PORT = 8002 

DELAY = 1
 # IR registration parameter



class myThread (threading.Thread):
        def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
                
                    print "Starting " + self.name
                    Thermo()

class myThread2 (threading.Thread):
        def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
               
                print "Starting " + self.name
		camera()
class myThread3 (threading.Thread):
        def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
                while True:
                        print "Starting " + self.name
                        Motors()


class myThread4 (threading.Thread):
        def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
                while True:
                        print "Starting " + self.name
                        GPS(1)

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

def reset():# resets database flag
	global reset 
	print "Reset is :"
	print reset
	return reset
	reset +=1

def camera():


	subprocess.call("./camerStreamer.sh",shell=True)
                                

def GPS(delay):
        
        database = MySQLdb.connect(host='localhost',user='root',passwd='root',db='GPS')# link to database
	id=0
        cursor = database.cursor()
	

	#time
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
        wait = float(get_single(18))
        wait += float(get_single(19))/10
        wait += float(get_single(20))/100
        wait += float(get_single(21))/1000
        latitude_minutes+=(60*(wait/1000))

        latitude_direction = chr(get_single(22))
        latitude ="%.0f, %.4f, %s" %(latitude_degrees,latitude_minutes,latitude_direction)
        print 'latitude: ',latitude
        wait = 0


        # Longitude
        longitude_degrees = float(get_single(23))*100
        longitude_degrees += float(get_double(24))
        longitude_minutes =  float(get_double(26))
        wait = float(get_single(28))
        wait += float(get_single(29))/10
        wait += float(get_single(30))/100
        wait += float(get_single(31))/1000
        longitude_minutes+=(60*(wait/1000))
        longitude_direction = chr(get_single(32))
        longitude ="%.0f, %.4f %s" %(longitude_degrees,longitude_minutes,longitude_direction)
        print 'longitude: ',longitude
        print "\n\n"

        cursor.execute(''' INSERT INTO `data`( `id`,`time`, `date`, `latitude-degrees`, `latitude-minutes`, `latitude-direction`, `longitude-degrees`, `longitude-minutes`, `longitude-direction`, `heading`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s ) ''',(id,time_gps, date_gps, latitude_degrees, latitude_minutes, latitude_direction, longitude_degrees, longitude_minutes, longitude_direction, heading))
        database.commit()
        time.sleep(delay)

def Thermo():
	ROT = np.deg2rad(90)
	SCALE = (36.2, 36.4)
	OFFSET = (530, 170)
	fifo = open('/var/run/mlx9062x.sock', 'r')


	def irImage():
		ir_raw = fifo.read()
		ir_trimmed = ir_raw[0:128]
		ir = np.frombuffer(ir_trimmed, np.uint16)
		ir = ir.reshape((16, 4))[::-1, ::-1]
		ir = img_as_float(ir)  
		p2, p98 = np.percentile(ir, (2, 98))
		ir = exposure.rescale_intensity(ir, in_range=(p2, p98))
		ir = exposure.equalize_hist(ir)

		cmap = plt.get_cmap('spectral')
		rgba_img = cmap(ir)
		rgb_img = np.delete(rgba_img, 3, 2)    
		# align the IR array with the image
		tform = transform.AffineTransform(scale=SCALE, rotation=ROT, translation=OFFSET)
		ir_aligned = transform.warp(rgb_img, tform.inverse, mode='constant')
		ir_byte = img_as_ubyte(ir_aligned)

		plt.imsave('test.jpg', rgb_img, cmap=cmap)

		img = Image.open("test.jpg")
		img = img.resize((160, 640), Image.ANTIALIAS)

		img2 = img.rotate(270,expand=True)
		img2= img2.transpose(Image.FLIP_LEFT_RIGHT)
		img2.save("ThermalImg.jpg")
		print("Image saved")

	
	def retImage(name,sock):
	
		irImage();
		sleep(0.15)   

		with open("ThermalImg.jpg",'rb') as readImage:
			imgToSend = readImage.read(1024)
			print "Sending messages"
			sock.send(imgToSend)
			while imgToSend != "" :
				imgToSend =  readImage.read(1024)
				sock.send(imgToSend)
			print "Finished"
			sock.send("")


	server_socket = socket.socket()
	server_socket.bind(('0.0.0.0',8000))
	while True:

		print ("waiting for connection")
		server_socket.listen(5)
		print ("Started")
		c,addr = server_socket.accept()
		print "Client connected ip: " + str(addr)
		t=threading.Thread(target=retImage, args = ("imageThread",c))
		t.start()
	
	    


	print('Error! Closing...')
	connection.close()
	server_socket.close()
	print ("ConnectiON CLOSED")
	fifo.close()	

 

            
def Motors():
    print "Motors\n"
    GPIO.setwarnings(False)
    Motor1A = 36
    Motor1B = 38
    Motor1E = 40


    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(22,GPIO.OUT)
    GPIO.setup(32,GPIO.OUT)
    GPIO.setup(16,GPIO.OUT)
    GPIO.setup(Motor1A,GPIO.OUT)#pin A
    GPIO.setup(Motor1B,GPIO.OUT)#pin B
    GPIO.setup(Motor1E,GPIO.OUT)#enable pin

    pwm1= GPIO.PWM(Motor1E,100)# sets up enable pin for pwm
    pwm1.start(1)

    frequencyHertz = 50
    pwm= GPIO.PWM(32,frequencyHertz)

    output = GPIO.PWM(16,frequencyHertz)

    pwm2 = GPIO.PWM(22,frequencyHertz)

    msPerCycle = 100/frequencyHertz

    server_socket = socket.socket()
    try:

            server_socket.bind(('0.0.0.0',PORT))
    except socket.error as msg:
            print "Bind Failed. Error Code : ",str(msg[0])+"Message "+msg[1]
            sys.exit() 
    print "Socket Created"
    server_socket.listen(1)

    #conn,addr = server_socket.accept()
    while(1):


            conn,addr = server_socket.accept()
            
            print("connected")
            #wait to accept a connection - blocking call
            print 'Connected with ' + addr[0] + ':' + str(addr[1])

            data = conn.recv(1024)
            print("data is :"+data)
	

            if str(data) != 0 :

        		if "A" in data:
        			angleMove=data.split('A', 1)[1]
                            	print "Postion of Steering "+ angleMove     
                            	pwm2.start(int(angleMove))
        		if "P" in data:
        			motorMove=data.split('P', 1)[1]
                            	print "Postion of pan "+ motorMove     
                            	pwm.start(int(motorMove))
        		if "T" in data:
        			tiltMotor = data.split("T",1)[1]
        			print "Position of Tilt" + data
        			output.start(int(tiltMotor))
        	        if "M" in data:
                		speedMotor = data.split("M",)[1]

        			if int(speedMotor) < 10 :
        				if speedMotor !=0:
                                           	pwm.start(int(speedMotor)*10)
                                            	print "Motor speed is reverse : "+ speedMotor
                                            	GPIO.output(Motor1A,GPIO.HIGH)
                                            	GPIO.output(Motor1B,GPIO.LOW)
                                            	GPIO.output(Motor1E,GPIO.HIGH)
        				else:
        					break

        			if int(speedMotor) >=10 :
        				Motor = speedMotor.split("1",)[1]#removes 1
        				if Motor != 0:
        					try:
        						newMotor = int(Motor)*10
                                    		
        					except ValueError:
        						print "Didnt work"
        					pwm.start(newMotor)
        					print "Motor speed is forward : "+ speedMotor
                                            	GPIO.output(Motor1A,GPIO.LOW)
                                            	GPIO.output(Motor1B,GPIO.HIGH)
                                           	GPIO.output(Motor1E,GPIO.HIGH)
        				else :
        					break
        			if int(speedMotor) == 0:
        			       pwm.start(0)
                                       GPIO.output(Motor1A,GPIO.LOW)
                                       GPIO.output(Motor1B,GPIO.LOW)
                                       GPIO.output(Motor1E,GPIO.HIGH)
            else:
                    break
     
            

            
    server_socket.close()
    GPIO.cleanup()

def wifiCon():
	try:
		socket.create_connection(("www.google.com",80))
		return True
	except  :
		return False


database = MySQLdb.connect(host='localhost',user='root',passwd='root',db='GPS')# link to database
cursor = database.cursor()
print "*** Database reset ***\n\n"
cursor.execute('DELETE FROM `data`')
database.commit()
cursor.execute('ALTER TABLE `data` AUTO_INCREMENT=1')
#cursor.execute(''' INSERT INTO `data`( `id`,`time`, `date`, `latitude-degrees`, `latitude-minutes`, `latitude-direction`, `longitude-degrees`, `longitude-minutes`, `longitude-direction`, `heading`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s ) ''',(0,0,0,0,0,0,0,0,0,0))
database.commit()

GPS(1)
        
# Create new threads
thread1 = myThread(1, "Thermo-1")
thread2 = myThread2(2, "Thread-2")
thread3 = myThread3(3, "Thread-3")
thread4= myThread4(4, "Thread-3")
# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

t=threading.Thread(target=Thermo, args = ("imageThread",c))
t.start()
#os.path.abspath('/home/pi/FinalYear/Thermo.py')

i=0
while True:
	connection=wifiCon();
	if connection == False:
        	print " * * * NOT CONNECTED TO THE INETERNET * * *"	
	

server_socket.close()
GPIO.cleanup()
print "Exiting Main Thread"
fifo.close()
        




