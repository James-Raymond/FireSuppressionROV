#To check if the camera is connected run
#	vcgencmd get_camera
#Type into VLC in network stream
#	 tcp/h264://my_pi_address:8000/


import socket
import time
import picamera

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
