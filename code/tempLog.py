#Import Libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite as mydb
import sys

#Assign GPIO pins
redPin = 27
tempPin = 17
buttonPin = 26
con = None

#Temp and Humidity Sensor

tempSensor = Adafruit_DHT.DHT11
#LED Variables--------------------------------------------------------
#Duration of each Blink
blinkDur = .1
#Number of times to Blink the LED
blinkTime = 7

#---------------------------------------------------------------------
#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def oneBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def readF(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor,tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}*F'.format(temperature)
	else:
		print('Error Reading Sensor')
	return tempFahr

try:

	#with open("../log/templog.csv", "a") as log:
	con = mydb.connect('../log/templog.db')
	cur = con.cursor()

		while True:
			time.sleep(60)
			for i in range (blinkTime):
				oneBlink(redPin)
			time.sleep(.2)
			data = readF(tempPin)
			print (data)
			log.write("{0},{1}\n".format(time.strftime("%Y/%m/%d-%H:%M:%S"),str(data)))

except KeyboardInterrupt:
	os.system('clear')
	print('Thanks for Blinking and Thinking!')
	GPIO.cleanup()
