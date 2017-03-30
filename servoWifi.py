
#local:8003

import socket
import time
import select, string, sys

import RPi.GPIO as GPIO
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(18,GPIO.OUT)

frequencyHertz = 50
pwm = GPIO.PWM(18,frequencyHertz)

msPerCycle = 1000/frequencyHertz

server_socket = socket.socket()
try:

	server_socket.bind(('0.0.0.0',8003))
except socket.error as msg:
	print "Bind Failed. Error Code : ",str(msg[0])+"Message "+msg[1]
	sys.exit() 
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
                print "Postion "+ data     
                pwm.start(int(data))

        else: break
 
        

	
server_socket.close()
GPIO.cleanup()

