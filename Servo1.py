import RPi.GPIO as GPIO	
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(18,GPIO.OUT)

frequencyHertz = 50
pwm = GPIO.PWM(18,frequencyHertz)

leftPosition = .50
rightPosition = 2.30
middlePosition = (rightPosition - leftPosition)/2+leftPosition

positionList=[leftPosition,middlePosition,rightPosition,middlePosition]

msPerCycle = 1000/frequencyHertz


for i in range(3):
	for position in positionList:
		dutyCyclePercentage = position *100 / msPerCycle
		print "Postion "+ str(position)
		print "Duty cyccle " + str(dutyCyclePercentage)+ "%"
		print ""
		pwm.start(dutyCyclePercentage)
		time.sleep(.5)
GPIO.cleanup()
