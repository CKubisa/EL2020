#Import Libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite3 as sql
import smtplib

#Assign GPIO pins
redPin = 27
tempPin = 17
greenPin = 22

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
GPIO.setup(greenPin,GPIO.OUT)

#connect to database
#---------------------------------------------------------------------
con = sql.connect('../log/templog.db')
cur = con.cursor()
eChk = 0

def oneBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def readF(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor,tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}'.format(temperature)
	else:
		print('Error Reading Sensor')
	return tempFahr

def readH(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	if humidity is not None and temperature is not None:
		humid = '{1:0.1f}'.format(temperature, humidity)
	else:
		print('Error Reading Sensor')
	return humid

def alert(tempF):
	global eChk
	if eChk == 0:
		Text = "Temperature is now "+str(tempF)
		eMessage = 'Subject: {}\n\n{}'.format(Subject, Text)
		server.login("ckubisa38@gmail.com", "aqrxhwiduipxdoxn")
		server.sendmail(eFROM, eTO, eMessage)
		server.quit
		eChk = 1

oldTime = time.time()

try:
	#with open("../log/templog.csv", "a") as log:
	while True:
		#oldTime = time();
		humid = readH(tempPin)
		tempF = readF(tempPin)

		if 60 <= float(tempF) <= 78:
			eChk = 0
			GPIO.output(redPin, True)
			GPIO.output(greenPin, False)
		else:
			GPIO.output(greenPin, True)
			alert(tempF)
			oneBlink(redPin)

		if time.time() - oldTime > 59:
			cur.execute('INSERT INTO templog values(?,?,?)', (time.strftime('%Y/%m/%d-%H:%M:%S'),tempF,humid))
			con.commit()
			table = con.execute("select * from templog")
			print("%-30s %-20s %-20s" % ("Date/Time", "Temp", "Humidity"))
			for row in table:
				print("%-30s %-20s %-20s" %(row[0], row[1], row[2]))
			oldTime = time.time();

except KeyboardInterrupt:
	os.system('clear')
	print('Thanks for Blinking and Thinking!')
	GPIO.cleanup()
