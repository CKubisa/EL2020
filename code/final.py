#Import Libraries we will be using
from flask import Flask, render_template, jsonify, Response
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite3 as sql
import smtplib
import socket
import json
import sqlite3 as sql
import smtplib

#Assign GPIO Pings
soundPin = 26
vibratePin = 5
motionPin = 23
buttonPin = 15 
AlarmPin = 27
activePin = 12
#Variables for GPIO
message = 'detected'
armed = False

#SMTP Variables
eFROM = "ckubisa38@gmail.com"
eTO = "6313526569@messaging.sprintpcs.com"
Subject = "Alarm Triggerd!"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)


#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(AlarmPin,GPIO.OUT)
GPIO.setup(activePin,GPIO.IN)
GPIO.setup(soundPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(vibratePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(motionPin, GPIO.IN)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#---------------------------------------------------------------------

#Connect to database
con = sql.connect('../log/finalData.db')
cur = con.cursor()
eChk = 0


#Function to turn on Alarm
def alarmActive(pin):
	active = True
	print(message+' detected, Alarm Activating')
	#sendMessage()
	cur.execute('INSERT INTO finalData values(?,?)', (message ,time.strftime('%Y/%m/%d-%H:%M:%S'))) 
	con.commit()
	GPIO.output(pin,True)
	time.sleep(3)
	while active == True:
		active = GPIO.input(activePin)
	time.sleep(3) 

#Function for sending text message
def sendMessage():
	eMessage = 'Subject: {}\n\n{}'.format(Subject, message)
	server.login("ckubisa38@gmail.com", "aqrxhwiduipxdoxn")
	server.sendmail(eFROM, eTO, eMessage)
	server.quit
	time.sleep(5)

GPIO.output(AlarmPin,False)
print('System On')
print('Press button to activate')
try:
	while True:
		input_sound = GPIO.input(soundPin)
		input_vibrate = GPIO.input(vibratePin)
		input_motion = GPIO.input(motionPin)
		input_button = GPIO.input(buttonPin)

		#Check is someone has armed the system)
		if input_button == True and armed == False:
			armed = True
			print('System arming in 3 seconds')
			time.sleep(3)
			print('System acvtivated')

		#Detect if Alarm is activated by Sound Sensor
		if input_sound == True and armed == True:
			message='Sound'
			alarmActive(AlarmPin)

		#Detect if Alarm is activated by Vibration Sensor
		if input_vibrate == True and armed == True:
			message='Vibration'
			alarmActive(AlarmPin)

		#Detect if Alarm is activated by Motion Sensor
		if input_motion == True and armed == True:
			message='Motion'
			alarmActive(AlarmPin)

except KeyboardInterrupt:
	os.system('clear')
	print('System Off')
	GPIO.cleanup()
